from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatRoom(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='chatrooms', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name="chatroom_participants", through="Participant")

    def __str__(self):
        return f"ChatRoom {self.id}"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="all_messages")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="messages_sender", null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:15]} by {self.sender}"

class Participant(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="all_participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_chats")

    class Meta:
        unique_together = ('chatroom', 'user')
        
    def __str__(self):
        return f"Participants {self.id}"

