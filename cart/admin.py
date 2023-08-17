from django.contrib import admin
from cart.models import Cart,CartItem,Strap,Order,OrderItem

class StrapAdmin(admin.ModelAdmin):
    list_display = ['id','product_id','strap','quantity','is_active']
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user','product','cart','quantity','is_active']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','order_date','order_status','payment_method','order_id']
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_no','product','strap','quantity']
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Strap,StrapAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)