from rest_framework import serializers
from . import models

class SalesSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Sales
    fields = '__all__'