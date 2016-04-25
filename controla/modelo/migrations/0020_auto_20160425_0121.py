# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0019_auto_20160424_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproyecto',
            name='codigo',
            field=models.CharField(default='-', max_length=255, verbose_name='codigo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='codigo',
            field=models.CharField(max_length=255, verbose_name='codigo'),
        ),
    ]
