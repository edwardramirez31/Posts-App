from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == "POST":
        # Si es POST, voy a validar los datos
        # Crear un form con los datos de la peticion
        form = UserCreationForm(request.POST)
        # Los datos de la peticion puede ser cualquier cosa
        # Por tanto se va a validar que se obtienen los datos deseados
        if form.is_valid():
            # obtener el nombre de usuario que se obtuvo
            # los datos validados del form van a estar en el diccionario
            # cleaned_Data
            userName = form.cleaned_data.get('username')
            # Colocar un flash message para mostrar que se obtuvieron buenos datos.
            # Un mensaje flash es una buena manera de mostrar alertas
            # Que se muestran una sola vez y que desparecen en la siguiente
            # peticion. Que tipo de mensaje quiero mostrar(succes, info, warning)
            messages.success(request, f"Account created for {userName}!")
            # Redirigir al usuario
            return redirect('blog:blog-home')
    else:
        # Blank form
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})
