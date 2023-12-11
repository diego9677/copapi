# Generated by Django 5.0 on 2023-12-11 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsignarMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_necesaria', models.IntegerField(verbose_name='Cantidad Necesaria')),
                ('cantidad_enviada', models.IntegerField(verbose_name='Cantidad Enviada')),
                ('fecha_envio', models.DateTimeField(verbose_name='Fecha Envio')),
            ],
        ),
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
                ('servicio_agua', models.BooleanField(default=False, verbose_name='Servicio Agua')),
                ('servicio_alcantarillado', models.BooleanField(default=False, verbose_name='Servicio Alcantarillado')),
                ('poblacion', models.IntegerField(verbose_name='Poblacion')),
                ('area', models.FloatField(verbose_name='Area')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('recp', 'Recepcion')], max_length=10, verbose_name='Rol')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Precio')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha Fin')),
                ('estado', models.PositiveIntegerField(choices=[(1, 'Preparado'), (2, 'Aprobado'), (3, 'En Curso'), (4, 'Terminado'), (5, 'Cancelado')], verbose_name='estado')),
            ],
        ),
        migrations.CreateModel(
            name='TipoProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripcion')),
            ],
        ),
    ]
