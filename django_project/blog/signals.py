from .models import Post, Comment
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from notifications.models import Notification
import os


@receiver(pre_save, sender=Post)
def file_update(sender, instance, raw, using, update_fields,**kwargs):
    """
    Signal used to delete the previous image when the user wants to update the post
    """
    if instance.id is None:
        pass

    else:
        previous = Post.objects.get(id=instance.id)
        if instance.image.path != previous.image.path:
            os.remove(previous.image.path)


@receiver(post_save, sender=Comment)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_sender = instance.author
        user_receiver = instance.post.author
        if user_sender != user_receiver:
            text = f"{user_sender} has commented your post"
            notification = Notification(comment=instance,
                sender=user_sender, user=user_receiver, notification_type=2, text_preview=text)
            notification.save()

