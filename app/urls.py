from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index_after_login',views.index_after_login,name='index_after_login'),

    path('logout/',views.logoutpage,name='logout'),
    # path('send_otp/',views.send_otppage,name='send_otp'),
    path('enter_otp/',views.enter_otppage,name='enter_otp'),
    

    path('admin_signin/',views.admin_signinpage,name='admin_signin'),
    path('admin_logout/',views.admin_logoutpage,name='admin_logout'),
    path('login/',views.loginpage,name='login'),
    path('signup/',views.signuppage,name='signup'),
    path('verify_otp/',views.verify_otppage,name='verify_otp'),


    path('users/',views.userspage,name='users'),
    path('user_block/<int:id>',views.user_blockpage,name="user_block"),
    path('user_unblock/<int:id>',views.user_unblockpage,name="user_unblock"),
    path('category/',views.categorypage,name='category'),
    path('category_list/',views.category_listpage,name='category_list'),
    path('delete_category/<int:id>',views.delete_categorypage,name="delete_category"),

    path('products/',views.productspage,name='products'),
    path('add_product/',views.add_productpage,name='add_product'),




    path('about/',views.aboutpage,name='about'),
    path('blog/',views.blogpage,name='blog'),
    path('cart/',views.cartpage,name='cart'),
    path('contact/',views.contactpage,name='contact'),
    path('shop/',views.shoppage,name='shop'),
    path('checkout/',views.checkoutpage,name='checkout'),
    path('blog-details/',views.blogdetailspage,name='blog-details'),
    path('confirm/',views.confirmpage,name='confirm'),
    path('elements/',views.elementspage,name='elements'),
    
   
]
