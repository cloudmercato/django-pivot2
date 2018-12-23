from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_pivot import defaults


def get_setting(base_name):
    name = 'PIVOT_%s' % base_name
    default = getattr(defaults, base_name)
    return getattr(settings, name, default)


AGGFUNCS = get_setting('AGGFUNCS')

HTML_BORDER = get_setting('HTML_BORDER')
HTML_NA_REP = get_setting('HTML_NA_REP')
HTML_CLASSES = get_setting('HTML_CLASSES')
