from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('products', views.ProductsAll.as_view()),
    path('sales', views.SalesAll.as_view())
    path('sales/predict/<int:pk>', views.predict),
    #path('sales', views.GetProduct.as_view()),
    #path('sales/predict/<int:pk>', views.predict),
    #path('sales/test', views.SalesAll.as_view())
    # Disabled for now. Opted to train the model outside the API.
    # path('sales/train/<int:pk>', views.train)
]

urlpatterns = format_suffix_patterns(urlpatterns)
