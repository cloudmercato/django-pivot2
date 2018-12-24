from django.test import TestCase
from django.urls import reverse_lazy as reverse
from django_pivot.tests import factories
from django_pivot.tests.test_project.testapp import models


class ListViewTest(TestCase):
    url = reverse('provider-list')
    csv_data = {
        'pivot-values': ['logs_count'],
        'pivot-rows': ['name'],
        'pivot-aggr': ['mean'],
        'pivot-format': 'csv',
    }

    def setUp(self):
        self.meteos = factories.MeteoFactory.create_batch_provider(10, 5)

    def test_empty_form(self):
        response = self.client.get(self.url)
        self.assertFalse(response.streaming)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'text/html; charset=utf-8')

    def test_filled_form(self):
        data = {
            'pivot-values': ['logs_count'],
            'pivot-rows': ['name'],
            'pivot-aggr': ['mean'],
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'text/html; charset=utf-8')
        self.assertIsNotNone(response.context_data['pivot_form'])
        self.assertTrue(response.context_data['pivot_form'].is_valid(), response.context_data['pivot_form'].errors)

    def test_export_csv(self):
        response = self.client.get(self.url, self.csv_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'text/csv')
        data = response.content.decode().strip().splitlines()
        self.assertEqual(8, len(data))


class FilterViewTest(ListViewTest):
    url = reverse('provider-filter')
    csv_data = {
        'pivot-values': ['logs_count'],
        'pivot-rows': ['name'],
        'pivot-aggr': ['mean'],
        'pivot-format': 'csv',
        'city': 'Douala'
    }

    def setUp(self):
        self.meteos = factories.MeteoFactory.create_batch_provider(10, 5, city='Douala')
        self.bad_meteos = factories.MeteoFactory.create_batch_provider(10, 5)
