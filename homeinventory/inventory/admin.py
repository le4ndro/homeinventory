from django.contrib import admin

from homeinventory.inventory.models import Category, Location, Item

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Item)
