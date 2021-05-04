from django.db import models
from blog.models import Comment
from users.models import Profile
from django.contrib.auth.models import User
from chat.models import Message
# Create your models here.
class Notification(models.Model):
    CHOICES = ((1, 'Message'), (2, 'Comment'), (3, 'Follow'))

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                            related_name="cmt_notifications", blank=True, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                            related_name="msg_notifications", blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_notifications_sent")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="get_all_notifications")
    notification_type = models.IntegerField(choices=CHOICES)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    has_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.id} by {self.sender}"
