import os
import json


class Data:
    def __init__(self, players_file="data/players.json", tournaments_dir="data/tournaments/"):
        self.players_file = players_file
        self.tournaments_dir = tournaments_dir

    def save_players(self, players):
        os.makedirs(os.path.dirname(self.players_file), exist_ok=True)
        if not os.path.exists(self.players_file):
            with open(self.players_file, "w") as file:
                json.dump([], file, indent=4)

        existing_players = self.load_players()
        all_players = sorted(existing_players + players, key=lambda player: player.last_name)

        with open(self.players_file, "w") as file:
            json.dump(all_players, file, default=lambda obj: obj.__dict__, indent=4)

    def load_players(self):
        try:
            with open(self.players_file, "r") as file:
                players_data = json.load(file)
                return players_data
        except FileNotFoundError:
            return []

    def save_tournament(self, tournament):
        tournament_filename = f"{tournament.name}_{tournament.location}.json"
        tournament_file_path = os.path.join(self.tournaments_dir, tournament_filename)

        os.makedirs(os.path.dirname(self.tournaments_dir), exist_ok=True)
        if not os.path.exists(tournament_file_path):
            with open(tournament_file_path, "w") as file:
                json.dump([], file, indent=4)

        with open(tournament_file_path, "w") as file:
            json.dump(tournament, file, default=lambda obj: obj.__dict__, indent=4)

    def load_tournaments(self):
        try:
            with open(self.tournaments_file, "r") as file:
                tournaments_data = json.load(file)
                return tournaments_data
        except FileNotFoundError:
            return []
