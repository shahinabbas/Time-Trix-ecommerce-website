from django.db import models
from app.models import CustomUser, Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField('app.product', through='CartItem')
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_id

    def cart_count(self):
        return CartItem.objects.filter(cart__user=self.user).count()

    def shipping_charge(self):
        ship_tot = self.offer_total_price()
        if ship_tot >= 3000:
            return 0
        else:
            return 40


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    strap = models.ForeignKey('Strap', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product

    def price(self):
        return self.product.price * self.quantity

    def sub_total(self):
        return self.product.offer_price * self.quantity

    def total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())

    def offer_total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())


class Strap(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    strap = models.CharField(max_length=50)
    quantity=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product
