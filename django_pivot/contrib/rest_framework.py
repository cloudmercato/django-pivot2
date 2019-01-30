import json

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework import renderers
from rest_framework import status
from rest_framework.response import Response

from django_pivot import utils
from django_pivot import forms
from django_pivot import settings


class BasePivotRenderer(renderers.BaseRenderer):
    export_options = settings.EXPORT_OPTIONS

    def _get_filename(self, data, renderer_context):
        return "%s-%s.%s" % (
            renderer_context['view'].model._meta.model_name,
            now().strftime('%Y-%m-%d'),
            self.extension
        )

    def _raise_error(self, msg):
        if isinstance(msg, dict):
            msg = str(msg)
        if self.render_style == 'binary' and isinstance(msg, str):
            msg = msg.encode()
        elif self.render_style == 'text' and isinstance(msg, bytes):
            msg = msg.decode()
        return msg

    def render(self, data, media_type=None, renderer_context=None):
        if 'response' in renderer_context:
            status_code = renderer_context['response'].status_code
            if status_code == 404:
                return self._raise_error('')
            if not status.is_success(status_code):
                return self._raise_error(data)
        renderer_context['response']['Content-Disposition'] = 'attachment; filename=%s' % (
            self._get_filename(data, renderer_context))
        queryset = data.pop('queryset')
        pivot_table = queryset.to_pivot_table(**data)
        export_options = self.export_options.get(self.format, {})
        buff = utils.get_formatted_data(pivot_table, self.format, export_options)
        return buff.read()


class ExcelRenderer(BasePivotRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'excel'
    charset = None
    render_style = 'binary'
    extension = 'xlsx'


class HtmlRenderer(BasePivotRenderer):
    export_options = settings.EXPORT_OPTIONS
    media_type = 'text/html'
    format = 'html'
    charset = None
    render_style = 'text'
    charset = 'utf-8'
    extension = 'html'


class CsvRenderer(BasePivotRenderer):
    export_options = settings.EXPORT_OPTIONS
    media_type = 'text/csv'
    format = 'csv'
    charset = None
    render_style = 'text'
    charset = 'utf-8'
    extension = 'csv'

RENDERERS = (
    ExcelRenderer,
    HtmlRenderer,
    CsvRenderer,
)


class PivotSerializer(serializers.Serializer):
    values = serializers.MultipleChoiceField(
        choices=(),
        required=True,
        label=_("Value(s)"),
        help_text=_("Field(s) to use to calculate."))
    rows = serializers.MultipleChoiceField(
        choices=(),
        required=True,
        label=_("Row(s)"),
        help_text=_("List of field names to group on."))
    cols = serializers.MultipleChoiceField(
        choices=(),
        required=False,
        label=_("Column(s)"),
        help_text=_("Optional list of column names to group on."))
    aggfunc = serializers.MultipleChoiceField(
        label=_("Aggregation function(s)"),
        choices=forms.AGGFUNC_CHOICES,
        help_text=_("The list of function used to aggregate."))
    apply = serializers.ChoiceField(
        required=False,
        label=_("Optional applied function"),
        choices=[(None, "-----")] + forms.AGGFUNC_CHOICES,
        help_text=_("The function to apply after aggregation."))

    def __init__(self, values, rows, cols, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['values'].choices = [(i, utils.verbose_name(i)) for i in values]
        self.fields['rows'].choices = [(i, utils.verbose_name(i)) for i in rows]
        self.fields['cols'].choices = [(i, utils.verbose_name(i)) for i in cols]


class PivotViewSetMixin:
    pivot_serializer_class = PivotSerializer

    def _export_pivot(self, request, queryset=None):
        queryset = queryset or self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.pivot_annotate()
        serializer = self.pivot_serializer_class(
            values=self.values_choices,
            rows=self.rows_choices,
            cols=self.cols_choices,
            data=self.request.GET
        )
        if serializer.is_valid():
            data = serializer.data.copy()
            data['queryset'] = queryset
            response = Response(data=data)
        else:
            errors = json.dumps(dict(serializer.errors))
            response = Response(data=errors, status=400, content_type='application/json')
        return response
