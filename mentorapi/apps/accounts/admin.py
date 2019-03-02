from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User


class ExtendedUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff']
    list_editable = ['first_name', 'last_name', 'role']

    class Meta:
        model = User


admin.site.register(User, ExtendedUserAdmin)
