from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تماس')

    def __str__(self):
        return self.username


class Province(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان ها'


class City(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام')
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='استان')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='کاربر')
    province = models.ForeignKey(Province, related_name='addresses', on_delete=models.CASCADE, null=True, blank=True, )
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE, null=True, blank=True, )
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='آدرس')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.user.username
