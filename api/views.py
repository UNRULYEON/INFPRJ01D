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
from api.lstm import createLaggedFrame, cleanUpDataframe, model_fit, forecast, df_preprocessing
import pandas as pd
from joblib import load

class SalesAll(generics.ListCreateAPIView):
    """
    List all sales or reate new sale
    """
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer
#    filter_backends = (DjangoFilterBackend,)
#    filterset_fields = ('stock', 'date',)
#    queryset = queryset.order_by('-date')


class GetProduct(generics.ListCreateAPIView):
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('item', 'location', 'type')
    pagination_class = LimitOffsetPagination
    
    def get_object(self, *args, **kwargs):
        return self.queryset.filter(stock=kwargs.get('year'))


@api_view(['GET'])
def predict(request, pk):
    response = requests.get(f"http://localhost:8000/api/sales?item={pk}")
    jsonObject = response.json()
    main_df = pd.DataFrame(jsonObject)
    forecast_df = main_df.tail(5)
    forecast_df = forecast_df.drop('id', axis=1)
    forecast_df.head()
    forecast_df = df_preprocessing(forecast_df,False)
    forecast_df = forecast_df.values.flatten()
    data = np.array(forecast_df)
    inputarray = data.reshape((1,30,1))
    model = load_model("./api/models/Product.model")
    result = model.predict(inputarray,1)
    scaler = load('./api/scaler.joblib')
    final = scaler.inverse_transform(result)[0][0].round()
    return HttpResponse(final)
