# Generated by Django 4.1.7 on 2023-05-09 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("fornecedor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MateriaPrima",
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
                ("nome", models.CharField(max_length=255)),
                ("descricao", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "verbose_name": "Materia Prima",
                "verbose_name_plural": "Materias Primas",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="UnidadeMedida",
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
                ("nome", models.CharField(max_length=255, verbose_name="Nome")),
                (
                    "descricao",
                    models.CharField(max_length=20, verbose_name="Descricao"),
                ),
            ],
            options={
                "verbose_name": "Unidade de Medida",
                "verbose_name_plural": "Unidades de Medidas",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="MateriaPrimaFornecedor",
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
                ("codigoproduto", models.CharField(max_length=255)),
                ("nome", models.CharField(max_length=255)),
                (
                    "fornecedor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="fornecedor.fornecedor",
                    ),
                ),
                (
                    "materiaprima",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="materiaprima.materiaprima",
                    ),
                ),
            ],
            options={
                "verbose_name": "Fornecedor de Materia Prima",
                "verbose_name_plural": "Fornecedor de Materias Prima",
                "ordering": ["nome"],
            },
        ),
        migrations.AddField(
            model_name="materiaprima",
            name="uni_med",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to="materiaprima.unidademedida",
            ),
        ),
    ]