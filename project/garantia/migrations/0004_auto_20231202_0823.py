# Generated by Django 3.2.20 on 2023-12-02 11:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('garantia', '0003_auto_20231202_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garantia',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='garantiatimeline',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]