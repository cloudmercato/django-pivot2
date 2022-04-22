from rest_framework import viewsets
from rest_framework.decorators import action
from django_pivot.contrib import rest_framework
from django_pivot.tests.test_project.testapp import models


class MeteoViewSet(rest_framework.PivotViewSetMixin, viewsets.ViewSet):
    model = models.Meteo
    queryset = model.objects.all()

    @action(
        detail=False,
        renderer_classes=rest_framework.RENDERERS,
    )
    def pivot(self, request, format=None):
        return self._export_pivot(request)
