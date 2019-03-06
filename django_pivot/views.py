from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from pandas.core.base import DataError

from django_pivot import forms
from django_pivot import utils
from django_pivot import settings


class PivotFormViewMixin:
    pivot_form_class = forms.PivotForm
    round = settings.ROUND

    @property
    def pivot_fieldnames(self):
        if not hasattr(self, '_pivot_fieldnames'):
            self._pivot_fieldnames = list(set(
                self.values_choices + self.rows_choices + self.cols_choices
            ))
        return self._pivot_fieldnames

    @property
    def pivot_table(self):
        if not hasattr(self, '_pivot_table'):
            # Get qs from django-filters or classic
            if hasattr(self, 'filterset'):
                qs = self.filterset.qs
            else:
                qs = self.get_queryset()
            try:
                pivot = self.pivot_form.get_pivot_table(qs)
            except DataError as err:
                if not qs.exists():
                    return
                raise
            apply_ = self.request.GET.get('pivot-apply')
            # Apply is made only on 1st column
            if apply_:
                first_col = pivot.columns[0][0] if isinstance(pivot.columns[0], tuple) else pivot.columns[0]
                name = '%s %s' % (apply_, first_col)
                pivot = pivot.aggregate(apply_, axis='columns').to_frame(name=name)
            if self.round is not None:
                pivot = pivot.round(self.round)
            pivot = utils.verbose_dataframe(pivot)
            self._pivot_table = pivot
        return self._pivot_table

    def get_pivot_form(self, values, rows, cols, fieldnames, prefix, data, **kwargs):
        return self.pivot_form_class(
            values=values,
            rows=rows,
            cols=cols,
            fieldnames=fieldnames,
            prefix=prefix,
            data=data,
            **kwargs
        )

    @property
    def pivot_form(self):
        if not hasattr(self, '_pivot_form'):
            self._pivot_form = self.get_pivot_form(
                values=self.values_choices,
                rows=self.rows_choices,
                cols=self.cols_choices,
                fieldnames=self.pivot_fieldnames,
                prefix='pivot',
                data=self.request.GET
            )
        return self._pivot_form


class PivotView(PivotFormViewMixin):
    html_params = settings.HTML
    export_options = settings.EXPORT_OPTIONS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.pivot_form.is_valid() and self.pivot_table is not None:
                data = mark_safe(self.pivot_table.to_html(**self.html_params))
            else:
                data = None
        except DataError as err:
            if err.args[0] == 'No numeric types to aggregate':
                self.pivot_form.errors['__all__'] = [
                    _("One or several fields don't have values to aggregate.")
                ]
                data = None
            else:
                raise
        context.update({
            'data': data,
            'pivot_form': self.pivot_form,
        })
        return context

    def _get_file(self):
        format_ = self.pivot_form.cleaned_data['format']
        filename = '%s.%s' % (self.model._meta.model_name, format_['ext'])
        data = utils.get_formatted_data(
            self.pivot_table,
            format_['id'],
            self.export_options.get(format_['id'], {})
        )
        response = HttpResponse(
            data,
            content_type=format_['ctype'],
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            smart_str(filename))
        return response

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        valid_form = self.pivot_form.is_valid()
        if valid_form and self.pivot_form.cleaned_data['format'] and self.pivot_table is not None:
            return self._get_file()
        return response
