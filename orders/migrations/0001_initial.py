# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID Pedido', primary_key=True, serialize=False)),
                ('order_init_date', models.DateTimeField(verbose_name='Fecha/hora Pedido')),
                ('order_end_date', models.DateTimeField(verbose_name='Fecha Fin Pedido')),
                ('pickup_lat', models.IntegerField(verbose_name='Latitud recogida')),
                ('pickup_lng', models.IntegerField(verbose_name='Longitud recogida')),
                ('delivery_lat', models.IntegerField(verbose_name='Latitud Destino')),
                ('delivery_lng', models.IntegerField(verbose_name='Longitud Destino')),
                ('created_by', models.CharField(verbose_name='Creado por', max_length=100)),
                ('created_date', models.DateField(verbose_name='Fecha Creacion', auto_now_add=True)),
                ('updated_by', models.CharField(verbose_name='Modificado por', max_length=100)),
                ('updated_date', models.DateField(verbose_name='Fecha Modificacion', blank=True, null=True)),
                ('id_driver', models.ForeignKey(verbose_name='Conductor', db_column='id_driver', related_name='order_driver', on_delete=django.db.models.deletion.PROTECT, to='drivers.Driver')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'order',
                'managed': True,
            },
        ),
    ]
