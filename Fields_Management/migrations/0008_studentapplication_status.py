# Generated by Django 4.1.5 on 2023-02-04 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fields_Management', '0007_alter_course_options_alter_coursefield_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplication',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending Application'), (1, 'Accepted Application'), (2, 'Declined Application')], default=0),
        ),
    ]
