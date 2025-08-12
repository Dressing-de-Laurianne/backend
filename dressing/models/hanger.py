from django.db import models
from rest_framework import serializers


# Create your models here.
class Hanger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    mqtt_topic = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return " [" + str(self.id) + "] " + self.mqtt_topic

    class Meta:
        ordering = ["created"]


class HangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hanger
        fields = ["id", "mqtt_topic", "created"]

    def to_representation(self, instance):
        from dressing.models import Tag

        rep = super().to_representation(instance)
        tag = Tag.objects.filter(hanger_id=instance.id).first()
        if tag:
            rep["tag"] = {"id": tag.pk, "tag": tag.tag}
        else:
            rep["tag"] = None
        return rep
