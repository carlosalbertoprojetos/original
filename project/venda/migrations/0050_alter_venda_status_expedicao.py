# Generated by Django 3.2.20 on 2024-03-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0049_rename_data_impresssao_venda_data_impressao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='status_expedicao',
            field=models.CharField(blank=True, default='Aguardando Concluir Produtos', max_length=60, null=True),
        ),
    ]