from rest_framework.test import APIClient
from django.test import TestCase
from users.models import User
from rest_framework.authtoken.models import Token

client = APIClient()


class TransactionsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_player_data = {
            "username": "Vini",
            "nickname": "vshiryu",
            "password": "1234",
            "birthday": "1995-05-15",
            "email": "kkkk@kkkk.com",
            "is_player": True,
            "is_staff": False,
        }

        cls.transaction_data = {"value": 1000}

        cls.user_player = User.objects.create_user(**cls.user_player_data)

    def test_create_transaction(self):
        token_player = Token.objects.create(user=self.user_player)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")

        response = client.post("/api/transactions/", self.transaction_data)

        self.assertEqual(201, response.status_code)

    def test_transaction_wo_data(self):
        token_player = Token.objects.create(user=self.user_player)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token_player}")

        response = client.post("/api/transactions/")

        self.assertEqual(400, response.status_code)

    def test_transaction_wo_token(self):
        response = client.post("/api/transactions/", self.transaction_data)

        self.assertEqual(401, response.status_code)
