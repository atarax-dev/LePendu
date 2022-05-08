import random

from django.contrib.auth import authenticate, logout, login
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

from LePendu.forms import LetterForm
from helpers import hide_word, check_for_badges, check_for_special_badges
from user.models import User


def home_view(request):
    return render(request, 'index.html')


def login_view(request):
    return render(request, 'login.html')


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


def pendu_view(request):
    if request.method == "GET":
        words = ["corbeau", "amoral", "admission", "humeur", "cadeau", "complice", "bouche",
                 "ballet",
                 "pictural", "infini", "messie", "regarder", "tragique", "bastion", "articulation",
                 "sabotage", "philosophie", "condition", "oiseau", "compagnie", "pratique"]

        mystery_word = random.choice(words).upper()
        found_letters = []
        tried_letters = []
        hidden_word = hide_word(mystery_word, found_letters)
        tries = 7
        cache.set_many({'mystery_word': mystery_word,
                        'hidden_word': hidden_word, 'tries': tries,
                        'found_letters': found_letters, 'tried_letters': tried_letters})
        if len(mystery_word) > 7:
            tries += 2
        letter_form = LetterForm()
        if request.user.is_authenticated:
            cache.set_many({'played_games': request.user.played_games,
                            'won_games': request.user.won_games, 'rank': request.user.rank,
                            'streak': request.user.streak})

        return render(request,
                      'pendu.html', context={'mystery_word': mystery_word,
                                             'hidden_word': hidden_word, 'tries': tries,
                                             'found_letters': found_letters, 'form': letter_form,
                                             'tried_letters': tried_letters})
    elif request.method == "POST":
        form = LetterForm(request.POST)
        mystery_word = cache.get("mystery_word")
        found_letters = cache.get("found_letters")
        hidden_word = cache.get("hidden_word")
        tries = cache.get("tries")
        tried_letters = cache.get("tried_letters")
        if request.user.is_authenticated:
            played_games = cache.get("played_games")
            won_games = cache.get("won_games")
            rank = cache.get("rank")
            streak = cache.get("streak")

        if form.is_valid():
            letter_try = request.POST.get("letter_try").upper()
            if letter_try not in tried_letters:
                tried_letters.append(letter_try)
            form = LetterForm()
            print(mystery_word, ",", found_letters, ",", hidden_word)
            if letter_try in mystery_word:
                result = "Gagné"
                found_letters.append(letter_try)
                hidden_word = hide_word(mystery_word, found_letters)
                cache.set_many({'mystery_word': mystery_word,
                                'hidden_word': hidden_word, 'tries': tries,
                                'found_letters': found_letters, 'tried_letters': tried_letters})

            else:
                tries -= 1
                result = f"Perdu. Réessayez! Il vous reste {tries} tentatives"
                cache.set_many({'mystery_word': mystery_word,
                                'hidden_word': hidden_word, 'tries': tries,
                                'found_letters': found_letters, 'tried_letters': tried_letters})

            if hidden_word == mystery_word:
                result = f"Vous avez gagné, le mot était {hidden_word}"
                restart = True
                if request.user.is_authenticated:
                    request.user.played_games += 1
                    request.user.won_games += 1
                    request.user.streak += 1
                    request.user.save()
                    badge = check_for_badges(request.user)
                    special_badge = check_for_special_badges(request.user)

            elif tries == 0:
                result = f"Vous avez été pendu, désolé. Le mot à trouver était {mystery_word}"
                restart = True
                if request.user.is_authenticated:
                    request.user.played_games += 1
                    request.user.streak = 0
                    request.user.save()
                    badge = check_for_badges(request.user)
                    special_badge = check_for_special_badges(request.user)

            return render(request,
                          'pendu.html', locals())
        else:
            return render(request,
                          'pendu.html', locals())


def ranking_view(request):
    players = User.objects.all()
    sorted_players = sorted(players, key=lambda player: player.win_rate, reverse=True)
    return render(request,
                  'ranking.html', locals())


def profile_view(request):
    pass
