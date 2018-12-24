import django_filters as filters
from django_pivot.tests.test_project.testapp import models

CITIES = models.Meteo.objects.values_list('city', 'city')


class ProviderFilterSet(filters.FilterSet):
    city = filters.MultipleChoiceFilter(
        field_name='logs__city',
        initial=[],
        choices=CITIES
    )

    class Meta:
        model = models.Provider
        fields = []
