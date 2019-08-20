from rest_framework import serializers
from chandler.models import Product,Profile,Cart,Cart_item,ShippingAddress,OrderHistroy,Discount
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from drf_writable_nested import WritableNestedModelSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self,instance):
    	return{
    	'product_name':instance.product_name,
    	'description':instance.product_description,
    	'price'      :instance.price,
    	'quantity'   :instance.quantity,
    	'thumbnail'  :instance.image1.url,
    	'id'         : instance.product_id,
      'image'      :[
              			instance.image1.url,
              			instance.image2.url,
              			instance.image3.url,
              			instance.image4.url,
              			instance.image5.url,
              		  ]
    	}

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
      model = ShippingAddress
      fields = ('__all__')

class ProfileSerializer(serializers.ModelSerializer):
    mobile_no        = serializers.CharField(required=True,validators=[UniqueValidator(queryset=Profile.objects.all())])
    # shiping_address  = AddressSerializer(required=False)
    class Meta:
        model = Profile
        fields = ('mobile_no', 'address',)

class UserSerializer(serializers.ModelSerializer):
    profile   = ProfileSerializer(required=True)
    shipping  = ShippingAddressSerializer(required=False)
    password  = serializers.CharField(write_only=True)
    email     = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model  = User
        fields = ('username','email','password','profile','shipping')


    def create(self, validated_data, instance=None):
            profile_data = validated_data.pop('profile')
            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            Profile.objects.update_or_create(user=user,**profile_data)
            return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email')


class CartSerializer(WritableNestedModelSerializer):
    # items   = ProductSerializer(required=False,many=True)
    user    = serializers.CharField(read_only=True)
    # url = serializers.HyperlinkedRelatedField(read_only=True,view_name='chandler:product-detail',source='product')
    class Meta:
        model = Cart
        fields = ('id','user','status')


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(required=True)
    product = ProductSerializer()
    class Meta:
      model = Cart_item
      fields = ('product_count','product','cart')

#for custom response in cart view
class CartItemtwoSerializer(serializers.ModelSerializer):
    # cart = CartSerializer(required=True)
    # product = ProductSerializer()
    class Meta:
      model = Cart_item
      fields = ('product_count','product','cart')

    def to_representation(self,instance):
      return{
          'product_name':instance.product.product_name,
          'product_in_cart':instance.product_count,
          'price'      :instance.product.price,
          'product_id':instance.product.product_id,
          'quantity'   :instance.product.quantity,
          'thumbnail'  :instance.product.image1.url,
          }

    # def create(self, validated_data, instance=None):
    #     # pdata = validated_data.pop('profile')
    #     items = Cart.objects.create(**validated_data)
    #     # user.set_password(validated_data['password'])
    #     items.save()
    #     # Cart.objects.update_or_create(user=user,**items)
    #     return items

class OrderHistroySerializer(serializers.ModelSerializer):

    class Meta:
        model  = OrderHistroy
        fields = ('__all__')

class CouponSerializer(serializers.ModelSerializer):

  class Meta:
      model = Discount
      fields = ('__all__')