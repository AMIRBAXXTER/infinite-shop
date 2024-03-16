from django.db.models import Avg
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Product, ProductColor, ProductRate


@receiver(pre_save, sender=Product)
def set_auto_fields(sender, instance: Product, **kwargs):
    # set final price
    instance.final_price = instance.price * (1 - instance.off_percent / 100)


@receiver(post_save, sender=Product)
def set_main_image(sender, instance, **kwargs):
    if not instance.product_images.filter(is_main=True).exists():
        main_image = instance.product_images.filter(title__iexact='main').first()
        if main_image:
            main_image.is_main = True
            main_image.save()
        else:
            first_image = instance.product_images.first()
            if first_image:
                first_image.is_main = True
                first_image.save()


@receiver(post_save, sender=ProductColor)
@receiver(post_delete, sender=ProductColor)
def update_product_stock(sender, instance: ProductColor, **kwargs):
    # calculate stock
    instance.product.stock = 0
    colors = instance.product.product_color.all()
    if colors.count() == 0:
        instance.product.stock = 0
        # instance.product.is_active = False
        instance.product.save()
    for color in colors:
        instance.product.stock += color.stock
    instance.product.is_active = instance.product.stock != 0
    instance.product.save()


@receiver(post_save, sender=ProductRate)
@receiver(post_delete, sender=ProductRate)
def update_product_rate(sender, instance: ProductRate, **kwargs):
    # calculate average rate
    if instance.product.rates.count() != 0:
        instance.product.average_rate = instance.product.rates.aggregate(Avg('rate'))['rate__avg']
    instance.product.save()
