# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modelo', '0015_auto_20160129_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoPersona',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('situacion', models.SmallIntegerField(default=1, verbose_name='situacion', choices=[(1, 'ALTA'), (2, 'BAJA')])),
                ('fechahora', models.DateTimeField(verbose_name='fecha y hora')),
                ('persona', models.ForeignKey(to='modelo.Persona')),
                ('usuario', models.ForeignKey(null=True, verbose_name='realizado por', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'movimiento de personas',
                'verbose_name': 'movimiento de persona',
            },
        ),
    ]
