from rest_framework import generics
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend

class SalesAll(generics.ListCreateAPIView):
    """
    List all sales or reate new sale
    """
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('stock', 'date',)

class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a sale instance
    """
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer