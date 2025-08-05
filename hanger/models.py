from django.db import models


# Create your models here.
class Hanger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, blank=True, default='')
    mqtt_topic = models.CharField(max_length=100, blank=True, default='')
  
    class Meta:
        ordering = ['created']