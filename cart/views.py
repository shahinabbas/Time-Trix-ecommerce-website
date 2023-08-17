
from app.models import CustomUser, Product,User_Profile,Category
from .models import Cart, CartItem,Strap,Order,OrderItem
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from psycopg2 import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.template.loader import render_to_string
import razorpay
from django.conf import settings
from django.http import Http404
import uuid

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:   
        try:
            cart=Cart.objects.get(user=request.user)
            print("----")
            print("old cart",type(cart) )  
            print(cart)
            if cart:
                print("insdie")
            else:
                print("no")  
        except:
            print("okkk")
            print(request.user)
            try:
                cart=Cart.objects.create(user=request.user)
            except Exception as e:
                print(e)
                print("cartttttt")

            print("new cart",cart)   
    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart=Cart.objects.create(cart_id=_cart_id(request))
        
    if request.method=='POST':
        strap_id=request.POST.get('strap_id')
        quantity = int(request.POST.get('quantity', 1)) 
        print("post method",cart)   
        cart_item,created=CartItem.objects.get_or_create(product=product,strap_id=strap_id,cart=cart)
        print(cart_item)
        if not created:
            cart_item.quantity += 1
            if cart_item.quantity > cart_item.strap.quantity:
                cart_item.quantity = cart_item.strap.quantity  
        else:
            cart_item.quantity = quantity   
        cart_item.save()
    return redirect('cart')

# def add_cart(request, product_id):
#     user=request.user
#     print(user)
#     if user.is_authenticated:
#         print(user)
#         product=get_object_or_404(Product,id=product_id)
#         if request.method=='POST':
#             try:
#                 print(user)
#                 cart = Cart.objects.filter(user=user)
#             except Cart.DoesNotExist:
#                 cart,_ = Cart.objects.create(user=user) 
#             strap_id=request.POST.get('strap_id')
#             quantity = int(request.POST.get('quantity', 1)) 
#             cart_item,created=Cart.get_or_create(product=product,strap_id=strap_id,user=user)
#             if not created:
#                 cart_item.quantity += 1
#                 if cart_item.quantity > cart_item.strap.quantity:
#                     cart_item.quantity = cart_item.strap.quantity  
#             else:
#                 cart_item.quantity = quantity   
#             cart_item.save()
#     else:
#         product=get_object_or_404(Product,id=product_id)
#         if request.method=='POST':
#             try:
#                 cart=Cart.objects.get(cart_id=_cart_id(request))

#             except Cart.DoesNotExist:
#                 cart = Cart.objects.create(cart_id=_cart_id(request))  
#             strap_id=request.POST.get('strap_id')
#             quantity = int(request.POST.get('quantity', 1)) 
#             cart_item,created=cart.cart_items.get_or_create(product=product,strap_id=strap_id)
                    
#             if not created:
#                 cart_item.quantity += 1
#                 if cart_item.quantity > cart_item.strap.quantity:
#                     cart_item.quantity = cart_item.strap.quantity  
#             else:
#                 cart_item.quantity = quantity   
#             cart_item.save()
#     return redirect('cart')



def cart_plus(request, strap_id):
    strap = get_object_or_404(Strap, id=strap_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(strap=strap, cart=cart)
        if cart_item.quantity >= 1:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')



def cart_minus(request, strap_id):
    strap = get_object_or_404(Strap, id=strap_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(strap=strap, cart=cart)
        if cart_item.quantity >= 1:
            cart_item.quantity -= 1
            cart_item.save()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


# def cart_plus(request,strap_id):
#     strap=get_object_or_404(Strap,id=strap_id)
#     try :
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(strap = strap,user = request.user)
#             if cart_item.cart_quantity >= 1:
#                 cart_item.cart_quantity += 1
#                 cart_item.save()
#     except:
#         cart = Cart.objects.get(cart_id = _cart_id(request))
#         cart_item = CartItem.objects.get(strap = strap,cart=cart)
#         if cart_item.cart_quantity >= 1:
#             cart_item.cart_quantity += 1
#             cart_item.save()
#     return redirect('cart')

# def cart_plus(request, strap_id):
#     strap = get_object_or_404(Strap, id=strap_id)
#     print(strap,'111111111111111111111111111111111111111111')
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(strap=strap,user=request.user)
#             if cart_item.quantity >= 1:
#                 cart_item.quantity += 1
#                 # if cart_item.quantity > cart_item.strap.quantity:
#                 #     cart_item.quantity = cart_item.strap.quantity
#                 #     messages.info(request, 'Out of stock')
#                 cart_item.save()
#     except:
#         print('88888888888888888888888888888888888888888888888')
#         cart=Cart.objects.get(card_id=_cart_id(request))
#         print(cart,'111111111111111111111111111111111111111111')
#         cart_item = CartItem.objects.get(strap=strap,cart=cart)
#         if cart_item.quantity >= 1:
#             cart_item.quantity += 1
#             # if cart_item.quantity > cart_item.strap.quantity:
#             #     cart_item.quantity = cart_item.strap.quantity
#             #     messages.info(request, 'Out of stock')
#             print("Before saving:", cart_item.quantity,'11111111111111111111111111111111111111111111111')
#             cart_item.save()
#             print("After saving:", cart_item.quantity,'1111111111111111111111111111111111111')

#     return redirect('cart')

    # updated_html = render_to_string('cart.html', {'cart_item': cart_item})
    # return JsonResponse({'html': updated_html})


# def cart_minus(request, strap_id):
#     if request.user.is_authenticated:
#         try:
#             strap = get_object_or_404(Strap, id=strap_id)
#             cart_item = CartItem.objects.get(strap=strap, user=request.user)
            
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 cart_item.save()
#             else:
#                 cart_item.delete()
#         except CartItem.DoesNotExist:
#             pass  # Handle the case when the cart item does not exist
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         strap = get_object_or_404(Strap, id=strap_id)
        
#         try:
#             cart_item = CartItem.objects.get(strap=strap, cart=cart)
            
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 cart_item.save()
#             else:
#                 cart_item.delete()
#         except CartItem.DoesNotExist:
#             pass  # Handle the case when the cart item does not exist
    
#     return redirect('cart')


# def cart_minus(request, strap_id):
#     if request.user.is_authenticated:
#         strap = get_object_or_404(Strap, id=strap_id)
#         cart_item = CartItem.objects.get(strap=strap,user=request.user)

#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     else:
#         cart = Cart.objects.get(cart_id = _cart_id(request))
#         strap = get_object_or_404(Strap, id=strap_id)
#         cart_item = CartItem.objects.get(strap=strap,cart=cart)

#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()

#     return redirect('cart')
    # updated_html = render_to_string('cart.html', {'cart_item': cart_item})
    # return JsonResponse({'html': updated_html})




def cartpage(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            print(cart_items)

        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
            pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        }
    return render(request, 'cart.html', context)



def delete_cart_item(request, product_id):
    cart_item = get_object_or_404(CartItem, id=product_id)
    cart_item.delete()
    return redirect('cart')
    

def order_details(request,id):
    order = get_object_or_404(Order, order_id=id)
    product = OrderItem.objects.filter(order_no=order)
    return render(request,"order_details.html",{'product':product,'order':order})


# def delete_cart_item(request, product_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get(product=product, cart=cart)
    # cart_item.delete()
    # return redirect('/cart')


# def add_cart(request, product_id):
#     product = get_object_or_404(Product,id=product_id)
#     strap_id=request.POST.get('strap_id')
    
#     try:
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#     except cart.DoesNotExist:
#         Cart.objects.create(cart_id=_cart_id(request))

#     strap = get_object_or_404(Strap, id=strap_id) 
        
#     try:
#         cart_item=CartItem.objects.get(product=product, strap=strap, cart=cart)
#         cart_item.quantity += 1
#         if cart_item.quantity > cart_item.Quantity:
#             cart_item.quantity=cart_item.Quantity
#             cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item=CartItem.objects.create(
#             product=product,
#             quantity=1,
#             cart=cart,
#             strap=strap
#         )
#     return redirect('/cart')


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







# def cart_plus(request,strap_id):
#     print('sadffffagr215212154125421525215412221111')
#     strap=get_object_or_404(Strap,id=strap_id)
#     try :
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(strap = strap,user = request.user)
#             if cart_item.quantity >= 1:
#                 cart_item.quantity += 1
#                 cart_item.save()
#     except:
#         cart = Cart.objects.get(cart_id = _cart_id(request))
#         cart_item = CartItem.objects.get(strap = strap,cart= cart)
#         if cart_item.quantity >= 1:
#             cart_item.quantity += 1
#             cart_item.save()
#     return redirect('cart')



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

# def remove_cart(request, product_id):
#     cart = Cart.objects.get(cart_id=_cart_id(request))
#     product = get_object_or_404(Product, id=product_id)
#     cart_item = CartItem.objects.get(product=product, cart=cart)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('/cart')

# def cartpage(request, total=0, quantity=0, cart_items=None):
#     tax = 0
#     grand_total = 0
#     org_tot = 0
#     tot = 0
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         tot = 0

#         # ship = 0
#         for cart_item in cart_items:
#             total += (cart_item.product.offer_price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (3 * total)//100
#         grand_total = total + tax
#         tot = (cart_item.product.price * cart_item.quantity)
#         org_tot = grand_total - tot

#     except ObjectDoesNotExist:
#         pass
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total,
#         'org_tot': org_tot,
#         # 'shipping_charge':CartItem.shipping_charge,
#     }
#     return render(request, 'cart.html', context)

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


    
def invoice(request,id):
    try:
        order=Order.objects.get(order_id=id)
        order_item=OrderItem.objects.filter(order_no=order)
        context={
            'order':order,
            'order_item':order_item,
        }
        return render(request,'invoice.html',context)
    except Order.DoesNotExist:
        return redirect('shop')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    org_tot = 0
    tot = 0
    user = request.user
    try:
        cart = Cart.objects.get(user=user)if user else None
        cart_items = CartItem.objects.filter(cart=cart)
        user_profile=User_Profile.objects.filter(user=user)

      
        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)//100
        grand_total = total + tax
        tot = (cart_item.product.price * cart_item.quantity)
        org_tot = grand_total - tot

    except ObjectDoesNotExist:
        pass

    amount=cart.total() * 10
    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID,settings.KEY_SECRET))
    payment=client.order.create({"amount":float(amount),"currency": "INR","payment_capture" : 1})
    cart.razor_pay_order_id=payment['id']
    cart.save()
    context = {
        'total': total,
        'cart': cart,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'org_tot': org_tot,
        'user_profile':user_profile,
        "payment":payment,

    }
    return render(request, 'checkout.html', context)

def success(request):
    messages.success(request,'Payment Successful now you can place order.')
    return redirect('checkout')

def myorders(request):
    user=request.user
    order=Order.objects.filter(user=user)
    # order_item=OrderItem.objects.filter(order_no__in=order)
    order_item = OrderItem.objects.filter(order_no__in=order).order_by('-order_no__order_date')

    context={
        'user':user,
        'order':order,
        'order_item':order_item,
    }
    return render(request,'myorders.html',context)

@login_required(login_url='login')
def create_order(request):
    print('11111111111111111111111111111111111111111111111111111111111111111111111111')
    if request.method == 'POST':
        address_id=request.POST.get('address')
        payment_method=request.POST.get('pay-method')
        print(payment_method)
    cart=get_object_or_404(Cart,user=request.user)
    address=get_object_or_404(User_Profile,id=address_id)
    price1=cart.total_price()
    payment_amount1=cart.total()
    shipping_charge=cart.shipping_charge()
    order=Order.objects.create(
        user=request.user,
        address=address,
        payment_method=payment_method,
        price=price1,
        offer_price=payment_amount1,
        payment_amount=payment_amount1,
        shipping_charge=shipping_charge,
        )
    if payment_method == "razorpay":
        print('raz111111111111111111111111111111111111111111111111111111111111111111111111111111111')
        order.payment_status = 'Completed'
        order.save()
    for cart_item in CartItem.objects.all():
        OrderItem.objects.create(
            order_no=order,
            product=cart_item.product,
            strap=cart_item.strap,
            quantity=cart_item.quantity,
            amount=payment_amount1,
            )
    # strap=Strap.objects.get(id=cart_item.quantity)
    # print(strap)
    # print(strap.quantity)
    # strap.quantity -= cart_item.quantity
    # print(strap.quantity)
    # strap.save()
    cart.delete()
    context={
        "address":address,
        'payment_method':payment_method,
        'order_id':order.order_id,
        }
    return render(request,'confirmation.html',context)

def payment(request):
    return render(request,'payment.html')

def confirmationpage(request):
    # order_id=Order.objects.get(id=order_id)
    all_category=Category.objects.all()
    return render(request, 'confirmation.html',{'all_category':all_category})