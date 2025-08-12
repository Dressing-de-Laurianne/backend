# Register your models here.
# admin.py
from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "tag",
        "hanger_id",
        "item_id",
    )
    ordering = ["-created"]  # Default sort by 'created' descending

    fieldsets = [
        ("Tag Details", {"fields": ["created", "id", "tag"]}),
        ("Tag Associated Hanger/Item", {"fields": ["hanger_id", "item_id"]}),
    ]

    readonly_fields = ("created", "id")

    list_editable = ("tag", "hanger_id", "item_id")
    list_display_links = ("created", "id")
    list_filter = ("tag", "created", "hanger_id", "item_id")
    search_fields = ["tag"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "hanger_id":
            formfield.required = False
        elif db_field.name == "item_id":
            formfield.required = False
        return formfield
