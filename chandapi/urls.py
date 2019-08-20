from django.urls import path
from django.conf.urls import include,url
from .views import *
# from .views import login
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework import routers
from . import views

app_name = 'chandlerapi'

router = routers.DefaultRouter()
# router.register(r'cart', views.CartAPIView,basename='cart')
router.register(r'cart', views.CartViewSet,basename='cart')

urlpatterns = [
    # url(r'^', include(router.urls)),
    # 'app.chandlerapi.views',
    # url(r'^add_to_cart/$', views.add_to_cart,name='add_to_cart'),
    path('product_api/', ProductApiView.as_view()),
    path('coupon_api/', CouponAPIView.as_view()),
    path('coupon_t/', CoupontAPIView.as_view()),
    path('cart_api/', CartAPIView.as_view()),
    path('shipad', Shipadd.as_view()),
    path('userlistapi/', UserList.as_view()),
    path('apiregister/', UserCreate.as_view()),
    path('auth/', include('rest_framework.urls')),
    path('tokth/', obtain_auth_token, name='api_token_auth'),
    path('login', login),
    # path('cre/<int:pk>/', Createcart.as_view()),
    url(r'^', include(router.urls)),

]

