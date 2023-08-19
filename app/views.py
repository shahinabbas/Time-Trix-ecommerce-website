from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from app.models import CustomUser, Category, Product, User_Profile, Wishlist
from cart.models import Strap,Cart,CartItem
from cart.views import _cart_id
import random
from twilio.rest import Client
import os
from django.core.paginator import Paginator
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# from cart.views import _cart_id

def index(request):
    all_category=Category.objects.all()
    return render(request, 'index.html', {'all_category':all_category})

from django.shortcuts import render
from .models import Product, Category

def user_category(request,id):
    all_category=Category.objects.all()
    category=Category.objects.get(pk=id)
    product=Product.objects.filter(category=category,is_deleted=False)
    context={
        'all_category':all_category,
        'category': category,
        'product': product,
    }
    return render(request,'user_category.html',context)




def search(request):
    if request.method=='GET':
        query=request.GET.get('query')
        if query:
            product=Product.objects.filter(Q(price__icontains=query)|Q(offer_price__icontains=query)|Q(product_name__icontains=query)|Q(shape__icontains=query))
            return render(request,'search.html',{'product':product})
        else:
            print("No information to show")
            return render(request,'search.html')
        
def autocomplete(request):
    if 'query' in request.GET:
        products = Product.objects.filter(product_name__icontains=request.GET.get('query'))
        terms = [product.product_name for product in products]
        return JsonResponse(terms, safe=False)
    return render(request, 'index.html')



# def autocomplete(request):
#     if 'term' in request.GET:
#         # search_query = request.GET.get('term')
#         product = Product.objects.filter(product_name__icontains=request.GET.get('term'))
#         terms = list() 
#         for term in product:
#             terms.append(term.termss)
#         return JsonResponse(terms,safe=False)
#     return render(request,'index.html')
 





def remove_wishlist(request, product_id):
    user = request.user
    pro = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.get(user=user, product=pro)
    wishlist_item.delete()
    messages.info(request,'Removed product from wishlist')
    return redirect('wishlist')

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    user = request.user
    pro = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.filter(user=user)
    if not wishlist.filter(product=pro).exists():
        Wishlist.objects.create(user=user, product=pro)
        messages.success(request,'Added product to wishlist')
    else:
        wishlist_item = Wishlist.objects.get(user=user, product=pro)
        wishlist_item.delete()
        messages.info(request,'Removed product from wishlist')
    
    return redirect('product_details', product_id=product_id)


@login_required(login_url='login')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {"wishlist": wishlist})


def edit_address(request, id):
    user = request.user
    profile_address = get_object_or_404(User_Profile, pk=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        house_no = request.POST.get('house_no')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_code = request.POST.get('pin_code')

        profile_address.name = name
        profile_address.phone_number = phone_number
        profile_address.house_no = house_no
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.pin_code = pin_code
        profile_address.save()
        messages.success(request, "successful")
        return redirect('address')
    return render(request, 'edit_address.html', {"profile_address": profile_address})


def delete_address(request, id):
    user = request.user
    profile = get_object_or_404(User_Profile, pk=id, user=user)
    profile.delete()
    return redirect('address')

@login_required(login_url='login')  # Only logged-in users can access this view
def reset(request):
    user = request.user  # Get the logged-in user
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if user.check_password(current_password):
            if password == confirm_password:
                user.set_password(password)  # Set the new password
                user.save()  # Save the user object
                messages.success(request, 'Password changed successfully')
                return redirect('reset')  # Redirect to the same view after successful password change
            else:
                messages.error(request, 'Entered passwords do not match')
                return redirect('reset')
    return render(request, 'reset.html')  # Render the template for password reset

def forgot(request):
    user = request.user  # Get the logged-in user
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user.set_password(password)  # Set the new password
            user.save()  # Save the user object
            messages.success(request, 'Password changed successfully')
            return redirect('login')  # Redirect to the same view after successful password change
        else:
            messages.error(request, 'Entered passwords do not match')
            return redirect('reset')
    return render(request, 'login.html')  # Render the template for password reset




def add_address(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        house_no = request.POST.get('house_no')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_code = request.POST.get('pin_code')

        profile_address = User_Profile(user=user)
        profile_address.name = name
        profile_address.phone_number = phone_number
        profile_address.house_no = house_no
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.pin_code = pin_code
        profile_address.save()
        messages.success(request, "successful")
        return redirect('address')
    return render(request, 'add_address.html')


@login_required
def user_profile(request):
    user = request.user
    user_profile = User_Profile.objects.filter(user=user)
    if user_profile.exists():
        user_profile = user_profile.all()
    else:
        user_profile = None

    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)


def edit_profile(request):
    return render(request, 'edit_profile.html')


@never_cache
def address(request):
    user = request.user
    user_profile = User_Profile.objects.filter(user=user)

    if user_profile.exists():
        user_profile = user_profile.all()
    else:
        user_profile = None

    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'address.html', context)

# @login_required(login_url='send_otp')


@never_cache
def loginpage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                return render(request,'404.html')
            if user.is_active:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.error(request, "User name or password is incorect")
    return render(request, 'login.html')


def new(request):
    return render(request, 'new.html')


def listpage(request, id):
    return render(request, 'list.html')


def product_details(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        wishlist=Wishlist.objects.filter(user=request.user,product=product).exists()
        all_categories = Category.objects.all()
        strap = Strap.objects.all()
        cart=CartItem.objects.filter(user=request.user)
        
       
        context = {
            'product': product,
            "category": all_categories,
            'strap': strap,
            'wishlist':wishlist,
            'cart':cart,
        }
        return render(request, "product_details.html", context)

    else:
        product = Product.objects.get(id=product_id)
        all_categories = Category.objects.all()
        strap = Strap.objects.all()
 
        context = {
            'product': product,
            "category": all_categories,
            'strap': strap,
        }

        return render(request, "product_details.html", context)
    return redirect('shop')
    # try:
    #     product = Product.objects.get(pk=product_id)
    #     in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()

    # except Exception as e:
    #     raise e

    # context = {
    #     'product': product,
    #     'in_cart': in_cart,
    # }
    # return render(request, 'product_details.html', context)

# @login_required


def shoppage(request):
    all_category=Category.objects.all()    
    product = Product.objects.all().filter(is_deleted=False)
    items_per_page = 10
    paginator = Paginator(product, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context= {
        'product': product,
        'all_category':all_category,
        'product': page_obj,
        }
    return render(request, 'shop.html',context)





def aboutpage(request):
    all_category=Category.objects.all()
    return render(request, 'about.html',{'all_category':all_category})


def blogpage(request):
    all_category=Category.objects.all()
    return render(request, 'blog.html',{'all_category':all_category})


def blogdetailspage(request):
    all_category=Category.objects.all()
    return render(request, 'blog-details.html',{'all_category':all_category})


def contactpage(request):
    all_category=Category.objects.all()
    return render(request, 'contact.html',{'all_category':all_category})





def elementspage(request):
    all_category=Category.objects.all()
    return render(request, 'elements.html',{'all_category':all_category})


def signuppage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not name:
            messages.error(request, "Name field cannot be empty")
            return redirect('/signup')
        if CustomUser.objects.filter(name=name):
            messages.error(request, "Username already Registered!!")
            return redirect('/signup')
        if len(phone_number) < 13 or len(phone_number) > 14:
            messages.error(request, 'Phone number is wrong')
            return redirect('/signup')
        if password == confirm_password:
            myuser = CustomUser.objects.create_user(
                name=name, email=email, phone_number=phone_number, password=password)
            myuser.save()
            return redirect("login")
        else:
            messages.error(
                request, "your password and confirm password incorrect")
            return redirect("/signup")
    return render(request, "signup.html")


def logoutpage(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logout success")
    return redirect('/')


def send_otppage(request):
    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        user_phone = CustomUser.objects.filter(phone_number=phone_number)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        print(otp)
        if user_phone.exists():
            user = user_phone.first()
            user.otp = otp
            user.save()
            request.session['phone_number'] = phone_number
            print(phone_number)
            account_sid = 'AC2052f7894a67013c46526f408871da08'
            auth_token = 'df3b7ba9f1bff3337178d446e6167cc1'

            try:
                client = Client(account_sid, auth_token)
                client.messages.create(
                    body=' Welcome to TIME TRIX Your OTP is: ' + otp,
                    from_='+12342616521',
                    to=phone_number
                )
                print('ok')
                return render(request, "enter_otp.html")
            except Exception as e:
                messages.error(
                    request, 'Failed to send OTP. Please try again later.')
                return render(request, 'send_otp.html')
        else:
            messages.warning(
                request, "No user registered with the provided mobile number")
            return render(request, 'send_otp.html')
    return render(request, 'send_otp.html')


def enter_otppage(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        print(entered_otp)
        phone_number = request.session.get('phone_number')

        if phone_number:
            user_number = CustomUser.objects.filter(phone_number=phone_number)
            if user_number.exists():
                user = user_number.first()
                print(user)
                if entered_otp == user.otp:
                    print(entered_otp)
                    user.is_otp_verified = True
                    user.save()
                    # del request.session['phone_number']
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid OTP')
        else:
            messages.error(request, 'Phone number not found in session.')
    phone_number = request.session.get('phone_number')
    return render(request, 'enter_otp.html', {'phone_number': phone_number})


def confirmationpage(request):
    all_category=Category.objects.all()
    return render(request, 'confirmation.html',{'all_category':all_category})

def error(request):
    return render(request,'404.html')
     