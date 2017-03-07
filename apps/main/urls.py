from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^books$', views.books_index),
	url(r'^books/new$', views.books_new),
	url(r'^books/(?P<id>\d+)$', views.books_show),
	url(r'^logout$', views.logout),
	
	url(r'^hot$', views.hot),
	url(r'^run$', views.run),
]
