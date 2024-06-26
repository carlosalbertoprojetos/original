# Generated by Django 3.2.20 on 2024-03-19 11:43

import datetime
from django.db import migrations, models
import django.db.models.deletion

# from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("suporte", "0007_auto_20240318_1603"),
    ]

    operations = [
        migrations.AddField(
            model_name="timeline",
            name="fluxo",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.RESTRICT,
                to="suporte.workflow",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="acoes",
            name="proximaacao",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
