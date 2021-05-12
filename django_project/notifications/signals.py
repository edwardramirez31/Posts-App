from django.dispatch import receiver
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
# se debe usar el convertidor dado que todo lo que trae django se corre sync
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification
from django.urls import reverse
# esta señal le manda un mensaje al consumidor

# en caso de querer colocar solo la app
# activity/__init__.py
# default_app_config = 'activity.apps.ActivityAppConfig'


@receiver(post_save, sender=Notification)
def new_user(sender, instance, created, **kwargs):
    # created no chequea el estado de updated
    # canal de comunicacion para todas las instancias
    channel_layer = get_channel_layer()
    group_name = f"user_{instance.user.id}"
    # print(group_name)
    # enviar un mensaje al channel layer en forma de broadcast
    async_to_sync(channel_layer.group_send)(
        # "groupname", {lo que voy a enviar al grupo}
        group_name, {
            "type": "new.follow",
            "event": "New Follower",
            "picture": instance.sender.profile.image.url,
            "message": instance.text_preview,
            "url": reverse("notifications:mark", args=[instance.id])
        }
    )
    
