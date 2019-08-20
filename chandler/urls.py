from django.conf.urls import url
from django.urls import path
from chandler import views
from .views import *
# SET THE NAMESPACE!

app_name = 'chandler'
# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^products/$',views.product_management,name='products'),
    url(r'^user_list/$',UserList.as_view(),name='user_list'),
    path('user_detail/<int:pk>/',UserDetail.as_view(),name='user_detail'),
    path('product_list/',ProductList.as_view(),name='product_list'),
    path('product_detail/<int:pk>/',ProductDetail.as_view(),name='product_detail'),
    path('<int:pk>/product_update',ProductUpdate.as_view(),name='product_update'),
    path('<int:pk>/product_delete',ProductDelete.as_view(),name='product_delete'),
    path('<int:pk>/user_delete',UserDelete.as_view(),name='user_delete'),
    path('<int:pk>/user_update',UserUpdate.as_view(),name='user_update'),
    url(r'^category/$',views.category_management,name='category'),
    path('category_list/',CategoryList.as_view(),name='category_list'),
    path('category_detail/<int:pk>/',CategoryDetail.as_view(),name='category_detail'),
    path('<int:pk>/category_update',CategoryUpdate.as_view(),name='product_update'),
    path('<int:pk>/category_delete',CategoryDelete.as_view(),name='product_delete'),
    url(r'^discount/$',views.discount_management,name='coupon'),
    path('discount_list/',DiscountList.as_view(),name='discount_list'),
    path('discount_detail/<int:pk>/',DiscountDetail.as_view(),name='discount_detail'),
    path('<int:pk>/discount_update',DiscountUpdate.as_view(),name='discount_update'),
    path('<int:pk>/discount_delete',DiscountDelete.as_view(),name='discount_delete'),
    url(r'^add_tax/$',views.tax_management,name='coupon'),
    path('tax_list/',TaxList.as_view(),name='tax_list'),
    path('tax_detail/<int:pk>/',TaxDetail.as_view(),name='tax_detail'),
    path('<int:pk>/tax_update',TaxUpdate.as_view(),name='tax_update'),
    path('<int:pk>/tax_delete',TaxDelete.as_view(),name='tax_delete'),

]