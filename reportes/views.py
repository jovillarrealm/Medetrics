from django.shortcuts import render

# Create your views here.
def reportes(req):
    context = {}
    return render(req, "reporte.html",context)