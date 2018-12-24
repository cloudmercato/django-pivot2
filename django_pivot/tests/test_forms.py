from django.test import TestCase
from django_pivot import forms
from django_pivot.tests import factories


class PivotFormTest(TestCase):
    form_class = forms.PivotForm

    def test_init(self):
        form = self.form_class(
            values=['temperature', 'humidity'],
            rows=['date', 'city'],
            cols=['provider'],
        )
