# Generated by Django 4.1.7 on 2023-05-24 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venda", "0005_alter_venda_cliente"),
    ]

    operations = [
        migrations.CreateModel(
            name="LimiteProducaoDiaria",
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
                ("qtde", models.IntegerField(default=10)),
            ],
        ),
    ]