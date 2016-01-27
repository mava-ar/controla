# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0007_auto_20160126_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='responsable',
        ),
    ]
