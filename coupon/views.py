from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from cart.models import Cart
from .models import Coupon, UserCoupon
# Create your views here.


class CouponView(View):
    template = 'cart.html'

    def post(self, request):
        user = request.user
        if request.method == 'POST':
            coupon_code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
            except Coupon.DoesNotExist:
                messages.warning(
                    request, 'Coupon not exist,check the coupon code')
                return redirect(reverse('cart'))
            if not coupon.is_valid():
                messages.warning(request, 'Enter valid coupon')
                return redirect(reverse('cart'))
            if UserCoupon.objects.filter(user=user, coupon_applied=coupon).exists():
                messages.warning(
                    request, "Try another coupon it's already used")
                return redirect(reverse('cart'))
            cart, created = Cart.objects.get_or_create(user=user)

            if cart.total() < coupon.minimum_amount:
                messages.warning(request, 'Minimum amount not met')
                return redirect(reverse('cart'))
            else:
                cart.coupon_applied = coupon
                cart.save()
                UserCoupon.objects.create(user=user, coupon_applied=coupon)
                messages.success(request, "Coupon applied successfully")
                return redirect(reverse('cart'))
        return render(request, 'template')


def coupon(request):
    return render(request, 'admin/coupon.html')
