from django.views.generic.list import ListView

from django_filters.views import FilterView

from django_pivot import views
from django_pivot.tests.test_project.testapp import models
from django_pivot.tests.test_project.testapp import filtersets


class BasePivotView(views.PivotView):
    template_name = 'pivot.html'

    def get_queryset(self):
        qs = super().get_queryset().all()
        return qs


class BaseProviderView(BasePivotView):
    model = models.Provider
    values_choices = model.pivot_opts['values']
    rows_choices = cols_choices = model.pivot_opts['rows']


class BaseMeteoView(BasePivotView):
    model = models.Meteo
    values_choices = model.pivot_opts['values']
    rows_choices = cols_choices = model.pivot_opts['rows']


class ProviderListView(BaseProviderView, ListView):
    pass


class ProviderFilterView(BaseProviderView, FilterView):
    filterset_class = filtersets.ProviderFilterSet


class MeteoListView(BaseMeteoView, ListView):
    pass


class MeteoFilterView(BaseMeteoView, FilterView):
    pass
