# Generated by Django 4.2 on 2024-01-31 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transit', '0010_drive_number_of_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drive',
            name='number_of_seats',
            field=models.IntegerField(default=3),
        ),
    ]
