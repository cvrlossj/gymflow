# Generated by Django 4.2.3 on 2023-11-21 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0003_remove_maquina_id_zonamuscular_delete_zonamuscular'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='imagen',
            field=models.ImageField(default=0, upload_to='imagenesMaquina'),
            preserve_default=False,
        ),
    ]