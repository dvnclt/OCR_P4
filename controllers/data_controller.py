from models.player import Player
from models.tournament import Tournament

import json
import os


class PlayerDataController:
    players_file = 'data/players.json'

    @staticmethod
    def check_directory(file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def save_players(players):
        file_path = PlayerDataController.players_file
        PlayerDataController.check_directory(file_path)

        saved_players = PlayerDataController.load_players()
        saved_players_dict = {player.chess_id: player.to_dict()
                              for player in saved_players
                              }

        for player in players:
            saved_players_dict[player.chess_id] = player.to_dict()

        with open(file_path, 'w') as file:
            json.dump(list(saved_players_dict.values()), file, indent=4)

    @staticmethod
    def load_players():
        file_path = PlayerDataController.players_file
        PlayerDataController.check_directory(file_path)

        players = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                players_data = json.load(file)
                for player_data in players_data:
                    player = Player.from_dict(player_data)
                    players.append(player)
        return players


class TournamentDataController:
    tournaments_file = 'data/tournaments.json'

    @staticmethod
    def check_directory(file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def save_tournament(tournament):
        file_path = TournamentDataController.tournaments_file
        TournamentDataController.check_directory(file_path)

        saved_tournaments = TournamentDataController.load_tournaments()
        saved_tournaments_dict = {saved_tournament.name:
                                  saved_tournament.to_dict()
                                  for saved_tournament in saved_tournaments
                                  }

        saved_tournaments_dict[tournament.name] = tournament.to_dict()

        with open(file_path, 'w') as file:
            json.dump(list(saved_tournaments_dict.values()), file, indent=4)

    @staticmethod
    def load_tournaments():
        file_path = TournamentDataController.tournaments_file
        TournamentDataController.check_directory(file_path)

        tournaments = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                tournaments_data = json.load(file)
                for tournament_data in tournaments_data:
                    tournament = Tournament.from_dict(tournament_data)
                    tournaments.append(tournament)
        return tournaments
