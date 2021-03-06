# Generated by Django 3.1.6 on 2021-02-07 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0010_auto_20210207_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='Rider',
            new_name='rider',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='riders',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='driver',
        ),
        migrations.AddField(
            model_name='trip',
            name='drive',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='drive', to='rides.ride'),
            preserve_default=False,
        ),
    ]
