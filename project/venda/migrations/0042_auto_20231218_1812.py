# Generated by Django 3.2.20 on 2023-12-18 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venda", "0041_venda_urgente"),
    ]

    operations = [
        migrations.AddField(
            model_name="venda",
            name="comentario",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="venda",
            name="status_venda",
            field=models.CharField(
                choices=[
                    ("orcamento", "Orçamento"),
                    ("autorizado", "Autorizado"),
                    ("emproducao", "Em Produção"),
                    ("expedicao", "Expedição"),
                    ("nfemitida", "Nota Fiscal Emitida"),
                    ("enviado", "Enviado"),
                    ("cancelado", "Cancelado"),
                ],
                max_length=50,
            ),
        ),
    ]