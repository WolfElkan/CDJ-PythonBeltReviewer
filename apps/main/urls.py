from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^hot$', views.hot),
	url(r'^run$', views.run),
]
