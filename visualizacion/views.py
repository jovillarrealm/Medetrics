from django.shortcuts import render
from .models import Visualizacion
from django.http import HttpRequest
from .forms import QueryForm

from datetime import datetime
from persistencia.visualizacion_dbops import get_reports, get_departamentos

# Create your views here.

def visualizacion(request:HttpRequest):
    disease, municipio, barrio = "disease", "municipio", "barrio"
    visualizacions = Visualizacion.objects.all().order_by('-date')
    if request.method == "GET":
        form = QueryForm()
        reports = tuple(get_reports())
        #print(form)
        departamentos = get_departamentos()
        print(departamentos)
        
        context = {"query_form": form,
                "visualizacions":visualizacions,
                "reports": reports,
                }
        return render(request, 'visualizacion.html', context)
        #return render(req, "reporte.html", context)
    elif request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            form_data: dict = form.cleaned_data
            form_data['diagnosis_date'] = datetime.combine(form_data['diagnosis_date'], datetime.min.time())
            match_stage = {}
            if form_data.get(disease) not in ["Enfermedades", "Enfermedad"]:
                match_stage[disease] = form_data.get(disease)
                #return render(request, "user_error.html")
            if form_data.get(municipio) != "Municipio":
                match_stage[municipio] = form_data.get(municipio)
                #return render(request, "user_error.html")
            if form_data.get(barrio) != "Barrio":
                match_stage[barrio] = form_data.get(barrio)
                #return render(request, "user_error.html")
            
            reports = tuple(get_reports(match_stage))
            
            
            context = {"query_form": form,
                    "visualizacions":visualizacions,
                    "reports": reports,
                    }
            return render(request, 'visualizacion.html', context)
    
from django.http import JsonResponse
from persistencia.mongo_data import get_db

def get_departamento_ciudad_barrio(request):
    departamento = request.GET.get('departamento')
    ciudad = request.GET.get('ciudad')
    barrio = request.GET.get('barrio')

    collection = get_db()["places"]

    if departamento:
        ciudades = collection.find({'departamento': departamento}, {'municipio': 1})
        ciudades = [ciudad['ciudad'] for ciudad in ciudades]
    else:
        ciudades = []

    if ciudad:
        barrios = collection.find({'municipio': ciudad}, {'centro_poblado': 1})
        barrios = [barrio['barrio'] for barrio in barrios]
    else:
        barrios = []

    response = {
        'departamento': departamento,
        'ciudades': ciudades,
        'barrios': barrios
    }
    print(response)
    return JsonResponse(response)

from visualizacion import covid_charts
from visualizacion import med_charts

def bienvenida_visualizaciones(req: HttpRequest):
    context = {}
    return render(req, "bienvenida_visualizaciones.html", context)


def visualiza_enfermedad(req: HttpRequest, enf:str):
    datos = {
        "VIH":(med_charts.chart_vih, "VIH"),
        "meningitis_influenzae": (med_charts.chart_meningitis, "Meningitis por Haemophilus Influenzae"),
        "dengue":(med_charts.chart_dengue,"Dengue" ),
        "viruela_simica":(med_charts.chart_viruela_sim, "Viruela símica"),
        "covid": (covid_charts.covid_charts, "COVID-19")
        }
    plots, enfermedad = datos[enf]
    plot_divs= plots()
    context = {"plotdivs": plot_divs, "enfermedad": enfermedad}
    return render(req, "visualiza_enfermedad.html", context)