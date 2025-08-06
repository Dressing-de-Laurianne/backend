from rest_framework import serializers

from item.models import Item
from tag.models import Tag


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
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
        rep = super().to_representation(instance)
        tag = Tag.objects.filter(item_id=instance.id).first()
        if tag:
            rep["tag"] = {"id": tag.pk, "tag": tag.tag}
        else:
            rep["tag"] = None
        return rep
