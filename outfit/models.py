from django.db import models


# Create your models here.
class Outfit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True, default="")
    items = models.ManyToManyField("item.Item", blank=True, symmetrical=False)

    class Meta:
        ordering = ["created"]
