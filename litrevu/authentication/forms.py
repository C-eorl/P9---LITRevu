from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class SignupForm(UserCreationForm):
    """Custom form for creating new users"""

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirmer le mot de passe'
        })

class LoginForm(AuthenticationForm):
    """Custom form for logging in"""

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Mot de passe'
        })