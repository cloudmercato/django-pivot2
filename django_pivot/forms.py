from django import forms
from django.utils.translation import ugettext_lazy as _
from django_pivot import settings
from django_pivot import constants
from django_pivot import utils

AGGFUNC_CHOICES = [
    (f['name'], utils.verbose_name(f['verbose']))
    for f in settings.AGGFUNCS
]
EXPORT_FORMAT_CHOICES = [
    (k, v['verbose'])
    for k, v in constants.EXPORT_FORMATS.items()
    if k in settings.EXPORT_FORMATS
]


class PivotForm(forms.Form):
    values = forms.MultipleChoiceField(
        label=_("Value(s)"),
        help_text=_("Field(s) to use to calculate."))
    rows = forms.MultipleChoiceField(
        label=_("Row(s)"),
        help_text=_("List of field names to group on."))
    cols = forms.MultipleChoiceField(
        required=False,
        label=_("Column(s)"),
        help_text=_("Optional list of column names to group on."))
    aggr = forms.MultipleChoiceField(
        label=_("Aggregation function(s)"),
        choices=AGGFUNC_CHOICES,
        help_text=_("The list of function used to aggregate."))
    apply = forms.ChoiceField(
        required=False,
        label=_("Optional applied function"),
        choices=[(None, "-----")] + AGGFUNC_CHOICES,
        help_text=_("The function to apply after aggregation."))
    format = forms.ChoiceField(
        required=False,
        label=_("Export format"),
        choices=[(None, "-----")] + EXPORT_FORMAT_CHOICES)

    def __init__(self, values, rows, cols, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['values'].choices = [(i, utils.verbose_name(i)) for i in values]
        self.fields['rows'].choices = [(i, utils.verbose_name(i)) for i in rows]
        self.fields['cols'].choices = [(i, utils.verbose_name(i)) for i in cols]

    def get_pivot_table(self, queryset):
        pivot = queryset.to_pivot_table(
            values=self.cleaned_data['values'],
            rows=self.cleaned_data['rows'],
            cols=self.cleaned_data['cols'],
            aggfunc={
                v: [
                    utils.get_aggr_func(f)
                    for f in self.cleaned_data['aggr']
                ]
                for v in self.cleaned_data['values']
            },
            coerce_float=True,
        )
        return pivot
