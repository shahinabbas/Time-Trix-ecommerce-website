from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index_after_login',views.index_after_login,name='index_after_login'),
    path('about/',views.aboutpage,name='about'),
    path('blog/',views.blogpage,name='blog'),
    path('cart/',views.cartpage,name='cart'),
    path('contact/',views.contactpage,name='contact'),
    path('shop/',views.shoppage,name='shop'),
    path('checkout/',views.checkoutpage,name='checkout'),
    path('login/',views.loginpage,name='login'),
    path('blog-details/',views.blogdetailspage,name='blog-details'),
    path('confirm/',views.confirmpage,name='confirm'),
    path('elements/',views.elementspage,name='elements'),
    path('signup/',views.signuppage,name='signup'),
    path('logout/',views.logoutpage,name='logout'),
    path('forgot_password/',views.forgot_passwordpage,name='forgot_password'),
    path('enter_otp/',views.enter_otppage,name='enter_otp'),
    

    path('admin_signin/',views.admin_signinpage,name='admin_signin'),
    path('admin_logout/',views.admin_logoutpage,name='admin_logout'),
    path('home/',views.homepage,name='home'),
]
