from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargarInicio),
    path('login', views.cargarLogin),

    # Maquina
    path('maquinas', views.cargarListaMaquinas),
    # Listar 
    path('list_maquinas/',views.list_maquinas),
    path('agregarMaquinaForm', views.agregarMaquina),
    path('editarMaquina/<id>', views.cargarEditarMaquina),
    path('editarMaquinaForm', views.editarMaquina),
    path('eliminarMaquina/<id>', views.eliminarMaquina),
    # Final Maquina

    # Configuración - GymEspacio
    path('configuracion', views.cargarPerfilGymEspacio),

    # Entrenador
    path('entrenadores', views.cargarEntrenadores),
    path('agregarEntrenadorForm', views.agregarEntrenador),
    path('editarEntrenador/<id>', views.cargarEditarEntrenador),
    path('editarEntrenadorForm', views.editarEntrenador),
    path('eliminarEntrenador/<id>', views.eliminarEntrenador),

    # Inicar sesión 
    path('accederUser', views.cargarAccederUser),
    path('iniciarSesionFormUser',views.iniciarSesion),

    # Cerrar sesión
    path('cerrar-sesion/',views.cerrarSesion, name='cerrarSesion'),


    # GymUser
    path('maquina/<id>', views.cargarDetalleMaquina)
    
]
