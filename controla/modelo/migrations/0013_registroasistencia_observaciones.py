# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0012_auto_20160127_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroasistencia',
            name='observaciones',
            field=models.CharField(verbose_name='observaciones', null=True, max_length=255, blank=True),
        ),
    ]
