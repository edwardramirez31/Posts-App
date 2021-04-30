from .models import Post
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os


@receiver(pre_save, sender=Post)
def file_update(sender, instance, raw, using, update_fields,**kwargs):
    """
    Signal used to delete the previous image when the user wants to update the post
    """
    if instance.id is None:
        pass

    else:
        # current = instance
        previous = Post.objects.get(id=instance.id)
        os.remove(previous.image.path)
