# Generated by Django 2.0.8 on 2018-08-30 11:31

from django.db import migrations
import quantity_field.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('concordance', '0003_auto_20180829_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasplanetpage',
            name='argument_of_periapsis',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(template='blocks/rich_text_block.html')), ('image', wagtail.images.blocks.ImageChooserBlock()), ('orbital_characteristics', wagtail.core.blocks.StructBlock([('style', wagtail.core.blocks.ChoiceBlock(choices=[('default', 'Default'), ('muted', 'Muted'), ('primary', 'Primary'), ('secondary', 'Secondary')]))])), ('rotational_characteristics', wagtail.core.blocks.StructBlock([('style', wagtail.core.blocks.ChoiceBlock(choices=[('default', 'Default'), ('muted', 'Muted'), ('primary', 'Primary'), ('secondary', 'Secondary')]))])), ('physical_characteristics', wagtail.core.blocks.StructBlock([('style', wagtail.core.blocks.ChoiceBlock(choices=[('default', 'Default'), ('muted', 'Muted'), ('primary', 'Primary'), ('secondary', 'Secondary')]))]))]),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='inclination',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='longitude_of_the_ascending_node',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='mass',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='obliquity',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='precessional_period',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='radius',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='rotational_period',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='gasplanetpage',
            name='semi_major_axis',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
        migrations.AlterField(
            model_name='starpage',
            name='mass',
            field=quantity_field.fields.MultiQuantityField(dim=1, max_length=255, units=()),
        ),
    ]
