import io
import importlib
from django.utils.translation import ugettext as _
from django_pivot import settings
from django_pivot import constants


def get_aggr_func(func_name):
    for func in settings.AGGFUNCS:
        if func_name == func['name'] and 'path' in func:
            module_path = '.'.join(func['path'].split('.')[:-1])
            name = func['path'].split('.')[-1]
            module = importlib.import_module(module_path)
            func = getattr(module, name)
            return func
    return func_name


def verbose_name(name):
    verbose = settings.VERBOSE_NAMES.get(name)
    return _(verbose) if verbose else name


def get_formatted_data(pivot, format_id, export_options):
    format_ = constants.EXPORT_FORMATS[format_id]
    buff = io.StringIO() if format_['ctype'].startswith('text/') else io.BytesIO()
    getattr(pivot, 'to_%s' % format_id)(buff, **export_options)
    buff.seek(0)
    return buff
