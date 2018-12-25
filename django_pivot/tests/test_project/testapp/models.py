from django.db import models
from django_pandas.managers import DataFrameQuerySet

SCORES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
)


class ProviderQuerySet(DataFrameQuerySet):
    def pivot_annontate(self):
        return self.annotate(
            logs_count=models.Count('logs'),
        )

    def all(self):
        qs = super().all()
        qs = qs.pivot_annontate()
        return qs


class MeteoQuerySet(DataFrameQuerySet):
    def pivot_annontate(self):
        return self.annotate(
            provider_name=models.F('provider__name'),
            score=models.F('provider__score'),
        )


class Provider(models.Model):
    name = models.CharField(max_length=64)
    score = models.CharField(max_length=1, choices=SCORES)

    objects = ProviderQuerySet.as_manager()

    pivot_opts = {
        'values': ['logs_count'],
        'rows': ['name', 'date', 'city'],
    }

    def __str__(self):
        return self.name


class Meteo(models.Model):
    date = models.DateField()
    provider = models.ForeignKey(Provider, related_name='logs', on_delete=models.CASCADE)
    city = models.CharField(max_length=64)
    temperature = models.FloatField()
    humidity = models.SmallIntegerField()

    objects = MeteoQuerySet.as_manager()

    pivot_opts = {
        'values': ['date', 'city', 'temperature', 'humidity'],
        'rows': ['provider_name', 'score', 'date', 'city'],
    }

    def __str__(self):
        return '%s %s %s' % (self.city, self.temperature, self.humidity)
