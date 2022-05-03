from django.db import models


class Driver(models.Model):

    id = models.AutoField(primary_key=True, verbose_name="ID Pedido")
    name = models.CharField(max_length=100, verbose_name='Nombre Conductor')
    latitude = models.IntegerField(verbose_name='Latitud')
    longitude = models.IntegerField(verbose_name='Longiutd')
    last_update = models.DateTimeField(verbose_name='Ultima Modificacion')

    def __str__(self):
        return '%d' % self.id

    class Meta:
        managed = True
        db_table = 'driver'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'

