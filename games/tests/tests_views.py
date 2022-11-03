from rest_framework.test import APIClient
from django.test import TestCase
from users.models import User
from games.models import Game
from championships.models import Championship
from teams.models import Team
from rest_framework.authtoken.models import Token


client = APIClient()


class GamesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game_data = {
            "name": "Game 1",
            "phase": "Quartas Upper",
        }

        cls.championship_data = {
            "name": "CS:GO Major",
            "initial_date": "2023-01-01",
            "e_sport": "Counter Strike",
            "entry_amount": 10,
            "prize": 100000,
        }

        cls.user_staff_data = {
            "username": "Shiryu",
            "nickname": "vshiryu",
            "password": "1234",
            "birthday": "1995-05-15",
            "email": "kkk@kkk.com",
            "is_player": False,
            "is_staff": True,
        }

        cls.user_staff2_data = {
            "username": "Vini",
            "nickname": "vshiryu2",
            "password": "1234",
            "birthday": "1995-05-15",
            "email": "kkkk@kkkk.com",
            "is_player": True,
            "is_staff": True,
        }

        cls.team_data = {
            "name": "Imperial",
            "initials": "IMP",
            "e_sports": "Counter Strike",
        }

        cls.user_staff = User.objects.create_user(**cls.user_staff_data)
        cls.user_staff2 = User.objects.create_user(**cls.user_staff2_data)
        cls.championship = Championship.objects.create(
            **cls.championship_data, staff_owner=cls.user_staff
        )
        cls.team = Team.objects.create(**cls.team_data)
        cls.game = Game.objects.get_or_create(**cls.game_data)[0]

    def test_edit_game_staff(self):
        token_staff = Token.objects.create(user=self.user_staff)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")

        response = client.patch(
            f"/api/championships/{self.championship.id}/games/{self.game.id}",
            {"team_1": {self.team}},
        )

        self.assertEqual(200, response.status_code)

    def test_edit_game_another_staff(self):
        token_staff2 = Token.objects.create(user=self.user_staff2)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff2}")

        response = client.patch(
            f"/api/championships/{self.championship.id}/games/{self.game.id}",
            {"team_1": {self.team}},
        )

        self.assertEqual(403, response.status_code)

    def test_delete_game_staff(self):
        token_staff = Token.objects.create(user=self.user_staff)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")

        response = client.delete(
            f"/api/championships/{self.championship.id}/games/{self.game.id}"
        )

        self.assertEqual(204, response.status_code)

    def test_delete_game_another_staff(self):
        token_staff2 = Token.objects.create(user=self.user_staff2)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff2}")

        response = client.delete(
            f"/api/championships/{self.championship.id}/games/{self.game.id}"
        )

        self.assertEqual(403, response.status_code)
