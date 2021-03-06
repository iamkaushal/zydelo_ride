# Generated by Django 3.1.6 on 2021-02-07 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rides', '0013_auto_20210207_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='drive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='riders', to='rides.ride'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='riding', to=settings.AUTH_USER_MODEL),
        ),
    ]
