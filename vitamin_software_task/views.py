import requests
from rest_framework import generics, status
from rest_framework.response import Response

from vitamin_software_task import settings
from vitamin_software_task.models import Company, StockPrice
from vitamin_software_task.serializers import StockPriceSerializer


class StockPriceDefault(generics.RetrieveAPIView):
    def get(self, _):
        return Response(
            status=status.HTTP_403_FORBIDDEN, data={"error": "You must provide a ticker "}
        )


class StockPriceAverage(generics.ListAPIView):
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        company_ticker = self.kwargs.get("ticker", "").upper()

        company, created = Company.objects.get_or_create(ticker=company_ticker)

        if created:
            stock_prices = self._fetch_stock_prices_from_nasdaq(company)
            return StockPrice.objects.bulk_create(stock_prices)

        latest_year = StockPrice.objects.filter(company=company).order_by("-date").first()

        if latest_year:
            new_prices = self._fetch_stock_prices_from_nasdaq(
                company, start_date=latest_year.date
            )

            existing_prices = StockPrice.objects.filter(
                company=company, date__lte=latest_year.date
            )

            StockPrice.objects.bulk_create(new_prices)

            return new_prices + list(existing_prices)

        return StockPrice.objects.bulk_create(
            self._fetch_stock_prices_from_nasdaq(company)
        )

    @staticmethod
    def _fetch_stock_prices_from_nasdaq(company, start_date="1900-01-01"):
        payload = {
            "collapse": "annual",
            "column_index": "1",
            "api_key": settings.NASDAQ_API_KEY,
            "start_date": start_date,
        }
        r = requests.get(settings.NASDAQ_API_URL.format(ticker=company.ticker), params=payload)

        stock_prices = []

        if r.ok:
            dataset = r.json().get("dataset", {})
            for yearly_data in dataset.get("data"):
                date, value = yearly_data
                stock_prices.append(StockPrice(company=company, date=date, value=value))

        return stock_prices
