from django.db import models
from app.models import CustomUser, Product,User_Profile
import uuid
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField('app.product', through='CartItem')
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.cart_id

    def cart_count(self):
        return CartItem.objects.filter(cart__user=self.user).count()

    def shipping_charge(self):
        ship_tot = self.offer_total_price()
        if ship_tot >= 10000:
            return 0
        else:
            return 140

    def total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())

    def offer_total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())
    

    def price(self):
        return self.product.price * self.quantity

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

    def sub_total(self):
        return self.product.offer_price * self.quantity

   

class Strap(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    strap = models.CharField(max_length=100)
    quantity=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product
    

class Order(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Out for Shipping', 'Out for Shipping'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
   )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS,default="pending")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS,default="pending")
    payment_method = models.CharField(max_length=50)
    address = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    # coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
    # delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Out for Shipping', 'Out for Shipping'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
   )
    order_no=models.ForeignKey(Order,on_delete=models.CASCADE)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS,default="pending")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    strap = models.ForeignKey(Strap, on_delete=models.CASCADE)
    quantity= models.IntegerField(null=False)
    amount =  models.IntegerField(null=False)

