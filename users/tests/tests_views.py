from rest_framework.test import APIClient
from django.test import TestCase
import ipdb

client = APIClient()

class UsersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_staff = {
            "name": "Gustavo",
            "nickname": "Buiu",
            "password": "1234",
            "birthday": "2000-05-22",
            "email": "gustavo@email.com",
            "is_player": False,
            "is_staff": True,
        }
        cls.user_player = {
            "name": "Pedro",
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
        ...
        
    def test_user_edit_properly(self):
        """
            Testing if user editing is correct AND if only owner
            can edit profile
        """
        ...
        
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