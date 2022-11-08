from rest_framework.test import APITestCase
from users.models import User
from ..models import Team
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import ipdb

client = APIClient()

class TeamViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

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
            "birthday": "2000-04-10",
            "email": "jp@email.com",
            "is_player": True,
            "is_staff": False,
        }
        
        cls.team_model = {
            'name': 'Pain Gaming',
            'initials': 'PNG',
            'e_sport': 'Valorant'
        }

        cls.team_model_updated = {
            'name': 'Pain',
            'initials': 'PNG',
            'e_sport': 'Valorant'
        }

        cls.team_users_insert = {
            'username': 'João'
        }

        cls.championship = {
            "name": "VALORANT $75 PRIZE",
            "initial_date": "2022-11-22",
            "e_sport": "Valorant",
            "entry_amount": 10.0,
            "prize": 75.0
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

        cls.players_to_add = {
            "username": "Carlos",
            "username1": "Pedro",
            "username2": "Roberta",
            "username3": "Clara",
            "username4": "Jonas",
        } 

        cls.transaction = {
            "value": 1000
        }

        def test_historys_exists(self):

            staff = User.objects.create_user(**self.user_staff)

            response_create_player = client.post("/api/users/register/", self.user_player)
            response_create_player1 = client.post("/api/users/register/", self.user_player1)
            response_create_player2 = client.post("/api/users/register/", self.user_player2)
            response_create_player3 = client.post("/api/users/register/", self.user_player3)
            response_create_player4 = client.post("/api/users/register/", self.user_player4)
            response_create_player5 = client.post("/api/users/register/", self.user_player5)
            response_create_player5 = client.post("/api/users/register/", self.user_player6)

            token_staff = Token.objects.create(user=staff)
            team_owner_id = response_create_player.data["id"]
            team_owner = User.objects.get(id=team_owner_id)
            team_owner_token = Token.objects.create(user=team_owner)


            client.credentials(HTTP_AUTHORIZATION=f"Token {team_owner_token}")
            response_create_team = client.post("/api/teams/register/", self.team_model)

            team_id = response_create_team.data["id"]

            client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
            response_create_championship = client.post(f"/api/championships/register/", data=self.championship)
            
            championship_id = response_create_championship.data["id"]

            client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
            response_inser_players = client.patch(f"/api/teams/add/{team_id}/", data=self.players_to_add)

            client.credentials(HTTP_AUTHORIZATION=f"Token {team_owner_token}")
            response_transaction = client.post(f"/api/transactions/", data=self.transaction)

            client.credentials(HTTP_AUTHORIZATION=f"Token {team_owner_token}")
            response_register_team_in_championship = client.patch(f"/api/championships/{championship_id}/add-teams/{team_id}/")

            client.credentials(HTTP_AUTHORIZATION=f"Token {team_owner_token}")
            response_register_team_in_championship = client.patch(f"/api/teams/remove/{team_id}/")

            client.credentials(HTTP_AUTHORIZATION=f"Token {team_owner_token}")
            response_remove_team_from_championship = client.patch(f"/api/championships/remove/{team_id}/champ/{championship_id}/")