from app.models import Product
from .models import Cart, CartItem,Strap
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from psycopg2 import IntegrityError
from django.contrib import messages


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart_plus(request,strap_id):
    print('sadffffagr215212154125421525215412221111')
    strap=get_object_or_404(Strap,id=strap_id)
    try :
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(strap = strap,user = request.user)
            if cart_item.quantity >= 1:
                cart_item.quantity += 1
                cart_item.save()
    except:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(strap = strap,cart= cart)
        if cart_item.quantity >= 1:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('cart')



def add_cart(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    strap_id=request.POST.get('strap_id')

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except cart.DoesNotExist:
        Cart.objects.create(cart_id=_cart_id(request))

    strap = get_object_or_404(Strap, id=strap_id) 
        
    try:
        cart_item=CartItem.objects.get(product=product, strap=strap, cart=cart)
        cart_item.quantity += 1
        if cart_item.quantity > cart_item.Quantity:
            cart_item.quantity=cart_item.Quantity
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            strap=strap
        )
    return redirect('/cart')


    





    # product = get_object_or_404(Product, id=product_id)
    # strap = request.POST.get('strap_id')
    # print(strap)

    # try:
    #     cart = Cart.objects.get(cart_id=_cart_id(request))
    # except Cart.DoesNotExist:
    #     cart = Cart.objects.create(cart_id=_cart_id(request))
    #     print('hiiiiiiiiiiiiiiiiiiii')

    # if CartItem.objects.filter(strap=strap).exists():
    #     print('hiiiiiiiiiiiiiiiiiiii')
    #     return cart_plus(request,strap)
    # else:
    #     cart_item = CartItem.objects.create(
    #         product=product,
    #         quantity=1,
    #         cart=cart,
    #         strap_id=strap,
    #     )
    # return redirect('/cart')



# def add_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     strap = request.POST.get('strap_id')
    
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(
#         cart_id=_cart_id(request)
#         )
#         cart.save()

#     if strap is not None:
#         try: 
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#                 strap_id=strap,
#             )
#             cart_item.save()
#         except:
#             messages.error(request,'select')
#     return redirect('/cart')

    # if request.method == 'POST':
    #         product=get_object_or_404(Product,id= product_id)
    #         user = request.user if request.user.is_authenticated else None
    #         cart, _ = Cart.objects.get_or_create(user=user)
    #         strap_id = request.POST.get('strap_id')  # Get the selected product size ID from the request

    #         if strap_id is not None:
    #             try:
    #                 cart_item, created = cart.cart_items.get_or_create(product=product, strap_id=strap_id)

    #                 if not created:
    #                     cart_item.quantity += 1
    #                     # if cart_item.quantity > cart_item.strap.Quantity:
    #                     #     cart_item.quantity = cart_item.strap.Quantity
    #                 cart_item.save()

    #             except IntegrityError:
    #                 messages.error(request, 'Please select a valid size.')
                    
    #         else:
    #             messages.error(request, 'Please select a size.')
    #             return redirect('product_details',product_id=product_id)

    # return redirect('cart')



def cartpage(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    org_tot = 0
    tot = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        tot = 0

        # ship = 0
        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)//100
        grand_total = total + tax
        tot = (cart_item.product.price * cart_item.quantity)
        org_tot = grand_total - tot

    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'org_tot': org_tot,
        # 'shipping_charge':CartItem.shipping_charge,
    }
    return render(request, 'cart.html', context)


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/cart')


def delete_cart_item(request, product_id):
    cart_item = get_object_or_404(CartItem, id=product_id)
    cart_item.delete()
    return redirect('/cart')
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get(product=product, cart=cart)
    # cart_item.delete()
    # return redirect('/cart')
