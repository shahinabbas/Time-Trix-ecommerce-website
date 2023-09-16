import json
from app.models import CustomUser, Product, User_Profile, Category, OrderAddress
from .models import Cart, CartItem, Strap, Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from psycopg2 import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
import razorpay
from django.conf import settings
from django.http import Http404
import uuid
from datetime import datetime

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        strap_id = request.POST.get("strap_id")
        varient = get_object_or_404(Strap, id=strap_id)

        print(strap_id)
        if varient.quantity == 0:
            messages.info(request, "selected strap not available")
            return redirect("product_details", product_id=product.id)

    if user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        try:
            cart_item = CartItem.objects.get(
                product=product, user=user, strap_id=strap_id
            )
            cart_item.quantity += 1
            if cart_item.quantity > cart_item.strap.quantity:
                cart_item.quantity = cart_item.strap.quantity
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
        return redirect("cart")
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        try:
            cart_item = CartItem.objects.get(
                product=product, cart=cart, strap_id=strap_id
            )
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
        return redirect("cart")


def cart_plus(request, strap_id):
    strap = get_object_or_404(Strap, id=strap_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(strap=strap, user=request.user)
        if cart_item.quantity < strap.quantity:
            cart_item.quantity += 1
        else:
            messages.error(request, "Product out of stock")
            cart_item.quantity = strap.quantity
        cart_item.save()
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(strap=strap, cart=cart)
        if cart_item.quantity < strap.quantity:
            cart_item.quantity += 1
        else:
            cart_item.quantity = strap.quantity
        cart_item.save()
    return redirect("cart")


def cart_minus(request, strap_id):
    strap = get_object_or_404(Strap, id=strap_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(strap=strap, user=request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    except:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(strap=strap, cart=cart)
        if cart_item.quantity >= 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect("cart")


def cartpage(request, total=0, quantity=0, cart_items=None):
    shp = qwe = tax = coup = amount = 0  # Initialize variables with default values
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.strap.quantity:
                cart_item.quantity = cart_item.strap.quantity
                cart_item.save()
            total += cart_item.product.offer_price * cart_item.quantity
            quantity += cart_item.quantity
            shp = cart_item.shipping_charge()
            qwe = cart_item.qwe()
            tax = cart_item.tax()
            coup = cart_item.coupon_discount()
            amount = cart_item.total()
    except ObjectDoesNotExist:
        return render(request, "error.html")

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "shp": shp,
        "qwe": qwe,
        "tax": tax,
        "coup": coup,
        "amount": amount,
    }
    return render(request, "cart.html", context)


@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
    tot = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.strap.quantity:
                cart_item.quantity = cart_item.strap.quantity
                messages.info(request, "Sorry selected quantity not available")
            elif cart_item.quantity == 0:
                return redirect("cart")
            total += cart_item.product.offer_price * cart_item.quantity
            quantity += cart_item.quantity
            amount = cart_item.total() * 10
            shp = cart_item.shipping_charge()
            qwe = cart_item.qwe()
            tax = cart_item.tax()
            amount = cart_item.total()
            off = cart_item.offer_sub_total()
            price = cart_item.sub_total()
            tot = cart_item.tot()
        coup = cart_item.coupon_discount()
        user_profile = User_Profile.objects.filter(user=request.user)

    except ObjectDoesNotExist:
        return render(request, "404.html")
    client = razorpay.Client(
        auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
    payment = client.order.create(
        {"amount": float(amount), "currency": "INR", "payment_capture": 1}
    )
    # cart_items.razor_pay_order_id=payment['id']
    # cart_items.save()
    context = {
        "quantity": quantity,
        "cart_items": cart_items,
        "user_profile": user_profile,
        # "payment":payment,
        "shp": shp,
        "qwe": qwe,
        "tax": tax,
        "coup": coup,
        "amount": amount,
        "off": off,
        "price": price,
        "tot": tot,
    }
    return render(request, "checkout.html", context)


def delete_cart_item(request, product_id):
    cart_item = get_object_or_404(CartItem, id=product_id)
    cart_item.delete()
    return redirect("cart")


# def delete_cart_item(request,product_id):
#     product=get_object_or_404(Strap,id=product_id)
#     if request.user.is_authenticated:
#         cart_item=CartItem.objects.get(product=product,user=request.user)
#     else:
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#         cart_item=CartItem.objects.get(product=product,cart=cart)
#     cart_item.delete()
#     return redirect('cart')


def order_details(request, id):
    order = get_object_or_404(Order, order_id=id)
    product = OrderItem.objects.filter(order_no=order)
    return render(request, "order_details.html", {"product": product, "order": order})


# def delete_cart_item(request, product_id):
# cart = Cart.objects.get(cart_id=_cart_id(request))
# product = get_object_or_404(Product, id=product_id)
# cart_item = CartItem.objects.get(product=product, cart=cart)
# cart_item.delete()
# return redirect('/cart')


def invoice(request, id):
    try:
        order = Order.objects.get(order_id=id)
        order_item = OrderItem.objects.filter(order_no=order)
        print(order_item)
        context = {"order": order,
                   "order_item": order_item, "now": datetime.now()}
        return render(request, "invoice.html", context)
    except Order.DoesNotExist:
        return redirect("shop")


def myorders(request):
    user = request.user
    order = Order.objects.filter(user=user)
    order_item = OrderItem.objects.filter(order_no__in=order).order_by(
        "-order_no__order_date"
    )

    context = {
        "user": user,
        "order": order,
        "order_item": order_item,
    }
    return render(request, "myorders.html", context)


@login_required(login_url="login")
def create_order(request):
    address_id = None
    if request.method == "POST":
        address_id = request.POST.get("address")
        request.session["address_id"] = address_id
        if not address_id:
            messages.error(request, "Please select an address.")
            return redirect("checkout")

    cart_items = CartItem.objects.filter(user=request.user)
    amount = 0
    for cart_item in cart_items:
        amount = cart_item.total() * 100

    address = get_object_or_404(User_Profile, id=address_id)
    context = {
        "address": address,
        "amount": amount,
    }
    return render(request, "payment.html", context)


def confirmation(request):
    payment_method = "razorpay"
    if request.method == "POST":
        payment_method = request.POST.get("pay-method")
        if not payment_method:
            messages.error(request, "Select a payment method...")
            return render(request, "payment.html")

    address_id = request.session.get("address_id", None)
    cart_item = CartItem.objects.filter(user=request.user)
    address = get_object_or_404(User_Profile, id=address_id)

    order_address = OrderAddress.objects.create(
        user=request.user,
        name=address.name,
        address=address.address,
        phone_number=address.phone_number,
        house_no=address.house_no,
        street=address.street,
        city=address.city,
        state=address.state,
        country=address.country,
        pin_code=address.pin_code,
    )
    price1 = 0
    payment_amount1 = 0
    shipping_charge = 0
    for cart_item in cart_item:
        price1 = cart_item.sub_total()
        payment_amount1 = cart_item.total()
        shipping_charge = cart_item.shipping_charge()

    order = Order.objects.create(
        user=request.user,
        address=order_address,
        payment_method=payment_method,
        price=price1,
        offer_price=payment_amount1,
        payment_amount=payment_amount1,
        shipping_charge=shipping_charge,
    )

    if payment_method == "razorpay":
        order.payment_status = "Completed"
        order.save()

    for cart_item in CartItem.objects.all():
        OrderItem.objects.create(
            order_no=order,
            product=cart_item.product,
            strap=cart_item.strap,
            quantity=cart_item.quantity,
            amount=payment_amount1,
        )
        strap = cart_item.strap
        strap.quantity -= cart_item.quantity
        strap.save()

    cart_item.delete()

    orderss = OrderItem.objects.filter(order_no=order.id)
    print(order.payment_amount)
    context = {
        "address": order_address,
        "payment_method": payment_method,
        "order_id": order.order_id,
        "orderss": orderss,
        "order": order,
    }
    context["payment_successful"] = True

    return render(request, "confirmation.html", context)
