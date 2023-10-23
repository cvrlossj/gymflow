from django.urls import path
from . import views

urlpatterns = [
    path('',views.cargarInicio),
    path('lista',views.cargarListaMaquinas),
    path('agregarmaquina',views.cargarAgregarMaquina),
    path('agregarMaquinaForm',views.agregarMaquina),
    path('editarMaquina/<id>',views.cargarEditarMaquina),
    path('editarMaquinaForm',views.editarMaquina),
    path('eliminarMaquina/<id>', views.eliminarMaquina),
]
