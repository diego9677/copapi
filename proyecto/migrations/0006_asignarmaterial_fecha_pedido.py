# Generated by Django 5.0 on 2023-12-13 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0005_alter_material_proyectos'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignarmaterial',
            name='fecha_pedido',
            field=models.DateTimeField(null=True, verbose_name='Fehca pedido'),
        ),
    ]
