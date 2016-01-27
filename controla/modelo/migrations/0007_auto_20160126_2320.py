# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_responsable(apps, schema_editor):
    Proyecto = apps.get_model("modelo", "Proyecto")
    Responsable = apps.get_model("modelo", "Responsable")

    for proy in Proyecto.objects.all():
        if proy.responsable:
            resp = Responsable()
            resp.persona = proy.responsable
            resp.proyecto = proy
            resp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0006_auto_20160126_2319'),
    ]

    operations = [
        migrations.RunPython(migrate_responsable)

    ]
