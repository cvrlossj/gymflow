# Generated by Django 4.2.3 on 2023-11-22 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0006_entrenador_foto_perfil_entrenador_precio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maquina',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='imagenesMaquina'),
        ),
    ]
