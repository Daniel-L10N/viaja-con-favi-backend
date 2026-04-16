# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinos', '0004_alter_destino_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonio',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='testimonios/'),
        ),
    ]
