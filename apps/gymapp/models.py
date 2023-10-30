from django.db import models


class TipoUsuario(models.Model):
    id_tipo = models.IntegerField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)

    def __str__(self):
        txt = "{0} - id: {1}"
        return txt.format(self.nombre_tipo, self.id_tipo)


class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    zona_muscular = models.CharField(max_length=50)
    descripcion = models.TextField()
    enlace_tutorial = models.URLField()
    qr_code = models.ImageField(upload_to='qr_codes', null=True, blank=True)


class UsuarioPadre(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=25)
    id_tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)


class GymEspacio(UsuarioPadre):
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    maquinas = models.ManyToManyField(Maquina)


class Entrenador(UsuarioPadre):
    servicios = models.TextField()
    id_gymespacio = models.ForeignKey('GymEspacio', on_delete=models.CASCADE)


class GymUser(UsuarioPadre):
    fecha_inscripcion = models.DateField()
    peso = models.CharField(max_length=10, null=True, blank=True)
    altura = models.CharField(max_length=10, null=True, blank=True)
    id_gymespacio = models.ForeignKey('GymEspacio', on_delete=models.CASCADE)
