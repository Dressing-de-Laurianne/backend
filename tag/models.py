from django.db import models


# Create your models here.
class Tag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(
        max_length=100, unique=True, help_text="Unique identifier for the tag."
    )
    hanger_id = models.OneToOneField(
        "hanger.Hanger",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=True,
        # limit_choices_to={"tag": None},
        help_text="Hanger associated with this tag. NULL is no hanger associated.",
    )
    item_id = models.OneToOneField(
        "item.Item",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=True,
        help_text="Item associated with this tag. NULL is no item associated.",
    )

    class Meta:
        ordering = ["created"]
