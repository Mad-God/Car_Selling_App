from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from .forms import  CustomUserCreationForm, LoginForm


# Create your views here.

def signup(request):
    form = CustomUserCreationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")

    form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email = email, password = password)
        if user:
            auth.login(request, user)
            return redirect("sales:home")
        else:
            return redirect('login')
    form = LoginForm()
    return render(request, "registration/login.html", {"form":form})


def logout(request):
    auth.logout(request)
    return redirect("login")