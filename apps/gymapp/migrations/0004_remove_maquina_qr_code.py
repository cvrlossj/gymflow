# Generated by Django 4.2.3 on 2023-10-24 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0003_tipousuario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maquina',
            name='qr_code',
        ),
    ]