# Generated by Django 5.1.3 on 2025-01-02 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_diaservicio_asistencia_servicio_diaservicio_servicio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asistencia',
            old_name='presente',
            new_name='aseo',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='servicio',
            field=models.BooleanField(default=False),
        ),
    ]
