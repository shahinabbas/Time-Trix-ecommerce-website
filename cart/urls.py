from django.urls import path
from cart import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("", views.cartpage, name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("remove_cart/<int:product_id>/", views.remove_cart, name="remove_cart"),
    path("delete_cart_item/<int:product_id>/", views.delete_cart_item, name="delete_cart_item"),
    path("cart_plus/<int:strap_id>/",views.cart_plus,name="cart_plus"),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
