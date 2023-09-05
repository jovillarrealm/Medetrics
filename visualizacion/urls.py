from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizacion, name='visualizacion'),
]