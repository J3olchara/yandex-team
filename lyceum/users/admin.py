from django.contrib import admin
import django.contrib.auth.admin
import django.contrib.auth.models

from .models import Profile


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(django.contrib.auth.models.User)
admin.site.register(django.contrib.auth.models.User, UserAdmin)
