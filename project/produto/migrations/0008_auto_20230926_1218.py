# Generated by Django 3.2.20 on 2023-09-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0007_auto_20230718_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='aliq_icms_interno',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='aliq_ipi',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
