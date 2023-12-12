from django.urls import path
from .views import ProyectoListView, asigancion_materiales, reportes, ProyectoCreateView

urlpatterns = [
    path('', ProyectoListView.as_view(), name='proyectos'),
    path('create/', ProyectoCreateView.as_view(), name='proyecto-create'),
    path('update/<int:pk>/', ProyectoCreateView.as_view(), name='proyecto-update'),
    path('delete/<int:pk>/', ProyectoCreateView.as_view(), name='proyecto-delete'),
    path('materiales/', asigancion_materiales, name='materiales'),
    path('reportes/', reportes, name='reportes'),
]
