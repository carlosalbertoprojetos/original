# Generated by Django 3.2.20 on 2024-03-08 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0046_venda_nfjaimpressa'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='status_posvenda',
            field=models.CharField(blank=True, default='Conferencia Final', max_length=60, null=True),
        ),
    ]