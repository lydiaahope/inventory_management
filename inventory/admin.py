from django.contrib import admin
from .models import InventoryItem, Author, Order

admin.site.register(InventoryItem)
admin.site.register(Author)
admin.site.register(Order)
