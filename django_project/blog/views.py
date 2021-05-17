from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Post, Comment, Favorite, Like
from .forms import CommentForm, PostForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
# ? ! * TODO Create your views here.
# TODO extensions to use:
# * Duplicate action
# * Better comments
# * profile switcher
# * Settings Sync


@login_required
def HomeView(request):
    searchValue = request.GET.get('search', False)
    if searchValue:
        query = Q(title__icontains=searchValue) | Q(
            content__icontains=searchValue)
        posts = Post.objects.filter(
            query).select_related().order_by('-updated_at')
        number = 20
    else:
        posts = Post.objects.all().order_by('-updated_at')
        number = 5

    paginator = Paginator(posts, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # users section
    all_users = set(User.objects.all().exclude(id=request.user.id))
    following = set(request.user.profile.following.all())
    users = all_users.difference(following)
    # trending Section
    last_week_day = timezone.now() - timedelta(days=30)
    trending = Post.objects.filter(updated_at__gte=last_week_day).annotate(
        c_count=Count("comments", distinct=True)).annotate(l_count=Count("likes", distinct=True)).order_by("-c_count", "-l_count")[:5]
    print(trending)
    context = {
        "searchValue": searchValue, 
        "search": True,
        'page_obj': page_obj,
        #excluir los que no se sigan
        # incluir en el perfil etiquetas de intereses y hacer un match
        'users': list(users),
        'favorites': request.user.all_favs.all(),
        "liked": request.user.all_liked.all(),
        "trending": trending
        }
    return render(request, 'blog/home.html', context)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content', 'image']
    template_name = "blog/form.html"
    form_class = PostForm
    success_url = reverse_lazy('blog:home')

    # ? https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/form.html"
    form_class = PostForm


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:detail', args=[self.object.id])

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/delete.html"
    success_url = reverse_lazy('blog:home')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class PostDetailView(View):
    def get(self, request, pk):
        # TODO Podría agregar un feature para buscar los comentarios con la searchbar
        # También se puede usar una create view con contexto extra
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()
        paginator = Paginator(comments, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cmt_number = len(comments)
        if cmt_number == 0:
            cmt_number = ""
        
        likes_number = len(post.likes.all())
        if likes_number == 0:
            likes_number = ""

        context = {'post': post, "comment_form": form, "comments": page_obj, 
        "cmt_number": cmt_number, "likes": likes_number}
        return render(request, 'blog/detail.html', context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('blog:detail', args=[pk]))

        context = {'post': post, "comment_form": form}
        return render(request, 'blog/detail.html', context)

class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        # post_id = comment.post.id
        comment.delete()
        # return redirect(reverse('blog:detail', args=[post_id]))
        return HttpResponse()

def CommentUpdateView(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post = comment.post
    form = CommentForm(request.POST, instance=comment)

    if form.is_valid():
        form.save()
        return redirect(reverse('blog:detail', args=[post.id]))
    
    comments = Comment.objects.filter(post=post)
    context = {'post': post, "comment_form": form, "comments": comments}
    return render(request, 'blog/detail.html', context)
    

class MarkFav(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            fav = Favorite(user=request.user, post=post)
            fav.save()
        except:
            pass
        return HttpResponse()

class UnMarkFav(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try: 
            fav = Favorite.objects.get(user=request.user, post=post)
            fav.delete()
        except:
            pass
        return HttpResponse()

class FavoritesView(LoginRequiredMixin, View):
    def get(self, request):
        posts = request.user.all_favs.all().order_by('-updated_at')
        all_users = set(User.objects.all().exclude(id=request.user.id))
        following = set(request.user.profile.following.all())
        users = all_users.difference(following)
        context = {"page_obj": posts, "users": list(
            users), "favorites": request.user.all_favs.all(), "liked": request.user.all_liked.all()}
        return render(request, "blog/home.html", context)


class LikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like(user=request.user, post=post)
            like.save()
        except:
            pass
        return HttpResponse()


class UnLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
        except:
            pass
        return HttpResponse()
