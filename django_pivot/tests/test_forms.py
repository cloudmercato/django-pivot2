from django.test import TestCase
from django_pivot import forms
from django_pivot import defaults
from django_pivot.tests import factories


class PivotFormTest(TestCase):
    form_class = forms.PivotForm

    def test_init(self):
        form = self.form_class(
            values=['temperature', 'humidity'],
            rows=['date', 'city'],
            cols=['provider'],
        )

    def test_clean_format(self):
        form = self.form_class(
            values=['temperature', 'humidity'],
            rows=['date', 'city', 'provider'],
            cols=['date', 'city', 'provider'],
            data={
                'values': ['temperature'],
                'rows': ['date'],
                'cols': ['city'],
                'aggr': ['mean'],
                'format': 'excel',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_empty_format(self):
        form = self.form_class(
            values=['temperature', 'humidity'],
            rows=['date', 'city', 'provider'],
            cols=['date', 'city', 'provider'],
            data={
                'values': ['temperature'],
                'rows': ['date'],
                'cols': ['city'],
                'aggr': ['mean'],
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_no_row_no_col(self):
        form = self.form_class(
            values=['temperature', 'humidity'],
            rows=['date', 'city', 'provider'],
            cols=['date', 'city', 'provider'],
            data={
                'values': ['temperature'],
                'rows': [],
                'cols': [],
                'aggr': ['mean'],
            }
        )
        self.assertFalse(form.is_valid())

    def test_clean_field_in_row_and_col(self):
        form = self.form_class(
            values=['temperature', 'humidity'],
            rows=['date', 'city', 'provider'],
            cols=['date', 'city', 'provider'],
            data={
                'values': ['temperature'],
                'rows': ['city'],
                'cols': ['city'],
                'aggr': ['mean'],
            }
        )
        self.assertFalse(form.is_valid())


class PivotFormGetPivotTableTest(TestCase):
    form_class = forms.PivotForm

    def test_aggrs(self):
        aggrs = [i['name'] for i in defaults.AGGFUNCS]
        for aggr in aggrs:
            form = self.form_class(
                values=['temperature', 'humidity'],
                rows=['date', 'city', 'provider'],
                cols=['date', 'city', 'provider'],
                data={
                    'values': ['temperature'],
                    'rows': ['city'],
                    'cols': ['provider'],
                    'aggr': [aggr],
                }
            )
            self.assertTrue(form.is_valid())
            meteos = factories.MeteoFactory.create_batch(3)
            qs = factories.MeteoFactory._meta.model.objects.all()
            form.get_pivot_table(qs)
