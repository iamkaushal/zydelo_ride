# Generated by Django 3.1.4 on 2021-02-06 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_auto_20210206_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
