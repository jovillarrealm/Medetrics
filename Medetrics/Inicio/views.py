from django.shortcuts import render

# Create your views here.
def inicio(req):
    context = {}
    return render(req, "inicio.html",context)