from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
# esto se podía hacer en una sola funcion
@receiver(post_save, sender=User)
def saveProfile(sender, instance, **kwargs):
    instance.profile.save()

#     Now i have an observation: when you delete a profile or a user you don't delete the picture attached to it. So I made a signal for this:

# @receiver(post_delete, sender=Profile)
# def delete_profile(sender, instance, **kwargs):
#     if instance.image != Profile.image.field.default:
#         os.remove(instance.image.path)