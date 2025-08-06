from django.db import models

STATUS_CHOICES = sorted(
    [(c, c) for c in ["Pending", "Processing", "Delivered", "Cancelled"]]
)


# Create your models here.
class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    items = models.ManyToManyField("item.Item", blank=True, symmetrical=False)

    class Meta:
        ordering = ["created"]
