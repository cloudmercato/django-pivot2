from django.test import TestCase
from django_pivot.contrib import rest_framework


class RendererTestMixin:
    def test_render(self):
        pass

    def test_render_no_response(self):
        pass

    def test_render_404(self):
        pass

    def test_render_error(self):
        pass


class ExcelRendererTest(RendererTestMixin, TestCase):
    pass


class HtmlRendererTest(RendererTestMixin, TestCase):
    pass


class CsvRendererTest(RendererTestMixin, TestCase):
    pass


class PivotSerializerTest(TestCase):
    def test_init(self):
        pass


class PivotViewSetTest(TestCase):
    def test_export_pivot(self):
        pass

    def test_invalid_export_pivot(self):
        pass
