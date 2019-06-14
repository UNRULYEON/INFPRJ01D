from rest_framework import generics
from . import models
from . import serializers
import numpy as np
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
import requests
from keras.models import load_model
from api.lstm import createLaggedFrame, cleanUpDataframe, model_fit, forecast, df_preprocessing, difference
import pandas as pd
from joblib import load
import keras.backend as K
class SalesAll(generics.ListCreateAPIView):
    """
    List all sales or reate new sale
    """
    serializer_class = serializers.SalesSerializer
    def get_queryset(self):
        queryset = models.Sales.objects.all()
        item = self.request.query_params.get('item')
        year = self.request.query_params.get('year')
        week = self.request.query_params.get('week')
        location = self.request.query_params.get('location')
        reverse = self.request.query_params.get('reverse')
        if item is not None:
            queryset = models.Sales.objects.filter(item=item)
        if year or week or location is not None:
            queryset = models.Sales.objects.filter(year=year,week=week,location=location)
        if reverse == 'False':
            queryset = queryset.order_by('id')[:6]
        else:
            queryset = queryset.order_by('-id')[:6]
        return queryset

class ProductsAll(generics.ListCreateAPIView):
    """
    List all products or create a new product
    """
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductsSerializer

@api_view(['GET'])
def predict(request, pk):
    response = requests.get(f"http://localhost:8000/api/sales?item={pk}")
    jsonObject = response.json()
    forecast_df = pd.DataFrame(jsonObject)
    forecast_df = forecast_df.drop('id', axis=1)
    forecast_df['stock'] = difference(forecast_df['stock'])
    forecast_df = forecast_df.head(5)
    forecast_df = forecast_df[::-1]
    forecast_df = df_preprocessing(forecast_df,False)
    forecast_df = forecast_df.values.flatten()
    data = np.array(forecast_df)
    inputarray = data.reshape((1,30,1))
    K.clear_session()
    model = load_model("./api/models/Product-model.model")
    model.load_weights("./api/models/weightTest-diffed.h5")
    result = model.predict(inputarray,1)
    item = pd.DataFrame(jsonObject)

    item = item['stock']
    item = item.tail(1).values
    final = item[0] + result[0][0]
    return HttpResponse(final.round())
