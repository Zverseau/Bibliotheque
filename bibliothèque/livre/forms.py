from django import forms
from .models import *

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'nbr_en_stock', 'description', 'isbn', 'photo']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le titre du livre'}),
            'auteur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de l\'auteur'}),
            'nbr_en_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nombre en stock'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez une description du livre', 'rows': 4}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro ISBN'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EmprunterForm(forms.ModelForm):
    class Meta:
        model = Emprunter
        fields = ['nom', 'prenom', 'email', 'telephone', 'photo', 'statut_emprunt', 'date_emprunt', 'date_retour']
        widgets = {
            'date_retour': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_emprunt': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'statut_emprunt': forms.Select(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']