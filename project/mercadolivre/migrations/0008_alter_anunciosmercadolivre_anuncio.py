# Generated by Django 3.2.20 on 2024-01-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadolivre', '0007_anunciosmercadolivre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anunciosmercadolivre',
            name='anuncio',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Anuncio'),
        ),
    ]