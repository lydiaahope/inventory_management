from django.contrib import admin
from .models import InventoryItem, Author, Order, Sale, SaleItem

admin.site.register(InventoryItem)
admin.site.register(Author)
admin.site.register(Order)
admin.site.register(Sale)
admin.site.register(SaleItem)
