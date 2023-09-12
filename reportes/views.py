from django.shortcuts import render
from django.http import HttpRequest
from reportes.forms import ReportForm


from reportes.mongo_data import get_db
import reportes.dbops as dbops
from typing import Any


# Create your views here.
def reportes(req: HttpRequest):
    if req.method == "GET":
        form = ReportForm()
        context = {"form": form}
        return render(req, "reporte.html", context)
    elif req.method == "POST":
        form: ReportForm = ReportForm(req.POST)
        if form.is_valid():
            form_data: dict[str, Any] = form.cleaned_data
            #print(form_data, type(form))
            form_data["diagnosis_date"] = form_data["diagnosis_date"].strftime("%Y-%m-%d")
            db = get_db()
            try:
                if dbops.send_report(form_data, db):
                    return render(req, "gracias.html")
                else:
                    return render(req, "error.html")
            except:
                return render(req, "error.html")
