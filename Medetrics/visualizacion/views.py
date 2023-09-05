from django.shortcuts import render
from .models import Visualizacion

# Create your views here.
def visualizacion(request):
    visualizacions = Visualizacion.objects.all().order_by('-date')
    return render(request, 'visualizacion.html', {'visualizacions':visualizacions})
