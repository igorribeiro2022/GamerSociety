from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer
from .models import Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }
    users = UserSerializer(read_only=True, many=True)
    # championship = ChampionshipSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

# class TeamListSerializer(ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'
#         extra_kwargs = {
#             'id': {
#                 'read_only': True
#             }
#         }
#     users = UserSerializer(read_only=True, many=True)
#     championship = ChampionshipSerializer(read_only=True, null=True)
#     owner = UserSerializer(read_only=True)