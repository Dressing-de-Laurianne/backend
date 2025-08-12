from django.db import models
from rest_framework import serializers

from dressing.models.item import Item, ItemSerializer

STATUS_CHOICES = sorted(
    [(c, c) for c in ["Pending", "Processing", "Delivered", "Cancelled"]]
)


# Create your models here.
class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    items = models.ManyToManyField(Item, blank=True, symmetrical=False)

    class Meta:
        ordering = ["created"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "status", "items", "created"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["items"] = [
            ItemSerializer(Item.objects.get(id=int(i))).data for i in rep["items"]
        ]
        return rep
