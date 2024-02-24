from django.contrib import admin

from ProductsApp.models import *


# Register your models here.

class ProductRateInline(admin.TabularInline):
    model = ProductRate
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'is_active')
    inlines = [
        ProductImageInline,
        ProductRateInline,
        ProductCommentInline,
    ]
