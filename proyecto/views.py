from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, DeleteView

from .models import Proyecto
from .forms import ProyectoForm


class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = Proyecto.objects.select_related('barrio', 'tipo').order_by('-pk').all()
        return qs


class ProyectoCreateView(FormView):
    template_name = 'proyecto_form.html'
    form_class = ProyectoForm
    success_url = '/proyecto/'

    def form_valid(self, form: Any) -> HttpResponse:
        print(form.cleaned_data)
        return super().form_valid(form)


class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'proyecto_delete_confirmation.html'
    model = Proyecto
    success_url = '/proyecto/'


def asigancion_materiales(request: HttpRequest):
    return render(request, 'materiales.html')


def reportes(request: HttpRequest):
    return render(request, 'reportes.html')
