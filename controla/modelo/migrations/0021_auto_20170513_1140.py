# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0020_auto_20160425_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproyecto',
            name='codigo_contable',
            field=models.CharField(verbose_name='código contable', max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='numero_contrato',
            field=models.CharField(verbose_name='número de contrato', max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='codigo_contable',
            field=models.CharField(verbose_name='código contable', max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='numero_contrato',
            field=models.CharField(verbose_name='número de contrato', max_length=255, blank=True, null=True),
        ),
    ]
