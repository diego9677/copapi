from django import forms
from .models import TipoProyecto, Proyecto
from transporte.models import Persona


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
        queryset=Persona.objects.order_by('pk').all(),
        widget=forms.CheckboxSelectMultiple
    )


class ReportPryectoForm(forms.Form):
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.order_by('pk').all(),
        label='Proyecto',
        required=False,
    )


class CommentForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=200)
    comentario = forms.CharField(label='Comentario', widget=forms.Textarea(attrs={'rows': 2, 'cols': 10}))
