============
django-pivot
============

django-pivot is a wrapper around numpy, pandas and django-pandas letting
you easily manipulate pivot tables on your queryset.

Install
=======

::

  pip install django-pivot2
  
Modify your model(s) to use ``django_pandas.managers.DataFrameManager`` or
``django_pandas.managers.DataFrameQuerySet``: ::

  class LongTimeSeries(models.Model):
    date_ix = models.DateTimeField()
    series_name = models.CharField(max_length=100)
    value = models.FloatField()

    objects = DataFrameManager()
    
Usage
=====

This app basicaly gives APIs to request a pivot table. Everything is not automatic
and developer must always declare:

- The possible values
- The possible rows and columns

And for a end-user the API will ask

- Values
- Rows
- Columns
- Aggregation functions
- Applied function
- Format

As class-based view
-------------------

A mixin is available to compose you own pivot. It has the following behavior:
- Display a form to collect parameters of pivot table
- Display pivot table as HTML if valid input is given
- Download data as file with format given in form

Example: ::

  from django_filters.views import FilterView
  from django_pivot.views import PivotView
  from myapp import models

  class LongTimeSeriesPivotView(PivotView, FilterView):
      template_name = "pivot.html
      model = models.LongTimeSeries
      
      values_choices = ['date_ix', 'value']
      rows_choices = cols_choices = ['serie_name', 'date_ix', 'value']
      
``PivotView`` is compatible with Django's ``ListView``, django-filters' ``FilterView``
or any kind of view with the same behavior.


With graphene-django
--------------------

Coming soon

With graphene-django-extras
---------------------------

Example of schema.py: ::

  from graphene_django import DjangoObjectType
  from django_pivot.contrib.graphene_django_extras import PivotField
  from myapp import models

  class LongTimeSeriesType(DjangoObjectType):
      class Meta:
          model = models.LongTimeSeries
  
  class Query:
      pivot_long_time_series = PivotField(
          LongTimeSeriesType,
          filterset_class=filtersets.LongTimeSeriesFilter,
          values_choices=['date_ix', 'value'],
          rows_choices=['serie_name', 'date_ix', 'value'],
          cols_choices=['serie_name', 'date_ix', 'value'],
      )
      
Example of request: ::

  query {
    pivot_long_time_series (values: ["value"], rows: ["serie_name"], cols: ["value"], aggfuncs: ["mean"])
  }

As GraphQL is supposed to return JSON only and pandas JSON format is ..hum... weird,
we convert pivot_table into CSV and after into a list of list, so fully compatible.

With Django REST Framework
--------------------------

Coming soon
