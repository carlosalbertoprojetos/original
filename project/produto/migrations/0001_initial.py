# Generated by Django 4.1.7 on 2023-05-09 18:37

from django.db import migrations, models
import django.db.models.deletion
import produto.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("materiaprima", "0001_initial"),
    ]

    operations = [
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
                ("unidade", models.CharField(max_length=10, verbose_name="UN")),
                ("descricao", models.TextField(blank=True, verbose_name="DESCRIÇÃO")),
            ],
            options={
                "verbose_name": "UNIDADE DE MEDIDA",
                "verbose_name_plural": "UNIDADES DE MEDIDA",
            },
        ),
        migrations.CreateModel(
            name="Produto",
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
                    "ncm",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        validators=[produto.models.validate_campos],
                    ),
                ),
                (
                    "cst",
                    models.CharField(
                        blank=True,
                        default=0,
                        max_length=3,
                        null=True,
                        validators=[produto.models.validate_campos],
                    ),
                ),
                (
                    "cfop",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        null=True,
                        validators=[produto.models.validate_campos],
                    ),
                ),
                (
                    "preco",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
                ),
                ("estoque_ini", models.FloatField(blank=True, default=0, null=True)),
                ("status_produto", models.BooleanField(default=True)),
                ("descricao", models.CharField(blank=True, max_length=255, null=True)),
                ("criadoem", models.DateTimeField(auto_now_add=True)),
                ("atualizadoem", models.DateTimeField(auto_now=True)),
                (
                    "unimed",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="produto.unidademedida",
                        verbose_name="UNIDADE",
                    ),
                ),
            ],
            options={
                "verbose_name": "PRODUTO",
                "verbose_name_plural": "PRODUTOS",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="MateriaPrimaProduto",
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
                    "valor_custo",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=9,
                        null=True,
                        verbose_name="VALOR CUSTO",
                    ),
                ),
                (
                    "qtde_mat_prima",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                        verbose_name="QUANTIDADE",
                    ),
                ),
                ("criadoem", models.DateTimeField(auto_now_add=True)),
                ("atualizadoem", models.DateTimeField(auto_now=True)),
                (
                    "materiaprima",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materiaprima.materiaprima",
                        verbose_name="MATERIA PRIMA",
                    ),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="produto.produto",
                        verbose_name="PRODUTO",
                    ),
                ),
            ],
            options={
                "verbose_name": "MATÉRIA PRIMA PRODUTO",
                "verbose_name_plural": "MATÉRIA PRIMA PRODUTOS",
            },
        ),
    ]