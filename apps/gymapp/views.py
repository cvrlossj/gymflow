from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
import os
from django.conf import settings


# Para extraer id del video y poder insertar el video
from urllib.parse import urlparse, parse_qs

# CODIGO QR
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO


# Inicio de la página - Iniciar Sesión
def cargarInicio(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "inicio.html", {"tipoUsuario": tipoUsuario})

def cargarLogin(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "loginUser.html", {"tipoUsuario": tipoUsuario})


# Maquinas
def cargarListaMaquinas(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    maquinas = Maquina.objects.all()
    maquinas_cont = Maquina.objects.count()
    return render(request, "listaMaquinas.html", {"maq": maquinas, "tipoUsuario": tipoUsuario, "tot": maquinas_cont})

def list_maquinas(request):
    maquinas = list(Maquina.objects.values())
    data={'maquinas':maquinas}
    return JsonResponse(data)

def agregarMaquina(request):
    m_nombre = request.POST['txtMaquina']
    m_zona_muscular = request.POST['txtZona']
    m_descripcion = request.POST['txtDesc']
    m_enlace = request.POST['txtEnlace']
    m_img = request.FILES['txtImagen']

    parsed = urlparse(m_enlace)
    video_id = parse_qs(parsed.query).get('v')

    if video_id:
        video_id = video_id[0]
    else:
        pass

    # Genera el código QR basado en el nombre
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
    qr.add_data(m_nombre)
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
        enlace_tutorial=video_id,
        imagen=m_img
    )

    # Asigna el código QR al campo qr_code de la maquina
    maquina.qr_code.save(f"qr_code_{maquina.id}.png", qr_image, save=True)

    return redirect('/maquinas')



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

    parsed = urlparse(m_enlace)
    video_id = parse_qs(parsed.query).get('v')

    if video_id:
        video_id = video_id[0]
    else:
        pass
    

    try:
        m_img = request.FILES['txtImagen']
        ruta_imagen = os.path.join(
            settings.MEDIA_ROOT, str(maquinaBD.imagen))
        os.remove(ruta_imagen)
    except:
        m_img = maquinaBD.imagen

    maquinaBD.nombre = m_nombre
    maquinaBD.zona_muscular = m_zona_muscular
    maquinaBD.descripcion = m_descripcion
    maquinaBD.enlace_tutorial = video_id
    maquinaBD.imagen = m_img

    maquinaBD.save()

    return redirect('/maquinas')


def eliminarMaquina(request, id):
    maquina = Maquina.objects.get(id=id)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(maquina.imagen))
    ruta_qr = os.path.join(settings.MEDIA_ROOT, str(maquina.qr_code))
    os.remove(ruta_imagen)
    os.remove(ruta_qr)
    maquina.delete()
    return redirect('/maquinas')


# Perfil GymEspacio

def cargarPerfilGymEspacio(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "perfilGymEspacio.html", {"tipoUsuario": tipoUsuario})



# Entrenadores


def cargarEntrenadores(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    gimnasio = GymEspacio.objects.all()
    entrenadores = Entrenador.objects.all()
    entrenadores_cont = Entrenador.objects.count()
    return render(request, "listaEntrenadores.html", {"gim": gimnasio, "ent": entrenadores, "tipoUsuario": tipoUsuario, "tot": entrenadores_cont})




def agregarEntrenador(request):
    e_nombre = request.POST['txtEntrenador']
    e_apellido = request.POST['txtApellido']
    e_correo = request.POST['txtCorreo']
    e_contrasenia = request.POST['txtPassword']
    e_tipo = request.POST['txtUsuario']
    e_img = request.FILES['txtImagen']

    # Obtén el ID del gimnasio como un número entero.
    e_gimnasio_id = request.POST['cmbGim']
    gimnasio = GymEspacio.objects.get(id=e_gimnasio_id)

    e_servicios = request.POST['txtServicio']
    e_precio = request.POST['txtPrecio']


    nuevo_entrenador = Entrenador.objects.create(
        nombre=e_nombre, 
        apellido=e_apellido, 
        correo=e_correo,
        contrasenia=e_contrasenia,
        id_tipo_id=e_tipo,
        foto_perfil=e_img,
        id_gymespacio=gimnasio,
        servicios=e_servicios, 
        precio=e_precio)

    return redirect('/entrenadores')




# Editar - Entrenador
def cargarEditarEntrenador(request, id):
    tipoUsuario = request.session.get('tipoUsuario', None)
    entrenador = Entrenador.objects.get(id=id)
    gimnasio = GymEspacio.objects.all()
    return render(request, "editarEntrenador.html", {"ent": entrenador, "gim": gimnasio, "tipoUsuario": tipoUsuario})



def editarEntrenador(request):
    e_id = request.POST['txtId']
    entrenadorBD = Entrenador.objects.get(id=e_id)
    e_nombre = request.POST['txtEntrenador']
    e_apellido = request.POST['txtApellido']
    e_servicios = request.POST['txtServicio']
    e_precio = request.POST['txtPrecio']
    e_correo = request.POST['txtCorreo']
    e_password = request.POST['txtPassword']
    e_gim = GymEspacio.objects.get(id=request.POST['cmbGim'])

    try:
        e_img = request.FILES['txtImagen']
        ruta_imagen = os.path.join(
            settings.MEDIA_ROOT, str(entrenadorBD.foto_perfil))
        os.remove(ruta_imagen)
    except:
        e_img = entrenadorBD.foto_perfil


    entrenadorBD.nombre = e_nombre
    entrenadorBD.apellido = e_apellido
    entrenadorBD.id_gymespacio = e_gim
    entrenadorBD.servicios = e_servicios
    entrenadorBD.correo = e_correo
    entrenadorBD.contrasenia = e_password
    entrenadorBD.precio = e_precio
    entrenadorBD.foto_perfil = e_img

    entrenadorBD.save()

    return redirect('/entrenadores')

def eliminarEntrenador(request, id):
    entrenador = Entrenador.objects.get(id=id)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(entrenador.foto_perfil))
    os.remove(ruta_imagen)
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


# FUNCIONES DEL GYMUSER

def cargarDetalleMaquina(request, id):
    tipoUsuario = request.session.get('tipoUsuario', None)
    maquinas = Maquina.objects.get(id=id)
    return render(request, "detalleMaquinas.html", {"maq": maquinas, "tipoUsuario": tipoUsuario})

