import math

from orders.models import Order
from .models import Driver


def get_available_drivers(lat, lng, date):
    """
    Obtener conductores disponibles

    Permite obtener el listado de los conductores disponibles para asignarle un pedido.
    Se obtiene una lista de los conductores disponibles mas cercanos a un punto geografico
    para la fecha indicada

    :param lat: latitud
    :param lng: longitud
    :param date: fecha/hora del pedido
    :return: lista de los ID de los conductores disponibles ordenamos desde el mas cercano al mas lejano del punto
    """

    # obtener los conductores que tengan pedidos asignados a la fecha y hora indicada
    busy_drivers = Order.objects.filter(
        order_init_date__gte=date,
        order_end_date__lte=date). \
        values_list('id_driver', flat=True)

    # obtener los conductores disponible en la hora indicada
    queryset = Driver.objects.filter(
        last_update=date
    ).exclude(pk__in=busy_drivers)

    driver_distance_list = []
    for driver in queryset:
        # calcular para cada conductor la distancia a la que se encuentra del punto de recogida
        d = distance(lat, lng, driver.latitude, driver.longitude)

        # se crea tupla con el id del conductor y la distancia
        driver_tuple = (driver.pk, d)
        driver_distance_list.append(driver_tuple)

    print(driver_distance_list)

    if driver_distance_list:
        # ordenar la lista de tuplas de menor a mayor distancia
        driver_distance_list.sort(key=lambda x: x[1])  # index 1 es el segundo elemento de la tupla

    # se obtiene los Id de los conductores
    drivers_list = [driver[0] for driver in driver_distance_list]

    return drivers_list


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