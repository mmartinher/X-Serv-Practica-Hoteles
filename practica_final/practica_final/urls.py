from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
	url(r'^$', 'practica_hoteles.views.index'),
	url(r'^alojamientos$', 'practica_hoteles.views.alojamientos'),
	url(r'^alojamientos/(\d+)$', 'practica_hoteles.views.paginahotel'),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^addcomentario/$', 'practica_hoteles.views.addcomentario'),
	url(r'^addfavorito/$', 'practica_hoteles.views.addfavorito'),
 	url(r'^css/style.css$', 'practica_hoteles.views.css'),
 	url(r'^about$', 'practica_hoteles.views.about'),
  	url(r'^(.*)/xml$', 'practica_hoteles.views.xmlusuario'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/$', 'practica_hoteles.views.redirect'),
    url(r'^js/(.*)$', 'practica_hoteles.views.js'),
   	url(r'^_(.*)$', 'practica_hoteles.views.paginausuario'),
]
