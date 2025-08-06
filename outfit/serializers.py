from rest_framework import serializers
from outfit.models import Outfit
from item.serializers import ItemSerializer, Item

class OutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ['id', 'title', 'description', 'items', 'created']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['items'] = [ItemSerializer(Item.objects.get(id= int(i))).data for i in rep['items']]
        return rep