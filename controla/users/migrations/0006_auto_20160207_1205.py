# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20160203_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='alertar_faltantes',
            field=models.BooleanField(help_text='Se alertará vía email la falta de asistencias del día, si existieran.', verbose_name='Alertarme sobre asistencias faltantes', default=True),
        ),
        migrations.AddField(
            model_name='historicaluser',
            name='notificar_alta_diario',
            field=models.BooleanField(help_text='Se notificará vía email, diariamente, el total de altas de asistencias.', verbose_name='Notificar diariamente las altas', default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='alertar_faltantes',
            field=models.BooleanField(help_text='Se alertará vía email la falta de asistencias del día, si existieran.', verbose_name='Alertarme sobre asistencias faltantes', default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='notificar_alta_diario',
            field=models.BooleanField(help_text='Se notificará vía email, diariamente, el total de altas de asistencias.', verbose_name='Notificar diariamente las altas', default=False),
        ),
    ]
