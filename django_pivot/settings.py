from django.conf import settings
from django_pivot import defaults


def get_setting(base_name):
    name = 'PIVOT_%s' % base_name
    default = getattr(defaults, base_name)
    return getattr(settings, name, default)


AGGFUNCS = get_setting('AGGFUNCS')

ROUND = get_setting('ROUND')

VERBOSE_NAMES = get_setting('VERBOSE_NAMES')

HTML = get_setting('HTML')

EXPORT_FORMATS = get_setting('EXPORT_FORMATS')
EXPORT_OPTIONS = get_setting('EXPORT_OPTIONS')
