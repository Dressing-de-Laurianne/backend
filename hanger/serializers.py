from rest_framework import serializers

from hanger.models import Hanger


class HangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hanger
        fields = ["id", "tag", "mqtt_topic"]
