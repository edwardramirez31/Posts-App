from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

# crear la lista de amigos en el momento en que se cree el profile
class FriendList(models.Model):
    user = models.OneToOneField(User, related_name="user_friend_list", on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, on_delete=models.CASCADE, related_name="all_friends", blank=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        This method is used to add an account to the user friend list
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        This method is used to remove an account to the user friend list
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, to_remove):
        """
        Initiate the action of removing an account from the user friend list
        """
        # person that is removing
        self.remove_friend(to_remove)
        # removing the remover from the other account friends list
        friend_list = FriendList.objects.get(user=to_remove)
        friend_list.remove_friend(self.user)

    def is_friend(self, account):
        """
        Method used to check whether or not the user account belongs to the 
        current logged in user friends list
        """
        if account in self.friends.all():
            return True

        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_requests_received")
    is_active = models.BooleanField(default=True, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requests"

    def accept(self):

        receiver_list = FriendList.objects.get(user=self.receiver)
        if receiver_list:
            receiver_list.add_friend(self.sender)
            sender_list = FriendList.objects.get(user=self.senders)
            if sender_list:
                sender_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):

        self.is_active = False
        self.save()

    def cancel(self):

        self.is_active = False
        self.save()