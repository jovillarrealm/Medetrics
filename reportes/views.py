from django.shortcuts import render
from django.http import HttpRequest
from reportes.forms import ReportForm


from datetime import datetime

from persistencia.reportes_dbops  import send_report
from typing import Any


# Create your views here.
def bienvenida_reportes(req: HttpRequest):
    context = {}
    return render(req, "bienvenida_reportes.html", context)


def reportes(req: HttpRequest):
    if req.method == "GET":
        numero_salud = req.session.get('numero_salud')  # Obtener el valor de la sesión
        form = ReportForm(initial={'numero_salud': numero_salud})
        context = {"form": form}
        return render(req, "reporte.html", context)
    elif req.method == "POST":
        form: ReportForm = ReportForm(req.POST)
        if form.is_valid():
            form_data: dict[str, Any] = form.cleaned_data
            if form_data.get("disease") == "Enfermedades":
                return render(req, "user_error.html")
            elif form_data.get("municipio") == "Municipios":
                return render(req, "user_error.html")
            elif form_data.get("barrio") == "Barrios":
                return render(req, "user_error.html")
            #print(form_data, type(form))
            form_data['diagnosis_date'] = datetime.combine(form_data['diagnosis_date'], datetime.min.time())    
            form_data['edad_paciente'] = form.cleaned_data['edad_paciente']
            form_data['sexo_paciente'] = form.cleaned_data['sexo_paciente']
            form_data['fecha_sintomas'] = datetime.combine(form_data['fecha_sintomas'], datetime.min.time())
            form_data['estrato'] = int(form.cleaned_data['estrato'])
            try:
                if send_report(form_data):
                    return render(req, "gracias.html")
                else:
                    return render(req, "error.html")
                    pass
            except:
                return render(req, "error.html")
        else:
            return render(req, "user_error.html")
        





