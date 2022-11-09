from django.test import TestCase
from users.models import User
from championships.models import Championship
from teams.models import Team
from games.models import Game
from bets.models import Bet
import ipdb
import math
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from historys.models import History

client = APIClient()


class BetTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_data = {
            "username": "Shiryu",
            "nickname": "vshiryu",
            "password": "1234",
            "birthday": "1995-05-15",
            "email": "kkk@kkk.com",
            "is_player": False,
            "is_staff": True,
        }

        cls.championship_data = {
            "name": "CS:GO Major",
            "initial_date": "2023-01-01",
            "e_sport": "Counter Strike",
            "entry_amount": 0,
            "prize": 100000,
        }

        cls.players_data = [
            {
                "username": f"player{i}",
                "nickname": f"Player{i}",
                "password": "1234",
                "birthday": "1995-05-15",
                "email": f"kkk{i}@kkk.com",
                "is_player": True,
            }
            for i in range(40)
        ]

        cls.teams_data = [
            {
                "name": f"Team{i}",
                "initials": f"TM{i}",
                "wins": 0,
                "losses": 0,
                "e_sport": "Counter Strike",
            }
            for i in range(8)
        ]

        cls.user_staff = User.objects.create_user(**cls.staff_data)

        cls.teams = []
        for item in cls.teams_data:
            cls.teams.append(Team.objects.create(**item))

        cls.players = []
        for i, item in enumerate(cls.players_data):
            cls.players.append(
                User.objects.create_user(**item, team=cls.teams[math.floor(i / 5)])
            )
            History.objects.create(user=cls.players[i])

    def test_bet_auto_create(self):
        token_staff = Token.objects.create(user=self.user_staff)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")

        championship_data = client.post(
            "/api/championships/register/", self.championship_data
        ).data

        championship = Championship.objects.get(id=championship_data["id"])
        teams = Team.objects.all()

        for team in teams:
            owner_team = team.users.all()[0]
            owner_team.is_team_owner = True
            owner_team.save()

        for i in range(8):
            token_owner = Token.objects.create(user=self.players[i * 5])
            client.credentials(HTTP_AUTHORIZATION=f"Token {token_owner}")
            client.patch(
                f"/api/championships/{championship.id}/add-teams/{teams[i].id}/"
            )

        games = Game.objects.filter(championship=championship)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        client.put(
            f"/api/games/{games[0].id}/",
            {
                "team_1": championship.teams.all()[0].id,
                "team_2": championship.teams.all()[1].id,
                "initial_date": "2023-01-02",
            },
        )

        bets = Bet.objects.all()

        self.assertEqual(1, len(bets))
