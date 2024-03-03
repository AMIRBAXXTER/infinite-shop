from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


@admin.register(User)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'national_code', 'date_of_birth', 'email', 'card_number', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': (
        'first_name', 'last_name', 'national_code', 'date_of_birth', 'email', 'card_number', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    inlines = [
        AddressInline,
    ]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
