from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def cargarInicio(request):
    return render(request, "inicio.html")


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

    return redirect('/lista')


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
    maquinaBD.enlace = m_enlace

    maquinaBD.save()

    return redirect('/lista')


def eliminarMaquina(request, id):
    maquina = Maquina.objects.get(id=id)
    maquina.delete()
    return redirect('/lista')


def cargarPerfilGymEspacio(request):
    return render(request, "perfilGymEspacio.html")


def cargarEntrenadores(request):
    entrenadores = Entrenador.objects.all()
    return render(request, "listaEntrenadores.html", {"ent": entrenadores})
