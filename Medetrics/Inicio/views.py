from django.shortcuts import HttpResponse

# Create your views here.
def inicio(request):
    return HttpResponse("hola")