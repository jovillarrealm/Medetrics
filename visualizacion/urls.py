from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizacion, name='visualizacion'),
    path('mapa/',views.mapa, name='mapa'),
    path('bienvenida/',views.bienvenida_visualizaciones, name='bienvenida_visualizaciones'),
    path('visualiza/<str:enf>/',views.visualiza_enfermedad, name='visualiza_enfermedad'),
]
