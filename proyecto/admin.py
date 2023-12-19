from django.contrib import admin
from .models import Barrio, Material, TipoProyecto, Proyecto, AsignarMaterial


@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'servicio_agua', 'servicio_alcantarillado')


# @admin.register(Empleado)
# class EmpleadoAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'rol')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'cantidad', 'precio')


@admin.register(TipoProyecto)
class TipoProyectoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'descripcion')


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado')


@admin.register(AsignarMaterial)
class AsignarMaterialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cantidad_necesaria', 'cantidad_enviada', 'fecha_envio')
