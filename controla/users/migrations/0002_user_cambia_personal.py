# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cambia_personal',
            field=models.BooleanField(verbose_name='¿Puede reasignar personas a proyectos?', default=False),
        ),
    ]
