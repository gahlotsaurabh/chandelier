from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from chandler.models import Product,Cart,Cart_item,ShippingAddress,Discount
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
        # if shipad.exists():
        # import ipdb;ipdb.set_trace()
        return Response(se.data,status=status.HTTP_200_OK)
        # else:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # else:

    def post(self, request, format=None):
        serializer = ShippingAddressSerializer(data=request.data)
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

    def post(self, request,*args, **kwargs):
        u = request.data['cc']
        coupon = Discount.objects.get(coupon_code=u)
        # co = CouponSerializer(coupon)
        # import ipdb;ipdb.set_trace()
        if coupon.is_active :
            co ={
                'coupon_value' : coupon.value,
                'typ': coupon.coupon_type
            }
            return Response(co)
        return Response({'error': 'coupon inactive'},
                        status=HTTP_404_NOT_FOUND)    

    def get_coupon(self, request,*args, **kwargs):
        coupon = Discount.objects.get_or_404(coupon_code=request)
        return coupon

    # def post(self, request, format=None):
    #     coup = get_coupon(request.data['ccode'])
    #     # test = get_object_or_404(Discount,coupon_id=coup.coupon_id)
    #     if coup.isexist():
    #         if coup.is_active == True :
    #             # if coup.coupon_type == PERCENT_TYPE :
    #             return coup.value
    #         return Response('inactive coupon')
    #     return Response(coup)    
            
#
class CartAPIView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_cart(self, request,*args, **kwargs):
        # cart_id = Cart.objects.all().filter(user_id=request.user.id)
        # cart_id = self.request.GET.get(self.request.user.id)
        # print(cart_id,'yyyyyyyyyyyy')
        # print(self.request.user)
        cart = Cart.objects.get(user=request.user)
        # import ipdb;ipdb.set_trace()
        # try:
        #     cart = Cart.objects.all(id=cart_id)
        # except:
        #     pass
            # cart = Cart.objects.get(id=2)
        return cart

    
    def get(self, request, format=None):
        car   = self.get_cart(request)
        ca    = Cart_item.objects.filter(cart=car.id)
        sera  = CartItemtwoSerializer(ca,many=True)
        ser = CartSerializer(car)
        ll = [sera.data,ser.data]
        # import ipdb;ipdb.set_trace()
        # data = [{
        #     "cart id" : cart.id,
        #     "items": cart.items.count(),
        #     'user' : cart.user.username,
        #     'req' : self.request.user.username,
        #     "product": cart.items.values(), #ca.values_list('product_count',flat=True),
        #     "qua" : ca.values_list('product_count',flat=True) ,
        #     # 'sub total': cart.items.price
        # }]

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
                            # 'data'    : 
                            # 'data'    : 
                            # 'data'    : 
                            # 'data'    :
                            # 'data'    : 
                        "cart id" : user_cart.id,
                        "items_in_cart"   : user_cart.items.count(),
                        'user'    : user_cart.user.username,
                        # 'req'     : self.request.user.username,
                        # 'count'   : all_counts,
                        'dom'     : ser_ial.data,
                        # 'custom'   : cart_items.values(),
                        # 'cartii'  : cart_items.values(),
                        # 'data'    : serializer.data,
                        # "product" : user_cart.items.values('price','product_id','product_name'),
                        }
                return Response(content)
            user_item.update(product_count=F('product_count')-1)
            # import ipdb;ipdb.set_trace()
            if (item_count[0] == 0):
                 user_item.delete()
                 content = {
                        'status': 1, 
                        'responseCode' : status.HTTP_200_OK,
                            # 'data'    : 
                            # 'data'    : 
                            # 'data'    : 
                            # 'data'    :
                            # 'data'    : 
                        "cart id" : user_cart.id,
                        "items_in_cart"   : user_cart.items.count(),
                        'user'    : user_cart.user.username,
                        # 'req'     : self.request.user.username,
                        # 'count'   : all_counts,
                        'dom'     : ser_ial.data,
                        # 'custom'   : cart_items.values(),
                        # 'cartii'  : cart_items.values(),
                        # 'data'    : serializer.data,
                        # "product" : user_cart.items.values('price','product_id','product_name'),
                        }
                 return Response(content)
                 # cart_serializer = CartSerializer(user_cart)
                 # serializer_list = serializer.data
                 #    # content = {
                 #    # 'status': 1, 
                 #    # 'responseCode' : status.HTTP_200_OK, 
                 #    # 'data': Serializer_list,
                 #    # }
                 # return Response(sera.data)
            # Serializer_list = [serializer.data, sera.data]
            content = {
            'status': 1, 
            'responseCode' : status.HTTP_200_OK,
                # 'data'    : 
                # 'data'    : 
                # 'data'    : 
                # 'data'    :
                # 'data'    : 
            "cart id" : user_cart.id,
            "items_in_cart"   : user_cart.items.count(),
            'user'    : user_cart.user.username,
            # 'req'     : self.request.user.username,
            # 'count'   : all_counts,
            'dom'     : ser_ial.data,
            # 'custom'   : cart_items.values(),
            # 'cartii'  : cart_items.values(),
            # 'data'    : serializer.data,
            # "product" : user_cart.items.values('price','product_id','product_name'),
            }
            return Response(content)
                # return Response(sera.data, status=status.HTTP_200_OK)
            # return Response(sera.data, status=status.HTTP_200_OK)
            # return Response(del_)
        else:
            # request.data['product_id']
            # if requeata['product_id']: 
            req = request.data['product_id']
            pro = Product.objects.get(product_id=req)
            old_cart,new_cart = Cart.objects.get_or_create(user=request.user)
            # o=k.values_list('product_count',flat=True)
            user_cart      = Cart.objects.get(user=request.user)
            cart_items     = Cart_item.objects.filter(cart=user_cart.id)
            all_counts     = cart_items.values_list('product_count',flat=True)
            ser_ial        = CartItemtwoSerializer(cart_items,many=True)
            # k = Cart_item.objects.filter(cart=new_cart.id).filter(product_id=req)

            # import ipdb;ipdb.set_trace()
            # if Cart_item.objects.filter(product_id=req).exists():
                # k = Cart_item.objects.filter(cart_id=request.user.id)
                # k.product_count += 1

            if old_cart:
                old = Cart_item.objects.filter(cart=old_cart.id).filter(product_id=req)
                # item_serializer       = CartItemSerializer(old,many=True)
                old.update(product_count=F('product_count')+1)
                old_cart.items.add(pro)
                cart_serializer= CartSerializer(old_cart)
                content = {
                            'status': 1, 
                            'responseCode' : status.HTTP_200_OK,
                                # 'data'    : 
                                # 'data'    : 
                                # 'data'    : 
                                # 'data'    :
                                # 'data'    : 
                            "cart id" : user_cart.id,
                            "items_in_cart"   : user_cart.items.count(),
                            'user'    : user_cart.user.username,
                            # 'req'     : self.request.user.username,
                            # 'count'   : all_counts,
                            'dom'     : ser_ial.data,
                            # 'custom'   : cart_items.values(),
                            # 'cartii'  : cart_items.values(),
                            # 'data'    : serializer.data,
                            # "product" : user_cart.items.values('price','product_id','product_name'),
                            }
                return Response(content) 
            else:
                    # new = Cart_item.objects.filter(cart=new_cart.id).filter(product_id=req)
                    # new.update(product_count=F('product_count'))
                new_cart.items.add(pro)
                old         = Cart_item.objects.filter(cart=old_cart.id).filter(product_id=req)
                # item_serializer       = CartItemSerializer(old,many=True)
                content = {
                            'status': 1, 
                            'responseCode' : status.HTTP_200_OK,
                                # 'data'    : 
                                # 'data'    : 
                                # 'data'    : 
                                # 'data'    :
                                # 'data'    : 
                            "cart id" : user_cart.id,
                            "items_in_cart"   : user_cart.items.count(),
                            'user'    : user_cart.user.username,
                            # 'req'     : self.request.user.username,
                            # 'count'   : all_counts,
                            # 'dom'     : sera.data,
                            # 'custom'   : cart_items.values(),
                            # 'cartii'  : cart_items.values(),
                            # 'data'    : serializer.data,
                            # "product" : user_cart.items.values('price','product_id','product_name'),
                            }
                return Response(content)
                # serializer  = CartSerializer(new_cart)
                # return Response(sera.data, status=status.HTTP_200_OK)
    # serializer_class = ProductSerializer




# class Createcart(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CartSerializer
#     lookup_field = 'pk'

#     def get_queryset(self):
#         return Cart.objects.all()

#     # def post(self, request, format=None):
#     #     serializer = CartSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk, format=None):
#         snip = self.get_or_404bject()
#         serializer = CartSerializer(snip, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    
    
#     @action(detail=True, methods=['post'])
#     def add_to_cart(self, request, pk):
#         cart_obj = Cart.objects.get_or_404(request)
#         product_id = pk
#         qs = Product.objects.filter(id=product_id)
#         if qs.count() == 1:
#             product_obj = qs.first()
#             if product_obj not in cart_obj.products.all():
#                 cart_obj.products.add(product_obj)
#             else:
#                 cart_obj.products.remove(product_obj)
#             request.session['cart_items'] = cart_obj.products.count()
#         return Response(status=status.HTTP_200_OK, data={'message': 'Product has been added to cart'


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
        # cart_obj = Cart.objects.get_or_404(request)
        # product_id = pk
        # qs = Product.objects.filter(id=pk)
        # if qs.count() == 1:
        #     product_obj = qs.first()
        #     if product_obj not in cart_obj.products.all():
        #         cart_obj.products.add(*product_obj)
        #         # items.set(product_obj)
        #     else:
        #         cart_obj.products.remove(product_obj)
        #     request.session['cart_items'] = cart_obj.products.count()
        # return Response(status=status.HTTP_200_OK, data={'message': 'Product has been added to cart'})

    # def put(self, request, pk, format=None):
    #     snip = self.get_object(id=pk)
    #     serializer = CartSerializer(snip, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


    # def get(self, request,pk):
    #     print(self.request.user)
    #     snip = self.get_object(pk)
    #     serializer = CartSerializer(snip)
    #     return Response(serializer.data)

# class AddProduct(ProductApiView, viewsets.ModelViewSet):

#     @action(detail=True, methods=['post'])
#     def add_to_cart(self, request, pk):
#         cart_obj = Cart.objects.get_or_404(request)
#         product_id = pk
#         qs = Product.objects.filter(id=product_id)
#         if qs.count() == 1:
#             product_obj = qs.first()
#             if product_obj not in cart_obj.products.all():
#                 cart_obj.products.add(product_obj)
#             else:
#                 cart_obj.products.remove(product_obj)
#             request.session['cart_items'] = cart_obj.products.count()
#         return Response(status=status.HTTP_200_OK, data={'message': 'Product has been added to cart'

# @permission_classes((AllowAny,))
# @api_view(['post'])
# def add_to_cart(request):
#     print('request')
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             #log.info(request.user.id)

#             data = JSONParser().parse(request)
#             # log.info(data)
#             product_id = data['product_id']
#             # size = data['size']
#             quantity = data['quantity']

#             user = User.objects.get(username='admin')
#             product = Product.objects.get(id=product_id)

#             price = float(quantity) * product.price
#             print(user)

#             #user = request.user
#             try:
#                 cart = Cart.objects.get(product_id=product_id, user=user)
#                 cart.quantity += 1
#                 cprice += product.price
#             except Cart.DoesNotExist:
#                 cart = Cart.objects.create(product_id=product_id, user=user,quantity=quantity, price=price)
#             cart.save()
#             carts = Cart.objects.filter(user=user)
#             cart_quantity = len(carts)

#             if cart:
#                 return Response({'message': 'success', 'quantity': cart_quantity, 'user_id': user.id},
#                                 status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
