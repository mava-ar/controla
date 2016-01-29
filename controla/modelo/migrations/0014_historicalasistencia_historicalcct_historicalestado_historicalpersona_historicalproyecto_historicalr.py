# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modelo', '0013_registroasistencia_observaciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAsistencia',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('fecha', models.DateField(verbose_name='Fecha de presentismo')),
                ('nombre_responsable', models.CharField(max_length=255, help_text='Se completará automaticamente con el responsable del proyecto seleccionado', verbose_name='Nombre del responsable')),
                ('nombre_proyecto', models.CharField(max_length=255, help_text='Se completará automaticamente con el nombre del proyecto seleccionado.', verbose_name='Nombre del proyecto')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Proyecto', blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical asistencia',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCCT',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre', db_index=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical CCT',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEstado',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('situacion', models.CharField(max_length=255, verbose_name='situación')),
                ('codigo', models.CharField(max_length=5, verbose_name='código', db_index=True)),
                ('observaciones', models.CharField(max_length=255, null=True, blank=True, verbose_name='observaciones')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical estado',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersona',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('legajo', models.IntegerField(verbose_name='legajo', db_index=True)),
                ('apellido', models.CharField(max_length=255, verbose_name='apellido')),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('cuil', models.CharField(max_length=15, verbose_name='CUIL')),
                ('fecha_baja', models.DateField(null=True, blank=True, verbose_name='fecha de baja')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('cct', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.CCT', blank=True)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Proyecto', blank=True)),
                ('usuario', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical persona',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProyecto',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre', db_index=True)),
                ('fecha_baja', models.DateField(null=True, blank=True, verbose_name='fecha de baja')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical proyecto',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRegistroAsistencia',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('codigo_estado', models.CharField(max_length=5, help_text='Se establecerá automaticamente con el código del estado seleccionado.', verbose_name='Código')),
                ('observaciones', models.CharField(max_length=255, null=True, blank=True, verbose_name='observaciones')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('asistencia', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Asistencia', blank=True)),
                ('estado', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Estado', blank=True)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('persona', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Persona', blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical registro de asistencia',
            },
        ),
        migrations.CreateModel(
            name='HistoricalResponsable',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, verbose_name='ID', db_index=True)),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Fecha de creación', editable=False)),
                ('modified_at', models.DateTimeField(blank=True, verbose_name='Fecha de modificación', editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('persona', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Persona', blank=True)),
                ('proyecto', models.ForeignKey(null=True, related_name='+', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='modelo.Proyecto', blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical responsable',
            },
        ),
    ]
