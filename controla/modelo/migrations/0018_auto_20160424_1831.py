# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0017_auto_20160213_2129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'verbose_name': 'proyecto', 'verbose_name_plural': 'proyectos', 'ordering': ['nombre']},
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='codigo',
            field=models.CharField(verbose_name='codigo', blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='codigo',
            field=models.CharField(verbose_name='codigo', blank=True, max_length=255, null=True),
        ),
    ]
