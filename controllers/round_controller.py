from models.round import Round
from models.tournament import Tournament

from datetime import datetime


class RoundController:

    @staticmethod
    def create_round(name: str) -> Round:
        round = Round(name)
        return round

    @staticmethod
    def start_round(round: Round) -> None:
        round.start_datetime = datetime.now().isoformat()

    @staticmethod
    def end_round(round: Round) -> None:
        round.end_datetime = datetime.now().isoformat()

    @staticmethod
    def next_round(tournament: Tournament, round) -> Round:
        current_round_index = tournament.rounds.index(round)
        if current_round_index < len(tournament.rounds)-1:
            current_round_index += 1
            return tournament.rounds[current_round_index]
