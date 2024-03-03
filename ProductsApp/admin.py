from django.contrib import admin

from ProductsApp.models import *


# Register your models here.

class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 0


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
        ProductPropertyInline,
    ]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand_image')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_title', 'parent')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'image_preview')
    list_filter = ('product',)


@admin.register(ProductVisited)
class ProductVisitedAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip')


@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')
