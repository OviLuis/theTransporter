import datetime as dt
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        order_init_date = validated_data.get('order_init_date')
        validated_data['order_end_date'] = order_init_date + dt.timedelta(hours=1)

        return Order.objects.create(**validated_data)

    class Meta:
        model = Order
        exclude = ('order_end_date', 'created_date', 'updated_date')