from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
from . import models
from . import serializers

@api_view(['GET', 'POSt'])
def sales_all(request):
  if request.method == 'GET':
    queryset = models.Sales.objects.all()
    serializer = serializers.SalesSerializer(queryset, many = True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = serializers.SalesSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sales_detail(request, id):
  try:
    q = models.Sales.objects.get(id = id)
  except:
    return Response(status = status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.SalesSerializer(q)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = serializers.SalesSerializer(q, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    q.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

