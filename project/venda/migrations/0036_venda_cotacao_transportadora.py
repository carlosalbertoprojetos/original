# Generated by Django 3.2.20 on 2023-11-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0035_venda_nickname_mercadolivre'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='cotacao_transportadora',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
