from django.shortcuts import redirect

def logout(request):
    # Establecer request.session.valido = 0
    request.session['valido'] = 0
    request.session['numero_salud'] = None

    # Redirigir al usuario a otra página
    return redirect('inicio')