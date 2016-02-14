# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0016_movimientopersona'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(blank=True, verbose_name='Usuario', null=True, help_text='Al asociar un usuario a la persona, este puede ingresar al sistema.', related_name='persona', to=settings.AUTH_USER_MODEL),
        ),
    ]
