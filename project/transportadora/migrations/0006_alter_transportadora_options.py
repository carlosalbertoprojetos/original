# Generated by Django 3.2.20 on 2024-02-20 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportadora', '0005_auto_20231013_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transportadora',
            options={'ordering': ['nome'], 'verbose_name': 'Transportadora', 'verbose_name_plural': 'Transportadoras'},
        ),
    ]