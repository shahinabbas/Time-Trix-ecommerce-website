from django.db import models
from app.models import CustomUser,Product

# Create your models here.


class order(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)