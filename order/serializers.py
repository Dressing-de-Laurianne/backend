from rest_framework import serializers
from order.models import Order
from item.serializers import ItemSerializer, Item

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'status', 'items', 'created']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['items'] = [ItemSerializer(Item.objects.get(id= int(i))).data for i in rep['items']]
        return rep