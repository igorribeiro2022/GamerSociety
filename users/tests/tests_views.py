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
            "team_id": None,
        }
        cls.user_staff_patch = {
            "username": "Gustavo",
            "nickname": "Buiu",
            "birthday": "2000-05-22",
            "balance": 0.00,
            "email": "gustavo@email.com",
            "is_player": False,
            "is_staff": True,
            "team_id": None,
        }
        cls.user_player = {
            "username": "Pedro",
            "nickname": "JP",
            "password": "1234",
            "birthday": "2000-04-10",
            "email": "jp@email.com",
            "is_player": True,
            "is_staff": False,
        }
        
    def test_user_create_properly(self):
        """
            Testing if user creating is correct
        """
        response = client.post('/api/users/', self.user_staff)
        msg_1 = 'Testing account creation'
        msg_2 = "Testing if created account equals to original"
        self.assertEqual(response.status_code, 201, msg_1)
        self.user_staff_response['id'] = response.json()['id']
        self.assertEqual(response.json(), json.dumps(self.user_staff_response), msg_2)
        
    def test_login(self):
        user = User.objects.create(**self.account)
        user.set_password('1234')
        user.save()
        response = client.post('/api/login/', self.user_staff_login)
        msg = "Test if login's status code equals 200"
        self.assertEqual(response.status_code, 200, msg)
        self.assertContains(response, text="token")
        
    def test_user_edit_properly(self):
        """
            Testing if user editing is correct AND if only owner
            can edit profile
        """
        response = client.patch('/api/users/', self.user_staff)
        
    def test_correct_soft_delete(self):
        """
            Testing if owner can delet himself AND staff too
        """
        ...
        
    def test_correct_list_users(self):
        """
            Testing if listing is correct AND only staff can list,
            response without balance
        """
        ...
        
    def test_list_one_user(self):
        """
            Testing if one user listing is correct AND only owner can do it,
            response with balance
        """
        ...