from random import choice

from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=12)


def pick_word():
    words_dict = Word.objects.all()
    words = []
    for word in words_dict:
        words.append(word.word)
    mystery_word = choice(words).upper()
    return mystery_word


class Game:
    def __init__(self, player, mystery_word="", hidden_word="", tries=7, found_letters=None,
                 tried_letters=None):

        self.player = player
        if mystery_word == "":
            mystery_word = pick_word()
        self.mystery_word = mystery_word
        self.hidden_word = hidden_word
        self.tries = tries
        if found_letters is None:
            found_letters = []
        self.found_letters = found_letters
        if tried_letters is None:
            tried_letters = []
        self.tried_letters = tried_letters

    def hide_word(self):
        hidden_word = self.mystery_word
        for letter in hidden_word:
            if letter not in self.found_letters:
                hidden_word = hidden_word.replace(letter, " _")
        self.hidden_word = hidden_word

    def run_game(self, letter_try):
        if letter_try not in self.tried_letters:
            self.tried_letters.append(letter_try)
        else:
            result = "Vous avez déjà essayé cette lettre"
            return result

        if letter_try in self.mystery_word:
            self.found_letters.append(letter_try)
            self.hide_word()
            if self.hidden_word == self.mystery_word:
                result = f"Vous avez gagné, le mot était {self.mystery_word}"
                if self.player.is_authenticated:
                    self.player.played_games += 1
                    self.player.won_games += 1
                    self.player.streak += 1
                    self.player.save()
                return result
            else:
                result = "Gagné"
                return result
        else:
            self.tries -= 1
            if self.tries == 0:
                result = f"Vous avez été pendu, désolé. Le mot à trouver était {self.mystery_word}"
                if self.player.is_authenticated:
                    self.player.played_games += 1
                    self.player.streak = 0
                    self.player.save()
                return result
            else:
                if self.tries > 1:
                    result = f"Perdu. Réessayez! Il vous reste {self.tries} tentatives"
                    return result
                else:
                    result = f"Perdu. Réessayez! Il vous reste {self.tries} tentative"
                    return result
