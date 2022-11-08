from django.db import models


class Phase(models.TextChoices):
    QUARTERS_UPPER = "Quartas Upper"
    SEMI_UPPER = "Semi Upper"
    SEMI_LOWER_1 = "Semi Lower 1"
    SEMI_LOWER_2 = "Semi Lower 2"
    FINAL_UPPER = "Final Upper"
    FINAL_LOWER_1 = "Final Lower 1"
    FINAL_LOWER_2 = "Final Lower 2"
    FINAL_CHAMPIONS = "Final Champions"
    DEFAULT = "Not Subscribed"


class Names(models.TextChoices):
    GAME_1 = "Game 1"
    GAME_2 = "Game 2"
    GAME_3 = "Game 3"
    GAME_4 = "Game 4"
    
game11 = {
    "name": Names.GAME_1,
    "phase": Phase.QUARTERS_UPPER,
}

game12 = {
    "name": Names.GAME_2,
    "phase": Phase.QUARTERS_UPPER,
}
game13 = {
    "name": Names.GAME_3,
    "phase": Phase.QUARTERS_UPPER,
}
game14 = {
    "name": Names.GAME_4,
    "phase": Phase.QUARTERS_UPPER,
}
game21 = {
    "name": Names.GAME_1,
    "phase": Phase.SEMI_UPPER,
}
game22 = {
    "name": Names.GAME_2,
    "phase": Phase.SEMI_UPPER,
}
game31 = {
    "name": Names.GAME_1,
    "phase": Phase.FINAL_UPPER,
}
game41 = {
    "name": Names.GAME_1,
    "phase": Phase.FINAL_CHAMPIONS,
}


game51 = {
    "name": Names.GAME_1,
    "phase": Phase.SEMI_LOWER_1,
}
game52 = {
    "name": Names.GAME_2,
    "phase": Phase.SEMI_LOWER_1,
}
game53 = {
    "name": Names.GAME_1,
    "phase": Phase.SEMI_LOWER_2,
}
game54 = {
    "name": Names.GAME_2,
    "phase": Phase.SEMI_LOWER_2,
}
game61 = {
    "name": Names.GAME_1,
    "phase": Phase.FINAL_LOWER_1,
}
game62 = {
    "name": Names.GAME_1,
    "phase": Phase.FINAL_LOWER_2,
}

games_list = []

games_list.append(game11)
games_list.append(game12)
games_list.append(game13)
games_list.append(game14)
games_list.append(game21)
games_list.append(game22)
games_list.append(game31)
games_list.append(game41)
games_list.append(game51)
games_list.append(game52)
games_list.append(game53)
games_list.append(game54)
games_list.append(game61)
games_list.append(game62)

    
