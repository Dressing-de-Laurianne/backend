from rest_framework import serializers
from order.models import Order
from item.serializers import ItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    #items = ItemSerializer(read_only=False,  many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'items', 'created']