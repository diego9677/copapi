from django.db import models


GENEROS = (
    ('M', 'Masculino'),
    ('F', 'Femenino')
)

CITIES = (
    ('scz', 'Santa Cruz'),
    ('lp', 'La Paz'),
    ('cbba', 'Cochabamba'),
    ('or', 'Oruro'),
    ('pt', 'Potosi'),
    ('bn', 'Beni'),
    ('pa', 'Pando'),
    ('ch', 'Chuquisaca'),
    ('tj', 'Tarija')
)

ESTADOS = (
    (1, 'Preparado'),
    (2, 'En curso'),
    (3, 'Finalizado'),
    (4, 'Cancelado'),
)

ROLES = (
    ('recp', 'Recepcion'),
    ('ctr', 'Constructor'),
    ('con', 'Contratista'),
    ('opr', 'Operador')
)


class Marca(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')

    def __str__(self) -> str:
        return self.nombre


class Modelo(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    marca = models.ForeignKey(Marca, related_name='modelos', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre


class Vehiculo(models.Model):
    placa = models.CharField(max_length=50, verbose_name='Placa')
    capacidad_carga = models.FloatField(verbose_name='Capacidad Carga')
    anho = models.CharField(max_length=4, verbose_name='Año')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descipcion')
    modelo = models.ForeignKey(Modelo, related_name='vehiculos', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.placa


class Persona(models.Model):
    ci = models.CharField(max_length=100, unique=True, verbose_name='CI')
    nombres = models.CharField(max_length=200, verbose_name='Nombres')
    apellidos = models.CharField(max_length=200, verbose_name='Apellidos')
    fecha_nacimiento = models.DateField(verbose_name='Fecha Nacimiento')
    email = models.CharField(max_length=200, verbose_name='Email')
    telefono = models.CharField(max_length=50, verbose_name='Telefono')
    genero = models.CharField(max_length=1, choices=GENEROS, verbose_name='Genero')
    ciudad = models.CharField(max_length=4, choices=CITIES, verbose_name='Ciudad')
    rol = models.CharField(null=True, max_length=20, choices=ROLES, verbose_name='Rol')

    def __str__(self) -> str:
        return f'{self.nombres} {self.apellidos}'


# class Chofer(models.Model):
#     persona = models.ForeignKey(Persona, related_name='choferes', on_delete=models.CASCADE)
#     licencia = models.CharField(max_length=100, verbose_name='Licencia')
#     fecha_contrato = models.DateField(verbose_name='Fecha Contrato')

#     def __str__(self) -> str:
#         return self.licencia


class Viaje(models.Model):
    chofer = models.ForeignKey(Persona, related_name='viajes', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, related_name='viajes', on_delete=models.CASCADE)
    proyecto = models.ForeignKey('proyecto.Proyecto', related_name='viajes', on_delete=models.CASCADE)
    fecha_programada = models.DateTimeField(verbose_name='Fecha Programada')
    fecha_ejecutada = models.DateTimeField(verbose_name='Fecha Ejecutada')
    estado = models.IntegerField(choices=ESTADOS, verbose_name='Estado')

    def __str__(self) -> str:
        return f'{self.pk}'
