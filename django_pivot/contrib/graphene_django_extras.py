from functools import partial

from pandas.core.base import DataError

from graphql import GraphQLError
import graphene
from graphene_django_extras import fields
from django.utils.translation import ugettext_lazy as _

from django_pivot import settings
from django_pivot.forms import PivotForm
from django_pivot import utils

AGGFUNCS = [f['name'] for f in settings.AGGFUNCS]

PivotType = graphene.List(graphene.List(graphene.String))


class PivotField(fields.DjangoFilterListField):
    pivot_args = {
        'values': graphene.List(graphene.String),
        'rows': graphene.List(graphene.String),
        'cols': graphene.List(graphene.String),
        'aggfuncs': graphene.List(graphene.String),
    }

    def __init__(self, _type, extra_filter_meta=None, filterset_class=None,
                 values_choices=None, rows_choices=None, cols_choices=None,
                 round=None, *args, **kwargs):
        self.values_choices = values_choices
        self.rows_choices = rows_choices
        self.cols_choices = cols_choices or rows_choices
        self.round = round or settings.ROUND

        self._base_type = _type
        _fields = _type._meta.filter_fields
        _model = _type._meta.model

        self.fields = fields or _fields
        meta = dict(model=_model, fields=self.fields)
        if extra_filter_meta:
            meta.update(extra_filter_meta)

        filterset_class = filterset_class or _type._meta.filterset_class
        self.filterset_class = fields.get_filterset_class(filterset_class, **meta)
        self.filtering_args = fields.get_filtering_args_from_filterset(self.filterset_class, _type)
        kwargs.setdefault('args', {})
        kwargs['args'].update(self.filtering_args)
        kwargs['args'].update(self.pivot_args)

        graphene.Field.__init__(self=self, type=PivotType, *args, **kwargs)

    def get_queryset(self, manager):
        return manager.all()

    def _get_filter_kwargs(self, kwargs, filtering_args):
        filter_kwargs = {
            k: v for k, v in kwargs.items() if k in filtering_args
        }
        return filter_kwargs

    def list_resolver(self, manager, filterset_class, filtering_args, root, info,
                      values, rows, cols, aggfuncs,
                      values_choices, rows_choices, cols_choices, round,
                      **kwargs):
        qs = self.get_queryset(manager)

        filter_kwargs = self._get_filter_kwargs(kwargs, filtering_args)
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs
        pivot_input = {
            'values': values,
            'rows': rows,
            'cols': cols,
            'aggr': aggfuncs,
        }
        pivot_form = PivotForm(
            data=pivot_input,
            values=values_choices,
            rows=rows_choices,
            cols=cols_choices
        )
        if not pivot_form.is_valid():
            key, values = pivot_form.errors.popitem()
            msg = "%s: %s" % (key, values[0])
            raise GraphQLError(msg)

        try:
            pivot = pivot_form.get_pivot_table(qs)
        except DataError as err:
            if err.args[0] == 'No numeric types to aggregate':
                msg = _("One or several fields don't have values to aggregate.")
                raise GraphQLError(msg)
            raise
        if round is not None:
            pivot = pivot.round(round)
        pivot = utils.verbose_dataframe(pivot)
        if pivot.empty:
            return []
        csv_data = pivot.to_csv()
        return [
            r.split(',')
            for r in csv_data.splitlines()
            if r.strip()
        ]

    def get_resolver(self, parent_resolver):
        return partial(
            self.list_resolver,
            self._base_type._meta.model._default_manager,
            self.filterset_class,
            self.filtering_args,
            values_choices=self.values_choices,
            rows_choices=self.rows_choices,
            cols_choices=self.cols_choices,
            round=self.round,
        )
