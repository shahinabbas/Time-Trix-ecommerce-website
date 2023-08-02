from django.contrib import admin
from cart.models import Cart,CartItem,Strap

class StrapAdmin(admin.ModelAdmin):
    list_display = ['product_id','strap','quantity']
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Strap,StrapAdmin)