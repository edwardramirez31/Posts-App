from django.shortcuts import render
from django.views import View
from .models import Post
# Create your views here.

def HomeView(request):
    posts = Post.objects.all()
    # posts = False
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)

def AboutView(request):
    pass