from django.contrib import admin
from .models import Category,Product,Client,Profile
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Profile)

#mix profile info and user info 
class ProfileInline(admin.StackedInline):
	model=Profile
#extend the user model 
class UserAdmin(admin.ModelAdmin):
	model=User
	field=["username","first_name","last_name","email"]
	inlines=[ProfileInline]
#unregister the oldway
admin.site.unregister(User)
#re register the new way 
admin.site.register(User,UserAdmin)


