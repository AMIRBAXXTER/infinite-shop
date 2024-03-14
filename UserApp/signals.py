from django.db.models.signals import post_save
from django.dispatch import receiver

from CartApp.models import CartModel
from .models import Address


@receiver(post_save, sender=Address)
def set_address_to_cart(sender, instance: Address, **kwargs):
    if instance.is_active:
        cart_model = CartModel.objects.filter(user=instance.user, status='در انتظار پرداخت').first()
        if cart_model:
            cart_model.address = instance
            cart_model.save()

