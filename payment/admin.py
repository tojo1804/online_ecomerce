from django.contrib import admin
from .models import ShippingAdress,Order,OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAdress)
admin.site.register(Order)
admin.site.register(OrderItem)



#create order item inline 
class OrderItemInline(admin.StackedInline):
	model=OrderItem
	extra=0
#extend our order 
class OrderAdmin(admin.ModelAdmin):
	model=Order
	readonly_fields=["date_ordered"]
	fields=['user','full_name','shipping_addresse','amount_paid','date_ordered','shipped','date_shipped']
	inlines=[OrderItemInline]

#unregister order model 
admin.site.unregister(Order)
#reactiver 
admin.site.register(Order,OrderAdmin)
