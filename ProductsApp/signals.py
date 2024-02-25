from django.db.models import Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def set_auto_fields(sender, instance: Product, **kwargs):
    instance.final_price = instance.price * (1 - instance.off_percent / 100)
    if instance.rates.count() != 0:
        instance.average_rate = instance.rates.aggregate(Avg('rate'))['rate__avg']
    instance.stock = 0
    colors = instance.product_color.all()
    for color in colors:
        instance.stock += color.stock
