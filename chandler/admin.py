from django.contrib import admin
from .models import Profile, Product, Category,Discount,Tax,Cart,Cart_item,ShippingAddress
# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(ShippingAddress)