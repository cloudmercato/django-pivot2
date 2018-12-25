import django_filters as filters
from django_pivot.tests.test_project.testapp import models


def get_cities():
    return models.Meteo.objects.values_list('city', 'city')


class ProviderFilterSet(filters.FilterSet):
    city = filters.ChoiceFilter(
        field_name='logs__city',
        initial=[],
        choices=get_cities
    )

    class Meta:
        model = models.Provider
        fields = []

    @property
    def qs(self):
        return super().qs.all()


class MeteoFilterSet(filters.FilterSet):
    city = filters.MultipleChoiceFilter(
        field_name='city',
        initial=[],
        choices=get_cities,
    )

    class Meta:
        model = models.Provider
        fields = []

    @property
    def qs(self):
        return super().qs.all()
