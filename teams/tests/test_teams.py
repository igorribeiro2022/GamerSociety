from django.test import TestCase
from rest_framework.test import APITestCase
from ..models import Team
from rest_framework.authtoken.models import Token

class TeamTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        ...

    def test_team_model(self):
        ...
    
    def test_team_instances(self):
        ...

class TeamViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        ...

    def test_tokens(self):
        ...
    
    def test_create_team_response(self):
        ...
    
    def test_update_team_response(self):
        ...

    def test_delete_team_response(self):
        ...

    def test_retrieve_team_response(self):
        ...

    
