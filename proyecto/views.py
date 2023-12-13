from typing import Any
from django.utils import timezone
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, FormView, DetailView

from .models import Proyecto, Barrio, Material, AsignarMaterial
from .forms import ProyectoForm, ReportPryectoForm


class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos.html'

    def get_queryset(self) -> QuerySet[Any]:
        search = self.request.GET.get('search', '')
        qs = Proyecto.objects.select_related('barrio', 'tipo').order_by('-pk').filter(
            Q(nombre__icontains=search) | Q(barrio__nombre__icontains=search) |
            Q(tipo__nombre__icontains=search)
        ).all()
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
        proyecto = Proyecto.objects.create(
            tipo=form.cleaned_data['tipo'],
            nombre=form.cleaned_data['nombre'],
            fecha_inicio=form.cleaned_data['fecha_inicio'],
            fecha_fin=form.cleaned_data['fecha_fin'],
            barrio=barrio,
            estado=1,
        )

        proyecto.empleados.set(form.cleaned_data['empleados'])
        proyecto.save()

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
        obj = Proyecto.objects.select_related('tipo', 'barrio').prefetch_related('empleados').get(pk=self.kwargs['pk'])
        initial.update({
            'tipo': obj.tipo,
            'nombre': obj.nombre,
            'barrio': obj.barrio.nombre,
            'poblacion': obj.barrio.poblacion,
            'area': obj.barrio.area,
            'fecha_inicio': obj.fecha_inicio,
            'fecha_fin': obj.fecha_fin,
            'empleados': obj.empleados.all()
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
        obj.empleados.set(form.cleaned_data['empleados'])
        obj.barrio.save()
        obj.save()
        return super().form_valid(form)


class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'proyecto_delete_confirmation.html'
    model = Proyecto
    success_url = '/proyecto/'


@login_required
def requerimientos_materiales(request: HttpRequest):
    context = {}
    search = request.GET.get('search', '')
    context['proyectos'] = Proyecto.objects.select_related('tipo', 'barrio').filter(
        Q(nombre__icontains=search) | Q(barrio__nombre__icontains=search) |
        Q(tipo__nombre__icontains=search)
    ).all()
    context['valid_statuses'] = [1, 2]
    return render(request, 'materiales.html', context)


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'proyecto_detalle.html'
    model = Proyecto

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['materiales'] = Material.objects.order_by('pk').all()
        return context


@login_required
def registro_materiales(request: HttpRequest, proyecto_id: int):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    data = request.POST.copy().dict()
    data.pop('csrfmiddlewaretoken')
    for k, v in data.items():
        if v != '':
            AsignarMaterial.objects.create(
                proyecto=proyecto,
                material_id=int(k),
                cantidad_necesaria=int(v),
                fecha_pedido=timezone.now(),
            )
    proyecto.estado = 2
    proyecto.save()
    return redirect(reverse_lazy('materiales'))


@login_required
def reportes(request: HttpRequest):
    context = {}
    form = ReportPryectoForm(data=request.GET, initial={'proyecto': request.GET.get('proyecto')})
    if form.is_valid():
        if form.cleaned_data['proyecto'] is not None:

            try:
                proyecto = Proyecto.objects.select_related('tipo', 'barrio').get(pk=form.cleaned_data['proyecto'].pk)
                asigancion = AsignarMaterial.objects.select_related('material').filter(proyecto=proyecto)
                context['proyecto'] = proyecto
                context['asignaciones'] = asigancion
            except Proyecto.DoesNotExist:
                pass

    context['form'] = form
    return render(request, 'reportes.html', context)


@login_required
def envio_materiales(request: HttpRequest):
    context = {}
    search = request.GET.get('search', '')
    context['proyectos'] = Proyecto.objects.select_related('tipo', 'barrio').filter(
        Q(nombre__icontains=search) | Q(barrio__nombre__icontains=search) |
        Q(tipo__nombre__icontains=search)
    ).all()
    context['valid_statuses'] = [1, 2]
    return render(request, 'envio_materiales.html', context)


class ProyectoEnvioDetailView(LoginRequiredMixin, DetailView):
    template_name = 'proyecto_envio_detalle.html'
    model = Proyecto

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        asignaciones = AsignarMaterial.objects.select_related('material').filter(proyecto_id=self.kwargs['pk'], fecha_envio__isnull=True).all()
        context['asignaciones'] = asignaciones
        return context


@login_required
def actulizar_envio_materiales(request: HttpRequest, proyecto_id: int):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    data = request.POST.copy().dict()
    data.pop('csrfmiddlewaretoken')
    for k, v in data.items():

        if v == '':
            messages.error(request, "Debe ingresar datos")
            return redirect(reverse_lazy('proyecto-envio-detail', kwargs={'pk': proyecto_id}))

        material = Material.objects.get(pk=int(k))
        asignacion = AsignarMaterial.objects.filter(
            proyecto=proyecto,
            material=material,
            fecha_envio__isnull=True,
        ).first()

        if int(v) > asignacion.cantidad_necesaria:
            messages.error(request, f"Solo necesita {asignacion.cantidad_necesaria} Unidades de {material.nombre}")
            return redirect(reverse_lazy('proyecto-envio-detail', kwargs={'pk': proyecto_id}))

        if int(v) > material.cantidad:
            messages.error(request, f"Stock insuficiente {material.nombre}: pedido {asignacion.cantidad_necesaria} U y actualmente cuenta con {material.cantidad} U en stock")
            return redirect(reverse_lazy('proyecto-envio-detail', kwargs={'pk': proyecto_id}))

        asignacion.fecha_envio = timezone.now()
        asignacion.cantidad_enviada = int(v)
        material.cantidad -= int(v)

        asignacion.save()
        material.save()

    proyecto.estado = 2
    proyecto.save()
    return redirect(reverse_lazy('envios'))
