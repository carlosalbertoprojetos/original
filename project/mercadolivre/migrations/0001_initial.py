# Generated by Django 3.2.20 on 2023-10-02 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContasMercadoLivre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(blank=True, null=True, verbose_name='id')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-MAIL')),
                ('first_name', models.CharField(blank=True, max_length=254, null=True, verbose_name='Primeiro Nome')),
                ('access_token', models.CharField(blank=True, max_length=254, null=True, verbose_name='Access Token')),
                ('last_name', models.CharField(blank=True, max_length=254, null=True, verbose_name='Expires IN')),
            ],
        ),
    ]