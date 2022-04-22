from django.utils.translation import ugettext_lazy as _


AGGFUNCS = [
    {'name': 'mean', 'verbose': _("mean")},
    {'name': 'std', 'verbose': _("standard deviation")},
    {'name': 'min', 'verbose': _("minimum")},
    {'name': 'median', 'verbose': _("median")},
    {'name': 'max', 'verbose': _("maximum")},
    {'name': 'sum', 'verbose': _("sum")},
    {'name': 'count', 'verbose': _("count")},
    {'name': 'bool', 'verbose': _("bool")},
]

ROUND = None

VERBOSE_NAMES = {}

HTML = {
    'border': 1,
    'na_rep': '-',
    'classes': ()
}

EXPORT_FORMATS = ['csv', 'excel', 'hdf', 'html', 'latex', 'pickle', 'stata', 'string']
EXPORT_OPTIONS = {}
