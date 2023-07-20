from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
# from .models import Customer
from django.contrib import messages
from .models import CustomUser

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


def admin_signinpage(request):
    return render(request, 'admin_signin.html')

def forgot_passwordpage(request):
    return render(request, 'forgot_password.html')


def enter_otppage(request):
    return render(request, 'enter_otp.html')

def signuppage(request):
    if request.method == "POST":
        # first_name=request.POST["first_name"]
        # last_name=request.POST["last_name"]
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone_number']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']
        if CustomUser.objects.filter(name=name):
            messages.error(request,"Username already Registered!!")
            return redirect('/signup')

        if pass1 == pass2:
            myuser = CustomUser.objects.create_user(name=name,email=email,phone_number=phone,password=pass1)
            myuser.save()
            return redirect("/login")
        else:
            messages.error(request,"your password and confirm password incorrect")
            return redirect("/signup")
    return render(request,"signup.html")      
def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('/index_after_login')
    # if request.method=="POST":
    #     uname=request.POST.get("username")
    #     pass1=request.POST.get("passord")
    #     myuser=authenticate(username=uname,password=pass1)
    #     if myuser is not None:
    #         login(request,myuser)
    #         messages.success(request,"Login Success")
    #         return redirect('/index_after_login')
    #     else:
    #         messages.error(request,"Invalid Credentails")
    #         return redirect('/login')
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    request.session.flush()
    messages.success(request,"Logout success")
    return redirect('/index')