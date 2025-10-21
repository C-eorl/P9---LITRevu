from django import forms
from .models import Review, Ticket

class TicketForm(forms.ModelForm):
    """Formulaire de base pour les tickets"""
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image'
            })
        }
        labels = {
            'title': 'Titre',
            'description': 'Description',
        }


class ReviewForm(forms.ModelForm):
    """Formulaire de base pour les critiques"""

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre critique'
            }),
            'rating': forms.Select(
                choices=[(i, '★' * i + '☆' * (5 - i)) for i in range(6)],
                attrs={'class': 'form-control'}
            ),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Votre critique'
            })
        }
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire'
        }


class ReviewWithTicketForm(ReviewForm):
    """Formulaire pour créer une critique avec un nouveau ticket"""

    ticket_title = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Titre du livre/article'
        }),
        label='Titre'
    )
    ticket_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Description (optionnel)'
        }),
        label='Description'
    )
    ticket_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        label='Image'
    )

    class Meta(ReviewForm.Meta):
        pass

    def save(self, commit=True, user=None):
        """Crée le ticket et la review en une seule transaction"""

        # Créer le ticket
        ticket = Ticket.objects.create(
            title=self.cleaned_data['ticket_title'],
            description=self.cleaned_data.get('ticket_description', ''),
            image=self.cleaned_data.get('ticket_image'),
            user=user
        )

        # Créer la review
        review = super().save(commit=False)
        review.ticket = ticket
        review.user = user

        if commit:
            review.save()

        return review
