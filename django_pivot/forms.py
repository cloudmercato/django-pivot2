from django import forms
from django.utils.translation import ugettext_lazy as _
from django_pivot import settings
from django_pivot import utils

AGGFUNC_CHOICES = [
    (f['name'], utils.verbose_name(f['verbose']))
    for f in settings.AGGFUNCS
]
AGGR_FUNCS = (
    ('mean', _("Mean")),
    ('std', _("Standard deviation")),
    ('min', _("Minimum")),
    ('quantile:0.01', _("1st percentile")),
    ('quantile:0.1', _("10th percentile")),
    ('quantile:0.25', _("25th percentile")),
    ('median', _("Median")),
    ('quantile:0.75', _("75th percentile")),
    ('quantile:0.90', _("90th percentile")),
    ('quantile:0.95', _("95th percentile")),
    ('quantile:0.99', _("99th percentile")),
    ('max', _("Maximum")),
    ('sum', _("Sum")),
    ('count', _("Count")),
)


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

    def __init__(self, values, rows, cols, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['values'].choices = [(i, utils.verbose_name(i)) for i in values]
        self.fields['rows'].choices = [(i, utils.verbose_name(i)) for i in rows]
        self.fields['cols'].choices = [(i, utils.verbose_name(i)) for i in cols]
