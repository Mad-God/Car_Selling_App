from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import auth
from .forms import CustomUserCreationForm, LoginForm
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

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

class SignupView(CreateView):
    """
    shows the signup form and registers a new user with the given data
    """
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    def get_success_url(self):
        return reverse('login')
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())




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

class LoginPageView(View):
    """
    authenticates the user if credentials are correct else redirects back to login page
    """
    template_name = 'registration/login.html'
    form_class = LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        # if form.is_valid():
        user = auth.authenticate(
            email=self.request.POST.get('email'),
            password=self.request.POST.get('password'),
        )
        if user is not None:
            auth.login(self.request, user)
            return redirect('sales:home')
        # message = 'Login failed!'
        return render(request, self.template_name, context={'form': form})




def logout(request):
    """
    logs the user out
    """
    auth.logout(request)
    return redirect("login")

class Logout(View):
    """
    logs the user out
    """
    def dispatch(self, *args, **kwargs,):
        """
        logs the user out
        """
        auth.logout(self.request)
        return redirect("login")

