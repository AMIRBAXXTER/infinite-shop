from django.db.models import Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def set_final_prize(sender, instance: Product, **kwargs):
    instance.final_price = instance.price * (1 - instance.off_percent / 100)


@receiver(pre_save, sender=Product)
def set_average_rate(sender, instance: Product, **kwargs):
    if instance.rates.count() != 0:
        instance.average_rate = instance.rates.aggregate(Avg('rate'))['rate__avg']
