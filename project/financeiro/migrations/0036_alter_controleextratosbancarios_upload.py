# Generated by Django 3.2 on 2024-05-03 19:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0035_auto_20240503_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controleextratosbancarios',
            name='upload',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 3, 16, 32, 52, 708925)),
        ),
    ]