from django.test import TestCase
from championships.models import Championship

class ChampionshipViewTest(TestCase):
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
        
        cls.user_player = {
            "username": "João",
            "nickname": "JP",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "jp@email.com",
            "is_player": True,
            "is_staff": False,
        }
        
        cls.championship = {
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e-sport": "VALORANT",
            "entry_amount": "$10",
            "prize": "$75"
        }
        #criar users e times, colocar users em times
        
    def test_create_champ_with_wrong_keys(self):
        ...
        
    def test_create_champ_and_relations(self):
        #testar o status code 201
        #testar se not staff consegue criar camp
        #testar length de teams = 0
        #testar length de games = 11
        #testar length de keys() = 9
        ...
    
    def test_champ_edit(self):
        #somente owner, testar se qualquer um pode, testar as chaves que podem ser editadas 
        ...
        
    def test_champ_delete(self):
        #somente owner, testar se qualquer um pode
        ...
        
    def test_list_one_championship_results(self):
        #open
        ...
    
    def test_list_championships(self):
        #open ver chaves
        ...
        
    def test_edit_put_team_in_camp(self):
        #somente owner do time, 
        # time precisa ter no minimo 5 players
        #não pode entrar se tiver em outro camp no raio de 7 dias
        #verificar se tirou dinheiro do owner
        ...