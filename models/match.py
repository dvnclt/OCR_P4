from .player import Player
# from typing import Tuple, List


class Match:
    def __init__(self, player1: Player, score1: float, player2: Player, score2: float):
        self.player1, self.score1 = player1, score1
        self.player2, self.score2 = player2, score2
        # self.match: Tuple[List, List] = ([player1, score1], [player2, score2])

    def __repr__(self):
        return (f"{self.player1.first_name} {self.player1.last_name} : {self.score1}\n"
                f"{self.player2.first_name} {self.player2.last_name} : {self.score2}\n")
