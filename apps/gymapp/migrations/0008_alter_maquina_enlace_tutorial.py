# Generated by Django 4.2.3 on 2023-11-22 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0007_alter_maquina_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maquina',
            name='enlace_tutorial',
            field=models.URLField(blank=True, null=True),
        ),
    ]