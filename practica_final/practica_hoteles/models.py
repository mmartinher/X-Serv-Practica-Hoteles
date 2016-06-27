from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hotel(models.Model):
	nombre = models.CharField(max_length=200)
	pagina = models.TextField()
	direccion = models.CharField(max_length=100)
	categoria = models.CharField(max_length=30)
	estrellas = models.CharField(max_length=30)
	descripcion = models.TextField()
	latitud = models.FloatField(default=0.0)
	longitud = models.FloatField(default=0.0)
	def __unicode__(self):
		return self.nombre

class Imagen(models.Model):
	hotel = models.ForeignKey('Hotel', default="")
	url = models.TextField()

class Comentario(models.Model):
	user = models.ForeignKey(User, default="")
	hotel = models.ForeignKey('Hotel', default="")
	titulo = models.CharField(max_length=100, blank=True, null=True)
	fecha = models.DateField(auto_now=True)
	comentario = models.TextField(blank=True, null=True)

class Config(models.Model):
	user = models.ForeignKey(User, default="")
	titulo = models.CharField(max_length=50, blank=True, null=True, default="default")
	color = models.CharField(max_length=10, blank=True, null=True)
	medida = models.IntegerField(blank=True, null=True)

class Fav(models.Model):
	user = models.ForeignKey(User, default="")
	hotel = models.ForeignKey('Hotel', default="")
	fecha = models.DateField(auto_now=True)
