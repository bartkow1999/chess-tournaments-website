from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from src.account.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('name', 'surname', 'username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('name', 'surname', 'username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
