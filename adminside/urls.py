from django.urls import path
from adminside import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('admin_index',views.admin_index,name='admin_index'),
    path('admin_signin',views.admin_signin,name='admin_signin'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    
    
    path('sales_report/',views.sales_report,name='sales_report'),
    path('stock_report/',views.stock_report,name='stock_report'),
    path('cancel_report/',views.cancel_report,name='cancel_report'),


    path('users/',views.userspage,name='users'),
    path('user_block/<int:id>',views.user_blockpage,name="user_block"),

    path('user_unblock/<int:id>',views.user_unblockpage,name="user_unblock"),

    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('category_list/',views.category_listpage,name='category_list'),
    path('varient/<int:id>',views.varient,name='varient'),
    path('add_varient/<int:id>',views.add_varient,name='add_varient'),
    path('edit_varient/<int:id>',views.edit_varient,name='edit_varient'),

    path('delete_category/<int:id>/',views.delete_category,name="delete_category"),

    path('products/',views.productspage,name='products'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:id>/',views.edit_productpage,name='edit_product'),
    path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('undo_product/<int:id>/',views.undo_productpage,name='undo_product'),
    path('admin_order_details/<str:id>/',views.admin_order_details,name='admin_order_details'),

    path('orders',views.orders,name='orders'),
    path('coupon_list',views.coupon_list,name='coupon_list'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('edit_coupon/<int:id>',views.edit_coupon,name='edit_coupon'),
    path('delete_coupon/<int:id>/', views.delete_coupon, name='delete_coupon'),
    path("update_order_status/<int:id>/", views.update_order_status, name="update_order_status"),
    
    path("cancel_order/<int:id>/",views.cancel_order,name="cancel_order"),
    # path("return_order/<int:id>/",views.return_order,name="return_order"),
    path('chart',views.chart,name='chart'),
    path('monthly',views.monthly,name='monthly'),
    path('yearly',views.yearly,name='yearly'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

