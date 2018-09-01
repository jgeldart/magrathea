# Generated by Django 2.0.8 on 2018-09-01 01:12

import concordance.models.planetary_bodies
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import quantity_field.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('concordance', '0006_auto_20180831_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmosphericComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('percentage', concordance.models.planetary_bodies.PercentageField()),
            ],
            options={
                'verbose_name': 'atmospheric component',
                'verbose_name_plural': 'atmospheric components',
            },
        ),
        migrations.CreateModel(
            name='AtmosphericGas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('short_name', models.CharField(blank=True, max_length=32)),
                ('molar_weight', quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=())),
                ('refractive_index', models.FloatField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='planetpage',
            name='surface_pressure',
            field=quantity_field.fields.MultiQuantityField(default=0, dim=1, max_length=255, units=()),
        ),
        migrations.AddField(
            model_name='atmosphericcomponent',
            name='atmospheric_gas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='concordance.AtmosphericGas'),
        ),
        migrations.AddField(
            model_name='atmosphericcomponent',
            name='planetary_body',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='atmospheric_components', to='concordance.PlanetPage'),
        ),
    ]