import io

from django.http import HttpResponse
from django.utils.encoding import smart_str

from django_pivot import forms
from django_pivot import utils
from django_pivot import settings
from django_pivot import constants


class PivotView:
    pivot_form = forms.PivotForm
    round = settings.ROUND
    html_params = settings.HTML
    export_options = settings.EXPORT_OPTIONS

    def get_pivot_table_kwargs(self):
        kwargs = {
            'values': self.request.GET.getlist('pivot-values'),
            'rows': self.request.GET.getlist('pivot-rows'),
            'cols': self.request.GET.getlist('pivot-cols'),
            'aggfunc': {
                v: [
                    utils.get_aggr_func(f)
                    for f in self.request.GET.getlist('pivot-aggr')
                ]
                for v in self.request.GET.getlist('pivot-values')
            }
        }
        return kwargs

    def get_pivot_table(self):
        qs = self.filterset.qs if hasattr(self, 'filterset') else self.get_queryset()
        pivot = qs.to_pivot_table(**self.get_pivot_table_kwargs())
        apply_ = self.request.GET.get('pivot-apply')
        # Apply is made only on 1st column
        if apply_:
            first_col = pivot.columns[0][0] if isinstance(pivot.columns[0], tuple) else pivot.columns[0]
            name = '%s %s' % (apply_, first_col)
            pivot = pivot.aggregate(apply_, axis='columns').to_frame(name=name)
        if self.round is not None:
            pivot = pivot.round(self.round)
        pivot.rename(utils.verbose_name, axis='index', inplace=True)
        pivot.rename(utils.verbose_name, axis='columns', inplace=True)
        return pivot

    def get_pivot_form(self):
        pivot_form = self.pivot_form(
            values=self.values_choices,
            rows=self.rows_choices,
            cols=self.cols_choices,
            prefix='pivot',
            data=self.request.GET)
        return pivot_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pivot_form = self.get_pivot_form()
        if pivot_form.is_valid():
            pivot = self.get_pivot_table()
            format_id = self.request.GET.get('pivot-format')
            if format_id:
                format_ = constants.EXPORT_FORMATS[format_id]
                buf = io.StringIO() if format_['ctype'].startswith('text/') else io.BytesIO()
                getattr(pivot, 'to_%s' % format_id)(buf, **self.export_options.get(format_id, {}))
                buf.seek(0)
                data = buf
                context['format'] = format_
            else:
                data = pivot.to_html(**self.html_params)
        else:
            data = None
        context.update({
            'data': data,
            'pivot_form': pivot_form,
        })
        return context

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self.request.GET.get('pivot-format'):
            filename = '%s.%s' % (
                self.model._meta.model_name,
                response.context_data['format']['ext']
            )
            content_type = response.context_data['format']['ctype']
            response = HttpResponse(response.context_data['data'], content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                smart_str(filename))

        return response
