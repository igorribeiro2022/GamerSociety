from django.test import TestCase
from championships.models import Championship
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from users.models import User
import ipdb
from django.forms.models import model_to_dict
from games.models import Game
from teams.models import Team

client = APIClient()

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

        cls.user_staff2 = {
            "username": "Ricardo",
            "nickname": "Ricardinho",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "ricardo@email.com",
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

        cls.user_player1 = {
            "username": "Ana",
            "nickname": "Anah",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "ana@email.com",
            "is_player": True,
            "is_staff": False,
        }

        cls.user_player2 = {
            "username": "Pedro",
            "nickname": "Pedrol",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "pedro@email.com",
            "is_player": True,
            "is_staff": False,
        }

        cls.user_player3 = {
            "username": "Roberta",
            "nickname": "Rooh",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "roberta@email.com",
            "is_player": True,
            "is_staff": False,
        }

        cls.user_player4 = {
            "username": "Clara",
            "nickname": "Clarinha",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "clara@email.com",
            "is_player": True,
            "is_staff": False,
        }

        cls.user_player5 = {
            "username": "Jonas",
            "nickname": "JN",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "jonas@email.com",
            "is_player": True,
            "is_staff": False,
        }

        cls.user_player6 = {
            "username": "Carlos",
            "nickname": "Carlitos",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "carlos@email.com",
            "is_player": True,
            "is_staff": False,
        }
        
        cls.championship = {
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e-sport": "Valorant",
            "entry_amount": 10.0,
            "prize": 75.0
        }

        cls.championship_return = {
            "id": str,
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e-sport": "Valorant",
            "winner": str,
            "staff_owner": object,
            "entry_amount": 10.0,
            "prize": 75.0,
            "teams": [Team],
            "games": [Game]
        }

        cls.championship_return_list = {
            "id": str,
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e-sport": "Valorant",
            "winner": str,
            "staff_owner": object,
            "teams": [Team],
            "games": [Game]
        }

        cls.championship_wrong_keys = {
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e-sport": "VALORANT",
            "entry_amount": "$10",
            "prize": "$75"
        }

        cls.team_model = {
            'name': 'Pain Gaming',
            'initials': 'PNG',
            'e_sports': 'League of Legends'
        }

        cls.players_to_add = {
            "username": "Anah",
            "username1": "Pedrol",
            "username2": "Rooh",
            "username3": "Clarinha",
            "username4": "JN",
        }        

        
    def test_create_champ_with_wrong_keys(self):

        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.post("/api/championships/register/", self.championship_wrong_keys)

        self.assertEqual(400, response.status_code)
        
        
    def test_create_champ_and_relations(self):

        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.post("/api/championships/register/", self.championship)

        user_not_staff = User.objects.create_user(**self.user_player)
        token_not_staff = Token.objects.create(user=user_not_staff)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_not_staff}")
        response_not_staff = client.post("/api/championships/register/", self.championship)

        champ = Championship.objects.get(staff_owner=user)

        #testar o status code 201
        self.assertEqual(201, response.status_code)
        #testar se not staff consegue criar camp
        self.assertEqual(403, response_not_staff.status_code)
        #testar length de teams = 0
        self.assertEqual(0, champ.teams.count())
        #testar length de games = 11
        self.assertEqual(11, champ.games.count())
        #testar length de keys() = 9
        expected_champ_keys = list(self.championship_return.keys())
        recieved_champ_keys = response.json().keys()
        self.assertEqual(len(expected_champ_keys), len(recieved_champ_keys))
    
    # Teste retirado devido a não ter a necessidade de edição de um championship - Pedro L, Gustavo.
    # def test_champ_edit(self):
    #     # ipdb.set_trace()
    #     #somente owner, testar se qualquer um pode, testar as chaves que podem ser editadas 
    #     ...
        
    def test_champ_delete(self):
        #somente owner, testar se qualquer um pode
        user_staff = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user_staff)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.post("/api/championships/register/", self.championship)

        champ_id = response.json()["id"]

        user_staff2 = User.objects.create_user(**self.user_staff2)
        token_staff2 = Token.objects.create(user=user_staff2)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff2}")
        response_staff2 = client.delete(f"/api/championships/{champ_id}/management/")

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_staff = client.delete(f"/api/championships/{champ_id}/management/")

        self.assertEqual(403, response_staff2.status_code)
        self.assertEqual(204, response_staff.status_code)
        
    def test_list_one_championship_results(self):

        user_staff = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user_staff)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.post("/api/championships/register/", self.championship)

        champ_id = response.json()["id"]

        response_get = client.get(f"/api/championships/{champ_id}/")

        self.assertEqual(200, response_get.status_code)
    
    def test_list_championships(self):
        #open ver chaves
        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_post = client.post("/api/championships/register/", self.championship)

        response = client.get("/api/championships/list/")

        expected_champ_keys = list(self.championship_return_list.keys())
        recieved_champ_keys = list(response.json()[0].keys())

        self.assertEqual(len(expected_champ_keys), len(recieved_champ_keys))
        
    def test_edit_put_team_in_camp(self):
        #somente owner do time, 
        # time precisa ter no minimo 5 players
        #não pode entrar se tiver em outro camp no raio de 7 dias
        #verificar se tirou dinheiro do owner
        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_post = client.post("/api/championships/register/", self.championship)

        user_player = User.objects.create_user(**self.user_player)
        token_player = Token.objects.create(user=user_player)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_post_team = client.post("/api/teams/", self.team_model)

        team_id = response_post_team.data["id"]
        
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_post_users = client.patch(f"/api/teams/add/{team_id}/", self.players_to_add)

        ipdb.set_trace()
        print("teste")
