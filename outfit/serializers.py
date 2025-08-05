from rest_framework import serializers
from outfit.models import Outfit
from item.serializers import ItemSerializer

class OutfitSerializer(serializers.ModelSerializer):
    #items = ItemSerializer(read_only=False,  many=True)

    class Meta:
        model = Outfit
        fields = ['id', 'title', 'description', 'items', 'created']