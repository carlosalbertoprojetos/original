# Generated by Django 3.2.20 on 2024-02-02 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesa', '0005_alter_despesa_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesa',
            name='comprovante',
            field=models.FileField(blank=True, null=True, upload_to='comprovante/despesa/'),
        ),
    ]