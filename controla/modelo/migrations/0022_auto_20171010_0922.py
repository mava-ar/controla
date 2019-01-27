# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0021_auto_20170513_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalasistencia',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalcct',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalestado',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalpersona',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalregistroasistencia',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalresponsable',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
