# Generated by Django 4.1.7 on 2023-06-28 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0007_alter_contareceber_parcela"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comissão",
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
                    "comissao",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("pgto", models.BooleanField()),
                ("data_comissao", models.DateField(null=True)),
                (
                    "parcela",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="financeiro.contareceber",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comissão",
                "verbose_name_plural": "Comissões",
            },
        ),
    ]
