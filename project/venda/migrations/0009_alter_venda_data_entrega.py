# Generated by Django 4.1.7 on 2023-05-24 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venda", "0008_alter_vendaproduto_quantidade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venda",
            name="data_entrega",
            field=models.DateField(blank=True, null=True),
        ),
    ]
