# Generated by Django 3.2.20 on 2023-07-18 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiaprima', '0001_initial'),
        ('produto', '0005_auto_20230718_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiaprimaproduto',
            name='materiaprima',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materiaprima.materiaprima', verbose_name='MATERIA PRIMA'),
        ),
        migrations.RemoveField(
            model_name='materiaprimaproduto',
            name='produto',
        ),
        migrations.CreateModel(
            name='ProdutosMatPri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.materiaprimaproduto')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.produto')),
            ],
        ),
        migrations.AddField(
            model_name='materiaprimaproduto',
            name='produto',
            field=models.ManyToManyField(blank=True, through='produto.ProdutosMatPri', to='produto.Produto'),
        ),
    ]