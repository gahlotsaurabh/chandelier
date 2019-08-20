from django import forms
from chandler.models import Profile, Product, Category,Discount,Tax
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from bootstrap_datepicker_plus import DatePickerInput
from datetime import date
# from django.contrib.admin.widgets import AdminDateWidget
	
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
        labels = {
            'cate_fk': ('Parent'),
            }

class ProductForm(forms.ModelForm):
    # product_category_fk = CategoryFormset
    class Meta():
        model  = Product
        fields = ('product_category_fk','product_name','product_description','price','quantity','image1','image2','image3','image4','image5',)

class DiscountForm(forms.ModelForm):
    # start_date_coupon = forms.DateFeild()
    # end_date_coupon   = forms.DateFeild()
    # end_date_coupon = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    # start_date_coupon = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        model = Discount
        widgets = {
            'start_date_coupon': DatePickerInput(format='%Y-%m-%d').start_of('event days'), # default date-format %m/%d/%Y will be used
            'end_date_coupon': DatePickerInput(format='%Y-%m-%d').end_of('event days'), 
             # 'start_date':DatePickerInput().start_of('event days'),
            # 'end_date':DatePickerInput().end_of('event days'),# specify date-frmat
        }
        fields = '__all__'

    def clean_date(self):
        start_date_coupon = self.cleaned_data['start_date_coupon']
        if start_date_coupon < date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return start_date_coupon

class TaxForm(forms.ModelForm):
    # start_date_coupon = forms.DateFeild()
    # end_date_coupon   = forms.DateFeild()
    class Meta:
        model = Tax
        fields = '__all__'