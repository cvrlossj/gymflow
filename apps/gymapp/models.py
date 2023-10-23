from django.db import models

# Create your models here.


class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    zona_muscular = models.CharField(max_length=50)
    descripcion = models.TextField()
    enlace_tutorial = models.CharField(max_length=100)

    def __str__(self):
        txt = "Nombre: {0} - id: {1}"
        return txt.format(self.nombre, self.id)


class Entrenador(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    servicios = models.TextField()
    correo = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)
    gymespacio = models.ForeignKey('GymEspacio', on_delete=models.CASCADE)

    def __str__(self):
        txt = "Nombre: {0} - Apellido: {1} - id: {2}"
        return txt.format(self.nombre, self.apellido, self.id)


class GymUser(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=100)
    fecha_inscripcion = models.DateField()
    contrasenia = models.CharField(max_length=100)
    peso = models.CharField(max_length=10)
    altura = models.CharField(max_length=10)
    gymespacio = models.ForeignKey('GymEspacio', on_delete=models.CASCADE)


class GymEspacio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)
    maquinas = models.ManyToManyField(Maquina)
