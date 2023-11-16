from django.shortcuts import redirect

def logout(request):
    # Establecer request.session.valido = 0
    request.session['valido'] = 0

    # Redirigir al usuario a otra página
    return redirect('inicio')