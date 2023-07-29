from django.contrib import admin
from .models import CustomUser,category,Product,user_profile,Cart,CartItem

class CustomUserAdmin(admin.ModelAdmin):
    # Customize the way the model is displayed in the admin site
    list_display = ['email', 'username', 'name', 'phone_number', 'otp']

# Register your CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(category)
admin.site.register(Product)
admin.site.register(user_profile)
admin.site.register(Cart)
admin.site.register(CartItem)

