from django.contrib import admin
from app.models import CustomUser,category,Product,User_Profile,Wishlist

class CustomUserAdmin(admin.ModelAdmin):
    # Customize the way the model is displayed in the admin site
    list_display = ['email', 'username', 'name', 'phone_number', 'otp']
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','name','city','state','country']
# Register your CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(category)
admin.site.register(Product)
admin.site.register(User_Profile, UserProfileAdmin)
admin.site.register(Wishlist)



