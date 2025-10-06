from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm
from .models import User

def redirection(request):
    if request.user.is_authenticated:
        return redirect('reviews:feed')
    return redirect("authentication:login")

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('reviews:feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Compte créé avec succès!')
        return response