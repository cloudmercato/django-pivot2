from django.test import TestCase
from django.test import Client as BaseClient
from django.urls import reverse_lazy as reverse
from django_pivot.tests import factories

INVALID_Q = """query {
    pivot_providers (values: [], rows: [], cols: [], aggfuncs: [])
}"""
Q = """query {
    pivot_providers (values: ["logs_count"], rows: ["name"], cols: [], aggfuncs: ["mean"])
}"""
FILTER_Q = """query {
    pivot_providers (values: ["logs_count"], rows: ["name"], cols: [], aggfuncs: ["mean"], city: "Douala")
}"""


class GrapheneClient(BaseClient):
    url = reverse('graphql')

    def query(self, query):
        response = self.get(path=self.url, data={'query': query})
        return response


class PivotFieldTest(TestCase):
    client_class = GrapheneClient

    def test_invalid_input(self):
        response = self.client.query(INVALID_Q)
        data = response.json()
        self.assertIsNone(data['data']['pivot_providers'])
        self.assertEqual(len(data['errors']), 1)
        self.assertIn('This field is required', data['errors'][0]['message'])

    def test_query(self):
        self.meteos = factories.MeteoFactory.create_batch_provider(10, 5)
        response = self.client.query(Q)
        data = response.json()
        self.assertIsNotNone(data['data'])
        self.assertEqual(8, len(data['data']['pivot_providers']))

    def test_filter(self):
        # Setup
        self.meteos = factories.MeteoFactory.create_batch_provider(10, 5, city="Douala")
        self.bad_meteos = factories.MeteoFactory.create_batch_provider(10, 5)
        # Test
        response = self.client.query(FILTER_Q)
        data = response.json()
        # Check
        self.assertIsNotNone(data['data'])
        self.assertEqual(8, len(data['data']['pivot_providers']))
