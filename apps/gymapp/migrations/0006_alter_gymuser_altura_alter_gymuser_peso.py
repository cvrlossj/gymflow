# Generated by Django 4.2.3 on 2023-10-24 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0005_alter_gymuser_altura_alter_gymuser_peso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymuser',
            name='altura',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='gymuser',
            name='peso',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]