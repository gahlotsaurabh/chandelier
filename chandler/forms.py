from django import forms
from chandler.models import Profile, Product, Category
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
	
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')
   
class UserProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('mobile_no','address','profile_pic')


class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Cate fk+ new category'}))
    class Meta:
        model = Category
        fields = ('category_name','cate_fk' )

class ProductForm(forms.ModelForm):
    # product_category_fk = CategoryFormset
    class Meta():
        model  = Product
        fields = ('product_category_fk','product_name','product_description','price','quantity','image1','image2','image3','image4','image5',)

# class ProductForm(forms.ModelForm):
#     product_name = forms.CharField(max_length=128)
#     product_description = forms.CharField(max_length=500, label="Item Description.")
#     price = forms.IntegerField()
#     quantity = forms.IntegerField()
#     class Meta:
#         model = Product
#         fields = ('product_name','product_description','price','quantity',)


# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Image')
#     class Meta:
#         model = Images
#         fields = ('image', )