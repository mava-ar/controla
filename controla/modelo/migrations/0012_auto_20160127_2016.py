# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def initial_data(apps, schema_editor):
    Proyecto = apps.get_model("modelo", "Proyecto")
    Estado = apps.get_model("modelo", "Estado")

    estado = Estado()
    estado.codigo = "SD"
    estado.situacion = "Sin dato"
    estado.observaciones = " No figura estado en la antigua planilla"
    estado.save()

    proyecto = Proyecto()
    proyecto.nombre = "Sin proyecto"
    proyecto.save()


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0011_remove_responsable_puede_asignar_persona'),
    ]

    operations = [
        migrations.RunPython(initial_data)

    ]
