# TheTransporter

aplicación para la gestion basica de pedidos construida en Django usando Django REST Framework


1. crear entorno virtual (opcional)
2. instalar las dependencias ( ejecutar en la raiz del proyecto pip install -r requirements.txt)
3. ejecutar las migraciones del proyecto (python manage.py makemigrations, python manage.py migrate)


Documentación API

/orders/ POST: permite Agendar un pedido
/orders/ GET: consulta todos los pedidos registradas
/orders/?order_date= GET: Obtiene todos los pedidos asignados en un día en específico ordenados por la hora
/orders/?order_date=&driver= GET: Obtiene todos los pedidos de un conductor en un día en específico ordenados por la hora.
/drivers/ POST: Permite registrar un conductor
/drivers/ GET: Obtiene todos los conductores registrados
/drivers/available/?lat=&lng=&order_date= GET: Buscar el conductor disponible que esté más cerca de un punto geográfico en una fecha y hora


* Actualización automatica de la ubicacion de los conductores
Se realiza la actualizacion de la ubicación de los conductores cada 60 segundos mediante una tarea programada en drivers/tasks.py

La tarea programada es invocada cuando la configuracion de la aplicacion drive (DriversConfig) esta lista (metodo ready())

la funcion start() permite modificar el intervalo con el que se quiere actualizar la ubicacion de los conductores
