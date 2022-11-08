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

    def test_tokens(self):

        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)
        player = User.objects.create_user(**self.user_player)
        token_player = Token.objects.create(user=player)
        self.assertTrue(bool(token_staff))
        self.assertTrue(bool(token_player))
    
    def test_create_team_response(self):

        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)
        player = User.objects.create_user(**self.user_player)
        token_player = Token.objects.create(user=player)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.post("/api/teams/", self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_player = client.post("/api/teams/", self.team_model)

        self.assertEqual(201, response.status_code)
        self.assertEqual(201, response_player.status_code)
    
    def test_update_team_response(self):
        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)
        player = User.objects.create_user(**self.user_player)
        token_player = Token.objects.create(user=player)

        team_created_by_staff = Team.objects.create(**self.team_model)

        team_created_by_player = Team.objects.create(**self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.patch(f"/api/teams/{team_created_by_staff.id}/", self.team_model_updated)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_player = client.patch(f"/api/teams/{team_created_by_player.id}/", self.team_model_updated)

        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response_player.status_code)

    def test_staff_delete_team_response(self):
        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        player = User.objects.create_user(**self.user_player)

        team_created_by_staff = Team.objects.create(**self.team_model)
        team_created_by_player = Team.objects.create(**self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_staff_can_delete_its_team_401 = client.delete(f"/api/teams/{team_created_by_staff.id}/")

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_staff_deleting_player_team_204 = client.delete(f"/api/teams/{team_created_by_player.id}/")

        self.assertEqual(204, response_staff_can_delete_its_team_401.status_code)
        self.assertEqual(204, response_staff_deleting_player_team_204.status_code)

    def test_player_delete_team_response(self):

        user = User.objects.create_user(**self.user_staff)
        player = User.objects.create_user(**self.user_player)

        token_player = Token.objects.create(user=player)

        team_created_by_player = Team.objects.create(**self.team_model)
        team_created_by_staff = Team.objects.create(**self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_player_204 = client.delete(f"/api/teams/{team_created_by_player.id}/")

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_staff_403 = client.delete(f"/api/teams/{team_created_by_staff.id}/")

        self.assertEqual(204, response_player_204.status_code)
        self.assertEqual(403, response_staff_403.status_code)

    def test_staff_retrieve_team_response(self):
        user = User.objects.create_user(**self.user_staff)
        token_staff = Token.objects.create(user=user)

        player = User.objects.create_user(**self.user_player)

        team_created_by_staff = Team.objects.create(**self.team_model)

        team_created_by_player = Team.objects.create(**self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_staff_200 = client.get(f"/api/teams/{team_created_by_player.id}/")

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response_staff_player_team_200 = client.get(f"/api/teams/{team_created_by_staff.id}/")

        self.assertEqual(200, response_staff_200.status_code)
        self.assertEqual(200, response_staff_player_team_200.status_code)

    def test_player_retrieve_team_response(self):
        user = User.objects.create_user(**self.user_staff)
        
        player = User.objects.create_user(**self.user_player)
        token_player = Token.objects.create(user=player)

        team_created_by_staff = Team.objects.create(**self.team_model)

        team_created_by_player = Team.objects.create(**self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_player_200 = client.get(f"/api/teams/{team_created_by_player.id}/")

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")
        response_player_staff_team_200 = client.get(f"/api/teams/{team_created_by_staff.id}/")

        self.assertEqual(200, response_player_200.status_code)
        self.assertEqual(200, response_player_staff_team_200.status_code)

    def test_update_teams_members(self):
        user = User.objects.create_user(**self.user_staff)
        player = User.objects.create_user(**self.user_player)
        token_staff = Token.objects.create(user=user)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        team_created_by_staff = Team.objects.create(**self.team_model)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_staff}")
        response = client.patch(f"/api/teams/add/{team_created_by_staff.id}/", data=self.team_users_insert)

        self.assertEqual(200, response.status_code)

    def test_remove_team_from_championship(self):
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
        response_remove_team_from_championship = client.patch(f"/api/championships/remove/{team_id}/champ/{championship_id}/")

        self.assertEqual(204, response_remove_team_from_championship.status_code)


