from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
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
        form.save()
        return redirect('blog:home')


from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile has been updated.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, 'users/profile.html', context)

# This method creates and saves a database object from the data bound to the form. A subclass of ModelForm can accept an existing model instance as the keyword argument instance; if this is supplied, save() will update that instance. If it’s not supplied, save() will create a new instance of the specified model: