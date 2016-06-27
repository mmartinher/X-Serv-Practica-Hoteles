from django.shortcuts import render
import itertools
from parser import getHotels
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from models import Hotel, Imagen, Comentario, Config, Fav
from django.contrib.auth.models import User
from django.db.models import Count
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#Cargar base de datos
def cargarhoteles (url, idioma, nombrehot):
	parser = getHotels(url)
	listanombre = parser.get('name')
	listadireccion = parser.get('address')
	listapagina = parser.get('web')
	listalatitud = [float(num) for num in parser.get('latitude')]
	listalongitud = [float(num) for num in parser.get('longitude')]
	listadescripcion = parser.get('body')
	listaimagenes = parser.get('images')
	listacategoria = parser.get('category')
	if not idioma:
		for nombre, direccion, pagina, latitud, longitud, descripcion, imagenes, categoria in itertools.izip(listanombre, listadireccion, listapagina, listalatitud, listalongitud, listadescripcion, listaimagenes, listacategoria):
			tipo = categoria[0]
			estrellas = categoria[1]
			hotel = Hotel(nombre=nombre, pagina=pagina, direccion=direccion, latitud=latitud, longitud=longitud, descripcion=descripcion, categoria=tipo, estrellas=estrellas)
			hotel.save()
			idhotel = Hotel.objects.get(nombre=nombre)
			enlaces =' '.join(imagenes)
			imagen = Imagen(hotel = idhotel, url = enlaces)
			imagen.save()
	else:
		posicion = 0
		for key, value in enumerate(listanombre):
			if value == nombrehot:
				posicion = key
		descripcion = listadescripcion[posicion]
		return descripcion

@csrf_exempt
def loginuser(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
	else:
		return HttpResponse("Not Found")
	return HttpResponseRedirect('/')

def redirect(request):
	return HttpResponseRedirect('/')

#Funcionalidad basica
def index(request):
	if request.method == "GET":
		lista_hoteles = []
		lista_usuarios = []
		url = 'http://www.esmadrid.com/opendata/alojamientos_v1_es.xml'
		hoteles = Hotel.objects.all()
		if not hoteles:
			cargarhoteles(url, None, "")
		comentarios = Hotel.objects.annotate(cantidad=Count('comentario')).order_by("-cantidad")
		if comentarios[0].cantidad > 0:
			for contador in range(10):
				if comentarios[contador].cantidad > 0:
					hotel = Hotel.objects.get(id=comentarios[contador].id)
					imagenes = Imagen.objects.get(hotel=hotel)
					imagen = imagenes.url.split(" ")[0]
					lista_hoteles += [(hotel, imagen)]
		usuarios = User.objects.all()
		for usuario in usuarios:
			config = Config.objects.get(user=usuario)
			if config.titulo == "default":
				titulo = "Pagina de " + usuario.username
			else:
				titulo = config.titulo
			lista_usuarios += [(usuario, titulo)]
		template = get_template("index.html")
		context = RequestContext(request, {'hoteles' : lista_hoteles, 'users' : lista_usuarios})
	else:
		return HttpResponse("Not found")
	return HttpResponse(template.render(context))

def alojamientos(request):
	lista_hoteles = []
	estrellas = request.POST.get('stars')
	categoria = request.POST.get('category')
	if not estrellas and not categoria:
		hoteles = Hotel.objects.all()
	else:
		if estrellas != " " and categoria == " ":
			hoteles = Hotel.objects.filter(estrellas=estrellas)
		elif categoria != " " and estrellas == " ":
			hoteles = Hotel.objects.filter(categoria=categoria)
		elif estrellas != " " and categoria != " ":
			hoteles = Hotel.objects.filter(estrellas=estrellas).filter(categoria=categoria)
	for hotel in hoteles:
		lista_hoteles +=[(hotel.nombre, hotel.id)]
	template = get_template("todos.html")
	context = RequestContext(request, {'hoteles' : lista_hoteles})
	return HttpResponse(template.render(context))

def paginahotel(request, identificador):
	lista_imagenes = []
	idioma = request.POST.get('idioma')
	try:
		hotel = Hotel.objects.get(id=identificador)
	except ObjectDoesNotExist:
		return HttpResponse("Does not exist")
	imagenes = Imagen.objects.get(hotel=hotel)
	if idioma:
		if idioma == "English":
			url = "http://www.esmadrid.com/opendata/alojamientos_v1_en.xml"
		elif idioma == "French":
			url = "http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml"
		else:
			url = "http://www.esmadrid.com/opendata/alojamientos_v1_es.xml"
		hotel.descripcion = cargarhoteles(url, idioma, hotel.nombre)
	for contador in range(5):
		try:
			lista_imagenes += [imagenes.url.split(" ")[contador]]
		except IndexError:
			pass
	comentarios = Comentario.objects.filter(hotel=hotel)
	template = get_template("hotel.html")
	context = RequestContext(request, {'hotel' : hotel, 'imagenes' : lista_imagenes, 'comentarios':comentarios})
	return HttpResponse(template.render(context))

def paginausuario (request, nick):
	usuario = User.objects.get(username=nick)
	if request.method == "GET":
		lista_hoteles = []
		try:
			favoritos = Fav.objects.filter(user=usuario)
			for favorito in favoritos:
				imagen = Imagen.objects.get(hotel=favorito.hotel)
				url = imagen.url.split(" ")[0]
				lista_hoteles += [(favorito.hotel, url, favorito.fecha)]
			template = get_template('favoritos.html')
			context = RequestContext(request, {'favoritos' : lista_hoteles, 'nick' : nick})
			return HttpResponse(template.render(context))
		except ObjectDoesNotExist:
			return HttpResponse("Not Found")
	elif request.method == "POST":
		medida = request.POST.get('medida')
		color = request.POST.get('color')
		if request.POST.get('titulo') and request.POST.get('titulo') != " ":
			titulo = request.POST.get('titulo')
		else:
			titulo = "Pagina de " + request.user.username
		config = Config.objects.get(user=usuario)
		config.titulo = titulo
		config.color = color
		config.medida = medida
		config.save()
		return HttpResponseRedirect("/_" + nick)
	else:
		return HttpResponse("Not Found")

def xmlusuario(request, nick):
	lista_favoritos = []
	if request.method == "GET":
		lista_hoteles = []
		try:
			usuario = User.objects.get(username=nick)
		except ObjectDoesNotExist:
			return HttpResponse ("Not Found")
		favoritos = Fav.objects.filter(user=usuario)
		for favorito in favoritos:
			imagen = Imagen.objects.get(hotel=favorito.hotel)
			url = imagen.url.split(" ")[0]
			lista_favoritos += [(favorito.hotel, url, favorito.fecha)]
		template = get_template('xml/usuario.xml')
		context = RequestContext(request, {'hoteles' : lista_favoritos})
		return HttpResponse(template.render(context), content_type="text/xml")
	else:
		return HttpResponse("Not Found")

def about(request):
    template = get_template('about.html')
    return HttpResponse(template.render())


#Almacenar comentarios
def addcomentario(request):
	if request.method == "POST":
		nick = request.user.username
		usuario = User.objects.get(username=nick)
		hotel = Hotel.objects.get(id=request.POST.get('identificador'))
		try:
			comentado = Comentario.objects.get(user=usuario, hotel=hotel)
		except ObjectDoesNotExist:
			titulo = request.POST.get('titulo')
			comentario = request.POST.get('comentario')
			savecom = Comentario(user=usuario, hotel=hotel, titulo=titulo, comentario=comentario)
			savecom.save()
			return HttpResponseRedirect("/alojamientos/" + str(hotel.id))
		return HttpResponseRedirect("/alojamientos/" + str(hotel.id))
	else:
		return HttpResponse("Not Found")

#Almacenar favoritos
def addfavorito(request):
	if request.method == "POST":
		identificador = request.POST.get('identificador')
		usuario = User.objects.get(username=request.user.username)
		hotel = Hotel.objects.get(id=identificador)
		favorito = Fav(user=usuario, hotel=hotel)
		favorito.save()
		return HttpResponseRedirect("/alojamientos/" + str(hotel.id))
	else:
		return HttpResponse("Not Found")

#Servir CSS
def css(request):
	color = "white"
	medida = 14
	template = get_template('css/style.css')
	if request.user.is_authenticated():
		usuario = User.objects.get(username=request.user.username)
		configuracion = Config.objects.get(user=usuario)
		color = configuracion.color
		medida = configuracion.medida
	context = RequestContext(request, {'color' : color, 'medida' : medida})
	return HttpResponse (template.render(context), content_type="text/css")

def js(request, js):
	template = get_template('js/' + js)
	return HttpResponse(template.render(), content_type="text/javascript")
