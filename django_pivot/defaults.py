from django.utils.translation import ugettext_lazy as _


AGGFUNCS = [
    {'name': 'mean', 'verbose': _("mean")},
    {'name': 'std', 'verbose': _("standard deviation")},
    {'name': 'min', 'verbose': _("minimum")},
    {'name': 'median', 'verbose': _("median")},
    {'name': 'max', 'verbose': _("maximum")},
    {'name': 'sum', 'verbose': _("sum")},
    {'name': 'count', 'verbose': _("count")},
]
HTML_BORDER = 1
HTML_NA_REP = '-'
HTML_CLASSES = ()
