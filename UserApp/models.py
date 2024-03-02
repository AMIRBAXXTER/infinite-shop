from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('باید شماره تلفن را وارد کنید.')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('مقدار این فیلد باید True باشد')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('مقدار این فیلد باید True باشد')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    first_name = models.CharField(max_length=25, verbose_name='نام')
    last_name = models.CharField(max_length=25, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد ملی')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    card_number = models.CharField(max_length=16, null=True, blank=True, verbose_name='شماره کارت')
    profile_image = models.ImageField(null=True, blank=True, verbose_name='تصویر پروفایل')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name != '' and self.last_name != '' else self.phone

    def __str__(self):
        return self.full_name()


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
    postal_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد پستی')
    receiver_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='تحویل گیرنده')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')

    def __str__(self):
        return f'{self.user}:{self.id}'
