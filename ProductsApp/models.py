from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_resized import ResizedImageField

from UserApp.models import User


# Create your models here.


class Rate(models.Model):
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])


class Category(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='children', blank=True, null=True)


class Brand(models.Model):
    title = models.CharField(max_length=50)
    brand_image = ResizedImageField(upload_to='product_brands/', blank=True, null=True)


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    off_percent = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], verbose_name='درصد تخفیف')
    final_price = models.PositiveIntegerField(verbose_name='قیمت نهایی')
    stock = models.PositiveIntegerField(verbose_name='موجودی')
    short_description = models.CharField(max_length=255, verbose_name='توضیحات کوتاه')
    long_description = models.TextField(verbose_name='توضیحات کامل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    average_rate = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name='میانگین امتیازات')
    rate = models.ManyToManyField(Rate, through='ProductRate', related_name='product_rates', verbose_name='امتیازات')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name='برند')
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته بندی')
    comment = models.ManyToManyField(User, through='ProductComment', related_name='product_comments', verbose_name='نظرات')


class ProductProperty(models.Model):
    title = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_properties')
    value = models.CharField(max_length=50)


class ProductImage(models.Model):
    title = models.CharField(max_length=50)
    image = ResizedImageField(upload_to='product_images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')


class ProductRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rates')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, related_name='rates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ColorOfProduct(models.Model):
    title = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='color_of_product')
    color = models.CharField(max_length=50)
