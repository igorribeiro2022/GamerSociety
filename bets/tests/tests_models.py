from django.test import TestCase
from users.models import User
from championships.models import Championship
from teams.models import Team
from games.models import Game
from bets.models import Bet
import ipdb


class BetTestModel(TestCase):
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
            "entry_amount": 10,
            "prize": 100000,
        }

        cls.user_staff = User.objects.create_user(**cls.staff_data)

        cls.championship = Championship.objects.create(
            **cls.championship_data, staff_owner_id=cls.user_staff.id
        )

        cls.game_data = {
            "name": "Game 1",
            "phase": "Quartas Upper",
        }

        cls.game = Game.objects.get_or_create(
            **cls.game_data, championship=cls.championship
        )[0]

        cls.bet_data = {
            "team_1": "Furia",
            "team_2": "Imperial",
        }

    def test_create_bet(self):
        """
        Testing create bet model
        """
        bet = Bet.objects.create(**self.bet_data, game=self.game)

        self.assertEqual(self.bet_data["team_1"], bet.team_1)
        self.assertEqual(self.bet_data["team_1"], bet.team_1)
        self.assertEqual(self.game, bet.game)
