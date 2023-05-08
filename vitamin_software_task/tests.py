from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from vitamin_software_task.models import Company, StockPrice


class StockPriceAverageTestCase(APITestCase):

    def setUp(self):
        self.ticker = 'AAPL'
        self.url = reverse('stock_prices_average', args=[self.ticker])
        self.company, _ = Company.objects.get_or_create(ticker=self.ticker)

    def test_missing_ticker_param(self):
        url = reverse('stock_prices_default')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'You must provide a ticker ')

    @patch('vitamin_software_task.views.requests.get')
    def test_created_company(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {'dataset': {'data': [['2022-01-01', '10'], ['2021-01-01', '20']]}}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertQuerysetEqual(StockPrice.objects.filter(company=self.company),
                                 [stock for stock in self.company.stockprice_set.all()], ordered=False)

    @patch('vitamin_software_task.views.requests.get')
    def test_existing_company(self, mock_get):
        existing_stock = StockPrice.objects.create(company=self.company, date='2020-01-01', value=50)
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {'dataset': {'data': [['2022-01-01', '10'], ['2021-01-01', '20']]}}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertIn(existing_stock, StockPrice.objects.filter(company=self.company))
        self.assertQuerysetEqual(StockPrice.objects.filter(company=self.company),
                                 [stock for stock in self.company.stockprice_set.all()], ordered=False)
