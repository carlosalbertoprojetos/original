# Generated by Django 3.2.20 on 2023-10-26 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("produto", "0020_auto_20231026_1415"),
    ]

    operations = [
        migrations.AddField(
            model_name="peca",
            name="quantidade",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name="produtomatpri",
            name="produto",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="produto.produto",
            ),
        ),
        migrations.AlterField(
            model_name="produtomatpri",
            name="quantidade",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=10, null=True
            ),
        ),
    ]
