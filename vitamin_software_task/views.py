from rest_framework import generics, status
from rest_framework.response import Response


class StockPriceDefault(generics.RetrieveAPIView):
    def get(self, _):
        return Response(
            status=status.HTTP_403_FORBIDDEN, data={"error": "You must provide a ticker "}
        )
