from .player import Player
from .round import Round

from datetime import datetime
from typing import List


class Tournament:
    def __init__(self, name: str, location: str, total_rounds: int = 4):
        self.name: str = name
        self.location: str = location
        self.start_date: datetime = None
        self.end_date: datetime = None
        self.total_rounds: int = total_rounds
        self.rounds: List = []
        self.players: List = []
        self.description: str = None

    def add_player(self, player: Player):
        self.players.append(player)
        self.players.sort(key=lambda player: player.last_name)

    def add_round(self, round: Round):
        self.rounds.append(round)

    def current_round(self) -> str:
        if self.rounds:
            return self.rounds[-1].name
        return None

    def set_description(self, description: str):
        self.description = description

    def start_tournament(self):
        self.start_date = datetime.now().isoformat()

    def end_tournament(self):
        self.end_date = datetime.now().isoformat()

    def __repr__(self):
        start_date_str = self.start_date if self.start_date else "Non commencé"
        end_date_str = self.end_date if self.end_date else "En cours"
        return (f"Tournament(name='{self.name}', location='{self.location}', "
                f"start_date='{start_date_str}', end_date='{end_date_str}', "
                f"total_rounds={self.total_rounds}, current_round={self.current_round()}, "
                f"players={len(self.players)}, rounds={len(self.rounds)}, "
                f"description='{self.description}')")
