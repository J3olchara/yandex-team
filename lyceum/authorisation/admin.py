import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import admin

from .models import Profile


class ProfileInline(admin.TabularInline):  # type: ignore[type-arg]
    model = Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(django.contrib.auth.models.User)
admin.site.register(django.contrib.auth.models.User, UserAdmin)
