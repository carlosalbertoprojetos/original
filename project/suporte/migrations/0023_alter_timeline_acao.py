# Generated by Django 3.2 on 2024-04-12 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suporte', '0022_auto_20240410_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='acao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='suporte.acoes'),
        ),
    ]