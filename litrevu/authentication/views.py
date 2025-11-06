from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .forms import SignupForm
from .models import User


def redirection(request):
    """ function view to redirect to login page """
    if request.user.is_authenticated:
        return redirect('reviews:feed')
    return redirect("authentication:login")


@login_not_required
class CustomLoginView(LoginView):
    """ Custom Login View """
    template_name = "authentication/login.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Redirects an already logged-in user to the feed page.
        """
        if request.user.is_authenticated:
            messages.info(request, "Vous êtes déjà connecté !")
            return redirect('reviews:feed')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         f"Bienvenue {self.request.user.username}")
        return response


@login_not_required
class SignupView(CreateView):
    """ Custom Signup View """
    model = User
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('reviews:feed')

    def dispatch(self, request, *args, **kwargs):
        """
        Redirects an already logged-in user to the feed page.
        """
        if request.user.is_authenticated:
            messages.info(request, "Vous êtes déjà connecté !")
            return redirect('reviews:feed')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Compte créé avec succès!')
        return response
