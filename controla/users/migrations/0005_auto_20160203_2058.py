# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_historicaluser'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='notificar_alta_individual',
            field=models.BooleanField(help_text='Se notificará vía email el alta de asistencia de proyectos relacionados.', verbose_name='Notificar alta asistencia', default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='notificar_alta_individual',
            field=models.BooleanField(help_text='Se notificará vía email el alta de asistencia de proyectos relacionados.', verbose_name='Notificar alta asistencia', default=True),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='cambia_personal',
            field=models.BooleanField(help_text='Al habilitar esta opción, el usuario puede cambiar el proyecto al cuál está asignado una persona.', verbose_name='¿Puede reasignar personas a proyectos?', default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='cambia_personal',
            field=models.BooleanField(help_text='Al habilitar esta opción, el usuario puede cambiar el proyecto al cuál está asignado una persona.', verbose_name='¿Puede reasignar personas a proyectos?', default=False),
        ),
    ]
