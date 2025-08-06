from rest_framework import serializers

from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "tag",
            "hanger_id",
            "item_id",
            "created",
        ]
