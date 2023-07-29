from django.shortcuts import render
from app.models import Product
from .models import Cart,CartItem
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('/cart')


def cartpage(request, total=0, quantity=0, cart_items=None):
    tax=0  
    grand_total = 0 
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        tot=0
        
        # ship = 0 
        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
            tot += (cart_item.product.price * cart_item.quantity)
        #     ship += cart_item.offer_total_price()

        # if ship >= 1000:
        #     shipping_charge = 0
        # else:
        #     shipping_charge = 40

        tax = (3 * total)/100
        grand_total=total + tax
        org_tot = tot - grand_total

    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        # 'org_tot':org_tot,
        # 'shipping_charge':shipping_charge,
    }
    return render(request, 'cart.html', context)


def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id = _cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/cart')


def delete_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id =_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('/cart')

