# Generated by Django 3.2.20 on 2023-11-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0007_merge_0006_auto_20231008_1743_0006_auto_20231012_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='natureza_operacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]