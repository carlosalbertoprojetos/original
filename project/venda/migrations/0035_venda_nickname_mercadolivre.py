# Generated by Django 3.2.20 on 2023-11-21 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0034_alter_venda_data_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='nickname_mercadolivre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]