from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    # if 'admin' in request.path:
    #     return {}
    # else:
    #     try:
    #         cart = Cart.objects.filter(cart_id=_cart_id(request))
    #         cart_item = CartItem.objects.all().filter(cart=cart[:1])
    #         for cart_item in cart_item:
    #             cart_count += cart_item.quantity
    #     except Exception as e:
    #         cart = Cart.objects.filter(cart_id=_cart_id(request))
    #         cart_item = CartItem.objects.all().filter(cart=cart[:1])
    #         for cart_item in cart_item:
    #             cart_count += cart_item.quantity
            
    return dict(cart_count=cart_count)
