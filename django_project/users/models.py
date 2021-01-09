from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    # directorio donde se va a guardar las imagenes en upload_to

    def __str__(self):
        return f'{self.user.username} Profile'

# el inverso se hace simplement con user.profile
# al acceder a la imagen tengo bastantes datos guardados
# debo guardar la localizacion de donde se van a guardar las imagenes