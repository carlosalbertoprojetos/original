# Generated by Django 4.1.7 on 2023-06-06 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("producao", "0004_produtoacabado_hora_produtoacabado_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricoMontagem",
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
                ("hora", models.DateField()),
                ("tempo_gasto_minutos", models.FloatField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("faltandomateriaprima", "Faltando Materia Prima"),
                            ("montagem", "Montagem"),
                            ("eletrica", "Elétrica"),
                            ("refrigeracao", "Refrigeração"),
                            ("acabamento", "Acabamento"),
                            ("estoque", "Estoque"),
                        ],
                        default="montagem",
                        max_length=255,
                    ),
                ),
                (
                    "produtoacabado",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="producao.produtoacabado",
                        verbose_name="PRODUTOACABADO",
                    ),
                ),
            ],
        ),
    ]