from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts
# Create your views here.


def home(request):
    # Mediante la llave post list voy a acceder a un objeto python
    # Que en este caso es una lista de diccionarios
    context = {
        'post_list': Posts.objects.all()

    }
    return render(request, 'blog/home.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)
