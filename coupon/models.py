from django.db import models

# Create your models here.
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=10,unique=True)
    description=models.TextField()
    discount_type=models.CharField(max_length=20)
    discount=models.DecimalField(max_digits=5,decimal_places=2)
    valid_from=models.DateField()
    valid_to=models.DateField()
    applicable_type=models.CharField(max_length=50)
    # category=