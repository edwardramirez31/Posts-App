from django.contrib import admin

# Register your models here.
from .models import Post, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)