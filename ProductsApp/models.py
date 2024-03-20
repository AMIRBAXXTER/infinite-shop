from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django_resized import ResizedImageField
from UserApp.models import User

from translate import Translator

tr = Translator('en', 'fa')


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    url_title = models.SlugField(max_length=50, default='automatic-set', verbose_name='عنوان در url', blank=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='children', blank=True, null=True,
                               verbose_name='والد')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def save(self, *args, **kwargs):
        if self.url_title == 'automatic-set' or self.url_title == '':
            self.url_title = slugify(tr.translate(self.title))
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    brand_image = ResizedImageField(upload_to='product_brands/', blank=True, null=True, verbose_name='تصویر برند')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    off_percent = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)],
                                              verbose_name='درصد تخفیف')
    final_price = models.PositiveIntegerField(verbose_name='قیمت نهایی', blank=True, null=True)
    stock = models.PositiveIntegerField(verbose_name='موجودی')
    weight = models.PositiveIntegerField(verbose_name='وزن به گرم')
    short_description = models.CharField(max_length=255, verbose_name='توضیحات کوتاه')
    long_description = models.TextField(verbose_name='توضیحات کامل')
    main_description = models.TextField(verbose_name='توضیحات اصلی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    sale_count = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')
    average_rate = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='میانگین امتیازات', default=1)
    rate = models.ManyToManyField(User, through='ProductRate', related_name='product_rates', verbose_name='امتیازات')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name='برند', blank=True,
                              null=True)
    category = models.ManyToManyField(Category, related_name='products', blank=True, verbose_name='دسته بندی')
    comment = models.ManyToManyField(User, through='ProductComment', related_name='product_comments',
                                     verbose_name='نظرات')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ProductsApp:product_detail', args=[self.id])

    def off_price(self):
        return self.price - self.final_price

    def delete(self, *args, **kwargs):
        for img in self.product_images.all():
            storage, path = img.image.storage, img.image.path
            storage.delete(path)
        super().delete(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['is_active']),
            models.Index(fields=['average_rate']),
            models.Index(fields=['brand']),
        ]
        ordering = ['-created_at']

        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'


class ProductProperty(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_properties',
                                verbose_name='محصول')
    value = models.CharField(max_length=50, verbose_name='مقدار')

    def __str__(self):
        return f'{self.title}:{self.value}'

    class Meta:
        verbose_name = 'مشخصات محصول'
        verbose_name_plural = 'مشخصات محصولات'


class ProductImage(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    image = ResizedImageField(upload_to='product_images/', force_format='webp', quality=100, blank=True, null=True,
                              verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', verbose_name='محصول')
    is_main = models.BooleanField(default=False, verbose_name=' تصویر اصلی')

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر های محصول'

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product).exclude(id=self.id).update(is_main=False)
        super(ProductImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def image_preview(self):
        return format_html(' <img src="{0}" width="150" height="150">'.format(self.image.url))
        # return f'<img src="{self.image.url}" width="100" height="100">'

    image_preview.short_description = 'تصویر'
    image_preview.allow_tags = True

    def __str__(self):
        return self.title


class ProductRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rates', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates', verbose_name='محصول')
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name='امتیاز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    def __str__(self):
        return f'{self.user.full_name}:{self.product.title}:{self.rate}'

    def save(self, *args, **kwargs):
        if self.user in self.product.rate.all():
            self.product.rate.remove(self.user)
        super(ProductRate, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'امتیاز محصول'
        verbose_name_plural = 'امتیاز محصول ها'


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    parent = models.ForeignKey('ProductComment', on_delete=models.CASCADE, related_name='children', blank=True,
                               null=True, verbose_name='والد')
    comment = models.TextField(verbose_name='نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    def __str__(self):
        return f'{self.user.full_name}:{self.id}'

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظر های محصول'


class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    def __str__(self):
        return f'{self.user.full_name}:{self.product.title}'

    class Meta:
        verbose_name = 'محصول مورد علاقه'
        verbose_name_plural = 'محصول های مورد علاقه'


class ProductColor(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_color',
                                verbose_name='محصول')
    color = models.CharField(max_length=50, verbose_name='رنگ')
    stock = models.PositiveIntegerField(verbose_name='موجودی')

    def __str__(self):
        return f'{self.product}:{self.color}'

    class Meta:
        verbose_name = 'رنگ محصول'
        verbose_name_plural = 'رنگ های محصول'


class ProductVisited(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_visited', verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_visited', null=True, blank=True,
                             verbose_name='کاربر')
    ip = models.CharField(max_length=100, verbose_name='آی پی')

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید محصولات'
