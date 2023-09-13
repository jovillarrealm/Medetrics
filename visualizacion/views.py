from django.shortcuts import render
from .models import Visualizacion
from django.http import HttpRequest
from .forms import QueryForm
from .dbops import get_reports
# Create your views here.
def visualizacion(request:HttpRequest):
    if request.method == "GET":
        form = QueryForm()
        print(form)
        reports = tuple(get_reports())
        visualizacions = Visualizacion.objects.all().order_by('-date')
        context = {"query_form": form,
                   'visualizacions':visualizacions,
                   "reports": reports}
        return render(request, 'visualizacion.html', context)
        #return render(req, "reporte.html", context)
    elif request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            form_data: dict = form.cleaned_data
            #print(form_data, type(form))
            try:
                if get_reports(form_data):
                    return render(request, "gracias.html")
                else:
                    return render(request, "error.html")
            except:
                return render(request, "error.html")
    
