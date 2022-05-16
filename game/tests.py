from django.test import TestCase, Client

from user.models import User


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username="Pampa",
            password="pampass",
            played_games=20,
            won_games=19,
            streak=6,
        )

    def test_home_page(self):

        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Page d'accueil</title>")
        self.assertTemplateUsed(response, "index.html")

    def test_login(self):
        response = self.client.post('/login', {'username': 'Pampa', 'password': 'pampass'})
        self.assertEqual(response.status_code, 200)

    def test_run_game(self):
        self.client.login(username='Pampa', password='pampass')
        response = self.client.get("/pendu")
        mystery_word = response.context["game"].mystery_word
        unique_letters = set(mystery_word)
        self.assertContains(response, "<p>Bonjour Pampa</p>")
        for letter in unique_letters:
            game_response = self.client.post('/pendu', {'letter_try': letter})
        self.assertContains(game_response, f"<p>Vous avez gagné, le mot était {mystery_word}</p>")
        self.assertContains(game_response, "Vous venez d'obtenir le badge Confirmé")
        self.assertContains(game_response, "<p>Vous venez d'obtenir le badge spécial Voltaire</p>")
