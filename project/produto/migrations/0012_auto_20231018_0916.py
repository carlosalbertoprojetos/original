# Generated by Django 3.2.20 on 2023-10-18 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0011_produto_peso'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materiaprimaproduto',
            options={'verbose_name': 'PRODUTO POR MATÉRIA PRIMA', 'verbose_name_plural': 'PRODUTOS POR MATÉRIAS PRIMAS'},
        ),
        migrations.AlterModelOptions(
            name='produtosmatpri',
            options={'verbose_name': 'QUANTIDADE DE MATÉRIA PRIMA POR PRODUTO'},
        ),
        migrations.AlterField(
            model_name='produtosmatpri',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.produto', verbose_name='Produto'),
        ),
        migrations.AlterField(
            model_name='produtosmatpri',
            name='quant',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='Quantidade'),
        ),
    ]