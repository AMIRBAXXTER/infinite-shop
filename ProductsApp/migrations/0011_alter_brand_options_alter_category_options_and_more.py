# Generated by Django 5.0.2 on 2024-02-25 08:21

import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0010_product_main_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'برند', 'verbose_name_plural': 'برند ها'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'verbose_name': 'محصول', 'verbose_name_plural': 'محصول ها'},
        ),
        migrations.AlterModelOptions(
            name='productcolor',
            options={'verbose_name': 'رنگ محصول', 'verbose_name_plural': 'رنگ های محصول'},
        ),
        migrations.AlterModelOptions(
            name='productcomment',
            options={'verbose_name': 'نظر محصول', 'verbose_name_plural': 'نظر های محصول'},
        ),
        migrations.AlterModelOptions(
            name='productfavorite',
            options={'verbose_name': 'محصول مورد علاقه', 'verbose_name_plural': 'محصول های مورد علاقه'},
        ),
        migrations.AlterModelOptions(
            name='productproperty',
            options={'verbose_name': 'مشخصات محصول', 'verbose_name_plural': 'مشخصات محصولات'},
        ),
        migrations.AlterModelOptions(
            name='productrate',
            options={'verbose_name': 'امتیاز محصول', 'verbose_name_plural': 'امتیاز محصول ها'},
        ),
        migrations.AddField(
            model_name='productcolor',
            name='stock',
            field=models.PositiveIntegerField(default=1, verbose_name='موجودی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name=' تصویر اصلی'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1920, 1080], upload_to='product_brands/', verbose_name='تصویر برند'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='title',
            field=models.CharField(max_length=50, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ProductsApp.category', verbose_name='والد'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='color',
            field=models.CharField(max_length=50, verbose_name='رنگ'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_of_product', to='ProductsApp.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='title',
            field=models.CharField(max_length=50, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='comment',
            field=models.TextField(verbose_name='نظر'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ProductsApp.productcomment', verbose_name='والد'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ProductsApp.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='productfavorite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='productfavorite',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='ProductsApp.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productfavorite',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش'),
        ),
        migrations.AlterField(
            model_name='productfavorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1920, 1080], upload_to='product_images/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='ProductsApp.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='title',
            field=models.CharField(max_length=50, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_properties', to='ProductsApp.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='title',
            field=models.CharField(max_length=50, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='value',
            field=models.CharField(max_length=50, verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='ProductsApp.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='rate',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='امتیاز'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش'),
        ),
        migrations.AlterField(
            model_name='productrate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='ProductsApp_price_c77698_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created_at'], name='ProductsApp_created_70778f_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['updated_at'], name='ProductsApp_updated_363c12_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active'], name='ProductsApp_is_acti_30e4aa_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['average_rate'], name='ProductsApp_average_8a99a0_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['brand'], name='ProductsApp_brand_i_c14946_idx'),
        ),
    ]
