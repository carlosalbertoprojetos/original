# Generated by Django 3.2.20 on 2024-03-19 23:46

import datetime
from django.db import migrations, models
import django.db.models.deletion

# from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("suporte", "0011_remove_timeline_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="timeline",
            name="acao",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.RESTRICT,
                to="suporte.acoes",
            ),
            preserve_default=False,
        ),
    ]