from django.contrib import admin

from ProductsApp.models import *


# Register your models here.

class ProductRateInline(admin.TabularInline):
    model = ProductRate
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 0


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'is_active')
    inlines = [
        ProductImageInline,
        ProductColorInline,
        ProductRateInline,
        ProductCommentInline,
    ]
