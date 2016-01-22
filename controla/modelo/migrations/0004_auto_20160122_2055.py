# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0003_auto_20160116_0334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asistencia',
            options={'verbose_name': 'asistencia', 'verbose_name_plural': 'asistencias'},
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fecha_baja',
            field=models.DateField(null=True, verbose_name='fecha de baja', blank=True),
        ),
    ]
