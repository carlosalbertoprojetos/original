# Generated by Django 4.1.7 on 2023-05-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contapagar",
            name="formapgto",
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name="contareceber",
            name="formapgto",
            field=models.CharField(max_length=300),
        ),
    ]
