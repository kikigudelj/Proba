# Generated by Django 4.2 on 2024-01-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('price', models.FloatField(max_length=10, null=True)),
                ('pub_date', models.DateTimeField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
    ]
