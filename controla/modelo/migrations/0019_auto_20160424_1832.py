# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0018_auto_20160424_1831'),
    ]

    operations = [
        migrations.RunSQL("update modelo_proyecto set codigo = LPAD(id, 6, 0);", "")
    ]
