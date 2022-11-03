from rest_framework.test import APITestCase
from users.models import User
from ..models import Team
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

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
            'e_sports': 'League of Legends'
        }
        cls.team_model_updated = {
            'name': 'Pain',
            'initials': 'PNG',
            'e_sports': 'Valorant'
        }

        cls.team_users_insert = {
            'username': 'João'
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

        print()
        print("="*50)
        print(response)
        print("="*50)
        print()
