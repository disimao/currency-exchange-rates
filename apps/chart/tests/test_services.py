from unittest.mock import patch


from django.test import SimpleTestCase


from apps.chart.services import get_rates_by_date_from_vatcomply


class VatcomplyRatesEndpointTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.rates = [
            {
                "date": "2023-02-02",
                "base": "USD",
                "rates": {
                    "EUR": 0.9179364787956674,
                    "USD": 1.0,
                    "JPY": 129.7686800073435,
                    "BRL": 5.064622728107215,
                    "CAD": 1.3315586561409951,
                },
            }
        ]
        self.rates_only_needed_currencies = self.rates
        del self.rates_only_needed_currencies[0]["rates"]["CAD"]
        return super().setUp()

    @patch("apps.chart.services.requests.get")
    def test_get_rates_by_date_from_vatcomply_with_date_range_more_than_five_business_days_return_only_business_days(
        self, mock_get
    ):
        mock_get.return_value.json.return_value = self.rates[0]
        rates_list = get_rates_by_date_from_vatcomply(
            "2023-01-01", "2023-01-13"
        )
        self.assertIsInstance(rates_list, list)
        self.assertListEqual(
            rates_list,
            [self.rates_only_needed_currencies[0] for i in range(10)],
        )

    @patch("apps.chart.services.requests.get")
    def test_get_rates_by_date_from_vatcomply_with_date_range_equal_to_five_business_days_return_list(
        self, mock_get
    ):
        mock_get.return_value.json.return_value = self.rates[0]
        rates_list = get_rates_by_date_from_vatcomply(
            "2023-02-06", "2023-02-10"
        )
        self.assertIsInstance(rates_list, list)
        self.assertTrue(len(rates_list) == 5)

    @patch("apps.chart.services.requests.get")
    def test_vatcomply_get_rates_by_date_return_ok(self, mock_get):
        mock_get.return_value.ok = True
        rates_list = get_rates_by_date_from_vatcomply(
            "2023-01-02", "2023-01-06"
        )
        self.assertIsNotNone(rates_list)

    @patch("apps.chart.services.requests.get")
    def test_vatcomply_get_rates_by_date_return_rates_list(self, mock_get):
        mock_get.return_value.json.return_value = self.rates[0]
        rates_list = get_rates_by_date_from_vatcomply(
            "2023-01-02", "2023-01-02"
        )
        self.assertIsInstance(rates_list, list)
        self.assertListEqual(rates_list, self.rates_only_needed_currencies)

    @patch("apps.chart.services.requests.get")
    def test_vatcomply_get_rates_by_date_return_only_needed_currencies(
        self, mock_get
    ):
        mock_get.return_value.json.return_value = self.rates[0]
        rates_list = get_rates_by_date_from_vatcomply(
            "2023-01-02", "2023-01-02"
        )
        self.assertIsInstance(rates_list, list)
        self.assertListEqual(rates_list, self.rates_only_needed_currencies)
