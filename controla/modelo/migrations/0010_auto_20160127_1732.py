# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0009_persona_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='fecha_baja',
            field=models.DateField(verbose_name='fecha de baja', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='usuario',
            field=models.ForeignKey(related_name='persona', to=settings.AUTH_USER_MODEL, null=True, help_text='Al asociar un usuario a la persona, este puede ingresar al sistema.', verbose_name='Usuario', blank=True),
        ),
    ]
