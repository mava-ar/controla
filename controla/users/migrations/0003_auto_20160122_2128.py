# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_cambia_personal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cambia_personal',
            field=models.BooleanField(help_text='Al l habilitar esta opción (con rol RESPONSABLE), el usuario puede cambiar el proyecto al cuál está asignado una persona.', default=False, verbose_name='¿Puede reasignar personas a proyectos?'),
        ),
    ]
