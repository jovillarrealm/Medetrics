from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizacion, name='visualizacion'),
    path('get_departamento_ciudad_barrio/', views.get_departamento_ciudad_barrio),
]