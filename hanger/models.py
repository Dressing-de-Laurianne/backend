from django.db import models


# Create your models here.
class Hanger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    mqtt_topic = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return " [" + str(self.id) + "] " + self.mqtt_topic

    class Meta:
        ordering = ["created"]
