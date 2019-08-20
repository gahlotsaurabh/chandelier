from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum
from django.utils.timezone import now
from django.utils import timezone   
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_no       = models.CharField(max_length=20, blank=True)
    address         = models.TextField(max_length=500, blank=False)
    profile_pic     = models.ImageField(upload_to='profile_pics',blank=True)
    # date_created    = models.DateTimeField(auto_now_add=True,default=timezone.now())
        
    def __str__(self):
        return self.user.username
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

class Category(models.Model):
    cate_id         = models.AutoField(primary_key=True)
    category_name   = models.CharField(max_length=45)
    cate_fk         = models.ForeignKey('self',on_delete=models.SET_NULL,null=True, blank=True)
    # date_created    = models.DateTimeField(auto_now_add=True))
    
    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id          = models.AutoField(primary_key=True)
    product_name        = models.CharField(max_length=45)
    product_description = models.TextField(blank=True, null=True)
    price               = models.IntegerField()
    quantity            = models.IntegerField()
    product_category_fk = models.ForeignKey('Category', on_delete=models.SET_NULL, db_column='product_category_fk',related_name='pros',null=True, blank=True)
    image1              = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image2              = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image3              = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image4              = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image5              = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    # date_created        = models.DateTimeField(auto_now_add=True))


    def get_absolute_url(self):
        return 'chandler/product_detail/%s/'%(self.product_id)

class CouponType(enum.Enum):
    PERCENT_TYPE = 2
    FLAT_TYPE    = 1


class Discount(models.Model):
    coupon_id           = models.AutoField(primary_key=True)
    coupon_name         = models.CharField(max_length=50)
    value               = models.IntegerField()
    coupon_code         = models.CharField(max_length=20)
    coupon_description  = models.CharField(max_length=200,blank=True,null=True)
    coupon_type         = enum.EnumField(CouponType, default=CouponType.PERCENT_TYPE)
    start_date_coupon   = models.DateField(blank=True)
    end_date_coupon     = models.DateField(blank=False)
    is_active           = models.BooleanField(default=False)
    # date_created        = models.DateTimeField(auto_now_add=True))


    def __str__(self):
        return self.coupon_name
        # self.get_discount_display()}

class Tax(models.Model):
    # coupon_id           = models.AutoField(primary_key=True)
    tax_name         = models.CharField(max_length=50)
    tax_value        = models.IntegerField()
    # coupon_code         = models.CharField(max_length=20)
    tax_description  = models.CharField(max_length=200,blank=True,null=True)
    # coupon_type         = enum.EnumField(CouponType, default=CouponType.PERCENT_TYPE)
    # start_date_coupon   = models.DateField(blank=True)
    # end_date_coupon     = models.DateField(blank=False)
    # is_active           = models.BooleanField(default=False)
    # date_created     = models.DateTimeField(auto_now_add=True))

    def __str__(self):
        return self.tax_name


class Cart(models.Model):
    # date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    status       = models.CharField(max_length=255, blank=True, null=True)
    user         = models.OneToOneField(User,on_delete=models.SET_NULL, null=True,related_name="carts")
    items        = models.ManyToManyField(Product,blank=True,through='Cart_item',related_name='in_cart')


class Cart_item(models.Model):
    cart          = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True,related_name='cart')
    product       = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    product_count = models.IntegerField(default=1)


class ShippingAddress(models.Model):
    name     = models.CharField("Full name",max_length=50)
    user     = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    address1 = models.CharField("Address line 1",max_length=1000)
    address2 = models.CharField("Address line 2",max_length=1024)
    zip_code = models.CharField("ZIP / Postal code",max_length=8)
    fone_no  = models.CharField(max_length=20, blank=True)
    city     = models.CharField("City",max_length=50)
    state    = models.CharField("State",max_length=50)


class OrderHistroy(models.Model):
    user             = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product          = models.ForeignKey(Product,on_delete=models.CASCADE)
    shippingaddress  = models.ForeignKey(ShippingAddress,on_delete=models.SET_NULL,null=True)
    txnid            = models.CharField(max_length=50)
    firstname        = models.CharField(max_length=20)
    item_no          = models.CharField(max_length=50)
    checksum         = models.CharField(max_length=50)
    status           = models.CharField(max_length=50)
    amount           = models.IntegerField()
    orderplaced_on   = models.DateField(auto_now_add=True)