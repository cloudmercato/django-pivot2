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
        required=False,
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

    fieldnames = None

    def __init__(self, values, rows, cols, fieldnames=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['values'].choices = [(i, utils.verbose_name(i)) for i in values]
        self.fields['rows'].choices = [(i, utils.verbose_name(i)) for i in rows]
        self.fields['cols'].choices = [(i, utils.verbose_name(i)) for i in cols]
        self.fieldnames = fieldnames or self.fieldnames or ()

    def clean_format(self):
        format_id = self.cleaned_data['format']
        if format_id:
            format_ = constants.EXPORT_FORMATS[format_id]
            format_['id'] = format_id
            return format_

    def clean(self):
        cleaned_data = super().clean()
        rows = cleaned_data.get('rows', [])
        cols = cleaned_data.get('cols', [])
        if not rows and not cols:
            raise forms.ValidationError(
                _("You must at least choose a row or a column."),
                code='invalid'
            )
        intsersec = set(rows) & set(cols)
        if intsersec:
            fieldnames = ', '.join([utils.verbose_name(str(r)) for r in intsersec])
            msg = _("You cannot put attributes in rows and columns at the same time:"
                    " %s") % fieldnames
            raise forms.ValidationError(msg, code='invalid')
        return cleaned_data

    def get_pivot_table(self, queryset):
        fieldnames = list(set(self.cleaned_data['values']) |
                          set(self.cleaned_data['rows']) |
                          set(self.cleaned_data['cols']))
        pivot = queryset.to_pivot_table(
            fieldnames=fieldnames,
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
        if hasattr(pivot, 'to_frame'):
            pivot = pivot.to_frame()
        return pivot
