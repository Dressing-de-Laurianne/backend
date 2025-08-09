from django.db import models
from rest_framework import serializers

from dressing.models.item import Item, ItemSerializer


# Create your models here.
class Outfit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True, default="")
    items = models.ManyToManyField(Item, blank=True, symmetrical=False)

    class Meta:
        ordering = ["created"]


class OutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ["id", "title", "description", "items", "created"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["items"] = [
            ItemSerializer(Item.objects.get(id=int(i))).data for i in rep["items"]
        ]
        return rep
