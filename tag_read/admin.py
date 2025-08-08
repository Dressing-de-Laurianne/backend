# Register your models here.
# admin.py
from django.contrib import admin

from tag_read.models import TagRead


class TagReadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "tag",
    )
    ordering = ["-created"]  # Default sort by 'created' descending

    fieldsets = [
        ("TagRead Details", {"fields": ["created", "id", "tag"]}),
    ]

    readonly_fields = (
        "created",
        "id",
    )

    list_editable = ("tag",)
    list_display_links = ("created", "id")
    list_filter = (
        "tag",
        "created",
    )
    search_fields = [
        "tag",
    ]


admin.site.register(TagRead, TagReadAdmin)
