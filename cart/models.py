
from django.db import models
from app.models import CustomUser, Product,User_Profile
import uuid
from decimal import Decimal
from coupon.models import Coupon
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # product = models.ManyToManyField('app.product', through='CartItem')
    # product=models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_applied=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.cart_id

    def cart_count(self):
        return CartItem.objects.filter(cart__user=self.user).count()

    def shipping_charge(self):
        ship_tot = self.offer_total_price()
        if ship_tot >= 10000:
            return 10
        else:
            return 140
    
    
    
    
    def total_price(self):
        return sum(item.sub_total() for item in self.cart_items.all())

    def offer_total_price(self):
        return sum(item.offer_sub_total() for item in self.cart_items.all())
   

    def price(self):
        return self.product.price * self.quantity
    
    # def save(self):
    #     return self.total_price - self.offer_total_price
    def tax(self):
        taxes=self.offer_total_price()
        return (3 * taxes)//100
    
    def coupon_discount(self):
        if self.coupon_applied and self.coupon_applied.is_valid():
            # if self.coupon_applied == 'amount':
            return self.coupon_applied.discount
            # elif self.coupon_applied.discount_type == 'percentage':
            #     return (self.coupon_applied.discount * self.total_price())/100
            
    def total(self):
        offer_price = self.offer_total_price()
        shipping_charge = self.shipping_charge()
        coupon_discount = self.coupon_discount() or Decimal('0.0')
        taxss=self.tax()
        return offer_price + shipping_charge + taxss - coupon_discount
  


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
    
    def offer_sub_total(self):
        return self.product.offer_price * self.quantity

    def sub_total(self):
        return self.product.price * self.quantity

   

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
    razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature=models.CharField(max_length=100,null=True,blank=True)


class OrderItem(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
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

