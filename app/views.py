from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
# from .models import Customer
from django.contrib import messages
from .models import CustomUser,category,Product
import random 
from twilio.rest import Client
import os
# from email import message
# from.forms import Aforms

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



# def forgot_passwordpage(request):
#     return render(request, 'forgot_password.html')



    

def signuppage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        print(email)
        print(name)
        print(pass1)
        print(pass2)
        if not name:
            messages.error(request, "Name field cannot be empty")
            return redirect('/signup')
        if CustomUser.objects.filter(name=name):
            messages.error(request,"Username already Registered!!")
            return redirect('/signup')
        # if CustomUser.objects.filter(phone_number=phone):
        #     messages.error(request,"Number already Registered!!")
        #     return redirect('/signup')
        if pass1 == pass2:
            CustomUser.objects.create_user(name=name,email=email,phone_number=phone,password=pass1)
            # myuser.save()
            print('created')
            return redirect("verify_otp")
        else:
            messages.error(request,"your password and confirm password incorrect")
            return redirect("/signup")
    return render(request,"signup.html")   

def verify_otppage(request):
    if request.method == 'POST':
        phone_number=request.POST.get('phone_number')
        user_phone=CustomUser.objects.filter(phone_number=phone_number)
        otp=''.join([str(random.randint(0,9)) for _ in range(6)])
        if user_phone.exists():
            user=user_phone.first()
            user.otp=otp
            user.save()
            request.session['phone_number']=phone_number

            account_sid = 'AC2052f7894a67013c46526f408871da08'
            auth_token = '02d4acb2f861128d177bb663db6e5d2c'


            client = Client(account_sid, auth_token)
            message = client.messages.create(
              body=' welcome to TIME TRIX Your OTP is: ' + otp,
              from_='+12342616521',
              to=phone_number
            )
            return render(request,'enter_otp.html')
        else:
            messages.warning(request,"No user registered with the provided mobile number")
    return render(request, 'verify_otp.html')

def enter_otppage(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        phone_number = request.session.get('phone_number')

        user_phone = CustomUser.objects.filter(phone_number=phone_number)
        if user_phone.exists():
            user = user_phone.first()
            if entered_otp == user.otp:
                # OTP verification successful
                user.is_otp_verified = True
                user.save()
                del request.session['phone_number']
                login(request, user)
                return redirect('/login')
            else:
               messages.error(request, 'Invalid OTP')
               return render(request, 'enter_otp.html')

    return redirect('send_otp')  # Redirect to the O


def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('/index_after_login')
    # else:
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email)
        print(password)
        user=authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect("/index_after_login")
            else:
                messages.error(request,"User name or password is incorect")
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    request.session.flush()
    messages.success(request,"Logout success")
    return redirect('/index')




def admin_signinpage(request):
    if request.user.is_authenticated:
        return redirect('/users')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print("Received name:", email)
        # print("Received password:", password)
        user = authenticate(request, email=email, password=password)
        # print("Authentication result:", user)
        # if user is not None:
        if user.is_superuser:
            login(request, user)
            return redirect('/users')
        else:
            messages.error(request, "User email or password is incorrect")
            return redirect('/admin_signin')
        # else:
        #     messages.error(request, "The email or password you entered is incorrect.")
        #     return redirect('/admin_signin')
    return render(request, 'admin/admin_signin.html')


def admin_logoutpage(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_signin')



def userspage(request):
    # if request.method == "POST":
    #     fm = Aforms(request.POST)
    #     if fm.is_valid():
    #         fm.save()
    #     fm = Aforms()
    # else:
    #     fm = Aforms()
    stu =CustomUser.objects.all()
    return render(request,"admin/users.html",{'stu':stu})
#    return render(request,"admin/users.html",{'fm':fm,'stu':stu})

def user_blockpage(request,id):
    if request.method == 'POST':
         user = CustomUser.objects.get(pk=id)
         user.is_active =False
         user.save()
    return redirect('users')

def user_unblockpage(request,id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active =True
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
            stu=category.objects.all()
            return render(request,'admin/category.html',{'stu':stu})
    return render(request,"admin/category.html")

def category_listpage(request):
    stu=category.objects.all()
    return render(request, "admin/category.html",{'stu':stu})

def delete_categorypage(request,id):
    if request.method == 'POST':
        co=category.objects.filter(pk=id).first()
        if co:
            co.delete()
        return redirect('/category_list')


def add_product1page(request):
    return render(request,"admin/add_product1.html")    

def productspage(request):
    stu=category.objects.all()
    products=Product.objects.all()
    product_sizes = ProductSize.objects.all()
    return render(request,'admin/products.html',{'products':products})


def add_productpage(request):
    categories = category.objects.all()
    if request.method == 'POST':
        # Retrieve data from the form
        product_name = request.POST.get('productName')
        category_name=request.POST.get('category')
        Product_Image = request.FILES.get('image')
        category = category.objects.get(categories=category_name)
        Category_id = category.pk
        description = request.POST.get('description')
        shapes = [ 'Square', 'Oval','Round']
        Price = request.POST.get('price')
        print('product image:',Product_Image)
        if Product.objects.filter(Product_name=product_name):
            return render(request,'admin/add_product.html')
        else:
        # Create the product object
             product = Product(price=Price, Shapes=shapes, Product_name=product_name, category=category,description=description,Product_Image=Product_Image)
             product.save()
        # for shape in shapes:
        #     # checkbox = request.POST.get(f'checkbox-{shape}')
        #     if checkbox:
        #         price = request.POST.get(f'price-{shape}')
        #         # offer_price = request.POST.get(f'offer-price-{shape}')
        #         quantity = request.POST.get(f'productCount-{shape}')
        #         product_shape = ProductSize(product_id=product, shape=shape, price=price,offer_price=offer_price,Quantity=quantity,)
        #         product_shape.save()  ,{'categories':categories}
    return render(request,"admin/add_product.html")


# def add_product(request):
#     if request.method=='POST':


def product_detailspage(request):
    return render(request,'product_details.html')