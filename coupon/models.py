from django.utils import timezone
from django.db import models
from datetime import date
from app.models import CustomUser

# Create your models here.
class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('amount', 'Amount'),
        ('percentage', 'Percentage'),
    )
    coupon_code=models.CharField(max_length=10,unique=True)
    description=models.TextField()
    minimum_amount=models.IntegerField()
    discount_type=models.CharField(max_length=20,choices=DISCOUNT_TYPE_CHOICES)
    discount=models.DecimalField(max_digits=5,decimal_places=2)
    valid_from=models.DateTimeField()
    valid_to=models.DateTimeField()
    active=models.BooleanField(default=True)
     
    def __str__(self):
        return self.coupon_code
    

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_to > now
    # def is_valid(self):
    #     # now=timezone.now()
    #     # return self.active and self.valid_from <= now and self.valid_to >= now
    #     now = date.today()  # Convert datetime.datetime to datetime.date
    #     return self.active and self.valid_from <= now and self.valid_to >= now

class UserCoupon(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
    coupon_applied=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    is_applied=models.BooleanField(default=True)