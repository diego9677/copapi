from django import forms
from .models import TipoProyecto, Empleado, Proyecto


class ProyectoForm(forms.Form):
    tipo = forms.ModelChoiceField(
        queryset=TipoProyecto.objects.order_by('pk').all(),
        label='Tipo',
    )
    nombre = forms.CharField(
        max_length=200,
        label='Nombre',
    )
    barrio = forms.CharField(max_length=200, label='Barrio')
    poblacion = forms.IntegerField(label='Poblacion')
    area = forms.FloatField(label='Area', widget=forms.TextInput(attrs={'type': 'number', 'step': '0.1'}))
    fecha_inicio = forms.DateField(label='Fecha Inicio', widget=forms.TextInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(label='Fecha Fin', widget=forms.TextInput(attrs={'type': 'date'}))
    empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.order_by('pk').all(),
        widget=forms.CheckboxSelectMultiple
    )


class ReportPryectoForm(forms.Form):
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.order_by('pk').all(),
        label='Proyecto',
        required=False,
    )
