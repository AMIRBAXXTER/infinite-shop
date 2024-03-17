from django.db import models

from ProductsApp.models import Product
from UserApp.models import User, Address


# Create your models here.

class CartModel(models.Model):
    status = [
        ('در انتظار پرداخت', 'در انتظار پرداخت'),
        ('پرداخت شده', 'پرداخت شده'),
        ('ارسال شده', 'ارسال شده'),
        ('تکمیل شده', 'تکمیل شده'),
    ]
    cart_random_number = models.CharField(max_length=10, unique=True, blank=True, verbose_name='شماره سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, verbose_name='آدرس', null=True, blank=True)
    status = models.CharField(max_length=25, default='در انتظار پرداخت', choices=status, verbose_name='وضعیت')
    final_price = models.PositiveIntegerField(default=0, verbose_name='مبلغ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    authority = models.CharField(max_length=50, null=True, blank=True, verbose_name='شماره تراکنش')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پرداخت')
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ارسال')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'Cart {self.id}'

    def save(self, *args, **kwargs):
        if not self.cart_random_number:
            import random
            self.cart_random_number = ''.join(random.choices('0123456789', k=10))
        super(CartModel, self).save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    color_id = models.PositiveIntegerField(verbose_name='id رنگ')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    final_price = models.PositiveIntegerField(verbose_name='قیمت کل')
    color = models.CharField(max_length=10, verbose_name='رنگ')
    color_stock = models.IntegerField(verbose_name='موجودی رنگ')
    weight = models.IntegerField(verbose_name='وزن')
    quantity = models.IntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'

    def __str__(self):
        return f'Cart {self.cart.id} Item {self.id}'

    def get_post_price(self):
        cart = self.cart
        products = cart.items.all()
        total_price = 0
        for product in products:
            total_price += product.final_price
        return total_price
