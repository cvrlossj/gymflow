from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *

# CODIGO QR
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO


# Inicio de la página - Iniciar Sesión
def cargarInicio(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "loginUser.html", {"tipoUsuario": tipoUsuario})


# Dashboard
def cargarDashboard(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "dashboard.html", {"tipoUsuario": tipoUsuario})


# Maquinas
def cargarListaMaquinas(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    maquinas = Maquina.objects.all()
    return render(request, "listaMaquinas.html", {"maq": maquinas, "tipoUsuario": tipoUsuario})


def agregarMaquina(request):
    m_nombre = request.POST['txtMaquina']
    m_zona_muscular = request.POST['txtZona']
    m_descripcion = request.POST['txtDesc']
    m_enlace = request.POST['txtEnlace']

    # Genera el código QR basado en el enlace_tutorial
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(m_enlace)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convierte la imagen del código QR en un archivo en memoria
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = ContentFile(buffer.getvalue())

    # Crea el registro de Maquina y asigna el código QR
    maquina = Maquina.objects.create(
        nombre=m_nombre,
        zona_muscular=m_zona_muscular,
        descripcion=m_descripcion,
        enlace_tutorial=m_enlace,
    )

    # Asigna el código QR al campo qr_code de la maquina
    maquina.qr_code.save(f"qr_code_{maquina.id}.png", qr_image, save=True)

    return redirect('/maquinas')


def cargarAgregarMaquina(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "agregarMaquina.html", {"tipoUsuario": tipoUsuario})


def cargarEditarMaquina(request, id):
    tipoUsuario = request.session.get('tipoUsuario', None)
    maquinas = Maquina.objects.get(id=id)
    return render(request, "editarMaquina.html", {"maq": maquinas, "tipoUsuario": tipoUsuario})


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
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "perfilGymEspacio.html", {"tipoUsuario": tipoUsuario})

# Entrenadores


def cargarEntrenadores(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    entrenadores = Entrenador.objects.all()
    return render(request, "listaEntrenadores.html", {"ent": entrenadores, "tipoUsuario": tipoUsuario})


# Agregar - Entrenador
def cargarAgregarEntrenadores(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    gimnasio = GymEspacio.objects.all()
    return render(request, "agregarEntrenador.html", {"gim": gimnasio, "tipoUsuario": tipoUsuario})


def agregarEntrenador(request):
    e_nombre = request.POST['txtEntrenador']
    e_apellido = request.POST['txtApellido']
    # Obtén el ID del gimnasio como un número entero.
    e_gimnasio_id = request.POST['cmbGim']
    e_servicios = request.POST['txtServicio']
    e_correo = request.POST['txtCorreo']
    e_contrasenia = request.POST['txtPassword']

    gimnasio = GymEspacio.objects.get(id=e_gimnasio_id)

    Entrenador.objects.create(nombre=e_nombre, apellido=e_apellido, id_gymespacio=gimnasio,
                              servicios=e_servicios, correo=e_correo, contrasenia=e_contrasenia)

    return redirect('/entrenadores')


# Editar - Entrenador
def cargarEditarEntrenador(request, id):
    entrenador = Entrenador.objects.get(id=id)
    gimnasio = GymEspacio.objects.all()
    return render(request, "editarEntrenador.html", {"ent": entrenador, "gim": gimnasio})


def eliminarEntrenador(request, id):
    entrenador = Entrenador.objects.get(id=id)
    entrenador.delete()
    return redirect('/entrenadores')


# Login de gym user
def cargarAccederUser(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "loginUser.html", {"tipoUsuario": tipoUsuario})


# Iniciar sesión - TODOS LOS ROLES
def iniciarSesion(request):
    if request.method == 'POST':
        correo = request.POST.get('txtCorreo')
        contrasenia = request.POST.get('txtContrasenia')

        usuarios = UsuarioPadre.objects.filter(correo=correo)
        if usuarios.exists():
            usuario = usuarios.first()
            if usuario.contrasenia == contrasenia:
                request.session['tipoUsuario'] = usuario.id_tipo.nombre_tipo
                request.session['usuario_id'] = usuario.id

                if usuario.id_tipo.id_tipo == 1:
                    return redirect('/maquinas')
                elif usuario.id_tipo.id_tipo == 2:
                    return redirect('/maquinas')
                elif usuario.id_tipo.id_tipo == 3:
                    return redirect('/maquinas')
                else:
                    return redirect('/')
            else:
                mensaje = 'Contraseña incorrecta'
                return render(request, 'loginUser.html', {'mensaje': mensaje, 'correo': correo})
        else:
            mensaje = 'El correo no está registrado'
            return render(request, 'loginUser.html', {'mensaje': mensaje, 'correo': correo})


# Cerrar sesión
def cerrarSesion(request):
    logout(request)
    return redirect('/')
