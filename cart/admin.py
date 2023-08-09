from django.contrib import admin
from cart.models import Cart,CartItem,Strap,Order,OrderItem

class StrapAdmin(admin.ModelAdmin):
    list_display = ['product_id','strap','quantity']
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','order_date','order_status']
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_no','product','strap','quantity']
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Strap,StrapAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)