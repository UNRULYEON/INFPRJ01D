from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers

# Create your views here.
def index(req):
  return render(req, 'index.html', {})

class Sales(generics.ListAPIView):
  queryset = models.Sales.objects.all()
  serializer_class = serializers.SalesSerializer