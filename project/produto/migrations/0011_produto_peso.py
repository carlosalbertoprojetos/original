# Generated by Django 3.2.20 on 2023-10-08 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0010_auto_20231006_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='peso',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
