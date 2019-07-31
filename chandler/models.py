from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=500, blank=False)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
        
    def __str__(self):
        return self.user.username
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

class Category(models.Model):
    cate_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45)
    cate_fk     = models.ForeignKey('self',on_delete=models.SET_NULL,null=True, blank=True)
    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=45)
    product_description = models.CharField(max_length=500, blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    product_category_fk = models.ForeignKey('Category', on_delete=models.SET_NULL, db_column='product_category_fk',related_name='pros',null=True, blank=True)
    image1 = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image2 = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image3 = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image4 = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')
    image5 = models.ImageField(upload_to='chand_imgs',blank=True,default='noimage.png')

    def get_absolute_url(self):
        return 'chandler/product_detail/%s/'%(self.product_id)