from django.contrib import admin
from coupon.models import Coupon, UserCoupon


class couponAdmin(admin.ModelAdmin):
    list_display = ['id', 'coupon_code', 'valid_to', 'discount']


admin.site.register(Coupon, couponAdmin)
admin.site.register(UserCoupon)
