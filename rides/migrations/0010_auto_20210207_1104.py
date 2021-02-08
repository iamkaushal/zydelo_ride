# Generated by Django 3.1.6 on 2021-02-07 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rides', '0009_ride_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='distance',
            field=models.DecimalField(decimal_places=1, default=10, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ride',
            name='price_per_km',
            field=models.IntegerField(default=10),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='riders', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]