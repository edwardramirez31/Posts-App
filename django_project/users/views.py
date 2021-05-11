from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from .models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
class Register(View):
    def get(self, request):
        form = RegisterForm()
        context = {"form": form}
        return render(request, "users/register.html", context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, "users/register.html", context)
        
        username = form.cleaned_data["username"]
        messages.success(request, f'Account created for {username}. Please, Log in')
        form.instance.is_staff = True
        form.save()
        return redirect('blog:home')



@login_required
def profile(request, pk):
    profile = get_object_or_404(User, pk=pk)
    followers = profile.all_followers.all()
    following = profile.profile.following.all()
    posts = profile.post_set.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"user_": profile, "page_obj": page_obj, "followers": followers, "following": following}
    return render(request, 'users/profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            left = float(request.POST.get('x'))
            top = float(request.POST.get('y'))
            right = left + float(request.POST.get('width'))
            bottom = top + float(request.POST.get('height'))
            coords = (left, top, right, bottom)
            user_form.save()
            instance = profile_form.save(commit=False)
            instance.save(coordinates=coords)
            messages.success(request, f'Your profile has been updated.')
            return redirect(reverse('profile', args=[request.user.id]))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, 'users/update_profile.html', context)


def follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user=request.user)
    profile.following.add(user)
    return HttpResponse()

def unFollow(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user=request.user)
    profile.following.remove(user)
    return HttpResponse()

def profiles(request):
    search_value = request.GET.get('search', False)
    if search_value:
        query = Q(username__icontains=search_value) | Q(email__icontains=search_value)
        users = User.objects.filter(query).select_related()
    else:
        profile = Profile.objects.get(user=request.user)
        all_users = set(User.objects.all().exclude(username=request.user.username))
        following = set(profile.following.all())
        users = all_users.difference(following)
        
    context = {'users': users}
    return render(request, 'users/profiles.html', context)
