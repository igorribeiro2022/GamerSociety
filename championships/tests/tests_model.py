from django.test import TestCase
from championships.models import Championship

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
            "e-sport": "VALORANT",
            "entry_amount": "$10",
            "prize": "$75"
        }
        
    def test_create_champ_model(self):
        #testar se cria 11 jogos
            #testar se jogos estão vazios
        #testar relacionamento com user, se retorna staff_owner_id
        ...