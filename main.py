import random
from game.helpers import hide_word

words = ["corbeau", "amoral", "admission", "humeur", "cadeau", "complice", "bouche", "ballet",
         "pictural", "infini", "messie", "regarder", "tragique", "bastion", "articulation",
         "sabotage", "philosophie", "condition", "oiseau", "compagnie", "pratique"]

mystery_word = random.choice(words).upper()
found_letters = []
hidden_word = hide_word(mystery_word, found_letters)
tries = 7
if len(mystery_word) > 7:
    tries += 2

while hidden_word != mystery_word and tries > 0:
    print(f"Le mot à trouver est {hidden_word}")
    letter_try = input("Quelle lettre souhaitez vous essayer? ").upper()
    if letter_try in mystery_word:
        print("Gagné")
        found_letters.append(letter_try)
        hidden_word = hide_word(mystery_word, found_letters)
    else:
        tries -= 1
        print(f"Perdu. Réessayez! Il vous reste {tries} tentatives")
if hidden_word == mystery_word:
    print(f"Vous avez gagné, le mot était {hidden_word}")
else:
    print(f"Vous avez été pendu, désolé. Le mot à trouver était {mystery_word}")


