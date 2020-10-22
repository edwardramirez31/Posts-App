from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Para agregar un campo al formulario necesito crear un nuevo form que herede
# el form principal


class UserRegisterForm(UserCreationForm):
    # Agregar los campos
    email = forms.EmailField()

    class Meta:
        # con qué modelo quiero que interactue este form
        model = User
        # campos que se van a mostrar en el formulario y su orden
        fields = ['username', 'email', 'password1', 'password2']
