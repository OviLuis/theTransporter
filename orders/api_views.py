import datetime


from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from drivers.rules import get_available_drivers
from drivers.models import Driver

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_init_date')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        lat = serializer.validated_data.get('pickup_lat')
        lng = serializer.validated_data.get('pickup_lng')
        order_date = serializer.validated_data.get('order_init_date')

        # obtener listado de los IDs de los conductores mas cercanos
        closer_drivers_list = get_available_drivers(lat, lng, order_date)

        print(closer_drivers_list)

        # Se valida que existan conductores disponibles para la fecha indicada
        # para asi asignar el conductor mas cercano disponible.
        # de lo contrario se deja el conductor enviado inicialmente en el request.
        if closer_drivers_list:
            # se obtiene el primer ID de  la lista por ser el mas cercano
            closer_driver = closer_drivers_list[0]

            # Listado de los conductores mas cercanos
            driver = Driver.objects.get(pk=closer_driver)

            # se asigna el conductor mas cercano que se encuentre.
            serializer.validated_data['id_driver'] = driver

        data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        final_status = status.HTTP_200_OK
        return Response(data=data, status=final_status, headers=headers)

    def update(self, request, *args, **kwargs):
        data = self.request.data

        serializer = self.get_serializer(self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        final_status = status.HTTP_200_OK
        return Response(status=final_status, template_name=None, content_type=None)

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        """
        Opcionalmente se puede restingir los pedidos retornados
        filtrando por los parametros 'order_date' o 'driver' enviados en la URL
        :return:
        """

        queryset = Order.objects.all().order_by('order_init_date')
        order_date = self.request.query_params.get('order_date')
        driver = self.request.query_params.get('driver')

        if order_date is not None:

            order_date = datetime.datetime.strptime(order_date, '%Y-%m-%d')

            queryset = queryset.filter(
                order_init_date__year=order_date.year,
                order_init_date__month=order_date.month,
                order_init_date__day=order_date.day)

        if driver is not None:
            queryset = queryset.filter(id_driver__pk=driver)

        return queryset

