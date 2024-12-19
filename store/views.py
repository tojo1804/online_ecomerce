from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Product,Category,Profile
# Create your views here.
from django.db.models import Q

from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,UpdateUserForm,UserInfoForm
from django.contrib.auth import authenticate,login,logout 
from django.db import models
from django.contrib.auth.decorators import login_required
from payment.forms import ShippingForm
from payment.models import ShippingAdress
from cart.cart import Cart

import json

def update_info(request):
	if request.user.is_authenticated:

		# current_user=Profile.objects.get(user__id=request.user.id)
		current_user = get_object_or_404(Profile, user__id=request.user.id)
		# shipping_user=ShippingAdress.objects.get(user=request.user.id)
		shipping_user, created = ShippingAdress.objects.get_or_create(user=request.user)
		form= UserInfoForm(request.POST or None,instance=current_user)
		shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
		
		if form.is_valid() or shipping_form.is_valid():
			form.save()
			shipping_form.save()

			return redirect('home')
		return render(request,'update_user_info.html',{"form":form,"shipping_form":shipping_form})
	else:
		messages.success(request,('error, you must be loged'))
		return redirect('home')








def product_detail(request,pk):
	product=Product.objects.get(id=pk)
	return render(request,'product_detail.html',{'product':product})

def search_product(request):
	# determine if they fill the form before searching
	if request.method=='POST':
		searched= request.POST['searched']
		#let querry the product 
		searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		#let test for the null ou tsis n 'inonona'
		if not searched:
			messages.success(request,'sorry, desolé, le produit n existe pas.. essayer encore..na tsy misy')
			return render(request,"search.html",{})
		else:
			return render(request,"search.html",{"searched":searched})

	else:
		return render(request,"search.html",{})


def home(request):
	products=Product.objects.all()
	return render(request,'home.html',{"products":products}) 


def category(request,foo):
	foo=foo.replace('-',  ' ') 
	try:
		category=Category.objects.get(name=foo)
		products=Product.objects.filter(category=category)
		return render(request,'category.html',{'products':products,'category':category})

	except:
		messages.success(request,("that category doesn't existe"))
		return redirect('home') 

def products_by_category(request):
    # Récupère la catégorie 'Book'
    book_category = Category.objects.get(name="Book")
    # Filtre les produits pour cette catégorie 
    products1 = Product.objects.filter(category=book_category)

    return render(request, 'category.html', {'products1': products1})

def register_user(request):
	if request.method=='POST':
		form=CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login_user')
			messages.success(request,("vous avez bien créé votre compte.. "))
			return redirect('update_info')

	else:
		form=CustomUserCreationForm()
		messages.success(request,("vous avez annulé l'authentification, tsy tafiditra, reessayer  "))
	return render(request,'register.html',{'form':form})

def login_user(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']

		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			#do some shopping stuff 
			current_user=Profile.objects.get(user__id=request.user.id)
			#get thier saved cart from database 
			saved_cart=current_user.old_cart
			#convert database string python dictionnary 
			if saved_cart:
				#convert to dictionnary using json 
				converted_cart=json.loads(saved_cart)
				#add the loaded dictionnary to our session 
				#get the cart 
				cart=Cart(request)
				#loop thru the cart and add the items from the database 
				for key,value in converted_cart.items():
					cart.db_add(product=key,quantity=value)
					



			messages.success(request,("vous êtes connecté au site de commerce"))
			return redirect('home')
		else:

			messages.success(request,("il y a un erreur.. essayer encore"))
			return redirect('login_user')
	else:
		return render(request ,'login.html',{})




def disconnect(request):
	logout(request)
	messages.success(request,("vous êtes déconnecté et reste visiteur seulement"))
	return redirect('home')


@login_required
def update_user(request):
	if request.method=='POST':
		form =UpdateUserForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'utilisateur bien modifier avec succée')
			return redirect('home')
	else:
		form=UpdateUserForm(instance=request.user)
		# messages.success(request,'non modifier')

	return render(request,'update_user.html',{'form':form})

def category_summary(request):
	categories=Category.objects.all()
	return render(request,'category_summary.html',{"categories":categories})
	
