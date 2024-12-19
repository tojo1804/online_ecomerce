from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm ,PaymentForm


from django.contrib.auth.models import User
from payment.models import ShippingAdress,Order,OrderItem
from django.contrib import messages

from store.models import Product,Profile
# Create your views here.
import datetime

def orders(request,pk):
	if request.user.is_authenticated and request.user.is_superuser:
		order=Order.objects.get(id=pk)
		#get the orderitem 
		items=OrderItem.objects.filter(order=pk)
		if request.POST:
			status=request.POST['shipping_status']
			#check if true or false
			if status=="true":
				order=Order.objects.filter(id=pk)
				now=datetime.datetime.now()
				order.update(shipped=True,date_shipped=now)
			else:
				order=Order.objects.filter(id=pk)
				order.update(shipped=False)
			messages.success(request,("miova..."))
			return redirect('home')

		return render(request,'payment/orders.html',{'order':order,'items':items})

	else:
		messages.success(request,("Non accées,reserver pour admin only"))
		return redirect('home')





def envoye_colis(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders=Order.objects.filter(shipped=True)
		if request.POST:
			status=request.POST['shipping_status']
			#check if true or false
			num=request.POST['num']		
			order=Order.objects.filter(id=num)
			now=datetime.datetime.now()
			order.update(shipped=False)
		
			messages.success(request,("miova..."))
			return redirect('home')
		return render(request,'payment/envoye_colis.html',{'orders':orders})
	else:
		messages.success(request,("Non accées,reserver pour admin only"))
		return redirect('home')


 

def non_envoye_colis(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders=Order.objects.filter(shipped=False)
		if request.POST:
			status=request.POST['shipping_status']
			#check if true or false
			num=request.POST['num']		
			order=Order.objects.filter(id=num)
			now=datetime.datetime.now()
			order.update(shipped=True,date_shipped=now)
		
			messages.success(request,("miova..."))
			return redirect('home')
		return render(request,'payment/non_envoye_colis.html',{'orders':orders})
	else:
		messages.success(request,("Non accées,reserver pour admin only"))
		return redirect('home')
	# return render(request,'payment/non_envoye_colis.html',{})











def process_order(request):
	if request.POST:
		cart=Cart(request)
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals=cart.cart_total()

		payment_form=PaymentForm(request.POST or None)
		#get shipping stuff
		my_shipping=request.session.get('my_shipping')
		#create order info 
		full_name=my_shipping['Shipping_full_name']
		email=my_shipping['Shipping_email']
		#let create  shipping adresse from session 	
		shipping_addresse = f"{my_shipping['Shipping_addresse']}\n{my_shipping['Shipping_city']}\n{my_shipping['Shipping_zipcode'],my_shipping['shipping_numberphone']}"
		amount_paid=totals
 
		
 
		if request.user.is_authenticated:
			user=request.user

			#create an order 
			create_order = Order(user=user,full_name=full_name,email=email,shipping_addresse=shipping_addresse,amount_paid=amount_paid)
			create_order.save()
			#add order item 
			#get the order ID 
			order_id=create_order.pk
			#get the product info
			for product in cart_products():
				product_id=product.id 
				#get product price 
				if product.is_sale:
					price=product.sale_price
				else:
					price=product.price 

				#get the  quantity 
				for key,value in quantities().items():
					if int(key) == product.id:
						# create order item 
						create_order_item=OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
						create_order_item.save()

			#let s delete our cart after order inline ou commande mipetraka 
			for key in list(request.session.keys()):
				if key == "session_key":
					#delete the key 
					del request.session[key]


			#delete cart from database 'old cart field'

			current_user=Profile.objects.filter(user__id=request.user.id)
			# delete shopping cart from database
			current_user.update(old_cart="")









			messages.success(request,("commande bien placé"))
			return redirect('home')
		else:
			#create an order 
			create_order=Order(full_name=full_name,email=email,shipping_addresse=shipping_addresse,amount_paid=amount_paid)
			create_order.save()
			#add order item 
			#get the order ID 
			order_id=create_order.pk
			#get the product info
			for product in cart_products():
				product_id=product.id 
				#get product price 
				if product.is_sale:
					price=product.sale_price
				else:
					price=product.price 

				#get the  quantity 
				for key,value in quantities().items():
					if int(key) == product.id:
						# create order item 
						create_order_item=OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
						create_order_item.save()
			#let s delete our cart after order inline ou commande mipetraka 
			for key in list(request.session.keys()):
				if key == "session_key":
					#delete the key 
					del request.session[key]
					
			messages.success(request,("commande bien placé"))
			return redirect('home')



	return redirect('home')
	messages.success(request,("acces denied"))


def payment_success(request):
	return render(request,'payment/payment_success.html',{})

def checkout(request):
	cart=Cart(request)
	cart_products=cart.get_prods
	quantities=cart.get_quants
	totals=cart.cart_total()
	if request.user.is_authenticated:
		shipping_user, created = ShippingAdress.objects.get_or_create(user=request.user)
		shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
		return render(request,'payment/checkout.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
	else:
		# shipping_form=ShippingForm(request.POST or None)
		# return render(request,'payment/checkout.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals})
		messages.success(request,("il connecter ou creer un nouveau pour avoir accées"))
		return redirect('home')
		


def billing_info(request):
	if request.POST:
		cart=Cart(request)
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals=cart.cart_total()
		#create a session with shipping info 
		my_shipping=request.POST
		request.session['my_shipping']=my_shipping
		# shipping_info=request.POST
		#check if user is logged
		if request.user.is_authenticated:
			billing_form = PaymentForm()
			return render(request,'payment/billing_info.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})
		else:
			billing_form = PaymentForm()
			return render(request,'payment/billing_info.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})


		
	else:
		return redirect('home')
		messages.success(request,"il faut connecter")



	