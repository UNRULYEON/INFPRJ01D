from django.urls import path
from . import views

app_name = "API"

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', views.Sales.as_view(), name='sales'),
]