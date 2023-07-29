from django.db import models
from app.models import CustomUser,Product

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product
    
    def price(self):
        return self.product.price * self.quantity

    def sub_total(self):
        return self.product.offer_price * self.quantity

    def total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())

    def offer_total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())
    
    def cart_count(self):
        return CartItem.objects.filter(cart__user = self.user).count()
        
    
