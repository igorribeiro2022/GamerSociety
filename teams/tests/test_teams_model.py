from django.test import TestCase
from users.models import User
from ..models import Team

class TeamTestClass(TestCase):
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

    def test_team_model(self):

        team = Team.objects.create(**self.team_model)
        self.assertTrue(bool(team.id))
        self.assertTrue(bool(team.name))
        self.assertTrue(bool(team.initials))
        self.assertTrue(bool(team.e_sport))
    
    def test_team_instances(self):

        team = Team.objects.create(**self.team_model)
        # team_in_champ = Team.objects.create(self.team_in_champ_model)
        self.assertIsInstance(team, Team)
        # self.assertIsInstance(team_in_champ, Team)


    
