from django.contrib import admin

from CartApp.models import CartModel, CartItem


# Register your models here.

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0


@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('cart_random_number', 'user', 'status')
    search_fields = ('user',)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price')


