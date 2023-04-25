from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'street_address',
                    'city', 'state', 'zip_code', 'orders')

    def orders(self, obj):
        return ", ".join([str(o.id) for o in obj.order_set.all()])
    orders.short_description = "Orders"

    # Add the following lines to use the new related names for groups and user permissions
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('groups__name', 'user_permissions__name')



admin.site.register(User, CustomUserAdmin)
