# Generated by Django 3.2.20 on 2023-10-12 11:38

from django.db import migrations
import django_cpf_cnpj.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedor', '0006_merge_0005_auto_20230920_2257_0005_auto_20230921_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedor',
            name='cnpj',
            field=django_cpf_cnpj.fields.CNPJField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='cpf',
            field=django_cpf_cnpj.fields.CPFField(blank=True, max_length=14, null=True),
        ),
    ]