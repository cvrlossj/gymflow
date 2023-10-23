from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def cargarInicio(request):
    return render(request, "inicio.html")


def cargarListaMaquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, "listaMaquinas.html", {"maq": maquinas})