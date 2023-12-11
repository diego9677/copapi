from django.db import models

ROLES = (
    ('admin', 'Administrador'),
    ('recp', 'Recepcion'),

)

ESTADOS = (
    (1, 'Preparado'),
    (2, 'Aprobado'),
    (3, 'En Curso'),
    (4, 'Terminado'),
    (5, 'Cancelado'),
)


class Barrio(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    servicio_agua = models.BooleanField(default=False, verbose_name='Servicio Agua')
    servicio_alcantarillado = models.BooleanField(default=False, verbose_name='Servicio Alcantarillado')
    poblacion = models.IntegerField(verbose_name='Poblacion')
    area = models.FloatField(verbose_name='Area')

    def __str__(self) -> str:
        return self.nombre


class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripcion')

    def __str__(self) -> str:
        return self.nombre


class Empleado(models.Model):
    persona = models.ForeignKey('transporte.Persona', related_name='empleados', on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, verbose_name='Rol')

    def __str__(self) -> str:
        return f'{self.persona.nombres} {self.rol}'


class Proyecto(models.Model):
    tipo = models.ForeignKey(TipoProyecto, related_name='proyectos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    fecha_inicio = models.DateField(verbose_name='Fecha Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha Fin')
    estado = models.PositiveIntegerField(choices=ESTADOS, verbose_name='estado')
    empleados = models.ManyToManyField(Empleado, related_name='proyectos')

    def __str__(self) -> str:
        return self.nombre


class Material(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    precio = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio')
    proyectos = models.ManyToManyField(Proyecto, through='AsignarMaterial', through_fields=('material', 'proyecto'))

    def __str__(self) -> str:
        return self.nombre


class AsignarMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cantidad_necesaria = models.IntegerField(verbose_name='Cantidad Necesaria')
    cantidad_enviada = models.IntegerField(verbose_name='Cantidad Enviada')
    fecha_envio = models.DateTimeField(verbose_name='Fecha Envio')

    def __str__(self) -> str:
        return str(self.pk)
