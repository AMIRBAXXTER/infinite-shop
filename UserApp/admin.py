from django.contrib import admin

from UserApp.models import *


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    fields = ('username', 'first_name', 'last_name', 'email', 'password')
    inlines = [
        AddressInline
    ]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
