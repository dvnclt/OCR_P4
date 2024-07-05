from models.round import Round
from models.tournament import Tournament


class RoundController:
    def __init__(self):
        self.current_round_index = 0

    def create_round(self, name):
        round = Round(name)
        return round

    def next_round(self, tournament: Tournament):
        if self.current_round_index < len(tournament.rounds)-1:
            self.current_round_index += 1
            return tournament.rounds[self.current_round_index]
        else:
            print("Tous les rounds créés ont été terminés")
            return None
