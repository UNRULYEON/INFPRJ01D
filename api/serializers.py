from rest_framework import serializers
from . import models

class ProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Products
    fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Sales
    fields = '__all__'