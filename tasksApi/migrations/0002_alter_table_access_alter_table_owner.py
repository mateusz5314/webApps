# Generated by Django 4.0.3 on 2022-04-13 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasksApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='access',
            field=models.ManyToManyField(blank=True, related_name='access', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='table',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
