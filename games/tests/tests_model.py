from games.models import Game, Phase, Names
from django.test import TestCase


class GameModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game_data = {
            "name": "Game 1",
            "phase": "Quartas Upper",
        }

        cls.game = Game.objects.create(**cls.game_data)

    def test_game_fields(self):
        self.assertEqual(self.game.name, self.game_data["name"])
        self.assertEqual(self.game.phase, self.game_data["phase"])
        self.assertIsNone(self.game.winner)
        self.assertIsNone(self.game.result_team_1)
        self.assertIsNone(self.game.result_team_2)
        self.assertIsNone(self.game.team_1)
        self.assertIsNone(self.game.team_2)

    def test_game_name_choices(self):
        choices = [obj.value for obj in (Names)]
        self.assertIn(self.game.name, choices)

    def test_game_phase_choices(self):
        choices = [obj.value for obj in (Phase)]
        self.assertIn(self.game.phase, choices)
