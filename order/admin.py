# Register your models here.
# admin.py
from django.contrib import admin

from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    def get_items(self, obj):
        return ", ".join(["[" + str(i.id) + "] " + i.title for i in obj.items.all()])

    filter_horizontal = ("items",)

    list_display = (
        "id",
        "created",
        "status",
        "get_items",
    )
    ordering = ["-created"]  # Default sort by 'created' descending

    fieldsets = [
        ("Order Details", {"fields": ["created", "id", "status"]}),
        ("Order Associated Items", {"fields": ["items"]}),
    ]

    readonly_fields = ("created", "id")

    list_editable = ("status",)
    list_display_links = ("created", "id")
    list_filter = ("status", "items")
    search_fields = ["status", "items__title"]


admin.site.register(Order, OrderAdmin)
