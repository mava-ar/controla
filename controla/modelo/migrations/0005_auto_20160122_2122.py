# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0004_auto_20160122_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='responsable',
            field=models.ForeignKey(null=True, blank=True, related_name='proyectos_responsable', to='modelo.Persona', verbose_name='Responsable'),
        ),
    ]
