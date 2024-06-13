
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0024_produto_cest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peca',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='produto.produto'),
        ),
    ]
