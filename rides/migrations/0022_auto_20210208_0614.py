# Generated by Django 3.1.6 on 2021-02-08 00:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rides', '0021_auto_20210208_0606'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='request',
            unique_together={('ride', 'user_requested')},
        ),
    ]