# Generated by Django 4.1.7 on 2023-05-24 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venda", "0007_delete_limiteproducaodiaria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendaproduto",
            name="quantidade",
            field=models.IntegerField(default=1),
        ),
    ]
