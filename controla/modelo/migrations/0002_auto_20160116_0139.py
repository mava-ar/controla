# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='responsable',
            field=models.ForeignKey(verbose_name='Responsable', to='modelo.Persona', null=True, related_name='proyectos_responsable'),
        ),
    ]
