# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0014_historicalasistencia_historicalcct_historicalestado_historicalpersona_historicalproyecto_historicalr'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='no_ocioso',
            field=models.BooleanField(help_text='Seleccione esta opción para indicar que el estado no implica ociosidad por parte del empleado', default=False, verbose_name='No está ocioso'),
        ),
        migrations.AddField(
            model_name='historicalestado',
            name='no_ocioso',
            field=models.BooleanField(help_text='Seleccione esta opción para indicar que el estado no implica ociosidad por parte del empleado', default=False, verbose_name='No está ocioso'),
        ),
        migrations.AlterField(
            model_name='registroasistencia',
            name='estado',
            field=models.ForeignKey(to='modelo.Estado', default=6, verbose_name='estado de presentismo'),
        ),
    ]
