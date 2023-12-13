from django.urls import path
from .views import (
    ProyectoListView,
    requerimientos_materiales,
    envio_materiales,
    registro_materiales,
    reportes,
    ProyectoCreateView,
    ProyectoUpdateView,
    ProyectoDeleteView,
    ProyectoDetailView,
    ProyectoEnvioDetailView,
    actulizar_envio_materiales
)

urlpatterns = [
    path('', ProyectoListView.as_view(), name='proyectos'),
    path('create/', ProyectoCreateView.as_view(), name='proyecto-create'),
    path('update/<int:pk>/', ProyectoUpdateView.as_view(), name='proyecto-update'),
    path('delete/<int:pk>/', ProyectoDeleteView.as_view(), name='proyecto-delete'),
    path('detail/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto-detail'),
    path('envio/<int:pk>/', ProyectoEnvioDetailView.as_view(), name='proyecto-envio-detail'),
    path('materiales/', requerimientos_materiales, name='materiales'),
    path('envios/', envio_materiales, name='envios'),
    path('registro/materiales/<int:proyecto_id>/', registro_materiales, name='registro-materiales'),
    path('registro/envio/<int:proyecto_id>/', actulizar_envio_materiales, name='envio-materiales'),
    path('reportes/', reportes, name='reportes'),
]
