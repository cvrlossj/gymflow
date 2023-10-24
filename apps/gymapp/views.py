from django.shortcuts import render, redirect
from .models import *


# Create your views here.


# Inicio de la página
def cargarInicio(request):
    return render(request, "inicio.html")




# Maquinas
def cargarListaMaquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, "listaMaquinas.html", {"maq": maquinas})


def agregarMaquina(request):
    m_nombre = request.POST['txtMaquina']
    m_zona_muscular = request.POST['txtZona']
    m_descripcion = request.POST['txtDesc']
    m_enlace = request.POST['txtEnlace']

    Maquina.objects.create(nombre=m_nombre, zona_muscular=m_zona_muscular,
                           descripcion=m_descripcion, enlace_tutorial=m_enlace)

    return redirect('/maquinas')


def cargarAgregarMaquina(request):
    return render(request, "agregarMaquina.html")


def cargarEditarMaquina(request, id):
    maquinas = Maquina.objects.get(id=id)
    return render(request, "editarMaquina.html", {"maq": maquinas})


def editarMaquina(request):
    m_id = request.POST['txtId']
    maquinaBD = Maquina.objects.get(id=m_id)
    m_nombre = request.POST['txtMaquina']
    m_zona_muscular = request.POST['txtZona']
    m_descripcion = request.POST['txtDesc']
    m_enlace = request.POST['txtEnlace']

    maquinaBD.nombre = m_nombre
    maquinaBD.zona_muscular = m_zona_muscular
    maquinaBD.descripcion = m_descripcion
    maquinaBD.enlace_tutorial = m_enlace

    maquinaBD.save()

    return redirect('/maquinas')


def eliminarMaquina(request, id):
    maquina = Maquina.objects.get(id=id)
    maquina.delete()
    return redirect('/maquinas')


# Perfil GymEspacio

def cargarPerfilGymEspacio(request):
    return render(request, "perfilGymEspacio.html")


# Entrenadores

def cargarEntrenadores(request):
    entrenadores = Entrenador.objects.all()
    return render(request, "listaEntrenadores.html", {"ent": entrenadores})



# Agregar - Entrenador
def cargarAgregarEntrenadores(request):
    gimnasio = GymEspacio.objects.all()
    return render(request,"agregarEntrenador.html", {"gim": gimnasio})


def agregarEntrenador(request):
    e_nombre = request.POST['txtEntrenador']
    e_apellido = request.POST['txtApellido']
    e_gimnasio_id = request.POST['cmbGim']  # Obtén el ID del gimnasio como un número entero.
    e_servicios = request.POST['txtServicio']
    e_correo = request.POST['txtCorreo']
    e_contrasenia = request.POST['txtPassword']

    gimnasio = GymEspacio.objects.get(id=e_gimnasio_id)

    Entrenador.objects.create(nombre=e_nombre, apellido=e_apellido, id_gymespacio=gimnasio, servicios=e_servicios, correo=e_correo, contrasenia=e_contrasenia)

    return redirect('/entrenadores')


# Editar - Entrenador
def cargarEditarEntrenador(request, id):
    entrenador = Entrenador.objects.get(id=id)
    gimnasio = GymEspacio.objects.all()
    return render(request, "editarEntrenador.html",{"ent": entrenador, "gim": gimnasio})



def eliminarEntrenador(request, id):
    entrenador = Entrenador.objects.get(id=id)
    entrenador.delete()
    return redirect('/entrenadores')

