# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0005_auto_20160122_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(verbose_name='Fecha de modificación', auto_now=True)),
                ('puede_asignar_persona', models.BooleanField(verbose_name='¿Puede reasignar personas?', default=False, help_text='Al seleccionar esta opción, el responsable del proyecto puede cambiar la asignación de personas a proyectos.')),
                ('persona', models.ForeignKey(to='modelo.Persona', null=True, verbose_name='persona', related_name='responsable_rel')),
                ('proyecto', models.OneToOneField(to='modelo.Proyecto', null=True, verbose_name='proyecto', related_name='responsable_rel')),
            ],
            options={
                'verbose_name_plural': 'responsables',
                'verbose_name': 'responsable',
            },
        ),
        migrations.AlterField(
            model_name='registroasistencia',
            name='estado',
            field=models.ForeignKey(to='modelo.Estado', verbose_name='estado de presentismo', default=5),
        ),
        migrations.AlterUniqueTogether(
            name='responsable',
            unique_together=set([('persona', 'proyecto')]),
        ),
    ]
