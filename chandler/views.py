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
from .models import Product,Profile,Category
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
	# print(request)
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
    # print("herere!!!0")
    form = ProductForm(request.POST,request.FILES)
    if request.method =='POST':
        if form.is_valid():
            post=form.save(commit=True)
            if 'picture' in request.FILES:
                form.picture =request.FILES['picture']
                # print("herere!!!1")
            return HttpResponseRedirect(reverse('chandler:product_list'))
        else:
             return render(request,'chandler/product.html',{'form':form}) 
             # print("herere!!!2")    
    else:
        form = ProductForm()
        # print("herere!!!3")
        return render(request,'chandler/product.html',{'form':form})     

@method_decorator(login_required, name='dispatch')
class ProductUpdate(UpdateView):
	form_class = ProductForm
	template_name = 'chandler/product.html'
	queryset = Product.objects.all()

	def get_success_url(self):
		return reverse('chandler:product_list')
	# def get_object(self):
	# 	id_ = self.kwargs.get('product_id')
	# 	return get_object_or_404(Product,id=id_)


@method_decorator(login_required, name='dispatch')
class ProductDelete(DeleteView):
	template_name = 'chandler/product_delete.html'
	queryset = Product.objects.all()

	def get_success_url(self):
		return reverse('chandler:product_list')

	# def get_object(self):
	# 	id_ = self.kwargs.get('product_id')
	# 	return get_object_or_404(Product,id=id_)


@method_decorator(login_required, name='dispatch')
class ProductList(ListView):
    template_name 	= 'chandler/product_list.html'
    queryset 	  	= Product.objects.all()
    ordering = ['product_id']

    # filterset_class	= ProductFilter

    # def get_queryset(self):
    #     self.product = get_object_or_404(Product, product_name=self.kwargs['product'])
    #     return Product.objects.filter(product=self.product)
    # def product_list(request):
    #     product = Product.objects.all()

    # # filter results!
    #     if request.method == 'GET':
    #         q = request.GET['q']
    #         # print(q)
    #         if q != '':
    #             product = product.filter(product_name__contains=q)
    #             print(product)
    #     context = {'product_name': product_name}
    #     return render_to_response('chandler/product_list.html', context)

@method_decorator(login_required, name='dispatch')
class ProductDetail(DetailView):
    template_name = 'chandler/product_detail.html'
    queryset 	  = Product.objects.all()


#category code below!!!!
@method_decorator(login_required, name='dispatch')
class CategoryList(ListView):
    template_name 	= 'chandler/category_list.html'
    queryset 	  	= Category.objects.all()
    ordering = ['cate_id']

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