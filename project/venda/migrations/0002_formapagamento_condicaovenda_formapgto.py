# Generated by Django 4.1.7 on 2023-05-09 19:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("venda", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormaPagamento",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(max_length=255, verbose_name="Forma de Pagamento"),
                ),
                ("descricao", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="condicaovenda",
            name="formapgto",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.RESTRICT,
                to="venda.formapagamento",
            ),
            preserve_default=False,
        ),
    ]