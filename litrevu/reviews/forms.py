from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    """Formulaire pour les critiques"""

    # Ajout d'un champ pour créer un ticket en même temps (critique libre)
    ticket_title = forms.CharField(
        max_length=128,
        required=False,
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