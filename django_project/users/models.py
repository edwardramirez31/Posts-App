from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    # directorio donde se va a guardar las imagenes en upload_to

    def __str__(self):
        return f'{self.user.username} Profile'

    # ! rezise the image when it is uploaded
    def save(self):
        # metodo que se corre despues de que el modelo es guardado
        # * correr el save de la clase padre con super
        super().save()
        # * abrir la imagen de la instancia actual
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            #tupla con el tamaño maximo
            output_size = (300, 300)
            img.thumbnail(output_size)
            # ! guardar esta imagen con el mism nombre en el mismo path de la imagen de la actual instancia. Overwriting the image uploaded by the user
            img.save(self.image.path)
# el inverso se hace simplement con user.profile
# al acceder a la imagen tengo bastantes datos guardados
# debo guardar la localizacion de donde se van a guardar las imagenes


