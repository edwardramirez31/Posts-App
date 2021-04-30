from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
# esto se podía hacer en una sola funcion
@receiver(post_save, sender=User)
def saveProfile(sender, instance, **kwargs):
    instance.profile.save()

#     Now i have an observation: when you delete a profile or a user you don't delete the picture attached to it. So I made a signal for this:

@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    if instance.image != Profile.image.field.default:
        os.remove(instance.image.path)


# @receiver(post_save, sender=Profile)
# def delete_image(sender, **kwargs):
#     upload_folder_instance = kwargs['instance']
#     if upload_folder_instance.id:
#         path = upload_folder_instance.image.path
#         os.remove(path)
@receiver(pre_save, sender=Profile)
def file_update(sender, instance, raw, using, update_fields, **kwargs):
    """
    Signal used to delete the previous image when the user wants to update the post
    """
    if instance.id is None:
        pass

    else:
        # current = instance
        previous = Profile.objects.get(id=instance.id)
        if not previous.image.path == instance.image.path:
            os.remove(previous.image.path)
