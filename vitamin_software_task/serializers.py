from rest_framework import serializers
from .models import Company, StockPrice


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "ticker"]


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        # {
        #     "year": YYYY,
        #     "value": VV.VV
        # }
        fields = ["date", "value"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["date"] = representation["date"][:4]  # YYYY-MM-DD -> YYYY
        return representation
