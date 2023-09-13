from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('bienvenida/',views.bienvenida_reportes, name='bienvenida_reportes'),
]