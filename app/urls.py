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
    path('reset/',views.reset,name='reset'),


    path('list/<int:id>/',views.listpage,name="list"),
    path('product_details/<int:product_id>/',views.product_details,name='product_details'),
    path('confirmation',views.confirmationpage,name="confirmation"),


    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('address',views.address,name='address'),
    path('add_address',views.add_address,name='add_address'),
    path('edit_address<int:id>',views.edit_address,name='edit_address'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),

   


    path('admin_index/',views.admin_indexpage,name='admin_index'),
    path('admin_signin/',views.admin_signinpage,name='admin_signin'),
    path('admin_logout/',views.admin_logoutpage,name='admin_logout'),


    path('users/',views.userspage,name='users'),
    path('user_block/<int:id>',views.user_blockpage,name="user_block"),
    path('user_unblock/<int:id>',views.user_unblockpage,name="user_unblock"),

    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
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
    path('contact/',views.contactpage,name='contact'),
    path('shop/',views.shoppage,name='shop'),
    path('blog-details/',views.blogdetailspage,name='blog-details'),
    path('confirm/',views.confirmpage,name='confirm'),
    path('elements/',views.elementspage,name='elements'),
    

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
