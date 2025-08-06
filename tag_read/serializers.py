from rest_framework import serializers

from tag_read.models import TagRead


class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRead
        fields = ["id", "tag", "created"]
