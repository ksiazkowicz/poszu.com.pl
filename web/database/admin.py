from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ["name", "source", "location", "gimme_link", "is_lost", "is_open", "is_successful"]
    list_filter = ["source", "location", "is_lost", "is_open", "is_successful"]
    
admin.site.register(Item, ItemAdmin)