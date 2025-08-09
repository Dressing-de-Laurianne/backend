# Register your models here.
# admin.py
from django.contrib import admin


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "title",
        "size",
        "type",
        "color",
        "image",
        "description",
        "hanger_id",
    )
    ordering = ["-created"]  # Default sort by 'created' descending

    fieldsets = [
        (
            "Item Details",
            {
                "fields": [
                    "created",
                    "id",
                    "title",
                    "size",
                    "type",
                    "color",
                    "image",
                    "description",
                ]
            },
        ),
        ("Item Associated Hanger", {"fields": ["hanger_id"]}),
    ]

    readonly_fields = ("created", "id")

    list_editable = (
        "title",
        "size",
        "type",
        "color",
        "image",
        "description",
        "hanger_id",
    )
    list_display_links = ("created", "id")
    list_filter = ("title", "size", "type", "color", "description", "hanger_id")
    search_fields = [
        "title",
        "size",
        "type",
        "color",
        "description",
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "hanger_id":
            formfield.required = False
        return formfield
