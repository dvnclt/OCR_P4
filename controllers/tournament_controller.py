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
        # Initialise la liste des matchs pour le round en cours
        matches = []
        # Créer une copie de la liste des participants dans une variable 'participants'
        participants = tournament.participants[:]

        # Si nombre de participants insuffisant -> Erreur
        if len(tournament.participants) < 2:
            return f"Erreur: Pas assez de participants ({len(tournament.participants)}). 2 min. requis."

        # Si Round 1, les matchs sont générés aléatoirement
        if round.name == "Round 1":
            random.shuffle(tournament.participants)
        else:
            # Pour les rounds suivants, les participants sont classés par ordre décroissant de points
            tournament.participants.sort(key=lambda p: p.points, reverse=True)

        # Boucle pour appairer les participants selon leur nombre de points
        while len(participants) > 1:
            participant1 = participants.pop(0)
            opponent_index = None

            # Cherche l'adversaire le plus proche en terme de points
            # A condition qu'il n'ai pas déjà été rencontré
            for index, participant in enumerate(participants):
                if participant not in participant1.played_opponents:
                    opponent_index = index
                    break

            # Si nouvel adversaire -> Création du match
            if opponent_index is not None:
                participant2 = participants.pop(opponent_index)
                match = Match(participant1, participant2)
                matches.append(match)
                participant1.played_opponents.add(participant2)
                participant2.played_opponents.add(participant1)
            else:
                # Si tous les participants ont déjà été affrontés
                print("\nTous les participants ont déjà été rencontré. L'adversaire sera donc le plus proche en terme de points")
                for index, participant in enumerate(participants):
                    opponent_index = index
                    break

        # Gestion du cas d'un participant sans adversaire car nombre de participants impair
        if participants:
            participant_forfeit = participants.pop(0)
            print(f"\n{participant_forfeit.first_name} {participant_forfeit.last_name} gagne par forfait (pas d'adversaire disponible).")
            # Ajoute un point au participant gagnant par forfait
            participant_forfeit.points += float(1)

        round.matches = matches

    def set_scores(self, round: Round):
        for match in round.matches:
            while True:
                try:
                    participant1_score = float(input(f"Indiquez le score de {match.participant1.first_name} {match.participant1.last_name}: "))
                    participant2_score = float(input(f"Indiquez le score de {match.participant2.first_name} {match.participant2.last_name}: "))

                    if (participant1_score == 0 and participant2_score == 1) or \
                            (participant1_score == 1 and participant2_score == 0) or \
                            (participant1_score == 0.5 and participant2_score == 0.5):

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
