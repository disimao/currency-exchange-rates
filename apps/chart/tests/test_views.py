import unittest
import copy


from currency_exchange_rates.settings.unit_tests import mongo_client


from rest_framework.test import APITestCase
from django.urls import reverse


class RatesEndpointTestCase(APITestCase):
    @unittest.mock.patch("apps.chart.api.views.mongo_client", mongo_client)
    def test_get_rates_endpoint(self):
        rates = [
            {
                "rates": {
                    "EUR": 0.91441111923921,
                    "USD": 1.0,
                    "JPY": 107.48902706656914,
                    "BRL": 5.2440563277249455,
                },
                "date": "2020-04-01",
                "base": "USD",
            },
            {
                "rates": {
                    "EUR": 0.9169264624977077,
                    "USD": 1.0,
                    "JPY": 107.33541169998166,
                    "BRL": 5.2285897671006785,
                },
                "date": "2020-04-02",
                "base": "USD",
            },
            {
                "rates": {
                    "EUR": 0.9272137227630969,
                    "USD": 1.0,
                    "JPY": 108.57672693555864,
                    "BRL": 5.275197032916087,
                },
                "date": "2020-04-03",
                "base": "USD",
            },
            {
                "rates": {
                    "EUR": 0.9266981744045965,
                    "USD": 1.0,
                    "JPY": 108.92410341951627,
                    "BRL": 5.287369103882865,
                },
                "date": "2020-04-06",
                "base": "USD",
            },
        ]

        db = mongo_client["exchange_rates"]
        collection = db["rates"]
        collection.insert_many(copy.deepcopy(rates))

        url = reverse("api_get_rates_by_date")
        response = self.client.get(
            url, QUERY_STRING="start_date=2020-04-01&end_date=2020-04-06"
        )
        self.assertEquals(rates, response.json())
