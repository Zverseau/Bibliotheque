from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here

# Vue pour l'inscription
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'livre/register.html', {'form': form})

# Vue pour la connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AuthenticationForm()
    return render(request, 'livre/login.html', {'form': form})

# Vue pour la déconnexion
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

@login_required
def home(request):
    livres = Livre.objects.all() 
    return render(request, 'livre/dashboard.html', {'livres': livres})

def ajouterLivre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Le livre a été ajouté avec succès.')
            return redirect('home')
    else:
        form = LivreForm()

    return render(request, 'livre/ajouterLivre.html', {'form': form})

def modifierInfoLivre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Les informations du livre ont été mises à jour avec succès.')
            return redirect('home')
    else:
        form = LivreForm(instance=livre)
    
    return render(request, 'livre/modifierInfoLivre.html', {'form': form})

def livre_detail(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    return render(request, 'livre/livreInfo.html', {'livre': livre}) 

def supprimer_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    livre.delete()
    messages.success(request, f'Le livre "{livre.titre}" a été supprimé avec succès.')
    return redirect('home')


def emprunter_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    if request.method == 'POST':
        form = EmprunterForm(request.POST, request.FILES)
        if form.is_valid():
            emprunt = form.save(commit=False)
            emprunt.livre = livre
            
            emprunt.save()
            
            # Décrémenter le nombre de livres en stock
            livre.nbr_en_stock -= 1
            livre.save()
            
            messages.success(request, 'Livre emprunté avec succès.')
            return redirect('home')
    else:
        form = EmprunterForm()

    return render(request, 'livre/emprunterLivre.html', {'form': form, 'livre': livre})


def modifier_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunter, id=emprunt_id)
    
    if request.method == 'POST':
        form = EmprunterForm(request.POST, request.FILES, instance=emprunt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Les informations de l\'emprunt ont été mises à jour avec succès.')
            return redirect('liste_emprunteurs')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = EmprunterForm(instance=emprunt)
    
    return render(request, 'livre/modifierEmprunt.html', {'form': form, 'emprunt': emprunt})


def liste_emprunteurs(request):
    emprunts = Emprunter.objects.all()
    return render(request, 'livre/emprunteur_info.html', {'emprunts': emprunts})
