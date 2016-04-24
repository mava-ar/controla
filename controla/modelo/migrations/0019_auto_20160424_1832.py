# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fill_codigo(apps, schema_editor):
    Proyecto = apps.get_model("modelo", "Proyecto")
    for proy in Proyecto.all_proyects.all():
        proy.codigo = "{0:05d}".format(proy.pk)
        proy.save()


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0018_auto_20160424_1831'),
    ]

    operations = [
        migrations.RunPython(fill_codigo, fill_codigo)
    ]
