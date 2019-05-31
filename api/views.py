from rest_framework import generics
from . import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
import requests
from api.lstm import createLaggedFrame, cleanUpDataframe, model_fit, forecast, model_loader
import pandas as pd

class SalesAll(generics.ListCreateAPIView):
    """
    List all sales or reate new sale
    """
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('stock', 'date',)
    queryset = queryset.order_by('-date')


class GetProduct(generics.ListCreateAPIView):
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('stock', 'date',)
    pagination_class = LimitOffsetPagination
    
    def get_object(self, *args, **kwargs):
        return self.queryset.filter(stock=kwargs.get('stock'))


@api_view(['GET'])
def predict(request, pk):
    # query string for when we add multiple products
    #response = requests.get(f"http://localhost:8000/api/sales?stock={pk}")
    response = requests.get(f"http://localhost:8000/api/sales")
    jsonObject = response.json()
    df = pd.DataFrame(jsonObject)
    df.drop(['date'], axis=1, inplace=True)
    df.drop(['id'], axis=1, inplace=True)
    model = model_loader(pk)
    result = forecast(model, df.tail(8), 7)
    final = result[0][0]
    return HttpResponse(final)
@api_view(['GET'])
def train(request, pk):
    #response = requests.get(f"http://localhost:8000/api/sales?stock={pk}")
    response = requests.get(f"http://localhost:8000/api/sales")
    jsonObject = response.json()
    df = pd.DataFrame.from_dict(jsonObject)
    df = createLaggedFrame(df)
    X_train_vals, X_valid_vals, Y_train, Y_valid = cleanUpDataframe(df)
    model_fit(X_train_vals, X_valid_vals, Y_train, Y_valid, pk)
    return HttpResponse(f"model {pk} has been trained")
