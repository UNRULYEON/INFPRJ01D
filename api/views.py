from rest_framework import generics
from . import models
from . import serializers

class SalesAll(generics.ListCreateAPIView):
    """
    List all sales or reate new sale
    """
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer


class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a sale instance
    """
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer