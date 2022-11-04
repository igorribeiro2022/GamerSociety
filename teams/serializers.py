from rest_framework.serializers import ModelSerializer
from users.serializers import UserForTeamSerializer
from .models import Team
import ipdb


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['championship']
    # championship = ListChampionshipsSerializer(read_only=True, allow_null=True)
    users = UserForTeamSerializer(many=True, allow_null=True, read_only=True)
    
    def update(self, instance, validated_data):
        users_list = validated_data['users']
        
        # ipdb.set_trace()

        for user in users_list:
            instance.users.add(user)
            
        instance.save()
        return instance
    
class TeamSerializerReturn(ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'name',
            'initials'
        ]

    # championship = ListChampionshipsSerializer(read_only=True, allow_null=True)
    # users = UserForTeamSerializer(many=True, allow_null=True, read_only=True)

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