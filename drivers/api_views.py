import datetime
import math


from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from orders.models import Order
from .models import Driver
from .serializers import DriverSerializer
from .rules import get_available_drivers

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all().order_by('-id')
    serializer_class = DriverSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        final_status = status.HTTP_200_OK
        return Response(data=data, status=final_status, headers=headers)

    def update(self, request, *args, **kwargs):
        print()
        updated_by = request.user
        data = self.request.data

        serializer = self.get_serializer(self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        final_status = status.HTTP_200_OK
        return Response(status=final_status, template_name=None, content_type=None)

    def get_object(self):
        return get_object_or_404(Driver, pk=self.kwargs.get('pk'))


@api_view(['GET'])
def available_drivers(request):
    """
    permite obtener el listado de los conductores disponibles
    que esten mas cerca a un punto geografico en una fecha y hora en especifico
    filtrando por los parametros 'lat', 'lng' y 'order_date' enviados en la URL
    :return:
    """

    queryset = Driver.objects.all()
    order_date = request.query_params.get('order_date')
    lat = int(request.query_params.get('lat'))
    lng = int(request.query_params.get('lng'))

    if not all([order_date, lat, lng]):
        data = {'detail': 'No fueron enviados los parametros requeridos: lat, lng, order_date'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_date = datetime.datetime.strptime(order_date, '%Y-%m-%dT%H:%M:%S')
    except Exception:
        data = {'detail': 'el formato de fecha debe ser aaaa-mm-ddThh:mm:ss'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    # obtener los IDs de los conductores mas cercanos
    closer_drivers_list = get_available_drivers(lat, lng, order_date)
    print(closer_drivers_list)

    # Listado de los conductores mas cercanos
    queryset = queryset.filter(pk__in=closer_drivers_list)

    serializer = DriverSerializer(queryset, many=True)
    data = serializer.data

    return Response(data=data, status=status.HTTP_200_OK)

