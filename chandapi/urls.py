from django.urls import path, include	
from .views import ProductApiView

urlpatterns = [
    path('product_api/', ProductApiView.as_view()),
]