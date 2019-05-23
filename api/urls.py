from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('sales/', views.SalesAll.as_view()),
    path('sales/<int:pk>', views.SaleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)