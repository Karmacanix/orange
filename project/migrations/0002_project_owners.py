# Generated by Django 2.0.1 on 2018-01-16 22:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]