from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os
from notifications.models import Notification
from django.core.files.storage import default_storage as storage

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
# esto se podía hacer en una sola funcion
@receiver(post_save, sender=User)
def saveProfile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    if instance.image != Profile.image.field.default:
        storage.delete(instance.image.name)

@receiver(pre_save, sender=Profile)
def file_update(sender, instance, raw, using, update_fields, **kwargs):
    """
    Signal used to delete the previous image when the user wants to update the profile picture
    """
    if instance.id is None:
        pass
    else:
        # current = instance
        previous = Profile.objects.get(id=instance.id)

        if not previous.image.name == instance.image.name and previous.image != Profile.image.field.default:
            storage.delete(previous.image.name)


@receiver(m2m_changed, sender=Profile.following.through)
def follow_update(sender, instance, action, pk_set, ** kwargs):
    if action == "post_add":
        user_sender = instance.user
        user_receiver = User.objects.get(pk=pk_set.pop())
        text = f"{user_sender} is following you!"
        notification = Notification(sender=user_sender, user=user_receiver, notification_type=3, text_preview=text)
        notification.save()
