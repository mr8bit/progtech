from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'departament',)


admin.site.register(Group, GroupAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('laboratory', 'user',)


admin.site.register(Report, ReportAdmin)


class LabaAdmin(admin.ModelAdmin):
    list_display = ('name', 'variant', 'group')


admin.site.register(Laboratory, LabaAdmin)


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'variant', 'group')


admin.site.register(UserGroup, UserGroupAdmin)