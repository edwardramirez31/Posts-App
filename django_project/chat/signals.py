from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import Notification


@receiver(post_save, sender=Message)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_sender = instance.sender
        chatroom = instance.chatroom
        user_receiver = chatroom.participants.all().exclude(id=user_sender.id)[0]
        text = f"{user_sender} sent you a message"
        notification = Notification(message=instance,
                                        sender=user_sender, user=user_receiver, notification_type=1, text_preview=text)
        notification.save()
