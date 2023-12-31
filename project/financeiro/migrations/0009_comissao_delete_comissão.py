# Generated by Django 4.1.7 on 2023-06-30 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0008_comissão"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comissao",
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
                ("pgto", models.BooleanField(null=True)),
                ("data_comissao", models.DateField(null=True)),
                (
                    "parcela",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="financeiro.contareceber",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comissão",
                "verbose_name_plural": "Comissões",
            },
        ),
        migrations.DeleteModel(
            name="Comissão",
        ),
    ]
