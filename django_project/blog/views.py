from django.shortcuts import render
from django.views import View
from .models import Post
from django.db.models import Q
# Create your views here.

def HomeView(request):
    searchValue = request.GET.get('search', False)
    if searchValue:
        query = Q(title__icontains=searchValue) | Q(content__icontains=searchValue)
        posts = Post.objects.filter(query).select_related()
    else:
        posts = Post.objects.all()
    # posts = False
    context = {'posts': posts, "searchValue": searchValue, "search":True}
    return render(request, 'blog/home.html', context)

def AboutView(request):
    pass