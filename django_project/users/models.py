from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage as storage


def get_path(self, filename):
    return f"profile_pics/user_{self.user.id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to=get_path)
    following = models.ManyToManyField(User, related_name='all_followers')
    presentation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     coords = kwargs.get('coordinates', False)
    #     if coords:
    #         kwargs.pop('coordinates')
    #         img = Image.open(self.image.path)
    #         img_cropped = img.crop(coords)
    #         img_cropped.save(self.image.path)
    #     else:
    #         super().save(*args, **kwargs)
