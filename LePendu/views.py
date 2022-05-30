import uuid

from django.contrib.auth import authenticate, logout, login
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

from LePendu.forms import LetterForm
from game.helpers import check_for_badges, check_for_special_badges
from game.models import Game
from user.models import User, Badge


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
        user = authenticate(username=username, password=pass1)
        login(request, user)
        return redirect('pendu')
    elif pass1 != pass2:
        signup_warning = "La confirmation du mot de passe ne correspond pas. Réessayez"
        return render(request, 'login.html', locals())

    else:
        signup_warning = "Username déjà existant. Réessayez"
        return render(request, 'login.html', locals())


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
        connect_warning = "Ce compte n'existe pas ou le mot de passe est invalide"
        return render(request, 'login.html', locals())


def logout_user(request):
    logout(request)
    return redirect('/')


def pendu_view(request):
    if request.method == "GET":
        user_game = uuid.uuid4().hex
        game = Game(request.user)
        game.hide_word()
        cache.set(f"game{user_game}", game)
        form = LetterForm()

        return render(request,
                      'pendu.html', locals())
    elif request.method == "POST":
        user_game = request.POST.get("user_game_id")
        form = LetterForm(request.POST)
        game = cache.get(f"game{user_game}")

        if form.is_valid():
            letter_try = request.POST.get("letter_try").upper()
            result = game.run_game(letter_try)
            form = LetterForm()
            cache.set(f"game{user_game}", game)
            print(game.mystery_word, ",", game.found_letters, ",", game.hidden_word)

            if game.hidden_word == game.mystery_word:
                restart = True
                if request.user.is_authenticated:
                    badge = check_for_badges(request.user)
                    special_badges = check_for_special_badges(request.user)

            elif game.tries == 0:
                restart = True
                if request.user.is_authenticated:
                    badge = check_for_badges(request.user)
                    special_badges = check_for_special_badges(request.user)

            return render(request,
                          'pendu.html', locals())
        else:
            return render(request,
                          'pendu.html', locals())


def ranking_view(request):
    players = User.objects.all()
    players = players.difference(User.objects.filter(username="superadmin"))
    sorted_players = sorted(players, key=lambda player: player.win_rate, reverse=True)
    return render(request,
                  'ranking.html', locals())


def profile_view(request):
    badges = Badge.objects.filter(owner=request.user)
    return render(request,
                  'profile.html', locals())
