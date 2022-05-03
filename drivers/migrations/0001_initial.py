# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(verbose_name='ID Pedido', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Nombre Conductor', max_length=100)),
                ('latitude', models.IntegerField(verbose_name='Latitud')),
                ('longitude', models.IntegerField(verbose_name='Longiutd')),
                ('last_update', models.DateTimeField(verbose_name='Ultima Modificacion')),
            ],
            options={
                'verbose_name': 'Conductor',
                'verbose_name_plural': 'Conductores',
                'db_table': 'driver',
                'managed': True,
            },
        ),
    ]
