from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

post_list = [
    {
        'author': 'Edward Ramirez',
        'Title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Aug 12 2016'
    },
    {
        'author': 'Ward',
        'Title': 'Django Tutorial',
        'content': 'In this tutorial I\'m covering the templates',
        'date_posted': 'Aug 13 2016'
    }

]


def home(request):
    # Mediante la llave post list voy a acceder a un objeto python
    # Que en este caso es una lista de diccionarios
    context = {
        'post_list': post_list

    }
    return render(request, 'blog/home.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)
