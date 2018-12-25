import graphene
from graphene_django import DjangoObjectType

from django_pivot.contrib.graphene_django_extras import PivotField
from django_pivot.tests.test_project.testapp import filtersets
from django_pivot.tests.test_project.testapp import models


class ProviderType(DjangoObjectType):
    class Meta:
        model = models.Provider


class Query(graphene.ObjectType):
    pivot_providers = PivotField(
        ProviderType,
        filterset_class=filtersets.ProviderFilterSet,
        values_choices=models.Provider.pivot_opts['values'],
        rows_choices=models.Provider.pivot_opts['rows'],
        cols_choices=models.Provider.pivot_opts['rows']
    )


schema = graphene.Schema(query=Query, auto_camelcase=False)
