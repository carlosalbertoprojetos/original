# Generated by Django 3.2.20 on 2024-03-26 19:01

import datetime
from django.db import migrations, models

# from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("suporte", "0012_timeline_acao"),
    ]

    operations = [
        migrations.AddField(
            model_name="suporte",
            name="conclusao",
            field=models.DateField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="timeline",
            name="conclusao",
            field=models.DateField(default=0),
            preserve_default=False,
        ),
    ]
