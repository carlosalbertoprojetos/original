# Generated by Django 3.2.20 on 2023-11-10 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0031_venda_status_expedicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='status_expedicao',
            field=models.CharField(blank=True, default='Parado', max_length=60, null=True),
        ),
    ]
