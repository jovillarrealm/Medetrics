from django.shortcuts import render
from django.http import HttpRequest
from signup.forms import registerForm
from persistencia.register_dbops  import send_register
from typing import Any

# Create your views here.

def signup(req: HttpRequest):
    if req.method == "GET":
        form = registerForm()
        context = {"form": form}
        return render(req, "signup.html", context)
    elif req.method == "POST":
        form: registerForm = registerForm(req.POST)
        if form.is_valid():
            form_data: dict[str, Any] = form.cleaned_data
            #print(form_data, type(form))   
            form_data['email'] = form.cleaned_data['email']
            form_data['contraseña'] = form.cleaned_data['contraseña']
            form_data['numero_salud'] = int(form.cleaned_data['numero_salud'])
            try:
                if send_register(form_data):
                    return render(req, "exitoso.html")
                else:
                    return render(req, "error_registro.html")
                    pass
            except:
                return render(req, "error_registro.html")
        else:
            return render(req, "error_registro.html")
        