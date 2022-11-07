from django.test import TestCase
from users.models import User

class UsersModelTest(TestCase):
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
        cls.user_staff_response = {
            "username": "Gustavo",
            "nickname": "Buiu",
            "birthday": "2000-05-22",
            "balance": 0.0,
            "email": "gustavo@email.com",
            "is_player": False,
            "is_staff": True,
            "is_active": True,
            # "team_id": None,
        }
         
    def test_user_model_create(self):
        """
            Testing if user model's create is correct
        """
        msg_1 = 'Testing user model creation'
        
        user_staff_created = User.objects.create_user(**self.user_staff)
        user_dict = user_staff_created.__dict__
        user_dict.pop('_state')
        self.user_staff_response['id'] = user_dict['id']
        self.user_staff_response['last_login'] = user_dict['last_login']
        self.user_staff_response['is_superuser'] = user_dict['is_superuser']
        self.user_staff_response['first_name'] = user_dict['first_name']
        self.user_staff_response['last_name'] = user_dict['last_name']
        self.user_staff_response['date_joined'] = user_dict['date_joined']
        self.user_staff_response['password'] = user_dict['password']

        self.maxDiff = None
        self.assertEqual(self.user_staff_response, user_dict, msg_1)
