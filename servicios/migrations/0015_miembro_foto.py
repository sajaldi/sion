# Generated by Django 5.1.3 on 2025-01-02 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0014_miembro_direccion_miembro_fecha_de_nacimiento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='foto',
            field=models.ImageField(default=1, upload_to=None),
            preserve_default=False,
        ),
    ]
