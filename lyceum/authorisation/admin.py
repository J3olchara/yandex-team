import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import admin

# isort: off
from authorisation.models import Profile  # noqa: I100

# isort: on


class ProfileInline(admin.TabularInline):  # type: ignore[type-arg]
    model = Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(django.contrib.auth.models.User)
admin.site.register(django.contrib.auth.models.User, UserAdmin)
