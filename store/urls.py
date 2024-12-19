from django.urls import path
from .import views
urlpatterns = [
	path('',views.home,name="home"),
	path('category/<str:foo>',views.category,name="category"),
	path('search_product',views.search_product,name="search_product"),
	path('product_detail/<int:pk>',views.product_detail,name='product_detail'),
	path('register_user/',views.register_user,name="register_user"),
	path('login/',views.login_user,name="login_user"),
	path('deconnecter',views.disconnect,name="disconnect"),
	path('update_user',views.update_user,name="update_user"),
	path('category_summary',views.category_summary,name="category_summary"),
	path('update_info',views.update_info,name="update_info"),
] 
