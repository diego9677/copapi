from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, FormView

from .models import Proyecto, Barrio
from .forms import ProyectoForm


class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = Proyecto.objects.select_related('barrio', 'tipo').order_by('-pk').all()
        return qs


class ProyectoCreateView(LoginRequiredMixin, FormView):
    template_name = 'proyecto_form.html'
    form_class = ProyectoForm
    success_url = '/proyecto/'

    def form_valid(self, form: ProyectoForm) -> HttpResponse:
        print(form.cleaned_data)
        barrio = Barrio.objects.create(
            nombre=form.cleaned_data['barrio'],
            poblacion=form.cleaned_data['poblacion'],
            area=form.cleaned_data['area'],
        )
        Proyecto.objects.create(
            tipo=form.cleaned_data['tipo'],
            nombre=form.cleaned_data['nombre'],
            fecha_inicio=form.cleaned_data['fecha_inicio'],
            fecha_fin=form.cleaned_data['fecha_fin'],
            barrio=barrio,
            estado=1,
        )

        return super().form_valid(form)


class ProyectoUpdateView(LoginRequiredMixin, FormView):
    template_name = 'proyecto_form.html'
    form_class = ProyectoForm
    success_url = '/proyecto/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['object'] = Proyecto.objects.select_related('tipo', 'barrio').get(pk=self.kwargs['pk'])
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        obj = Proyecto.objects.select_related('tipo', 'barrio').get(pk=self.kwargs['pk'])
        initial.update({
            'tipo': obj.tipo,
            'nombre': obj.nombre,
            'barrio': obj.barrio.nombre,
            'poblacion': obj.barrio.poblacion,
            'area': obj.barrio.area,
            'fecha_inicio': obj.fecha_inicio,
            'fecha_fin': obj.fecha_fin,
        })
        return initial

    def form_valid(self, form: ProyectoForm) -> HttpResponse:
        obj = Proyecto.objects.select_related('tipo', 'barrio').get(pk=self.kwargs['pk'])
        obj.tipo = form.cleaned_data['tipo']
        obj.nombre = form.cleaned_data['nombre']
        obj.barrio.nombre = form.cleaned_data['barrio']
        obj.barrio.poblacion = form.cleaned_data['poblacion']
        obj.barrio.area = form.cleaned_data['area']
        obj.fecha_inicio = form.cleaned_data['fecha_inicio']
        obj.fecha_fin = form.cleaned_data['fecha_fin']
        obj.barrio.save()
        obj.save()
        return super().form_valid(form)


class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'proyecto_delete_confirmation.html'
    model = Proyecto
    success_url = '/proyecto/'


def asigancion_materiales(request: HttpRequest):
    return render(request, 'materiales.html')


def reportes(request: HttpRequest):
    return render(request, 'reportes.html')
