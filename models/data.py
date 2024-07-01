from .player import Player
from .tournament import Tournament
import os
import json


class Data:
    def __init__(self, players_file="data/players.json", tournaments_file="data/tournaments.json"):
        self.players_file = players_file
        self.tournaments_file = tournaments_file

    def save_players(self, players):
        os.makedirs(os.path.dirname(self.players_file), exist_ok=True)
        if not os.path.exists(self.players_file):
            with open(self.players_file, "w") as file:
                json.dump([], file, indent=4)

        existing_players = self.load_players()
        existing_players_dict = {f"{player.first_name}{player.last_name}{player.birth_date}": player for player in existing_players}

        for player in players:
            key = f"{player.first_name}{player.last_name}{player.birth_date}"
            if key not in existing_players_dict:
                existing_players_dict[key] = player

        with open(self.players_file, "w") as file:
            json.dump([player.to_dict() for player in existing_players_dict.values()], file, indent=4)

    def load_players(self):
        try:
            with open(self.players_file, "r") as file:
                players_data = json.load(file)
                return [Player.from_dict(player) for player in players_data]
        except FileNotFoundError:
            return []

    def save_tournament(self, tournament):
        os.makedirs(os.path.dirname(self.tournaments_file), exist_ok=True)
        if not os.path.exists(self.tournaments_file):
            with open(self.tournaments_file, "w") as file:
                json.dump([], file, indent=4)

        existing_tournaments = self.load_tournaments()
        existing_tournaments_dict = {f"{t.name}{t.location}": t for t in existing_tournaments}

        key = f"{tournament.name}{tournament.location}"
        if key not in existing_tournaments_dict:
            existing_tournaments_dict[key] = tournament

        with open(self.tournaments_file, "w") as file:
            json.dump([t.to_dict() for t in existing_tournaments_dict.values()], file, indent=4)

    def load_tournaments(self):
        try:
            with open(self.tournaments_file, "r") as file:
                tournaments_data = json.load(file)
                return [Tournament.from_dict(t) for t in tournaments_data]
        except FileNotFoundError:
            return []
