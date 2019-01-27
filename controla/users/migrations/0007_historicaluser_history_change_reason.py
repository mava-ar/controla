# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160207_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
