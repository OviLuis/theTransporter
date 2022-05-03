from django.db import models


class Order(models.Model):

    id = models.AutoField(primary_key=True, verbose_name="ID Pedido")
    order_init_date = models.DateTimeField(verbose_name='Fecha/hora Pedido')
    order_end_date = models.DateTimeField(verbose_name='Fecha Fin Pedido')
    pickup_lat = models.IntegerField(verbose_name='Latitud recogida')
    pickup_lng = models.IntegerField(verbose_name='Longitud recogida')
    delivery_lat = models.IntegerField(verbose_name='Latitud Destino')
    delivery_lng = models.IntegerField(verbose_name='Longitud Destino')
    id_driver = models.ForeignKey('drivers.Driver', db_column='id_driver', related_name='order_driver',
                                  on_delete=models.PROTECT, verbose_name='Conductor')
    created_by = models.CharField(max_length=100, verbose_name='Creado por')
    created_date = models.DateField(auto_now_add=True, editable=False, verbose_name='Fecha Creacion')
    updated_by = models.CharField(max_length=100, verbose_name='Modificado por')
    updated_date = models.DateField(blank=True, null=True, verbose_name='Fecha Modificacion')

    def __str__(self):
        return '%d' % self.id

    class Meta:
        managed = True
        db_table = 'order'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
