# Generated by Django 3.2.20 on 2023-10-31 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_auto_20231025_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estoquepecaacabada',
            options={'ordering': ['peca'], 'verbose_name': 'Estoque de Peças', 'verbose_name_plural': 'Estoque de Peças'},
        ),
    ]
