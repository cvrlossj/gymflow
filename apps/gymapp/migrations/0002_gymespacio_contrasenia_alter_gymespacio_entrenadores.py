# Generated by Django 4.2.3 on 2023-10-23 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymespacio',
            name='contrasenia',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gymespacio',
            name='entrenadores',
            field=models.ManyToManyField(null=True, related_name='gimnasios', to='gymapp.entrenador'),
        ),
    ]
