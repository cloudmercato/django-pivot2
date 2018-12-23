from django_pivot import forms
from django_pivot import utils
from django_pivot import settings


class PivotView:
    pivot_form = forms.PivotForm

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
        pivot = pivot.round(3)
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
            data = pivot.to_html(
                border=settings.HTML_BORDER,
                na_rep=settings.HTML_NA_REP,
                classes=settings.HTML_CLASSES,
            )
        else:
            data = pivot = None
        context.update({
            'data': data,
            'pivot_form': pivot_form,
        })
        return context
