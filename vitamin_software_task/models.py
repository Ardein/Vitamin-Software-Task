from django.db import models


class Company(models.Model):
    ticker = models.CharField(max_length=5)


class StockPrice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()
