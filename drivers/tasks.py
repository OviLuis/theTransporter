import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt

from .models import Driver


def update_driver_location():
    """
    tarea programada para actualizar la ubicacion de los conductores
    cada cierto tiempo
    :return:
    """
    print('update_driver_location..........')
    print(dt.datetime.today())
    url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        drivers_data = data.get('alfreds')
        for item in drivers_data:
            qs = Driver.objects.filter(pk=item.get('id'))
            last_update = item.get('lastUpdate')
            last_update = dt.datetime.strptime(last_update[:-5], '%Y-%m-%dT%H:%M:%S')
            if qs.exists():
                qs.update(
                    latitude=item.get('lat'),
                    longitude=item.get('lng'),
                    last_update=last_update
                )
            else:
                Driver.objects.create(
                    name='conductor-{}'.format(item.get('id')),
                    latitude=item.get('lat'),
                    longitude=item.get('lng'),
                    last_update=last_update
                )


def star():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_driver_location, 'interval', minutes=1)
    scheduler.start()
