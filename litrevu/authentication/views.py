from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import CreateView

from .forms import SignupForm, LoginForm
from .models import User


def redirection(request):
    """ function view to redirect to login page """
    if request.user.is_authenticated:
        return redirect('reviews:feed')
    return redirect("authentication:login")


class RedirectAuthenticatedUserMixin:
    """Redirects users who are already logged in"""
    redirect_url = '/reviews/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, self.message_redirection)
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_not_required, name='dispatch')
class CustomLoginView(RedirectAuthenticatedUserMixin, LoginView):
    """ Custom Login View """
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    form_class = LoginForm
    message_redirection = "Vous êtes déjà connecté(e)."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         f"Bienvenue {self.request.user.username}")
        return response


@method_decorator(login_not_required, name='dispatch')
class SignupView(RedirectAuthenticatedUserMixin, CreateView):
    """ Custom Signup View """
    model = User
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    message_redirection = "Vous ne pouvez pas créer un nouveau utilisateur."
    success_url = reverse_lazy('reviews:feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Compte créé avec succès!')
        return response
