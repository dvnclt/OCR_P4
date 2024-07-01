from models.tournament import Tournament
from models.round import Round
from models.match import Match

from controllers.player_controller import PlayerController

import random


class TournamentController:
    def create_tournament(self, name, location, total_rounds=4):
        tournament = Tournament(name, location, total_rounds)
        return tournament

    def generate_matches(self, tournament: Tournament, round: Round):
        if len(tournament.players) < 2:
            return "Erreur: Pas assez de joueurs pour créer un match"

        random.shuffle(tournament.players)

        for i in range(0, len(tournament.players) - 1, 2):
            player1 = tournament.players[i]
            player2 = tournament.players[i + 1]
            match = Match(player1, player2)
            round.matches.append(match)

    def simulate_auto_add_players(self, tournament: Tournament, num_players: int):
        player_controller = PlayerController()
        for i in range(num_players):
            first_name = f"Joueur{i+1}"
            last_name = f"Automatique{i+1}"
            birth_date = "01/01/2000"
            chess_id = f"ID{i+1}"

            player = player_controller.add_player(first_name, last_name, birth_date, chess_id)
            tournament.add_player(player)
