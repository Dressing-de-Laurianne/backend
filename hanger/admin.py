# Register your models here.
# admin.py
from django.contrib import admin

from hanger.models import Hanger


class HangerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "mqtt_topic",
    )
    ordering = ["-created"]  # Default sort by 'created' descending

    fieldsets = [
        ("Hanger Details", {"fields": ["created", "id", "mqtt_topic"]}),
    ]

    readonly_fields = ("created", "id")

    list_editable = ("mqtt_topic",)
    list_display_links = ("created", "id")
    list_filter = ("mqtt_topic",)
    search_fields = [
        "mqtt_topic",
    ]


admin.site.register(Hanger, HangerAdmin)
