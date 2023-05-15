from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ['id', 'user', 'created_at',
                    'total_items', 'calculate_total']

    def total_items(self, obj):
        return obj.items.count()

    total_items.short_description = 'Total Items'


admin.site.register(Cart, CartAdmin)
