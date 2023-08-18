
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


def add_cart(request, product_id):
    user=request.user
    product = Product.objects.get(id=product_id)
    if request.method=='POST':
        strap_id=request.POST.get('strap_id')
    if user.is_authenticated:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
            try:
                cart_item = CartItem.objects.get(product=product, user=user,strap_id=strap_id)
                cart_item.quantity += 1
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1, 
                    cart=cart, 
                    user=request.user,
                    strap_id=strap_id,
                    )
                cart_item.save()
            return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, strap_id=strap_id)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1, 
                cart=cart, 
                strap_id=strap_id,
                )
            cart_item.save()
        return redirect('cart')            



def cart_plus(request,strap_id):
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

def cart_minus(request,strap_id):
    strap=get_object_or_404(Strap,id=strap_id)
    try :
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(strap = strap,user = request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    except:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(strap = strap,cart= cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')



def cartpage(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
            
        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
            shp=cart_item.shipping_charge()
            qwe=cart_item.qwe()
            tax=cart_item.tax()
            coup=cart_item.coupon_discount()
            amount=cart_item.total()
    except ObjectDoesNotExist:
            pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shp':shp,
        'qwe':qwe,
        'tax':tax,
        'coup':coup,
        'amount':amount,
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
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
      
        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
            amount=cart_item.total() * 10
            shp=cart_item.shipping_charge()
            qwe=cart_item.qwe()
            tax=cart_item.tax()
            coup=cart_item.coupon_discount()
            amount=cart_item.total()
            off=cart_item.offer_sub_total()
            price=cart_item.sub_total()
        tax = (3 * total)//100
        grand_total = total + tax
        tot = (cart_item.product.price * cart_item.quantity)
        org_tot = grand_total - tot
        user_profile=User_Profile.objects.filter(user=request.user)

    except ObjectDoesNotExist:
        pass
    # amount=100000
    # client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID,settings.KEY_SECRET))
    # payment=client.order.create({"amount":float(amount),"currency": "INR","payment_capture" : 1})
    # cart_items.razor_pay_order_id=payment['id']
    # cart_items.save()
    context = {
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'org_tot': org_tot,
        'user_profile':user_profile,
        # "payment":payment,
        'shp':shp,
        'qwe':qwe,
        'tax':tax,
        'coup':coup,
        'amount':amount,
        'off':off,
        'price':price,
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