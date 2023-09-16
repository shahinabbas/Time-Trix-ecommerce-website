from django.contrib import admin
from app.models import CustomUser, Category, Product, User_Profile, Wishlist, OrderAddress


class CustomUserAdmin(admin.ModelAdmin):
    # Customize the way the model is displayed in the admin site
    list_display = ['email', 'username', 'name', 'phone_number', 'otp']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'state', 'country']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'is_deleted']


# Register your CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(User_Profile, UserProfileAdmin)
admin.site.register(Wishlist)
admin.site.register(OrderAddress)
