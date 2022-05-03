from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date')