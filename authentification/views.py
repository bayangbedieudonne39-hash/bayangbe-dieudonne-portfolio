# authentification/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 1. Page de Connexion
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Accès accordé. Bienvenue Agent {user.username}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Accès refusé : Identifiant ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()

    return render(request, 'authentification/login.html', {'form': form})

# 2. Page de Création de compte
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Connectez-vous.")
            return redirect('login')
        else:
            messages.error(request, "Erreur lors de la création du compte.")
    else:
        form = UserCreationForm()

    return render(request, 'authentification/register.html', {'form': form})

# 3. Déconnexion
def logout_view(request):
    logout(request)
    messages.info(request, "Session clôturée avec succès.")
    return redirect('login')

# 4. Tableau de bord sécurisé (Page d'accueil après connexion)
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'authentification/dashboard.html')