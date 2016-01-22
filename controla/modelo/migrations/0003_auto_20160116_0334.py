# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0002_auto_20160116_0139'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='asistencia',
            unique_together=set([('fecha', 'proyecto')]),
        ),
        migrations.AlterUniqueTogether(
            name='registroasistencia',
            unique_together=set([('asistencia', 'persona')]),
        ),
    ]
