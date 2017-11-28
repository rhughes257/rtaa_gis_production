# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-28 04:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomainValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('code', 'description'),
            },
        ),
        migrations.CreateModel(
            name='FeatureClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog_path', models.CharField(max_length=255, unique=True)),
                ('base_name', models.CharField(max_length=255)),
                ('count', models.IntegerField(null=True)),
                ('feature_type', models.CharField(max_length=25)),
                ('hasM', models.BooleanField()),
                ('hasZ', models.BooleanField()),
                ('has_spatial_index', models.BooleanField()),
                ('shape_field_name', models.CharField(max_length=25)),
                ('shape_type', models.CharField(max_length=25)),
            ],
            options={
                'ordering': ('base_name',),
            },
        ),
        migrations.CreateModel(
            name='FeatureDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_name', models.CharField(max_length=50, unique=True)),
                ('change_tracked', models.BooleanField()),
                ('dataset_type', models.CharField(max_length=25)),
                ('is_versioned', models.BooleanField()),
                ('spatial_reference', models.CharField(max_length=255)),
                ('xy_resolution', models.FloatField()),
                ('z_resolution', models.FloatField()),
                ('pcs_name', models.CharField(max_length=255)),
                ('pcs_code', models.CharField(max_length=100, null=True)),
                ('gcs_code', models.CharField(max_length=100, null=True)),
                ('gcs_name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'ordering': ('base_name',),
            },
        ),
        migrations.CreateModel(
            name='FeatureLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_version', models.CharField(max_length=10)),
                ('layer_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=255)),
                ('service_item_id', models.CharField(max_length=255)),
                ('is_view', models.BooleanField()),
                ('is_updatetable_view', models.BooleanField()),
                ('source_schema_changes_allowed', models.BooleanField()),
                ('display_field', models.CharField(max_length=255)),
                ('geometry_type', models.CharField(max_length=100)),
                ('min_scale', models.IntegerField()),
                ('max_scale', models.IntegerField()),
                ('x_min', models.FloatField()),
                ('y_min', models.FloatField()),
                ('x_max', models.FloatField()),
                ('y_max', models.FloatField()),
                ('wkid', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('default_visibility', models.BooleanField()),
                ('supports_append', models.BooleanField()),
                ('supports_calculate', models.BooleanField()),
                ('supports_truncate', models.BooleanField()),
                ('supports_attachments_by_upload_id', models.BooleanField()),
                ('supports_rollback_on_failure', models.BooleanField()),
                ('supports_statistics', models.BooleanField()),
                ('supports_advanced_queries', models.BooleanField()),
                ('supports_validate_sql', models.BooleanField()),
                ('supports_coordinates_quantization', models.BooleanField()),
                ('supports_apply_edits_with_guids', models.BooleanField()),
                ('supports_multi_scale_geo', models.BooleanField()),
                ('has_geo_updates', models.BooleanField()),
            ],
            options={
                'ordering': ('layer_id', 'name'),
            },
        ),
        migrations.CreateModel(
            name='FieldObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('alias_name', models.CharField(max_length=100)),
                ('base_name', models.CharField(max_length=100)),
                ('percent', models.FloatField()),
                ('default_value', models.CharField(max_length=100, null=True)),
                ('editable', models.BooleanField()),
                ('is_nullable', models.BooleanField()),
                ('length', models.IntegerField()),
                ('precision', models.FloatField()),
                ('required', models.BooleanField()),
                ('scale', models.FloatField()),
                ('type', models.CharField(max_length=50)),
                ('domain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.DomainValues')),
                ('feature_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.FeatureClass')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_name', models.CharField(max_length=255)),
                ('catalog_path', models.CharField(max_length=255, unique=True)),
                ('workspace_type', models.CharField(max_length=25)),
                ('workspace_factory_prog_ID', models.CharField(max_length=255)),
                ('release', models.CharField(max_length=255)),
                ('current_release', models.BooleanField()),
                ('connection_string', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('workspace_type',),
            },
        ),
        migrations.CreateModel(
            name='PublisherLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.CharField(max_length=25)),
                ('timestamp', models.DateField(auto_now=True)),
                ('feature_class', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.FeatureClass')),
                ('feature_layer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.FeatureLayer')),
            ],
            options={
                'ordering': ('feature_layer',),
            },
        ),
        migrations.CreateModel(
            name='WebMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('item_id', models.IntegerField()),
                ('layers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.FeatureLayer')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='featuredataset',
            name='gdb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.GDB'),
        ),
        migrations.AddField(
            model_name='featureclass',
            name='feature_dataset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.FeatureDataset'),
        ),
        migrations.AddField(
            model_name='domainvalues',
            name='gdb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloudSync.GDB'),
        ),
    ]
