from django.contrib import admin

from IndexApp.models import *


class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    extra = 0


# Register your models here.
@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'is_active')
    inlines = [TeamMemberInline]
