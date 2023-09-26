from django.db import models
from django.contrib.auth.models import User

class Componente(models.Model):
    producto = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=600)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to="componentes", null=True, blank=True)
    stock = models.IntegerField()

    @property
    def imagen_url(self):
        return self.imagen.url if self.imagen else ''
    
    def __str__(self):
        return f"{self.id} - {self.producto} - {self.precio}"

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    mail = models.CharField(max_length=100, null=True)
    red_social = models.CharField(max_length=20, null=True)
    numero = models.IntegerField()
    domicilio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    altura = models.IntegerField()
    codigoPostal = models.IntegerField()