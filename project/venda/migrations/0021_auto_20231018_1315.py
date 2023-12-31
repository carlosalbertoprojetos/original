# Generated by Django 3.2.20 on 2023-10-18 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0010_auto_20231015_1235'),
        ('produto', '0014_auto_20231018_1315'),
        ('venda', '0020_venda_notafiscal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendaproduto',
            options={},
        ),
        migrations.AlterField(
            model_name='venda',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cliente.cliente'),
        ),
        migrations.AlterField(
            model_name='vendaproduto',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.produto'),
        ),
    ]
