from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from chandler.models import Product,Cart,Cart_item,ShippingAddress,Discount,OrderHistroy
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import generics,filters,viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

import logging
from math import floor
import json
from rest_framework.parsers import JSONParser
from django.db.models import F
# Create your views here.

class ProductApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserCreate(generics.CreateAPIView):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer
    # queryset = User.objects.all() 

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Shipadd(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = ShippingAddressSerializer
    
    # @api_view(['GET'])
    def get(self,request,*args,**kwargs):
        shipad = ShippingAddress.objects.filter(user=request.user)
        # if (shipad != NULL):
        se = ShippingAddressSerializer(shipad,many=True)
        if se.data == None:
            return Response({'error':'no address'},status=status.HTTP_400_BAD_REQUEST)
        return Response(se.data,status=status.HTTP_200_OK)
        # import ipdb;ipdb.set_trace()
   
    def post(self, request, format=None):
        user= request.user
        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

class CouponAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class    = CouponSerializer
    queryset            = Discount.objects.all()
    filter_backends     = (DjangoFilterBackend,SearchFilter)
    search_fields       = ('coupon_code',)

class CoupontAPIView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CouponSerializer

    def post(self, request, format=None):
        uww = request.data['cc']
        coupon = Discount.objects.get(coupon_code=uww)
        if coupon.is_active :
            co ={
                'coupon_value' : coupon.value,
                'typ': coupon.coupon_type
            }
            return Response(co)
        return Response({'error': 'coupon inactive'})

    def get_coupon(self, request,*args, **kwargs):
        coupon = Discount.objects.get_or_404(coupon_code=request)
        return coupon

  
class CartAPIView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_cart(self, request,*args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        # import ipdb;ipdb.set_trace()
        return cart

    
    def get(self, request, format=None):
        car   = self.get_cart(request)
        ca    = Cart_item.objects.filter(cart=car.id)
        sera  = CartItemtwoSerializer(ca,many=True)
        ser = CartSerializer(car)
        ll = [sera.data,ser.data]
        # import ipdb;ipdb.set_trace()
        return Response(ll, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # try:
           #add or delete product from requested user cart 
        if 'delete_product' in request.data :          
           
            to_delete        = request.data['delete_product']
            # ca          = Cart_item.objects.filter(cart=car.id)
            delete_product   = Product.objects.get(product_id=to_delete)
            user_cart        = Cart.objects.get(user=request.user)
            user_item        = Cart_item.objects.filter(cart=user_cart.id).filter(product_id=request.data['delete_product'])
            item_count       = user_item.values_list('product_count',flat=True)
            cart_items       = Cart_item.objects.filter(cart=user_cart.id)
            #     de.delete()
            all_counts      = cart_items.values_list('product_count',flat=True)
            cart_serializer = CartSerializer(user_cart)    
            # item_serializer = CartItemSerializer(user_item,many=True)
            ser_ial            = CartItemtwoSerializer(cart_items,many=True)
            if (item_count[0] == 0):
                content = {
                        'status': 1, 
                        'responseCode' : status.HTTP_200_OK,
                        "cart id" : user_cart.id,
                        "items_in_cart"   : user_cart.items.count(),
                        'user'    : user_cart.user.username,
                        'dom'     : ser_ial.data,
                        }
                return Response(content)
            user_item.update(product_count=F('product_count')-1)
            # import ipdb;ipdb.set_trace()
            if (item_count[0] == 0):
                 user_item.delete()
                 content = {
                        'status': 1, 
                        'responseCode' : status.HTTP_200_OK,
                        "cart id" : user_cart.id,
                        "items_in_cart"   : user_cart.items.count(),
                        'user'    : user_cart.user.username,
                        'dom'     : ser_ial.data,
                        }
                 return Response(content)
                 
            content = {
            'status': 1, 
            'responseCode' : status.HTTP_200_OK, 
            "cart id" : user_cart.id,
            "items_in_cart"   : user_cart.items.count(),
            'user'    : user_cart.user.username,
            'dom'     : ser_ial.data,
             }
            return Response(content)
        else:
            req = request.data['product_id']
            pro = Product.objects.get(product_id=req)
            old_cart,new_cart = Cart.objects.get_or_create(user=request.user)
            # o=k.values_list('product_count',flat=True)
            user_cart      = Cart.objects.get(user=request.user)
            cart_items     = Cart_item.objects.filter(cart=user_cart.id)
            all_counts     = cart_items.values_list('product_count',flat=True)
            ser_ial        = CartItemtwoSerializer(cart_items,many=True)
            

            if old_cart:
                old = Cart_item.objects.filter(cart=old_cart.id).filter(product_id=req)
                # item_serializer       = CartItemSerializer(old,many=True)
                old.update(product_count=F('product_count')+1)
                old_cart.items.add(pro)
                cart_serializer= CartSerializer(old_cart)
                content = {
                            'status': 1, 
                            'responseCode' : status.HTTP_200_OK,
                            "cart id" : user_cart.id,
                            "items_in_cart"   : user_cart.items.count(),
                            'user'    : user_cart.user.username,
                            'dom'     : ser_ial.data,
                            }
                return Response(content) 
            else:
                new_cart.items.add(pro)
                old         = Cart_item.objects.filter(cart=old_cart.id).filter(product_id=req)
                content = {
                            'status': 1, 
                            'responseCode' : status.HTTP_200_OK,
                            
                            "cart id" : user_cart.id,
                            "items_in_cart"   : user_cart.items.count(),
                            'user'    : user_cart.user.username,
                            }
                return Response(content)

class CartViewSet(viewsets.ModelViewSet):
    model = Cart
    serializer_class = CartSerializer
    
    def get_queryset(self,):
        return Cart.objects.filter(user=1)

    @action(detail=True, methods=['put'])
    def add_to_cart(self, request, pk):
        pro = Product.objects.filter(id=pk)
        cart_obj= Cart.objects.get_or_404(request)
        cart_obj.items.set()
        cart_obj.product.add(*product_obj)
        return cart_obj
    # return Response(status=status.HTTP_200_OK, data={'message': 'Product has been added to cart'})


class OrderHistroyAPIView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = OrderHistroySerializer

    def get(self,request,*args,**kwargs):
        shipad = ShippingAddress.objects.filter(user=request.user)
        # if (shipad != NULL):
        se = OrderHistroySerializer(shipad,many=True)
        if se.data == None:
            return Response({'error':'no order found'},status=status.HTTP_400_BAD_REQUEST)
        return Response(se.data,status=status.HTTP_200_OK)
        # import ipdb;ipdb.set_trace()
        # if shipad.exists():        # else:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # else:

    def post(self, request, format=None):
        user        = request.user
        user_cart   = Cart.objects.get(user=request.user)
        cart_items  = Cart_item.objects.filter(cart=user_cart.id)
        ci          = cart_items.values_list('product_id')
        # od          = OrderHistroy.objects.create(user=user,product_id=ci)
        # import ipdb;ipdb.set_trace()
        for i in range(0,3):
            # j=0
            pro    = Product.objects.get(i[0][0])
            OrderHistroy.product.add(pro)
            # j+=1       
        serializer  = OrderHistroySerializer(data=request.data)
        if serializer.is_valid():

            serializer.validated_data['user'] = user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
