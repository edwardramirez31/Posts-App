from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from .models import Post
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# ? ! * TODO Create your views here.
# TODO extensions to use:
# * Duplicate action
# * Better comments
# * profile switcher
# * Settings Sync

def HomeView(request):
    searchValue = request.GET.get('search', False)
    if searchValue:
        query = Q(title__icontains=searchValue) | Q(content__icontains=searchValue)
        posts = Post.objects.filter(query).select_related().order_by('-updated_at')
    else:
        posts = Post.objects.all().order_by('-updated_at')
    # posts = False
    context = {'posts': posts, "searchValue": searchValue, "search":True}
    return render(request, 'blog/home.html', context)

def AboutView(request):
    pass

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/form.html"
    success_url = reverse_lazy('blog:home')

    # ? https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/form.html"
    success_url = reverse_lazy('blog:home')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {'post': post}
        return render(request, 'blog/detail.html', context)