# Generated by Django 4.2.3 on 2023-11-19 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0002_zonamuscular_maquina_id_zonamuscular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maquina',
            name='id_zonamuscular',
        ),
        migrations.DeleteModel(
            name='ZonaMuscular',
        ),
    ]
