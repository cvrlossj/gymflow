from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver



class TipoUsuario(models.Model):
    id_tipo = models.IntegerField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)

    def __str__(self):
        txt = "{0} - id: {1}"
        return txt.format(self.nombre_tipo, self.id_tipo)


@receiver(post_migrate)
def crear_roles_por_defecto(sender, **kwargs):
    if sender.name == 'apps.gymapp': 
        if kwargs.get('interactive') and kwargs.get('app_config').name == 'apps.gymapp':
            if not TipoUsuario.objects.exists():
                TipoUsuario.objects.create(id_tipo=1, nombre_tipo='gymespacio')
                TipoUsuario.objects.create(id_tipo=2, nombre_tipo='entrenador')
                TipoUsuario.objects.create(id_tipo=3, nombre_tipo='gymuser')



class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    zona_muscular = models.CharField(max_length=50)
    descripcion = models.TextField()
    enlace_tutorial = models.URLField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenesMaquina', null=True, blank=True)
    # Campo para los nuevos inquilinos asociados


class UsuarioPadre(models.Model):
    nombre = models.CharField(max_length=50) 
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=25)
    id_tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)


class GymEspacio(UsuarioPadre): 
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    maquinas = models.ManyToManyField(Maquina, blank=True, null=True)


class Entrenador(UsuarioPadre):
    servicios = models.TextField()
    precio = models.IntegerField()
    foto_perfil = models.ImageField(upload_to='imagenesEntrenador')
    id_gymespacio = models.ForeignKey('GymEspacio', on_delete=models.CASCADE)

    


class GymUser(UsuarioPadre):
    fecha_inscripcion = models.DateField()
    foto_perfil = models.ImageField(upload_to='imagenesUsuario')
    peso = models.CharField(max_length=10, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    id_gymespacio = models.ForeignKey('GymEspacio', on_delete=models.CASCADE)

