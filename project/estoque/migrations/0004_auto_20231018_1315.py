# Generated by Django 3.2.20 on 2023-10-18 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producao', '0019_alter_limiteproducaodiaria_quantidade'),
        ('estoque', '0003_alter_estoquemateriaprima_enderecoestoque'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conferenciaestoque',
            old_name='produto',
            new_name='materiaprima',
        ),
        migrations.AlterField(
            model_name='estoqueprodutoacabado',
            name='produtoacabado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='producao.produtoacabado'),
        ),
        migrations.DeleteModel(
            name='ProdutoAcabado',
        ),
    ]