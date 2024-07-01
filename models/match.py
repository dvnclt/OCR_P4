from .player import Player
from typing import Tuple, List


class Match:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.player1_score: float = 0
        self.player2_score: float = 0
        self.match: Tuple[List, List] = ([self.player1, self.player1_score], [self.player2, self.player2_score])

    def result(self, player1_score: float, player2_score: float):
        self.player1_score = player1_score
        self.player2_score = player2_score

        if self.player1_score == 1 and self.player2_score == 0:
            return f"Vainqueur {self.player1.first_name} {self.player1.last_name}\n"
        elif self.player1_score == 0 and self.player2_score == 1:
            return f"Vainqueur {self.player2.first_name} {self.player2.last_name}\n"
        elif self.player1_score == 0.5 and self.player2_score == 0.5:
            return "Match Nul"
        else:
            return "Erreur dans la saisie des scores"

    def __repr__(self):
        return (f"{self.player1.first_name} {self.player1.last_name} : {self.player1_score}\n"
                f"{self.player2.first_name} {self.player2.last_name} : {self.player2_score}\n")

    def to_dict(self):
        return {
            'player1': self.player1.to_dict(),
            'player1_score': self.player1_score,
            'player2': self.player2.to_dict(),
            'player2_score': self.player2_score
        }

    @classmethod
    def from_dict(cls, data):
        match = cls(
            player1=Player.from_dict(data['player1']),
            player2=Player.from_dict(data['player2'])
        )
        match.player1_score = data['player1_score']
        match.player2_score = data['player2_score']
        return match
