import datetime as dt
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    def validate(self, data):
        order_init_date = data.get('order_init_date')
        order_end_date = order_init_date + dt.timedelta(hours=1)
        # Validar si el conductor ya tiene asignado un pedido para la fecha ingresada
        qs = Order.objects.filter(id_driver=data.get('id_driver'), order_init_date__gte=order_init_date, order_end_date__lte=order_end_date)
        if qs.exists():
            raise serializers.ValidationError('El conductor no esta disponible.')

        return data

    def validate_pickup_lat(self, value):
        if value:
            if self._validate_point(value):
                raise serializers.ValidationError('La Latitud de recogida es incorrecta debe estar entre 0 y 100')

    def validate_pickup_lng(self, value):
        if value:
            if self._validate_point(value):
                raise serializers.ValidationError('La Longitud de recogida es incorrecta debe estar entre 0 y 100')

    def validate_delivery_lat(self, value):
        if value:
            if self._validate_point(value):
                raise serializers.ValidationError('La Latitud de entrega es incorrecta debe estar entre 0 y 100')

    def validate_delivery_lng(self, value):
        if value:
            if self._validate_point(value):
                raise serializers.ValidationError('La Longitud de entrega es incorrecta debe estar entre 0 y 100')

    def validate_id_driver(self, value):
        """
        valida
        :param value:
        :return:
        """
        pass

    def _validate_point(self, value):
        """
            Valida que una cordena no se salga del rango
            para el caso el rango es [0, 100]

            value: valor del a coordena
            return 1 --> se sale del rango
                    None --> no se sale del rango
        """

        if not 0 <= value <= 100:
            return 1

        return

    def create(self, validated_data):
        order_init_date = validated_data.get('order_init_date')
        validated_data['order_end_date'] = order_init_date + dt.timedelta(hours=1)

        # Validar si el conductor ya tiene asignado un pedido para la fecha ingresada


        return Order.objects.create(**validated_data)

    class Meta:
        model = Order
        exclude = ('order_end_date', 'created_date', 'updated_date')