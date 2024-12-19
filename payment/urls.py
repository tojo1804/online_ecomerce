from django.urls import path
from .import views
urlpatterns=[
	path('payment_success',views.payment_success,name='payment_success'),
	path('checkout',views.checkout,name='checkout'),
	path('billing_info',views.billing_info,name="billing_info"),
	path('process_order',views.process_order,name="process_order"),
	path('envoye_colis',views.envoye_colis,name="envoye_colis"),
	path('non_envoye_colis',views.non_envoye_colis,name="non_envoye_colis"),
	path('orders/<int:pk>',views.orders,name="orders"),
	
	
]