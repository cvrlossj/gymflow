# Generated by Django 4.2.3 on 2023-10-24 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0004_remove_maquina_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymuser',
            name='altura',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='gymuser',
            name='peso',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
