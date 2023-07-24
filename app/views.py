from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import CustomUser, category, Product
import random
from twilio.rest import Client
import os
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect


def signuppage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        if not name:
            messages.error(request, "Name field cannot be empty")
            return redirect('/signup')
        if CustomUser.objects.filter(name=name):
            messages.error(request, "Username already Registered!!")
            return redirect('/signup')
        if len(phone) < 13 or len(phone) > 14:
            messages.error(request, 'Phone number is wrong')
            return redirect('/signup')
        if pass1 == pass2:
            request.session['name'] = name
            request.session['email'] = email
            print('created')
            return redirect("send_otp")
        else:
            messages.error(
                request, "your password and confirm password incorrect")
            return redirect("/signup")
    return render(request, "signup.html")


def send_otppage(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        print(phone_number)
        user_phone = CustomUser.objects.filter(phone_number=phone_number)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        print(otp)
        if user_phone.exists():
            user = user_phone.first()
            user.save()
            request.session['phone_number'] = phone_number

            account_sid = 'AC2052f7894a67013c46526f408871da08'
            auth_token = '877a58ee20aeed59b55f628b7b61a0f4'

            try:
                client = Client(account_sid, auth_token)
                client.messages.create(
                    body=' Welcome to TIME TRIX Your OTP is: ' + otp,
                    from_='+12342616521',
                    to=phone_number
                )
                return HttpResponseRedirect(request, 'enter_otp.html')
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
        phone_number = request.session.get('phone_number')
        print('hi')
        user_phone = CustomUser.objects.filter(phone_number=phone_number)
        if user_phone.exists():
            user = user_phone.first()
            if entered_otp == user.otp:
                print('sup')
                # OTP verification successful
                user.is_otp_verified = True
                user.save()
                print("kk")
                name = request.session.get('name')
                email = request.session.get('email')
                user = CustomUser(name=name, email=email,
                                  phone_number=phone_number)
                user.save()

                del request.session['phone_number']
                del request.session['name']
                del request.session['email']

                login(request, user)
                print("ok")
                return redirect('/index_after_login')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'enter_otp.html')

    return redirect('send_otp')  # Redirect to the O


@never_cache
def loginpage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("/index_after_login")
            else:
                messages.error(request, "User name or password is incorect")
    return render(request, 'login.html')


@never_cache
def logoutpage(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logout success")
    return redirect('/index')


def admin_signinpage(request):
    if request.user.is_authenticated:
        return redirect('/users')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user.is_superuser:
            login(request, user)
            return redirect('/users')
        else:
            messages.error(request, "User email or password is incorrect")
            return redirect('/admin_signin')

    return render(request, 'admin/admin_signin.html')


def admin_logoutpage(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_signin')


def userspage(request):
    stu = CustomUser.objects.all()
    return render(request, "admin/users.html", {'stu': stu})


def user_blockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
    return redirect('users')


def user_unblockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
    return redirect('users')


def admin_indexpage(request):
    return render(request, "admin/admin_index.html")


def categorypage(request):
    if request.method == 'POST':
        category_name = request.POST['categoryname']
        if category.objects.filter(categories=category_name).exists():
            error_message = 'Category name already exists.'
            return render(request, 'admin/category.html', {'error_message': error_message})
        else:
            Category = category.objects.create(categories=category_name)
            stu = category.objects.all()
            return render(request, 'admin/category.html', {'stu': stu})
    return render(request, "admin/category.html")


def category_listpage(request):
    stu = category.objects.all()
    return render(request, "admin/category.html", {'stu': stu})


def delete_categorypage(request, id):
    if request.method == 'POST':
        co = category.objects.filter(pk=id).first()
        if co:
            co.delete()
        return redirect('/category_list')


def add_product1page(request):
    return render(request, "admin/add_product1.html")


def productspage(request):
    stu = category.objects.all()
    products = Product.objects.all()
    return render(request, 'admin/products.html', {'products': products})


def add_productpage(request):
    categories = category.objects.all()
    if request.method == 'POST':
        # Retrieve data from the form
        product_name = request.POST.get('name')
        category_name = request.POST.get('category')
        product_Image = request.FILES.get('image')
        description = request.POST.get('description')
        shape = ['Square', 'Oval', 'Round']
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        stock = request.POST.get('stock')
        print('product image:', product_Image)

        if Product.objects.filter(product_name=product_name).exists():
            return render(request, 'admin/add_product.html', {'error_message': 'Product already exists.'})
        else:
            # Create the product object
            try:
                selected_category = category.objects.get(
                    categories=category_name)
            except category.DoesNotExist:
                selected_category = category.objects.create(
                    category_name=category_name)

            product = Product(
                product_name=product_name,
                category=selected_category,
                product_Image=product_Image,
                description=description,
                shape=shape,
                price=price,
                offer_price=offer_price,
                stock=stock
            )
            product.save()
            messages.success(request, 'New product added successfully')

    return render(request, "admin/add_product.html", {'categories': categories})


# def add_product(request):
#     if request.method=='POST':


def product_detailspage(request):
    return render(request, 'product_details.html')


def index(request):
    return render(request, 'index.html')


def index_after_login(request):
    return render(request, 'index_after_login.html')


def aboutpage(request):
    return render(request, 'about.html')


def blogpage(request):
    return render(request, 'blog.html')


def blogdetailspage(request):
    return render(request, 'blog-details.html')


def cartpage(request):
    return render(request, 'cart.html')


def checkoutpage(request):
    return render(request, 'checkout.html')


def shoppage(request):
    return render(request, 'shop.html')


def contactpage(request):
    return render(request, 'contact.html')


def confirmpage(request):
    return render(request, 'confirmation.html')


def elementspage(request):
    return render(request, 'elements.html')
