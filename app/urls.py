from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.loginpage,name='login'),

    path('logout/',views.logoutpage,name='logout'),
    path('enter_otp/',views.enter_otppage,name='enter_otp'),
    path('signup/',views.signuppage,name='signup'),
    path('send_otp/',views.send_otppage,name='send_otp'),
    # path('reset_password/',views.reset_passwordpage,name='reset_password'),

    path('list/<int:id>/',views.listpage,name="list"),
    path('product_details/<int:product_id>/',views.product_detailspage,name='product_details'),
    path('confirmation',views.confirmationpage,name="confirmation"),

    path('profile',views.profilepage,name='profile'),
    path('address',views.addresspage,name='address'),


    path('admin_index/',views.admin_indexpage,name='admin_index'),
    path('admin_signin/',views.admin_signinpage,name='admin_signin'),
    path('admin_logout/',views.admin_logoutpage,name='admin_logout'),

    path('users/',views.userspage,name='users'),
    path('user_block/<int:id>',views.user_blockpage,name="user_block"),
    path('user_unblock/<int:id>',views.user_unblockpage,name="user_unblock"),

    path('category/',views.categorypage,name='category'),
    path('category_list/',views.category_listpage,name='category_list'),
    path('delete_category/<int:id>',views.delete_categorypage,name="delete_category"),

    path('products/',views.productspage,name='products'),
    path('add_product/',views.add_productpage,name='add_product'),
    path('edit_product/<int:id>/',views.edit_productpage,name='edit_product'),
    path('delete_product/<int:id>/',views.delete_productpage,name='delete_product'),
    path('undo_product/<int:id>/',views.undo_productpage,name='undo_product'),
    
    

    path('about/',views.aboutpage,name='about'),
    path('blog/',views.blogpage,name='blog'),
    path('cart/',views.cartpage,name='cart'),
    path('contact/',views.contactpage,name='contact'),
    path('shop/',views.shoppage,name='shop'),
    path('checkout/',views.checkoutpage,name='checkout'),
    path('blog-details/',views.blogdetailspage,name='blog-details'),
    path('confirm/',views.confirmpage,name='confirm'),
    path('elements/',views.elementspage,name='elements'),
    
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
