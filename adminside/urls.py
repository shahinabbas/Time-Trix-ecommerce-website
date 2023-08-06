from django.urls import path
from adminside import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('admin_index',views.admin_index,name='admin_index'),
    path('admin_signin',views.admin_signin,name='admin_signin'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),


    path('users/',views.userspage,name='users'),
    path('user_block/<int:id>',views.user_blockpage,name="user_block"),
    path('user_unblock/<int:id>',views.user_unblockpage,name="user_unblock"),

    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('category_list/',views.category_listpage,name='category_list'),
    path('delete_category/<int:id>',views.delete_categorypage,name="delete_category"),


    path('products/',views.productspage,name='products'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:id>/',views.edit_productpage,name='edit_product'),
    path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('undo_product/<int:id>/',views.undo_productpage,name='undo_product'),
       
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

