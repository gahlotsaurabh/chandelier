from rest_framework import serializers
from chandler.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self,instance):
    	return{
    	'product_name':instance.product_name,
    	'description':instance.product_description,
    	'price':instance.price,
    	'stock':instance.quantity,
    	'thumbnail':instance.image1.url,
    	'id': instance.product_id,
    	'image':[
    			instance.image1.url,
    			instance.image2.url,
    			instance.image3.url,
    			instance.image4.url,
    			instance.image5.url,
    		]
    	}