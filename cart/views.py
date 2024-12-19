from django.shortcuts import render,redirect
from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	cart=Cart(request)
	cart_products=cart.get_prods
	quantities=cart.get_quants
	totals=cart.cart_total()
	return render(request,'cart_summary.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals})

def cart_add(request):
	#get cart
	cart=Cart(request)
	if request.POST.get('action')=='post':
		#get stuufd
		product_id=int(request.POST.get('product_id'))
		product_qty=int(request.POST.get('product_qty'))
		#look up product in db
		product= get_object_or_404(Product,id=product_id)
		#save to session
		cart.add(product=product,quantity=product_qty)
		#let get quantity
		cart_quantity=cart.__len__()
		#return response
		# response=JsonResponse({'Product Name':product.name})
		response=JsonResponse({'qty':cart_quantity})
		messages.success(request,("produit ajouté dans la cart","ao soa"))
		return response 

def cart_update(request):
	cart=Cart(request)
	if request.POST.get('action')=='post':
		#get stuufd
		product_id=int(request.POST.get('product_id'))
		product_qty=int(request.POST.get('product_qty'))
		cart.update(product=product_id,quantity=product_qty)

		response=JsonResponse({'qty':product_qty})
		return response
		# return redirect('cart_summary')


def cart_delete(request):
	cart=Cart(request)
	if request.POST.get('action')=='post':
		#get stuufd
		product_id=int(request.POST.get('product_id'))
		# call the fonction delete
		cart.delete(product=product_id)
		response=JsonResponse({'product':product_id})
		return response