from .models import Post, Comment, Like
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from notifications.models import Notification
from django.core.files.storage import default_storage as storage


@receiver(pre_save, sender=Post)
def file_update(sender, instance, raw, using, update_fields,**kwargs):
    """
    Signal used to delete the previous image when the user wants to update the post
    """
    if instance.id is None:
        pass

    else:
        previous = Post.objects.get(id=instance.id)
        if instance.image.name != previous.image.name:
            storage.delete(previous.image.name)


@receiver(post_save, sender=Comment)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_sender = instance.author
        user_receiver = instance.post.author
        if user_sender != user_receiver:
            text = f"{user_sender} commented your post"
            notification = Notification(comment=instance,
                sender=user_sender, user=user_receiver, notification_type=2, text_preview=text)
            notification.save()


@receiver(post_save, sender=Like)
def new_like(sender, instance, created, **kwargs):
    if created:
        user_sender = instance.user
        user_receiver = instance.post.author
        if user_sender != user_receiver:
            try:
                notification = Notification.objects.get(post=instance.post, user=user_receiver)
                people = len(notification.post.likes.all())
                if people > 1:
                    notification.text_preview = f"{user_sender} and {people - 1} more liked your post"
                else :
                    notification.text_preview = f"{user_sender} liked your post"
                notification.has_seen = False
                notification.save()


            # DoesNotExist
            except:
                text = f"{user_sender} liked your post"
                notification = Notification(post=instance.post,
                                            sender=user_sender, user=user_receiver, notification_type=4, text_preview=text)
                notification.save()
                print(notification)
