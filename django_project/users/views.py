from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
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