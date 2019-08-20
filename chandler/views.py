from django.shortcuts import render, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.generic import (ListView,DetailView,UpdateView,DeleteView)
from .models import Product,Profile,Category,Tax
from .filters import ProductFilter
from django.forms.models import model_to_dict
from django.contrib.auth.models import User



def index(request):
	return render(request,'chandler/index.html')

@login_required
def special(request):
	return HttpResponse("you are logged in !")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def register(request):
	registered = False
	if request.method =='POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'profile_pic' in request.FILES:
				print('found it')
				profile.profile_pic = request.FILES['profile_pic']
			profile.save()
			registered = True
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request,'chandler/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
	form_class = UserProfileForm
	template_name = 'chandler/registration.html'
	queryset = Profile.objects.all()

	def get_success_url(self):
		return reverse('chandler:user_list')

@method_decorator(login_required, name='dispatch')
class UserDetail(DetailView):
    template_name = 'chandler/user_detail.html'
    queryset = Profile.objects.all()

@method_decorator(login_required, name='dispatch')
class UserDelete(DeleteView):
	template_name = 'chandler/user_delete.html'
	queryset = Profile.objects.all()

	def get_success_url(self):
		return reverse('chandler:user_list')

@method_decorator(login_required, name='dispatch')
class UserList(ListView):
    template_name 	= 'chandler/userlist.html'
    queryset 	  	= Profile.objects.all()
    context_object_name = 'profile_list'

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user:
			if user.is_staff:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Gain staff access first!")
		else:
			print("someone tried to login and failed.!")
			print("they used username: {} and password:{}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request,'chandler/login.html',{})	

#product!!!!!!!!!!!!!

@login_required
def product_management(request):
    form = ProductForm(request.POST,request.FILES)
    if request.method =='POST':
        if form.is_valid():
            post=form.save(commit=True)
            if 'picture' in request.FILES:
                form.picture =request.FILES['picture']
            return HttpResponseRedirect(reverse('chandler:product_list'))
        else:
             return render(request,'chandler/product.html',{'form':form}) 
    else:
        form = ProductForm()
        return render(request,'chandler/product.html',{'form':form})     

@method_decorator(login_required, name='dispatch')
class ProductUpdate(UpdateView):
	form_class = ProductForm
	template_name = 'chandler/product.html'
	queryset = Product.objects.all()

	def get_success_url(self):
		return reverse('chandler:product_list')

@method_decorator(login_required, name='dispatch')
class ProductDelete(DeleteView):
	template_name = 'chandler/product_delete.html'
	queryset = Product.objects.all()

	def get_success_url(self):
		return reverse('chandler:product_list')

@method_decorator(login_required, name='dispatch')
class ProductList(ListView):
    template_name 	= 'chandler/product_list.html'
    queryset 	  	= Product.objects.all()
    ordering		= ['product_id']

@method_decorator(login_required, name='dispatch')
class ProductDetail(DetailView):
    template_name = 'chandler/product_detail.html'
    queryset 	  = Product.objects.all()

#category code below!!!!
@method_decorator(login_required, name='dispatch')
class CategoryList(ListView):
    template_name 	= 'chandler/category_list.html'
    queryset 	  	= Category.objects.all()
    ordering 		= ['cate_fk']

@method_decorator(login_required, name='dispatch')
class CategoryDetail(DetailView):
    template_name = 'chandler/category_detail.html'
    queryset 	  = Category.objects.all()

@method_decorator(login_required, name='dispatch')
class CategoryDelete(DeleteView):
	template_name = 'chandler/category_delete.html'
	queryset = Category.objects.all()

	def get_success_url(self):
		return reverse('chandler:category_list')


@method_decorator(login_required, name='dispatch')
class CategoryUpdate(UpdateView):
	form_class = CategoryForm
	template_name = 'chandler/add_category.html'
	queryset = Category.objects.all()

	def get_success_url(self):
		return reverse('chandler:category_list')

@login_required
def category_management(request):
    form = CategoryForm(request.POST)
    if request.method =='POST':
        if form.is_valid():
            post=form.save(commit=True)
            return HttpResponseRedirect(reverse('chandler:category_list'))
        else:
             return render(request,'chandler/add_category.html',{'form':form})
    else:
        form = CategoryForm()
        return render(request,'chandler/add_category.html',{'form':form}) 

#  Discounts
@method_decorator(login_required, name='dispatch')
class DiscountList(ListView):
    template_name 	= 'chandler/discount_list.html'
    queryset 	  	=   Discount.objects.all()
    ordering = ['coupon_id']

@method_decorator(login_required, name='dispatch')
class DiscountDetail(DetailView):
    template_name = 'chandler/discount_detail.html'
    queryset 	  =   Discount.objects.all()

@method_decorator(login_required, name='dispatch')
class DiscountDelete(DeleteView):
	template_name = 'chandler/discount_delete.html'
	queryset =   Discount.objects.all()

	def get_success_url(self):
		return reverse('chandler:discount_list')


@method_decorator(login_required, name='dispatch')
class DiscountUpdate(UpdateView):
	form_class =   DiscountForm
	template_name = 'chandler/add_discount.html'
	queryset =   Discount.objects.all()

	def get_success_url(self):
		return reverse('chandler:discount_list')

@login_required
def discount_management(request):
    form = DiscountForm(request.POST)
    if request.method =='POST':
        if form.is_valid():
            post=form.save(commit=True)
            return HttpResponseRedirect(reverse('chandler:discount_list'))
        else:
             return render(request,'chandler/add_discount.html',{'form':form})
    else:
        form =   DiscountForm()
        return render(request,'chandler/add_discount.html',{'form':form}) 

#tax
@method_decorator(login_required, name='dispatch')
class TaxList(ListView):
    template_name 	= 'chandler/tax_list.html'
    queryset 	  	=  Tax.objects.all()
    ordering 		= ['id']

@method_decorator(login_required, name='dispatch')
class TaxDetail(DetailView):
    template_name = 'chandler/tax_detail.html'
    queryset 	  =   Tax.objects.all()

@method_decorator(login_required, name='dispatch')
class TaxDelete(DeleteView):
	template_name = 'chandler/tax_delete.html'
	queryset 	  = Tax.objects.all()

	def get_success_url(self):
		return reverse('chandler:tax_list')


@method_decorator(login_required, name='dispatch')
class TaxUpdate(UpdateView):
	form_class 		=  TaxForm
	template_name 	= 'chandler/add_tax.html'
	queryset 		=  Tax.objects.all()

	def get_success_url(self):
		return reverse('chandler:tax_list')

@login_required
def tax_management(request):
    form = TaxForm(request.POST)
    if request.method =='POST':
        if form.is_valid():
            post=form.save(commit=True)
            return HttpResponseRedirect(reverse('chandler:tax_list'))
        else:
             return render(request,'chandler/add_tax.html',{'form':form})
    else:
        form =   TaxForm()
        return render(request,'chandler/add_tax.html',{'form':form}) 