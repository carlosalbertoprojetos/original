# Generated by Django 3.2.20 on 2023-10-20 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0021_auto_20231018_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='notafiscal',
        ),
    ]