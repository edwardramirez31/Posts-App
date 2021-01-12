from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_pic', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(
        User, through='Comment', related_name='posts_comments')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    # related name means, give me all the comments of this user
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_posts_comments")
    # dame todos los comentarios de este post
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='all_comments')
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if len(self.text) > 15:
            return self.text[:15]
        else:
            return self.text
