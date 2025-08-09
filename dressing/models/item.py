import os
import re
import uuid

from django.db import models
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

SIZE_CHOICES = sorted([(s, s) for s in ["XS", "S", "M", "L", "XL", "XXL"]])
TYPE_CHOICES = sorted(
    [(t, t) for t in ["Shirt", "Pants", "Dress", "Skirt", "Jacket", "Coat"]]
)
COLOR_CHOICES = sorted(
    [
        (c, c)
        for c in [
            "Black",
            "White",
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Pink",
            "Purple",
            "Brown",
            "Grey",
            "Orange",
            "Beige",
        ]
    ]
)


def file_location(instance, filename, **kwargs):
    ext = os.path.splitext(filename)[1]
    safe_title = re.sub(r"[^A-Za-z0-9_-]+", "_", instance.title)
    file_path = f"items/{instance.uuid}---{safe_title}{ext}"
    return file_path


# Create your models here.
class Item(models.Model):

    from dressing.models import Hanger

    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100, blank=True, default="")
    size = models.CharField(choices=SIZE_CHOICES, default="M", max_length=100)
    type = models.CharField(choices=TYPE_CHOICES, default="Shirt", max_length=100)
    image = models.ImageField(
        upload_to=file_location, blank=True, null=True, default=None
    )
    color = models.CharField(
        choices=COLOR_CHOICES, default="Black", max_length=100, blank=True
    )
    description = models.TextField(blank=True, default="")
    # hanger_id = models.ForeignKey('hanger.Hanger', on_delete=models.SET_NULL, related_name='items', unique=True, blank=True, null=True, help_text="Hanger associated with this item. NULL is no hanger associated.")
    hanger_id = models.OneToOneField(
        Hanger,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Hanger associated with this item. NULL is no hanger associated.",
    )

    def __str__(self):
        return " [" + str(self.id) + "] " + self.title

    class Meta:
        ordering = ["created"]


class ItemSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required=False)

    class Meta:
        model = Item
        fields = [
            "id",
            "uuid",
            "title",
            "size",
            "type",
            "color",
            "image",
            "description",
            "hanger_id",
            "created",
        ]

    def to_representation(self, instance):
        from dressing.models import Tag

        rep = super().to_representation(instance)
        tag = Tag.objects.filter(item_id=instance.id).first()
        if tag:
            rep["tag"] = {"id": tag.pk, "tag": tag.tag}
        else:
            rep["tag"] = None
        return rep
