# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('fecha', models.DateField(verbose_name='Fecha de presentismo')),
                ('nombre_responsable', models.CharField(verbose_name='Nombre del responsable', max_length=255, help_text='Se completará automaticamente con el responsable del proyecto seleccionado')),
                ('nombre_proyecto', models.CharField(verbose_name='Nombre del proyecto', max_length=255, help_text='Se completará automaticamente con el nombre del proyecto seleccionado.')),
            ],
            options={
                'verbose_name': 'asistencia diaria',
                'verbose_name_plural': 'asistencias diarias',
            },
        ),
        migrations.CreateModel(
            name='CCT',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('nombre', models.CharField(verbose_name='nombre', unique=True, max_length=255)),
            ],
            options={
                'verbose_name': 'CCT',
                'verbose_name_plural': 'CCTs',
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('situacion', models.CharField(verbose_name='situación', max_length=255)),
                ('codigo', models.CharField(verbose_name='código', unique=True, max_length=5)),
                ('observaciones', models.CharField(verbose_name='observaciones', max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'estado',
                'ordering': ('situacion',),
                'verbose_name_plural': 'estados',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('legajo', models.IntegerField(verbose_name='legajo', unique=True)),
                ('apellido', models.CharField(verbose_name='apellido', max_length=255)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('cuil', models.CharField(verbose_name='CUIL', max_length=15)),
                ('cct', models.ForeignKey(verbose_name='CCT', to='modelo.CCT', related_name='personas')),
            ],
            options={
                'verbose_name': 'persona',
                'ordering': ('apellido', 'nombre'),
                'verbose_name_plural': 'personas',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('nombre', models.CharField(verbose_name='nombre', unique=True, max_length=255)),
                ('responsable', models.ForeignKey(verbose_name='Responsable', to='modelo.Persona', related_name='proyectos_responsable')),
            ],
            options={
                'verbose_name': 'proyecto',
                'verbose_name_plural': 'proyectos',
            },
        ),
        migrations.CreateModel(
            name='RegistroAsistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('codigo_estado', models.CharField(verbose_name='Código', max_length=5, help_text='Se establecerá automaticamente con el código del estado seleccionado.')),
                ('asistencia', models.ForeignKey(to='modelo.Asistencia', related_name='items')),
                ('estado', models.ForeignKey(verbose_name='estado de presentismo', to='modelo.Estado')),
                ('persona', models.ForeignKey(to='modelo.Persona', related_name='registro_asistencia')),
            ],
            options={
                'verbose_name': 'registro de asistencia',
                'verbose_name_plural': 'registros de asistencia',
            },
        ),
        migrations.AddField(
            model_name='persona',
            name='proyecto',
            field=models.ForeignKey(verbose_name='proyecto', to='modelo.Proyecto', related_name='personas_involucradas'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='proyecto',
            field=models.ForeignKey(to='modelo.Proyecto', related_name='asistencias'),
        ),
    ]
