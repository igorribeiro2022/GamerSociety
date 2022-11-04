from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from historys.models import History


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=20, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "password",
            "birthday",
            "email",
            "is_active",
            "is_player",
            "team",
            "is_staff",
            "is_team_owner",
            "is_superuser",
            "date_joined",
        ]


class UserCreateSerializer(UserSerializer):
    is_staff = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        History.objects.create(user=user)
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "birthday",
            "email",
            "is_active",
            "is_player",
            "team",
            "is_staff",
        ]


class UserForTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname"]


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "is_active",
        ]
