# Generated by Django 3.2.20 on 2024-01-08 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadolivre', '0005_contasmercadolivre_refresh_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensagensMercadoLivre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.IntegerField(blank=True, null=True, verbose_name='identificador')),
                ('user_id', models.IntegerField(blank=True, null=True, verbose_name='user_id')),
                ('text', models.TextField(blank=True, max_length=254, null=True, verbose_name='Texto')),
                ('received', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PacksMercadoLivre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.IntegerField(blank=True, null=True, verbose_name='url')),
            ],
        ),
    ]
