from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from django.core.files.storage import default_storage as storage
from io import BytesIO

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['presentation', 'image']

    def save(self, *args, **kwargs):
        coords = kwargs.pop('coordinates', False)
        profile = super().save(*args, **kwargs)

        if coords:
            memfile = BytesIO()
            img = Image.open(profile.image)
            img_cropped = img.crop(coords)
            img_cropped.save(memfile, 'JPEG')
            name = profile.image.name
            if profile.image != Profile.image.field.default:
                storage.delete(profile.image.name)
                storage.save(name, memfile)
            memfile.close()
            img.close()
        
        return profile
