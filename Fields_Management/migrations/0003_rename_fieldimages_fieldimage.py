# Generated by Django 4.1.5 on 2023-01-07 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Fields_Management', '0002_field_location_field_meata_details_fieldimages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FieldImages',
            new_name='FieldImage',
        ),
    ]