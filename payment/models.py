from django.db import models
from django.contrib.auth.models import User 
from store.models import Product
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver 
import datetime

from phonenumber_field.modelfields import PhoneNumberField



class ShippingAdress(models.Model): #addresse de livraison
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	Shipping_full_name=models.CharField(max_length=255)
	Shipping_email=models.EmailField(max_length=255)
	Shipping_addresse=models.CharField(max_length=255,null=True,blank=True)
	Shipping_city=models.CharField(max_length=255)
	Shipping_zipcode=models.CharField(max_length=255,null=True,blank=True)
	shipping_numberphone=models.CharField(max_length=10,null=True, blank=True)
	

	#dont pluralize addrese
	class Meta:
		# verbose_name_plural = "Shipping Address"
		verbose_name_plural = "Adresse Livraison"


	def __str__(self):
		# return f' Shipping Address -{str(self.id)}'
		return f' Address livraison -{str(self.id)}'

# # creat shipping by default when user signup 
# def create_shipping(sender,instance,created,**kwargs):
# 	if created:
# 		user_shipping=ShippingAdress(user=instance)
# 		user_shipping.save()
# #automate the profile thing 
# post_save.connect(create_shipping,sender=User) 







#create orders models 
class Order(models.Model):   #commande
	#foreign key 
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	full_name=models.CharField(max_length=250)
	email=models.EmailField(max_length=250)
	shipping_addresse=models.TextField(max_length=15000)
	amount_paid=models.DecimalField(max_digits=7,decimal_places=0)
	date_ordered=models.DateTimeField(auto_now_add=True)
	shipped=models.BooleanField(default=False)
	date_shipped=models.DateTimeField(blank=True,null=True)
	def __str__(self):
		return  f' Commande - {str(self.id)}'


#auto add shipping date
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwargs):
	if instance.pk:
		now=datetime.datetime.now()
		obj=sender._default_manager.get(pk=instance.pk)
		if instance.shipped and not obj.shipped:
			instance.date_shipped=now
			



#order items
class OrderItem(models.Model):
	#foreign key 
	order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
	product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	quantity=models.PositiveBigIntegerField(default=1)
	price=models.DecimalField(max_digits=7,decimal_places=0)
	def __str__(self):
		return f' order item -{str(self.id)}'

