from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.participant import Participant

from controllers.player_controller import PlayerController
from controllers.participant_controller import ParticipantController

import random


class TournamentController:
    def create_tournament(self, name, location, total_rounds=4):
        tournament = Tournament(name, location, total_rounds)
        return tournament

    def generate_matches(self, tournament: Tournament, round: Round):
        if len(tournament.participants) < 2:
            return f"Erreur: Pas assez de participants ({len(tournament.participants)}). 2 min. requis."

        if round.name == "Round 1":
            random.shuffle(tournament.participants)
        else:
            tournament.participants.sort(key=lambda p: p.points, reverse=True)

        points_dict = {}
        for participant in tournament.participants:
            points = participant.points
            if points not in points_dict:
                points_dict[points] = []
            points_dict[points].append(participant)

        matches = []
        # Pour chaque groupe de points, les matchs sont générés aléatoirement
        for points_group in points_dict.values():
            random.shuffle(points_group)

        while len(points_group) >= 2:
            participant1 = points_group.pop(0)
            participant2 = points_group.pop(0)

            match = Match(participant1, participant2)
            matches.append(match)

        # Si nombre de joueur impair dans un groupe, le joueur seul gagne par forfait
        if len(points_group) == 1:
            participant_forfeit = points_group[0]
            print(f"{participant_forfeit.first_name} {participant_forfeit.last_name} gagne par forfait.")

        # Vérifie que les recontres ne soient pas composés des mêmes participants
        for points_group in points_dict.values():
            while len(points_group) >= 2:
                participant1 = points_group.pop(0)
                opponent_index = None

                for index, participant in enumerate(points_group):
                    if participant not in participant1.played_opponents:
                        opponent_index = index
                        break

                if opponent_index is not None:
                    participant2 = points_group.pop(opponent_index)
                    match = Match(participant1, participant2)
                    matches.append(match)
                    participant1.played_opponents.add(participant2)
                    participant2.played_opponents.add(participant1)

        round.matches = matches

    def set_scores(self, round: Round):
        for match in round.matches:
            while True:
                try:
                    participant1_score = float(input(f"Indiquez le score de {match.participant1.first_name} {match.participant1.last_name}: "))
                    participant2_score = float(input(f"Indiquez le score de {match.participant2.first_name} {match.participant2.last_name}: "))

                    if participant1_score + participant2_score in [0, 1, 1.5]:
                        match.participant1_score = participant1_score
                        match.participant2_score = participant2_score

                        match.participant1.points += participant1_score
                        match.participant2.points += participant2_score

                        if match.participant1_score == 1 and match.participant2_score == 0:
                            print(f"\nVainqueur : {match.participant1.first_name} {match.participant1.last_name}\n")
                        elif match.participant1_score == 0 and match.participant2_score == 1:
                            print(f"\nVainqueur : {match.participant2.first_name} {match.participant2.last_name}\n")
                        elif match.participant1_score == 0.5 and match.participant2_score == 0.5:
                            print("\nMatch Nul\n")

                        break
                    else:
                        print("\nErreur: Les scores doivent être : 0 pour le perdant, 0.5 en cas de match nul et 1 pour le vainqueur.\n")

                except ValueError:
                    print("\nErreur: Entrée non valide.")

    def simulate_auto_add_participants(self, tournament: Tournament, num_players: int):
        # Méthode de test
        player_controller = PlayerController()
        for i in range(num_players):
            first_name = f"Joueur{i+1}"
            last_name = f"Automatique{i+1}"
            birth_date = "01/01/2000"
            chess_id = f"ID{i+1}"

            player = player_controller.create_player(first_name, last_name, birth_date, chess_id)

            participant_controller = ParticipantController()
            participant = participant_controller.create_participant(player)

            tournament.add_participant(participant)
