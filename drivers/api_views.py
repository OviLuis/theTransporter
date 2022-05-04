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

    # obtener los conductores que tengan pedidos asignados a la fecha y hora indicada
    busy_drivers = Order.objects.filter(
        order_init_date__gte=order_date,
        order_end_date__lte=order_date).\
        values_list('id_driver', flat=True)

    # obtener los conductores disponible en la hora indicada
    queryset = queryset.filter(
        last_update=order_date
    ).exclude(pk__in=busy_drivers)

    distance_list = []
    for driver in queryset:
        # calcular para cada conductor la distancia a la que se encuentra del punto de recogida
        d = distance(lat, lng, driver.latitude, driver.longitude)

        # se crea tupla con el id del conductor y la distancia
        driver_tuple = (driver.pk, d)
        distance_list.append(driver_tuple)

    print(distance_list)

    if distance_list:
        # ordenar la tupla de manor a mayor distancia
        distance_list.sort(key=lambda x: x[1])  # index 1 es el segundo elemento de la tupla

    print(distance_list)
    # con la tupla ordenada se obtiene el conductor que se encuentra mas cerca al punto geografico indicado
    closer_driver = distance_list[0]

    queryset = queryset.filter(pk=closer_driver[0])

    serializer = DriverSerializer(queryset, many=True)
    data = serializer.data

    return Response(data=data, status=status.HTTP_200_OK)


def distance(x1, y1, x2, y2):
    """
    Funcion auxiliar para calcular la distancia entre dos puntos P1(x1, y1) P2(X2, y2)

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return: distnacia entre P1 y P2
    """

    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return d