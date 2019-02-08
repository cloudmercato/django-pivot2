from rest_framework import viewsets
try:
    from rest_framework.decorators import action
except ImportError:
    action = None
from rest_framework.decorators import list_route
from django_pivot.contrib import rest_framework
from django_pivot.tests.test_project.testapp import models


class MeteoViewSet(rest_framework.PivotViewSetMixin, viewsets.ViewSet):
    model = models.Meteo
    queryset = model.objects.all()

    @list_route(
        renderer_classes=rest_framework.RENDERERS,
    )
    def pivot(self, request, format=None):
        return self._export_pivot(request)
