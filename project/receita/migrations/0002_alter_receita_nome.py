# Generated by Django 3.2.20 on 2023-08-11 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receita', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receita',
            name='nome',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
