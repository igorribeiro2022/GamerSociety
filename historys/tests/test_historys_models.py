from django.test import TestCase
from users.models import User
from ..models import Team

class HistoryViewTest(TestCase):
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
        cls.user = User.objects.create_user(**cls.user_staff)

        cls.team_model = {
            'name': 'Pain Gaming',
            'initials': 'PNG',
            'e_sport': 'League of Legends'
        }
        # cls.team_in_champ_model = {
        #     'name': 'Pain Gaming',
        #     'initials': 'PNG',
        #     'e_sports': 'League of Legends'
        # }
        cls.not_in_championship_team_created = {
            'id': str,
            'name': 'Pain Gaming',
            'initials': 'PNG',
            'wins': 0,
            'losses': 0,
            'e_sport': 'League of Legends',
            'championship': 'Is not in a championship'
        }
        # cls.in_championship_team_created = {
        #     'id': str,
        #     'name': 'Pain Gaming',
        #     'initials': 'PNG',
        #     'e_sports': 'League of Legends',
        #     'championship': 
        # }