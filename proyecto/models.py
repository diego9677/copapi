from django.db import models

ESTADOS = (
    (1, 'Aprobado'),
    (2, 'En Curso'),
    (3, 'Terminado'),
    (4, 'Cancelado'),
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


# class Empleado(models.Model):
#     persona = models.OneToOneField('transporte.Persona', related_name='empleados', on_delete=models.CASCADE)


#     def __str__(self) -> str:
#         return self.persona.nombres


class Proyecto(models.Model):
    tipo = models.ForeignKey(TipoProyecto, related_name='proyectos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    fecha_inicio = models.DateField(verbose_name='Fecha Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha Fin')
    estado = models.PositiveIntegerField(choices=ESTADOS, verbose_name='estado')
    barrio = models.ForeignKey(Barrio, null=True, blank=True, related_name='proyectos', on_delete=models.CASCADE)
    empleados = models.ManyToManyField('transporte.Persona', related_name='proyectos')

    def __str__(self) -> str:
        return self.nombre


class Material(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    precio = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio')
    proyectos = models.ManyToManyField(Proyecto, related_name='materiales', through='AsignarMaterial', through_fields=('material', 'proyecto'))

    def __str__(self) -> str:
        return self.nombre


class AsignarMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cantidad_necesaria = models.IntegerField(verbose_name='Cantidad Necesaria')
    cantidad_enviada = models.IntegerField(null=True, verbose_name='Cantidad Enviada')
    fecha_pedido = models.DateTimeField(null=True, verbose_name='Fehca pedido')
    fecha_envio = models.DateTimeField(null=True, verbose_name='Fecha Envio')

    def __str__(self) -> str:
        return str(self.pk)


class Comentario(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='comentarios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    texto = models.TextField(verbose_name='Texto')
    puntuacion = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.nombre
