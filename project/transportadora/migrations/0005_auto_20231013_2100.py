# Generated by Django 3.2.20 on 2023-10-14 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportadora', '0004_auto_20231012_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportadora',
            name='tel_contato',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='transportadora',
            name='tel_principal',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
