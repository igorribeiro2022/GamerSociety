import ipdb
from rest_framework import generics
from .models import Championship
from .permissions import (
    IsChampionshipOwner,
    IsATeamOwner,
    HaveFivePlayers,
    IsTeamEsportCorrectly,
    IsChampionshipFull,
    IsChampOwnerTryngToEnterInIt,
    HasAnotherChampionshipAroundSevenDays,
    TeamOwnerHasBalanceToEnterInChampionship,
    InitialDateProvidedIsAtLeastSevenDaysAfter
)
from transactions.serializers import TransactionSerializer
from .serializers import (
    CreateChampionshipsSerializer,
    ChampionshipDetailSerializer,
    RetrieveChampionShipWithGamesSerializer,
    ListAllChampionshipsSerializer,
    AddTeamOnChampionshipsSerializer,
    RetrieveChampionAddingGamesSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsStaff
from teams.models import Team
from rest_framework import views


class ListAllChampionshipsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ListAllChampionshipsSerializer
    queryset = Championship.objects.all()


class ListOneChampionshipView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveChampionShipWithGamesSerializer
    queryset = Championship.objects.all()
    lookup_url_kwarg = "cs_id"


class CreateChampionshipsView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff, InitialDateProvidedIsAtLeastSevenDaysAfter]

    serializer_class = CreateChampionshipsSerializer
    queryset = Championship.objects.all()

    def perform_create(self, serializer):
        return serializer.save(staff_owner=self.request.user)


class DeleteChampionshipView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsChampionshipOwner]
    serializer_class = ChampionshipDetailSerializer
    lookup_url_kwarg = "cs_id"
    queryset = Championship.objects.all()
    
    def perform_destroy(self, instance):
        teams = Team.objects.filter(championship=instance.id)
        for team in teams:
            for user in team.users.all():
                if user.is_team_owner:
                    prize = {"value": instance.entry_amount}
                    trans = TransactionSerializer(data=prize)
                    trans.is_valid(raise_exception=True)
                    trans.save(user=user)
        # ipdb.set_trace()
        return instance.delete()

    # Comentado o perfom_create pois não se aplica dentro de uma classe que apenas possui a responsabilidade de destroy. - Pedro L.
    # def perform_create(self, serializer):
    #     return serializer.save(staff_owner=self.request.user)


class AddTeamsInChampionshipView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsATeamOwner,
        HaveFivePlayers,
        IsTeamEsportCorrectly,
        IsChampionshipFull,
        IsChampOwnerTryngToEnterInIt,
        HasAnotherChampionshipAroundSevenDays,
        TeamOwnerHasBalanceToEnterInChampionship
        
    ]
    queryset = Team.objects.all()
    lookup_url_kwarg = "team_id"
    serializer_class = AddTeamOnChampionshipsSerializer

    def patch(self, request, *args, **kwargs):
        # Linha 82 é o retorno do update do ListChampionshipSerializer, só feita a relação
        self.partial_update(request, *args, **kwargs)
        cs_id = kwargs["cs_id"]
        # Capturar o championship atualizado para repassá-lo no serializer
        #       para controlar retorno
        champ_updated = Championship.objects.get(id=cs_id)
        cham_serializer = RetrieveChampionAddingGamesSerializer(champ_updated)
        # Criar transação de entrada no camp
        
        prize = {
            "value": -champ_updated.entry_amount
        }
        trans = TransactionSerializer(data=prize)
        trans.is_valid(raise_exception=True)
        trans.save(user=request.user)
        
        return_dict = {
            "detail": "Team has been added",
            "teams_in_championship": cham_serializer.data["teams"],
        }
        return views.Response(return_dict)
