from rest_framework import permissions
from rest_framework.views import Request, View
from games.models import Game
from bets.models import Bet


class HasMoneyToBet(permissions.BasePermission):
    def has_permission(self, request, view):
        self.message = "You don't have enough money to make bet value"
        user_balance = request.user.history.balance
        user_bet = request.data["value"]

        return user_balance > user_bet


class UserToBetIsInGame(permissions.BasePermission):
    def has_object_permission(self, request, view, game: Game):
        self.message = "Not allowed to bet in games that you're going to play"

        user_team_id = None

        if request.user.team:
            user_team_id = str(request.user.team.id)

        team_1_id = game.team_1
        team_2_id = game.team_2

        if user_team_id == team_1_id:
            return False

        if user_team_id == team_2_id:
            return False

        return True


class TeamToBetWillPlayInGame(permissions.BasePermission):
    def has_object_permission(self, request, view, game: Game):
        self.message = "Team to bet will not play this game"
        team = view.kwargs["team_id"]
        team_1 = game.team_1
        team_2 = game.team_2

        if team == team_1:
            return True

        if team == team_2:
            return True

        return False


class CantBetInUnactiveGameBet(permissions.BasePermission):
    def has_object_permission(self, request, view, game: Game):
        self.message = "This game bet is closed, you can only bet in active games bets"
        bet = Bet.objects.get(id=game.bet.id)
        return bet.is_active
