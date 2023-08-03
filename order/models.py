# from django.db import models
# from app.models import CustomUser,Product,User_Profile
# from django.utils.translation import gettext as _

# # Create your models here.


# class order(models.Model):
#     user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     address=models.ForeignKey(User_Profile, on_delete=models.CASCADE)
#     price=models.DecimalField(max_digits=8, decimal_places=2)
#     offer_price=models.DecimalField(max_digits=8,decimal_places=2)
#     delivery_charge=models.DecimalField(max_digits=8,decimal_places=2)
#     payment_method=models.CharField(max_length=50)
#     payment_status=models.CharField(max_length=50)
#     order_date=models.DateTimeField(auto_now_add=True)
