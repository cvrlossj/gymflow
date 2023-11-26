from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
import os
from django.conf import settings
from datetime import datetime
from django.contrib import messages


# Para extraer id del video y poder insertar el video
from urllib.parse import urlparse, parse_qs
import json

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

    # Crear un diccionario con la información de la máquina
    maquina_info = {
        'nombre': m_nombre,
        'zona_muscular': m_zona_muscular,
        'descripcion': m_descripcion,
        'enlace_tutorial': video_id 
    }

    
    json_data = json.dumps(maquina_info)


    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
    qr.add_data(json_data)
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



# Entrenadores - LISTAR
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


# Editar - Entrenador
def editarEntrenador(request):
    e_id = request.POST['txtId']
    entrenadorBD = Entrenador.objects.get(id=e_id)
    e_nombre = request.POST['txtEntrenador']
    e_apellido = request.POST['txtApellido']
    e_servicios = request.POST['txtServicio']
    e_precio = request.POST['txtPrecio']
    e_correo = request.POST['txtCorreo']
    e_password = request.POST['txtPassword']

    try:
        e_img = request.FILES['txtImagen']
        ruta_imagen = os.path.join(
            settings.MEDIA_ROOT, str(entrenadorBD.foto_perfil))
        os.remove(ruta_imagen)
    except:
        e_img = entrenadorBD.foto_perfil


    entrenadorBD.nombre = e_nombre
    entrenadorBD.apellido = e_apellido
    entrenadorBD.servicios = e_servicios
    entrenadorBD.correo = e_correo
    entrenadorBD.contrasenia = e_password
    entrenadorBD.precio = e_precio
    entrenadorBD.foto_perfil = e_img

    entrenadorBD.save()

    return redirect('/entrenadores')

# Eliminar - Entrenador
def eliminarEntrenador(request, id):
    entrenador = Entrenador.objects.get(id=id)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(entrenador.foto_perfil))
    os.remove(ruta_imagen)
    entrenador.delete()
    return redirect('/entrenadores')


# GYMUSER
def cargarGymUser(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    gimnasio = GymEspacio.objects.all()
    gymuser = GymUser.objects.all()
    gymuser_cont = GymUser.objects.count()
    return render(request, "listaUsuarios.html", {"gim": gimnasio, "gusr": gymuser, "tipoUsuario": tipoUsuario, "tot": gymuser_cont})


def agregarGymUser(request):
    gu_nombre = request.POST['txtUsuario']
    gu_apellido = request.POST['txtApellido']
    gu_correo = request.POST['txtCorreo']
    gu_contrasenia = request.POST['txtPassword']
    gu_tipo = request.POST['txtTipo']
    gu_img = request.FILES['txtImagen']

    # Obtén el ID del gimnasio como un número entero.
    gu_gimnasio_id = request.POST['cmbGim']
    gimnasio = GymEspacio.objects.get(id=gu_gimnasio_id)

    gu_peso = request.POST['txtPeso']
    gu_altura = request.POST['txtAltura']
    gu_fecha_inscripcion = request.POST['dateInscripcion']

    fecha_inscripcion = datetime.strptime(gu_fecha_inscripcion,'%Y-%m-%d').date()


    nuevo_usuario = GymUser.objects.create(
        nombre=gu_nombre, 
        apellido=gu_apellido, 
        correo=gu_correo,
        contrasenia=gu_contrasenia,
        id_tipo_id=gu_tipo,
        foto_perfil=gu_img,
        id_gymespacio=gimnasio,
        peso=gu_peso,
        altura=gu_altura,
        fecha_inscripcion=fecha_inscripcion
    )

    return redirect('/gymuser')
    

# Editar - Gymuser [cargar info]
def cargarEditarUsuario(request, id):
    tipoUsuario = request.session.get('tipoUsuario', None)
    gymuser = GymUser.objects.get(id=id)
    gimnasio = GymEspacio.objects.all()
    return render(request, "editarUsuario.html",{"gusr": gymuser, "tipoUsuario": tipoUsuario})


def editarUsuario(request):
    gu_id = request.POST['txtId']
    gymUserBD = GymUser.objects.get(id=gu_id)
    gu_nombre = request.POST['txtUsuario']
    gu_apellido = request.POST['txtApellido']
    gu_correo = request.POST['txtCorreo']
    gu_password = request.POST['txtPassword']
    gu_peso = request.POST['txtPeso']
    gu_altura = request.POST['txtAltura']

    try:
        gu_img = request.FILES['txtImagen']
        ruta_imagen = os.path.join(
            settings.MEDIA_ROOT, str(gymUserBD.foto_perfil))
        os.remove(ruta_imagen)
    except:
        gu_img = gymUserBD.foto_perfil
    
    gymUserBD.nombre = gu_nombre
    gymUserBD.apellido = gu_apellido
    gymUserBD.correo = gu_correo
    gymUserBD.contrasenia = gu_password
    gymUserBD.peso = gu_peso
    gymUserBD.altura = gu_altura
    gymUserBD.foto_perfil = gu_img

    gymUserBD.save()
    return redirect('/gymuser')

# Eliminar - GymUser
def eliminarGymUser(request, id):
    gymuser = GymUser.objects.get(id=id)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(gymuser.foto_perfil))
    os.remove(ruta_imagen)
    gymuser.delete()
    return redirect('/gymuser')


# Iniciar sesión - TODOS LOS ROLES
def iniciarSesion(request):
    if request.method == 'POST':
        correo = request.POST.get('txtCorreo')
        contrasenia = request.POST.get('txtContrasenia')

        try:
            usuarios = UsuarioPadre.objects.filter(correo=correo)
            if usuarios.exists():
                usuario = usuarios.first()
                if usuario.contrasenia == contrasenia:
                    request.session['tipoUsuario'] = usuario.id_tipo.nombre_tipo
                    request.session['usuario_id'] = usuario.id

                    if usuario.id_tipo.id_tipo in [1, 2, 3]:
                        return redirect('/maquinas')
                    else:
                        return redirect('/login')
                else:
                    mensaje = 'Contraseña incorrecta'
                    return render(request, 'loginUser.html', {'mensaje': mensaje, 'correo': correo})
            else:
                mensaje = 'El correo no está registrado'
                return render(request, 'loginUser.html', {'mensaje': mensaje, 'correo': correo})
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('/login')
    return render(request, 'loginUser.html')

# Cerrar sesión
def cerrarSesion(request):
    logout(request)
    return redirect('/')


# FUNCIONES DEL GYMUSER

def cargarDetalleMaquina(request, id):
    tipoUsuario = request.session.get('tipoUsuario', None)
    maquinas = Maquina.objects.get(id=id)
    return render(request, "detalleMaquinas.html", {"maq": maquinas, "tipoUsuario": tipoUsuario})



# Login de gym user
def cargarAccederUser(request):
    tipoUsuario = request.session.get('tipoUsuario', None)
    return render(request, "loginUser.html", {"tipoUsuario": tipoUsuario})
