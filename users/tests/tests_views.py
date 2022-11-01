from rest_framework.test import APIClient
from django.test import TestCase
from users.models import User
import ipdb
import json

client = APIClient()

class UsersViewTest(TestCase):
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
        cls.user_staff_login = {
            "username": "Gustavo",
            "password": "1234",
        }
        cls.user_staff_response = {
            "username": "Gustavo",
            "nickname": "Buiu",
            "birthday": "2000-05-22",
            "balance": 0.00,
            "email": "gustavo@email.com",
            "is_player": False,
            "is_staff": True,
            "is_active": True
            # "team_id": None,
        }
        cls.user_staff_patch = {
            "nickname": "Buiuzinho",
        }
        cls.user_activiy_patch = {
            "is_active": False,
        }
        cls.user_activiy_patch_true = {
            "is_active": True,
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
        cls.user_player_2 = {
            "username": "Pedro",
            "nickname": "PJPJ",
            "password": "1234",
            "birthday": "2000-04-10",
            "email": "pj@email.com",
            "is_player": True,
            "is_staff": False,
        }
        cls.user_player_login = {
            "username": "João",
            "password": "1234",
        }
        
    def test_user_create_properly(self):
        """
            Testing if user creating is correct
        """
        response = client.post('/api/users/register/', self.user_staff)
        msg_1 = 'Testing account creation'
        msg_2 = "Testing if created account equals to original"
        self.assertEqual(response.status_code, 201, msg_1)
        self.user_staff_response['id'] = response.data['id']
        self.assertDictEqual(response.data, self.user_staff_response, msg_2)
        
        
    def test_login(self):
        user = User.objects.create(**self.user_staff)
        user.set_password('1234')
        user.save()
        response = client.post('/api/login/', self.user_staff_login)
        msg = "Test if login's status code equals 200"
        self.assertEqual(response.status_code, 200, msg)
        
    def test_user_edit_properly(self):
        """
            Testing if user editing is correct AND if only owner
            can edit profile
        """
        msg = "Test if user editing's status code equals 200"
        msg_1 = "Test if current changes persisted"
        msg_2 = "Test if others can edit one profile"
        
        user_staff_created = User.objects.create(**self.user_staff)
        user_staff_created.set_password('1234')
        user_staff_created.save()
        
        response_login_staff = client.post('/api/login/', self.user_staff_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_staff.json()['token'])
        
        response_patch = client.patch(f"/api/users/{user_staff_created.id}/", self.user_staff_patch)
        
        self.assertEqual(response_patch.status_code, 200, msg)
        self.assertEqual(response_patch.json()['nickname'], self.user_staff_patch['nickname'], msg_1)
        
        user_player_created = User.objects.create(**self.user_player)
        user_player_created.set_password('1234')
        user_player_created.save()
        
        response_login_player = client.post('/api/login/', self.user_player_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_player.json()['token'])
        
        response_patch_2 = client.patch(f"/api/users/{user_staff_created.id}/", self.user_staff_patch)
        self.assertEqual(response_patch_2.status_code, 403, msg_2)
        
        
        
    def test_correct_soft_delete(self):
        """
            Testing if owner can soft delete himself AND staff too
        """
        msg_1 = "Test if others can change it's activity"
        msg = "Test if owner can change it's activity"
        msg_3 = "Test if user's activity has changed to false"
        msg_2 = "Test if staff can change other's activity"
        
        user_staff_created = User.objects.create(**self.user_staff)
        user_staff_created.set_password('1234')
        user_staff_created.save()
        
        user_player_created = User.objects.create(**self.user_player)
        user_player_created.set_password('1234')
        user_player_created.save()
        
        user_player2_created = User.objects.create(**self.user_player_2)
        user_player2_created.set_password('1234')
        user_player2_created.save()
        
        response_login_player = client.post('/api/login/', self.user_player_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_player.json()['token'])
        
        response_patch = client.patch(f"/api/users/{user_player2_created.id}/activity/", self.user_activiy_patch)
        self.assertEqual(response_patch.status_code, 403, msg_1)
        
        response_patch_2 = client.patch(f"/api/users/{user_player_created.id}/activity/", self.user_activiy_patch)
        self.assertEqual(response_patch_2.status_code, 200, msg)
        self.assertEqual(response_patch_2.json()['is_active'], False, msg_3)
        
        response_login_staff = client.post('/api/login/', self.user_staff_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_staff.json()['token'])
        
        response_patch_3 = client.patch(f"/api/users/{user_player2_created.id}/activity/", self.user_activiy_patch)
        self.assertEqual(response_patch_3.status_code, 200, msg_2)
        self.assertEqual(response_patch_3.json()['is_active'], False, msg_3)
        
        
        
        
        
        
    def test_correct_list_users(self):
        """
            Testing if listing is correct AND only staff can list,
            response without balance
        """
        msg = "Testing if not staff can list users"
        msg_1 = "Testing if staff can list users"
        msg_2 = "Testing length of list result"
        msg_3 = "Testing if list result has balance key"
        
        user_staff_created = User.objects.create(**self.user_staff)
        user_staff_created.set_password('1234')
        user_staff_created.save()
        
        user_player_created = User.objects.create(**self.user_player)
        user_player_created.set_password('1234')
        user_player_created.save()
        
        response_login_player = client.post('/api/login/', self.user_player_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_player.json()['token'])
        
        response_list = client.get('/api/users/')
        self.assertEqual(response_list.status_code, 403, msg)
        
        response_login_staff = client.post('/api/login/', self.user_staff_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_staff.json()['token'])
        
        response_list_2 = client.get('/api/users/')
        # ipdb.set_trace()
        has_balance = False
        if "balance" in response_list_2.json()[0].keys():
            has_balance = True
             
        
        self.assertEqual(response_list_2.status_code, 200, msg_1)
        self.assertEqual(len(response_list_2.json()), 2, msg_2)
        self.assertEqual(has_balance, False, msg_3)
        
    def test_list_one_user(self):
        """
            Testing if one user listing is correct AND only owner can do it,
            response with balance
        """
        
        msg = "Testing if anyone can list one user"
        msg_1 = "Testing user can list himself"
        msg_2 = "Testing if user list object has balance"
        
        user_staff_created = User.objects.create(**self.user_staff)
        user_staff_created.set_password('1234')
        user_staff_created.save()
        
        user_player_created = User.objects.create(**self.user_player)
        user_player_created.set_password('1234')
        user_player_created.save()
        
        response_login_staff = client.post('/api/login/', self.user_staff_login)
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_staff.json()['token'])
        
        response_list = client.get(f"/api/users/{user_player_created.id}/")
        self.assertEqual(response_list.status_code, 403, msg)
        
        response_list_2 = client.get(f"/api/users/{user_staff_created.id}/")
        # ipdb.set_trace()
        
        self.assertEqual(response_list_2.status_code, 200, msg_1)
        self.assertEqual(response_list_2.json()['balance'], 0.0, msg_2)