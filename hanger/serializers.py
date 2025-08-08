from rest_framework import serializers

from hanger.models import Hanger
from tag.models import Tag


class HangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hanger
        fields = ["id", "mqtt_topic", "created"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        tag = Tag.objects.filter(hanger_id=instance.id).first()
        if tag:
            rep["tag"] = {"id": tag.pk, "tag": tag.tag}
        else:
            rep["tag"] = None
        return rep
