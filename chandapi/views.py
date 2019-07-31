from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from chandler.models import Product
from rest_framework.views import APIView
from rest_framework import generics,filters,viewsets
# Create your views here.

class ProductApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer