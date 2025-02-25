# Generated by Django 4.2 on 2024-02-01 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=5000)),
                ('m_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_receiver', to=settings.AUTH_USER_MODEL)),
                ('m_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
