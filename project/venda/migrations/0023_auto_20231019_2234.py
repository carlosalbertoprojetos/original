# Generated by Django 3.2.20 on 2023-10-20 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0022_remove_venda_notafiscal'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='chave',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='motivo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='status',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='uuid',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
