# Generated by Django 4.1.7 on 2023-05-09 18:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("despesa", "0001_initial"),
        ("compra", "0001_initial"),
        ("venda", "0001_initial"),
        ("receita", "0001_initial"),
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
        migrations.CreateModel(
            name="ContaReceber",
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
                ("parcela", models.CharField(max_length=11)),
                (
                    "valor",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("datadocumento", models.DateField(default=datetime.date.today)),
                ("datavencimento", models.DateField(verbose_name="Data do vencimento")),
                ("datapagamento", models.DateField(null=True)),
                ("detalhes", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "formapgto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="financeiro.formapagamento",
                    ),
                ),
                (
                    "receita",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="receita.receita",
                    ),
                ),
                (
                    "venda",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="venda.venda",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ContaPagar",
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
                    "valor",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("datadocumento", models.DateField(default=datetime.date.today)),
                ("datavencimento", models.DateField()),
                ("datapagamento", models.DateField(blank=True, null=True)),
                ("detalhes", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "compra",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="compra.compra",
                    ),
                ),
                (
                    "despesa",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="despesa.despesa",
                    ),
                ),
                (
                    "formapgto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="financeiro.formapagamento",
                    ),
                ),
            ],
        ),
    ]