# Generated by Django 3.2.20 on 2023-09-30 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0025_contareceber_dados_boleto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contareceber',
            name='dados_boleto',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
