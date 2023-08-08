from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from coupon import views

from coupon.views import CouponView

urlpatterns = [

    path('coupon_view', CouponView.as_view(), name='coupon_view'),
    path('coupon', views.coupon, name='coupon'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
