from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('sales', views.GetProduct.as_view()),
    path('sales/predict/<int:pk>', views.predict),
    # Disabled for now. Opted to train the model outside the API.
    # path('sales/train/<int:pk>', views.train)
]

urlpatterns = format_suffix_patterns(urlpatterns)
