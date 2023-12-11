from django.contrib import admin

from .models import Chofer, Persona, Marca, Modelo, Vehiculo, Viaje


@admin.register(Chofer)
class ChoferAdmin(admin.ModelAdmin):
    list_display = ('pk', 'licencia')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ci', 'nombres', 'apellidos')


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre')


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre')


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'placa')


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_programada', 'fecha_ejecutada', 'estado')
