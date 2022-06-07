from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from .forms import CustomUserCreationForm, LoginForm


# Create your views here.


def signup(request):
    """
    shows the signup form and registers a new user with the given data
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")

    form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


def login(request):
    """
    authenticates the user if credentials are correct else redirects back to login page
    """
    if request.method == "POST":
        user = auth.authenticate(
            email=request.POST.get("email"), password=request.POST.get("password")
        )
        if user:
            auth.login(request, user)
            return redirect("sales:home")
        else:
            return redirect("login")
    form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout(request):
    """
    logs the user out
    """
    auth.logout(request)
    return redirect("login")
