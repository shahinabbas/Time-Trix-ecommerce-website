from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [


    path("", views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('new/', views.new, name='new'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_wishlist//<int:product_id>/',
         views.remove_wishlist, name='remove_wishlist'),
    path('add_to_wishlist/<int:product_id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path("search/", views.search, name='search'),
    path('user_category/<int:id>/', views.user_category, name='user_category'),
    path('logout/', views.logoutpage, name='logout'),
    path('enter_otp/', views.enter_otppage, name='enter_otp'),
    path('signup/', views.signuppage, name='signup'),
    path('send_otp/', views.send_otppage, name='send_otp'),
    path('reset/', views.reset, name='reset'),
    path('forgot/', views.forgot, name='forgot'),
    path('list/<int:id>/', views.listpage, name="list"),
    path('product_details/<int:product_id>/',
         views.product_details, name='product_details'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('address/', views.address, name='address'),
    path('add_address', views.add_address, name='add_address'),
    path('edit_address<int:id>', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('coupons/', views.coupons, name="coupons"),
    path('about/', views.aboutpage, name='about'),
    path('blog/', views.blogpage, name='blog'),
    path('contact/', views.contactpage, name='contact'),
    path('shop/', views.shoppage, name='shop'),
    path('blog-details/', views.blogdetailspage, name='blog-details'),
    path('elements/', views.elementspage, name='elements'),
    path('error', views.error, name='error'),
    path('price_sort',views.price_sort,name='price_sort'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'app.views.error'
