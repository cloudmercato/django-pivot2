from django.utils.translation import ugettext_lazy as _

EXPORT_FORMATS = {
    'csv': {'verbose': _("CSV"), 'ctype': 'text/csv', 'ext': 'csv'},
    'excel': {'verbose': _("Excel"), 'ctype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'ext': 'xlsx'},
    'hdf': {'verbose': _("HDF"), 'ctype': 'application/octet-stream', 'ext': 'hdf'},
    # 'gbq': {'verbose': _("Google Big Query"), 'ctype': '', 'ext': ''},
    'html': {'verbose': _("HTML"), 'ctype': 'text/html', 'ext': 'html'},
    # 'json': {'verbose': _("JSON"), 'ctype': 'text/json', 'ext': 'json'},
    'latex': {'verbose': _("LaTeX"), 'ctype': 'application/x-latex', 'ext': 'tex'},
    # 'msgpack': {'verbose': _("msgpack"), 'ctype': '', 'ext': ''},
    'pickle': {'verbose': _("Pandas"), 'ctype': 'application/octet-stream', 'ext': 'pkl'},
    'stata': {'verbose': _("Stata"), 'ctype': 'application/octet-stream', 'ext': 'dta'},
    'string': {'verbose': _("Text"), 'ctype': 'text/plain', 'ext': 'txt'},
}
