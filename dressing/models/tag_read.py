from django.db import models
from rest_framework import serializers


# Create your models here.
class TagRead(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, help_text="Unique identifier readed.")

    class Meta:
        ordering = ["created"]


class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagRead
        fields = ["id", "tag", "created"]
