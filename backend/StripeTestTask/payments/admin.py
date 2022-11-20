from django.contrib import admin

from payments.models import Item, Discount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('item', 'percent_of_discount',)
