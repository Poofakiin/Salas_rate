from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


#Modelo para guardar informacion de las salas
class Sala(models.Model):
    NombreSala = models.CharField(max_length=50)
    Edificio = models.CharField(max_length=50)
    CapacidadNormal = models.IntegerField()
    CapacidadExamen = models.IntegerField()
    Aforo = models.IntegerField()
    Hibrido = models.BooleanField()
    # Foto = models.ImageField(upload_to='fotos/', null=True) Posible atributo del siguiente sprint
    PromedioVisibilidad = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    PromedioSonido = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    PromedioAsientos = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    PromedioIluminacion = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    # CalificacionPromedioGlobal es el promedio de los 4 atributos anteriores
    CalificacionPromedioGlobal = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    
    Link = models.URLField(max_length=200)

    def save(self, *args, **kwargs):
        self.CalificacionPromedioGlobal = (self.PromedioVisibilidad + self.PromedioSonido + self.PromedioAsientos + self.PromedioIluminacion) / 4.0
        super(Sala, self).save(*args, **kwargs)

    def __str__(self):
        return self.NombreSala
    

#Modelo para registrar usuarios
class Usuario(AbstractUser):
    TYPE = (
        ('Alumno','Alumno'),
        ('Docente','Docente'),
        ('Moderador','Moderador'),
    )
    UserType = models.CharField(max_length=50,choices=TYPE,default='Alumno')
    #FotoPerfil = models.ImageField() Posible atributo del siguiente sprint

    #Numero de reseñas hechas, funcionalidad para contar reseñas aun no implementada
    ReviewsN = models.IntegerField(default=0)

    #Reputacion total de sus reseñas, funcionalidad de reputacion aun no implementada
    Reputacion = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.username


#Modelo para guardar reseñas
class Review(models.Model):
    
    Sala = models.ForeignKey(Sala, on_delete=models.CASCADE, default=None)
    User = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #Calificacion de la sala
    Visibilidad = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    Sonido = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    Asientos = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    Iluminacion = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    #Promedio es el promedio de los 4 atributos anteriores
    Promedio = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    Reseña = models.TextField(max_length=400)
    #Fecha de la reseña
    Fecha = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Usuario, related_name='review_posts', default=None)
    @property
    def puntuacion(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        self.Promedio = (self.Visibilidad + self.Sonido + self.Asientos + self.Iluminacion) / 4.0
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return self.Reseña

class Anuncio(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    comentario = models.TextField()
    imagen = models.ImageField(upload_to='imagenes_anuncios/')
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

#Model for storing review comments
class Comentario(models.Model):
    User = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=0)
    Fecha = models.DateTimeField(auto_now_add=True)
    Reseña = models.ForeignKey(Review, on_delete=models.CASCADE)
    Comentario = models.TextField(max_length=400)
    likes = models.ManyToManyField(Usuario, related_name='comment_posts', default=None)

    @property
    def puntuacion(self):
        return self.likes.count()

    def __str__(self):
        return self.Comentario
    
