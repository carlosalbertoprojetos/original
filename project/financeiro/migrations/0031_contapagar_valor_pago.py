# Generated by Django 3.2.20 on 2024-03-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0030_contareceber_valor_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='contapagar',
            name='valor_pago',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
