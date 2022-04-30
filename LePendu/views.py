import random

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

from helpers import hide_word
from user.models import User


def home_view(request):
    return render(request, 'index.html')


def create_user(request):
    username = request.POST.get("register_name")
    pass1 = request.POST.get("pass1")
    pass2 = request.POST.get("pass2")
    if pass1 == pass2 and not username_exists(username):
        User.objects.create_user(username, '', pass1)
        return HttpResponse(
            "Votre compte a été créé. Connectez vous via l'écran de connexion")
    elif pass1 != pass2:
        return HttpResponse(
            "La confirmation du mot de passe ne correspond pas. Réessayez")
    else:
        return HttpResponse("Username déjà existant. Réessayez")


def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


def log_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('pendu')
    else:
        return HttpResponse("Compte invalide. Réessayez")


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def pendu_view(request):
    if request.method == "GET":
        words = ["corbeau", "amoral", "admission", "humeur", "cadeau", "complice", "bouche",
                 "ballet",
                 "pictural", "infini", "messie", "regarder", "tragique", "bastion", "articulation",
                 "sabotage", "philosophie", "condition", "oiseau", "compagnie", "pratique"]

        mystery_word = random.choice(words).upper()
        found_letters = []
        hidden_word = hide_word(mystery_word, found_letters)
        tries = 7
        cache.set_many({'mystery_word': mystery_word,
                        'hidden_word': hidden_word, 'tries': tries,
                        'found_letters': found_letters})
        if len(mystery_word) > 7:
            tries += 2
        return render(request,
                      'pendu.html', context={'mystery_word': mystery_word,
                                             'hidden_word': hidden_word, 'tries': tries,
                                             'found_letters': found_letters})
    elif request.method == "POST":
        letter_try = request.POST.get("letter_try").upper()
        mystery_word = cache.get("mystery_word")
        found_letters = cache.get("found_letters")
        hidden_word = cache.get("hidden_word")
        tries = cache.get("tries")
        print(mystery_word, ",", found_letters, ",", hidden_word)
        if letter_try in mystery_word:
            result = "Gagné"
            found_letters.append(letter_try)
            hidden_word = hide_word(mystery_word, found_letters)
            cache.set_many({'mystery_word': mystery_word,
                            'hidden_word': hidden_word, 'tries': tries,
                            'found_letters': found_letters})

        else:
            tries -= 1
            result = f"Perdu. Réessayez! Il vous reste {tries} tentatives"
            cache.set_many({'mystery_word': mystery_word,
                            'hidden_word': hidden_word, 'tries': tries,
                            'found_letters': found_letters})

        if hidden_word == mystery_word:
            result = f"Vous avez gagné, le mot était {hidden_word}"
            restart = True
        elif tries == 0:
            result = f"Vous avez été pendu, désolé. Le mot à trouver était {mystery_word}"
            restart = True

        return render(request,
                      'pendu.html', locals())
