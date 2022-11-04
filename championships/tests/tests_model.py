from django.test import TestCase
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from championships.models import Championship
from games.models import Game

client = APIClient()

class ChampionshipModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_staff = {
            "username": "Gustavo",
            "nickname": "Buiu",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "gustavo@email.com",
            "is_player": False,
            "is_staff": True,
        }
        cls.championship = {
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e-sport": "Valorant",
            "entry_amount": 10.0,
            "prize": 75.0
        }
        
    def test_create_champ_model(self):
        #testar se cria 11 jogos
            #testar se jogos estão vazios
        #testar relacionamento com user, se retorna staff_owner_id
        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.post("/api/championships/register/", self.championship)

        champ = Championship.objects.get(staff_owner=user)

        games_queryset_size = champ.games.count()
        game_instance = champ.games.last()
        
        self.assertEqual(11, games_queryset_size)
        self.assertIsInstance(game_instance, Game)
        self.assertEqual(201, response.status_code)

