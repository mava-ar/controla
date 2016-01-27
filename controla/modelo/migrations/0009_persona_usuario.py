# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modelo', '0008_remove_proyecto_responsable'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='usuario', null=True, verbose_name='Usuario', help_text='Al asociar un usuario a la persona, este puede ingresar al sistema.', blank=True),
        ),
    ]
