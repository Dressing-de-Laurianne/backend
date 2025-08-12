# Register your models here.
# admin.py
from django.contrib import admin


class OutfitAdmin(admin.ModelAdmin):
    def get_items(self, obj):
        return ", ".join(["[" + str(i.id) + "] " + i.title for i in obj.items.all()])

    filter_horizontal = ("items",)

    list_display = (
        "id",
        "created",
        "title",
        "description",
        "get_items",
    )
    ordering = ["-created"]  # Default sort by 'created' descending

    fieldsets = [
        ("Outfit Details", {"fields": ["created", "id", "title", "description"]}),
        ("Outfit Associated Items", {"fields": ["items"]}),
    ]

    readonly_fields = ("created", "id")

    list_editable = (
        "title",
        "description",
    )
    list_display_links = ("created", "id")
    list_filter = (
        "title",
        "description",
    )
    search_fields = [
        "title",
        "description",
        "items__title",
    ]
