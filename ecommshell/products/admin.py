from django.contrib import admin
from .models import Product
# Register your models here.


@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('productName', 'productCode', 'total',)
