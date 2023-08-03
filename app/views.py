from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from app.models import CustomUser, category, Product,User_Profile
from cart.models import Strap
import random
from twilio.rest import Client
import os
from django.contrib.auth.models import auth
from django.views.decorators.cache import never_cache
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# from cart.views import _cart_id



def edit_address(request,id):
    user=request.user
    profile_address=get_object_or_404(User_Profile,pk=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        house_no = request.POST.get('house_no')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_code = request.POST.get('pin_code')
        

        profile_address.name=name
        profile_address.phone_number=phone_number
        profile_address.house_no=house_no
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.pin_code = pin_code
        profile_address.save()
        messages.success(request,"successful")
        return redirect('address')
    return render(request,'edit_address.html',{"profile_address":profile_address})


def delete_address(request,id):
    user=request.user
    profile=get_object_or_404(User_Profile,pk=id,user=user)
    profile.delete()
    return redirect('address')


@login_required(login_url='login')
def reset(request):
    user=request.user
    if request.method=='POST':
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed succsessfully')
            return redirect('reset')
        else:
            messages.error(request,'Entered passwords are not same')
        return redirect('reset')  
    return render(request,'reset.html')
   
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
        profile_address.name=name
        profile_address.phone_number=phone_number
        profile_address.house_no=house_no
        profile_address.street = street
        profile_address.city = city
        profile_address.state = state
        profile_address.country = country
        profile_address.pin_code = pin_code
        profile_address.save()
        messages.success(request,"successful")
        return redirect('address')
    return render(request,'add_address.html')
   
@login_required
def user_profile(request):
    user=request.user
    user_profile=User_Profile.objects.filter(user=user)
    print(user)
    if user_profile.exists():
        user_profile=user_profile.all()
    else:
        user_profile=None

    context={
        'user':user,
        'user_profile':user_profile
    }
    return render(request, 'profile.html',context)


def edit_profile(request):
    return render(request, 'edit_profile.html')


    

# def reset_passwordpage(request):
#     error_message = None
#     print('hi')
#     if request.session.has_key('phone_number'):
#         phone_number= request.session['phone_number']
#         user = CustomUser.objects.get(phone_number=phone_number)
#         if request.method == 'POST':
#             new_password=request.POST.get('new_password')
#             confirm_password=request.POST.get('confirm_password')

#             if new_password == confirm_password:
#                 if new_password:
#                     error_message= "Enter new password"
#                 elif not confirm_password:
#                     error_message ="Reenter password"
#                 elif new_password == user.password:
#                     error_message = "This password already exist"
#                 if not error_message:
#                     user.set_password(new_password)
#                     print(user.password)
#                     user.save()
#                     del request.session['phone_number']

#                 messages.success(request,"password changed Sucess fully")
#                 return redirect('/login')
#     return render(request,"reset.html",{'error':error_message})

@never_cache
def address(request):
    user=request.user
    user_profile=User_Profile.objects.filter(user=user)

    if user_profile.exists():
        user_profile=user_profile.all()
    else:
        user_profile=None

    context={
        'user':user,
        'user_profile':user_profile
    }
    return render(request, 'address.html',context)

# @login_required(login_url='send_otp')

@never_cache
def loginpage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        print(email)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.error(request, "User name or password is incorect")
    return render(request, 'login.html')


@never_cache
@login_required(login_url='admin_signin')
def admin_logoutpage(request):
    auth.logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_signin')


@never_cache
@login_required(login_url='admin_signin')
def userspage(request):
    stu = CustomUser.objects.all()
    return render(request, "admin/users.html", {'stu': stu})


@login_required(login_url='admin_signin')
def user_blockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
    return redirect('users')


@login_required(login_url='admin_signin')
def user_unblockpage(request, id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
    return redirect('users')


@never_cache
@login_required(login_url='admin_signin')
def admin_indexpage(request):
    return render(request, "admin/admin_index.html")

@never_cache
@login_required(login_url='admin_signin')
def categorypage(request):
    if request.method == 'POST':
        category_name = request.POST['categoryname']
        if category.objects.filter(categories=category_name).exists():
            error_message = 'Category name already exists.'
            return render(request, 'admin/category.html', {'error_message': error_message})
        else:
            Category = category.objects.create(categories=category_name)
            # stu = category.objects.all()
            return render(request, 'admin/category.html')
    return render(request, "admin/category.html")

@never_cache
@login_required(login_url='admin_signin')
def category_listpage(request):
    stu = category.objects.all()
    return render(request, "admin/category.html", {'stu': stu})

@never_cache
def edit_category(request,id):
    catgry=category.objects.get(pk=id)
    if request.method=='POST':
        categories=request.POST.get('category')
        if category.objects.filter(categories=categories).exclude(pk=id).exists():
            messages.error(request,'Category name already exists')
            return redirect('category')
        else:
            catgry.categories = categories
            catgry.save()
            messages.success(request,'edit successful')
        return redirect('category')
    return render(request,'admin/category.html',{'category':categories})






@never_cache
@login_required(login_url='admin_signin')
def delete_categorypage(request, id):
    if request.method == 'POST':
        co = category.objects.filter(pk=id).first()
        if co:
            co.delete()
        return redirect('/category_list')

@never_cache
@login_required(login_url='admin_signin')
def productspage(request):
    stu = category.objects.all()
    products = Product.objects.all()
    strap=Strap.objects.all()
    context={
        'products': products,
        'strap': strap
    }

    return render(request, 'admin/products.html', context)

@never_cache
@login_required(login_url='admin_signin')
def add_productpage(request):
    categories = category.objects.all()
    strap = ['Rubber', 'Leather', 'Chain']
    if request.method == 'POST':
        product_name = request.POST.get('name')
        category_name = request.POST.get('category')
        product_Image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        print('product image:', product_Image)

        if Product.objects.filter(product_name=product_name).exists():
            return render(request, 'admin/add_product.html', {'error_message': 'Product already exists.'})
        else:
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
                # strap=strap,
                price=price,
                offer_price=offer_price,
                # quantity=quantity,
            )
            product.save()
            messages.success(request, 'New product added successfully')
        for straps in strap:
            quantity = request.POST.get(f'quantity-{straps}')
            print(f'{straps} quantity: {quantity}')
            strap.append({'name':straps,'quantity':quantity})
            strap=Strap(product_id=product,strap=strap,quantity=quantity)
            strap.save()

    return render(request, "admin/add_product.html", {'categories': categories, 'strap': strap})


@login_required(login_url='admin_signin')
def delete_productpage(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.soft_delete()
        return redirect('products')


@login_required(login_url='admin_signin')
def undo_productpage(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.is_deleted = False
        product.save()
        return redirect('products')

@never_cache
@login_required(login_url='admin_signin')
def edit_productpage(request, id):
    try:
        product = Product.objects.get(pk=id)
        strap=Strap.objects.filter(product=product)
        categories = category.objects.all()
        context = {
            'product': product,
            # 'shape': shape,
            'categories': categories
        }
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        category_id = request.POST.get('categoryId')
        category = get_object_or_404(category, pk=category_id)
        description = request.POST.get('description')
        product_image = request.FILES.get('image')

        product.product_name = product_name
        product.category = category
        product.description = description

        if product_image:
            product.product_Image = product_image
        product.save()
        return redirect('products')
    return render(request, "admin/edit_product.html", context)










def listpage(request, id):
    return render(request, 'list.html')


def product_details(request, product_id):
    product = Product.objects.get(id=product_id) 
    all_categories = category.objects.all()
    strap = Strap.objects.all()
    context = {
              'product': product, 
              "category":all_categories,
              'strap':strap,
    }
   
    return render(request,"product_details.html",context)
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
    product = Product.objects.all().filter(is_deleted=False)
    return render(request, 'shop.html', {'product': product})


def index(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')


def blogpage(request):
    return render(request, 'blog.html')


def blogdetailspage(request):
    return render(request, 'blog-details.html')





def contactpage(request):
    return render(request, 'contact.html')


def confirmpage(request):
    return render(request, 'confirmation.html')


def elementspage(request):
    return render(request, 'elements.html')


def add_product1page(request):
    return render(request, "admin/add_product1.html")


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
            auth_token = 'b14780861a285e84c4e906c676806b79'

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

def admin_signinpage(request):
    if request.user.is_authenticated:
        return redirect('admin_index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user.is_superuser:
            auth.login(request, user)
            return redirect('/users')
        else:
            messages.error(request, "User email or password is incorrect")
            return redirect('/admin_signin')
    return render(request, 'admin/admin_signin.html')





def confirmationpage(request):
    return render(request, 'confirmation.html')
