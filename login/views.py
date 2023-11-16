from django.shortcuts import render, redirect
from .forms import LoginForm
from persistencia.login_dbops import buscar_coincidencia_credenciales  # Reemplaza con la ubicación correcta del archivo
from persistencia.login_dbops import buscar_numero_salud
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contrasena']

            # Llama a la función de búsqueda de credenciales
            credenciales_validas = buscar_coincidencia_credenciales(email, contraseña)
            numero_salud = buscar_numero_salud(email, contraseña)
            
            if credenciales_validas:
                # Aquí puedes redirigir a la página de inicio, por ejemplo
                request.session['numero_salud'] = numero_salud
                request.session['valido'] = 1
                return redirect('inicio')  # Reemplaza 'home' con la URL de tu página de inicio
            else:
                # En caso de credenciales inválidas, puedes mostrar un mensaje de error
                error_message = "Credenciales inválidas. Por favor, inténtalo de nuevo."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})