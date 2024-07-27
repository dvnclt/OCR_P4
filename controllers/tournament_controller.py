from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.participant import Participant

from controllers.player_controller import PlayerController
from controllers.participant_controller import ParticipantController
from controllers.round_controller import RoundController
from controllers.data_controller import (PlayerDataController,
                                         TournamentDataController)

from utils import get_user_input, display_message

import random
from datetime import datetime


class TournamentController:
    def __init__(self):
        self.tournament: Tournament = None
        self.active_round: Round = None

    def setup_tournament(self):
        # Configure un tournoi et le créer
        while True:
            display_message(
                "\nSaisissez les informations demandées et "
                "validez avec 'Entrée'"
                "\nPour annuler, saisissez 'esc' et validez avec 'Entrée'"
            )

            name = get_user_input("\nNom du tournoi : ")
            if name.lower() == "esc":
                display_message("\nCréation du tournoi annulée.\n")
                return

            location = get_user_input("Lieu du tournoi : ")
            if location.lower() == "esc":
                display_message("\nCréation du tournoi annulée.\n")
                return

            try:
                total_rounds_input = get_user_input(
                    "Nombre de tours (4 par défaut) : "
                    )
                if total_rounds_input.lower() == "esc":
                    display_message("\nCréation du tournoi annulée.\n")
                    return
                total_rounds = int(total_rounds_input or 4)
            except ValueError:
                display_message(
                    "\nErreur: Saisie invalide. Indiquez un nombre entier."
                    )
                continue
            break

        self.tournament = self.create_tournament(name, location, total_rounds)
        display_message(f"\nTournoi '{self.tournament.name}' créé.\n")

        # Créer le nombre de rounds définis
        for i in range(total_rounds):
            round_name = f"Round {i + 1}"
            round = RoundController.create_round(round_name)
            self.tournament.rounds.append(round)
            display_message(f"{round_name} créé.\n")

        # Sélectionne le 1er round comme round actif par défaut
        self.active_round = self.tournament.rounds[0]
        RoundController.start_round(self.active_round)
        display_message(f"Round actuel : {self.active_round.name}\n")

        # Sauvegarde les données Tournament
        TournamentDataController.save_tournament(self.tournament)

    def select_tournament(self):
        # Charge la liste des tournois enregistrés
        tournaments = TournamentDataController.load_tournaments()
        # Si des tournois existent
        if tournaments:
            # Affiche la liste des tournois avec un numéro associé
            display_message(
                "\nSélectionnez un tournoi en saisisssant le numéro "
                "associé :"
                                    )
            for index, tournament in enumerate(tournaments, 1):
                display_message(
                    f"\n{index}. {tournament.name} - "
                    f"{tournament.location} - "
                    f"{tournament.start_datetime} - "
                    f"{tournament.end_datetime}"
                                        )
        else:
            display_message("\nAucun tournoi n'a été trouvé")
            return

        # Demande à l'utilisateur de saisir un numéro
        while True:
            choice = int(get_user_input(
                "Entrez le numéro du tournoi : ")) - 1
            if 0 <= choice < len(tournaments):
                self.tournament = tournaments[choice]

                # Sélectionne le premier round non terminé
                self.active_round = next(
                    (round for round in self.tournament.rounds if
                     round.end_datetime is None
                     ), None
                )

                # Si tous les rounds sont terminés, sélectionne le dernier
                if self.active_round is None:
                    self.active_round = self.tournament.rounds[-1]
            else:
                print("Numéro invalide, veuillez réessayer.")
            break

    def setup_player(self):
        # Configure un joueur et l'ajoute en tant que participant
        # Possibilité d'annuler en saisissant 'esc'

        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Le tournoi est terminé")
            return

        # Vérifie que le tournoi n'a pas déjà commencé
        if self.tournament.start_datetime:
            display_message("Erreur: Le tournoi a déjà commencé")
            return

        while True:
            display_message(
                "\nSaisissez les informations demandées et "
                "validez avec 'Entrée'"
                "\nPour annuler, saisissez 'esc' et validez avec 'Entrée'"
                )

            first_name = get_user_input("\nPrénom : ")
            if first_name.lower() == "esc":
                display_message("\nAjout du joueur annulé.\n")
                break
            last_name = get_user_input("Nom de famille : ")
            if first_name.lower() == "esc":
                display_message("\nAjout du joueur annulé.\n")
                break
            birth_date = get_user_input(
                "Date de naissance (DD/MM/YYYY) : "
                )
            if first_name.lower() == "esc":
                display_message("\nAjout du joueur annulé.\n")
                break
            chess_id = get_user_input("Identifiant national : ")
            if first_name.lower() == "esc":
                display_message("\nAjout du joueur annulé.\n")
                break

            player = PlayerController.create_player(
                first_name, last_name, birth_date, chess_id
                )
            # Sauvegarde les données Player
            PlayerDataController.save_players([player])

            # Ajoute le participant au tournoi
            participant = ParticipantController.create_participant(
                player
                )
            self.add_participant(participant)
            display_message(f"\nJoueur '{player.first_name} "
                            f"{player.last_name}' "
                            f"participe au tournoi.\n")

            # Sauvegarde les données Tournament
            TournamentDataController.save_tournament(self.tournament)
            break

    def generate_matches(self):
        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Le tournoi est terminé")
            return

        # Vérifie que les matchs n'ont pas déjà été générés
        if self.active_round.matches:
            display_message("Les matchs pour ce round ont déjà été générés")
            return

        # Génère les matchs si au moins 2 participants
        self.match_pairing()
        if self.match_pairing is None:
            return f"Erreur: Pas assez de participants : {len(
                self.tournament.participants)}. Min. 2 requis"
        else:
            # S'il y a assez de joueurs, commence le tournoi si non commencé
            if self.tournament.start_datetime is None:
                self.start_tournament()

        display_message(f"\nNombre de matchs : "
                        f"{len(self.active_round.matches)}"
                        )
        # Sauvegarde les données Tournament
        TournamentDataController.save_tournament(self.tournament)

        display_message(f"\nListe des matchs pour le "
                        f"{self.active_round.name} : \n"
                        )
        for match in self.active_round.matches:
            display_message(
                f"{match.participant1.first_name} "
                f"{match.participant1.last_name}: "
                f"{match.participant1.color} "
                f"{match.participant1.points} point(s)\n"
                f"contre\n"
                f"{match.participant2.first_name} "
                f"{match.participant2.last_name}: "
                f"{match.participant2.color} "
                f"{match.participant2.points} point(s)\n"
            )

    def set_scores(self):
        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Le tournoi est terminé")
            return

        # Vérifie si les matchs ont déjà été générés
        if not self.active_round.matches:
            display_message(f"Les matchs du {self.active_round.name} n'ont "
                            f"pas encore été générés")
            return

        # Vérifie si les scores ont déjà été entrés
        no_registered_score = all(
            match.participant1_score is None and
            match.participant2_score is None for
            match in self.active_round.matches
        )
        # Si les scores n'ont pas encore été enregistrés
        # Demande l'enregistrement
        if no_registered_score:
            self.record_matches_results(self.active_round)
        else:
            # Si des scores ont déjà été enregistrés
            # Réinitialise les scores
            for match in self.active_round.matches:
                match.participant1_score = None
                match.participant2_score = None

            # Demande à les saisir à nouveau
            self.record_matches_results(self.active_round)
        self.active_round.is_completed = True

        TournamentDataController.save_tournament(self.tournament)

    def get_current_round(self):
        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Le tournoi est terminé")
            return

        display_message(f"\n{self.active_round.name} en cours\n")
        display_message("Classement actuel : \n")

        # Trie les participants par ordre de points
        sorted_participants = sorted(
            self.tournament.participants, key=lambda p: p.points,
            reverse=True
            )
        for participant in sorted_participants:
            display_message(f"{participant.first_name} "
                            f"{participant.last_name}: "
                            f"{participant.points} points"
                            )

    def get_next_round(self):
        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Le tournoi est terminé")
            return

        # Vérifie si tous les matchs sont terminés
        if self.active_round.is_completed:
            # Met fin au round en cours
            RoundController.end_round(self.active_round)

            # Passe au round suivant s'il existe
            next_round = RoundController.next_round(
                self.tournament, self.active_round
                )
            if next_round is None:
                display_message("Erreur: Il n'y a pas de round suivant\n")
            else:
                self.active_round = next_round
                RoundController.start_round(self.active_round)
                display_message(f"\nLe {self.active_round.name} "
                                f"a débuté.\n"
                                )

                # Affiche le classement actuel pour le nouveau round
                # Trie les participants par ordre décroissant de points
                display_message("Classement actuel : \n")
                sorted_participants = sorted(
                    self.tournament.participants, key=lambda p:
                    p.points, reverse=True
                )
                for participant in sorted_participants:
                    display_message(
                        f"{participant.first_name} "
                        f"{participant.last_name}: "
                        f"{participant.points} points"
                    )

        else:
            display_message("Les matchs ne sont pas "
                            "encore tous terminés.\n"
                            )

        # Sauvegarde les données du tournoi
        TournamentDataController.save_tournament(self.tournament)

    def add_round(self):
        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Le tournoi est terminé")
            return

        while True:
            user_input = get_user_input(
                "\nSélectionnez le numéro du nouveau round :"
                "\nPour annuler, saisissez 'esc' et appuyez sur 'Entrée'\n"
                )

            # Vérifie si l'utilisateur souhaite annuler
            if user_input.lower() == "esc":
                display_message("\nCréation du round annulée.")
                return

            try:
                round_number = int(user_input)
                round_name = f"Round {round_number}"
                round = RoundController.create_round(round_name)
                self.tournament.rounds.append(round)
                display_message(f"{round_name} créé.\n")

                # Sauvegarde les données Tournament
                TournamentDataController.save_tournament(self.tournament)

                break
            except ValueError:
                display_message(
                    "\nErreur: Saisie invalide. Indiquez un numéro de round."
                )

    def end_tournament(self):
        # Vérifie que le tournoi n'est pas terminé
        if self.tournament.end_datetime:
            display_message("Erreur: Ce tournoi est déjà terminé")
            return

        # Vérifie que tous les rounds sont terminés
        if not (
            self.active_round is self.tournament.rounds[-1] and
            self.active_round.is_completed
        ):
            display_message("Erreur: Tous les rounds ne sont pas terminés")
            return

        # Termine le round en cours
        RoundController.end_round(self.active_round)
        # Vérifie que le tournoi n'a pas déjà été terminé
        if self.tournament.end_datetime:
            display_message(f"\nTournoi déjà terminé :"
                            f"{self.tournament.end_datetime}"
                            )
            return
        else:
            # Termine le tournoi
            self.tournament.end_datetime = datetime.now().isoformat()
            display_message(f"\nTournoi {self.tournament.name} terminé : "
                            f"{self.tournament.end_datetime}"
                            )

            TournamentDataController.save_tournament(self.tournament)

            # Affiche le classement final
            display_message("\nClassement final : \n")
            sorted_participants = sorted(
                self.tournament.participants, key=lambda p: p.points,
                reverse=True
                )
            for participant in sorted_participants:
                display_message(f"{participant.first_name} "
                                f"{participant.last_name}: "
                                f"{participant.points} points"
                                )

    def display_participants_list(self):
        if not self.tournament.participants:
            display_message("Erreur: Aucun participant trouvé")
            return
        # Affiche le nombre et la liste des participants (ordre alphabétique)
        display_message(f"\nNombre de participants : "
                        f"{len(self.tournament.participants)}"
                        )

        display_message("\nListe des participants : \n")
        sorted_participants = sorted(
            self.tournament.participants, key=lambda participant:
            (participant.last_name, participant.first_name)
            )

        for participant in sorted_participants:
            ParticipantController.display_participant_info(participant)

    def display_rounds_list(self):
        if not self.tournament.rounds:
            display_message("Erreur: Aucun round n'a été trouvé")
            return
        # Affiche la liste des rounds et leurs matchs
        for round in self.tournament.rounds:
            display_message(f"\n{round.name}")

            display_message(f"\nNombre de matchs : "
                            f"{len(round.matches)}")

            for match in round.matches:
                display_message(
                    f"\n{match.participant1.first_name} "
                    f"{match.participant1.last_name} "
                    f"{match.participant1_score}"
                    f"\ncontre"
                    f"\n{match.participant2.first_name} "
                    f"{match.participant2.last_name} "
                    f"{match.participant2_score}"
                )

    def set_description(self):
        display_message("Veuillez saisir une description et appuyez sur "
                        "'Entrée'.")
        self.tournament.description = get_user_input("")

        # Sauvegarde les données Tournament
        TournamentDataController.save_tournament(self.tournament)

    def _auto_add_participants(self, num_players: int):
        # Méthode de test
        for i in range(num_players):
            first_name = f"Joueur{i+1}"
            last_name = f"Automatique{i+1}"
            birth_date = "01/01/2000"
            chess_id = f"ID{i+1}"

            player = PlayerController.create_player(first_name, last_name,
                                                    birth_date, chess_id)

            participant = ParticipantController.create_participant(player)

            self.add_participant(participant)

            PlayerDataController.save_players([player])
            TournamentDataController.save_tournament(self.tournament)

    def _create_tournament(self, name: str, location: str,
                           total_rounds: int = 4
                           ):
        # Créer un tournoi
        self.tournament = Tournament(name, location, total_rounds)
        return self.tournament

    def _start_tournament(self):
        # Vérifie que le tournoi n'a pas déjà commencé
        if self.tournament.start_datetime:
            display_message(f"Le tournoi a déjà débuté : "
                            f"{self.tournament.start_datetime}.")
            return
        else:
            # Commence le tournoi
            self.tournament.start_datetime = datetime.now().isoformat()
            display_message(f"\nDébut du tournoi "
                            f"{self.tournament.name} : "
                            f"{self.tournament.start_datetime}."
                            )

    def _add_participant(self, participant: Participant):
        # Ajoute un participant à la liste des participants
        self.tournament.participants.append(participant)

    def _match_pairing(self):
        # Vérifie qu'il y a assez de participants avant de générer les matchs
        if len(self.tournament.participants) < 2:
            return None

        # Créer une copie de la liste des participants
        participants = self.tournament.participants[:]

        # Si Round 1, les matchs sont générés aléatoirement
        if self.active_round.name == "Round 1":
            random.shuffle(participants)
        else:
            # Pour les rounds suivants:
            # les participants sont classés par ordre décroissant de points
            participants.sort(key=lambda p: p.points, reverse=True)

        # Boucle pour appairer les participants selon leur nombre de points
        while len(participants) > 1:
            participant1 = participants.pop(0)
            opponent_index = None

            # Cherche l'adversaire le plus proche en termes de points
            # À condition qu'il n'ait pas déjà été rencontré
            for index, participant in enumerate(participants):
                if participant not in participant1.played_opponents:
                    opponent_index = index
                    break

            # Si nouvel adversaire -> Création du match
            if opponent_index is not None:
                participant2 = participants.pop(opponent_index)

                # Assignation aléatoire de la couleur
                colors = ["Noir", "Blanc"]
                random.shuffle(colors)
                participant1.color, participant2.color = colors

                match = Match(participant1, participant2)
                self.active_round.matches.append(match)
                participant1.played_opponents.append(participant2)
                participant2.played_opponents.append(participant1)
            else:
                # Si tous les participants ont déjà été affrontés
                print("\nTous les participants ont déjà été rencontrés. "
                      "L'adversaire sera donc le plus proche en points.")
                for index, participant in enumerate(participants):
                    opponent_index = index
                    break

        # Gestion du cas d'un participant sans adversaire
        if participants:
            unmatched_participant = participants.pop(0)
            print(f"\n{unmatched_participant.first_name} "
                  f"{unmatched_participant.last_name} "
                  f"gagne par forfait (pas d'adversaire disponible)."
                  )
            # Ajoute un demi-point au participant pour forfait
            unmatched_participant.points += 0.5

    def _record_matches_results(self, round: Round):
        # Pour chaque match d'un round donné :
        for match in round.matches:
            while True:
                try:
                    # Demande le score du participant1
                    participant1_score = float(get_user_input(
                        f"Indiquez le score de "
                        f"{match.participant1.first_name} "
                        f"{match.participant1.last_name}: "))
                    # Demande le score du participant1
                    participant2_score = float(get_user_input(
                        f"Indiquez le score de "
                        f"{match.participant2.first_name} "
                        f"{match.participant2.last_name}: "))

                    # Vérifie la validité des scores indiqués
                    if (
                        (participant1_score == 0 and participant2_score == 1)
                        or (participant1_score == 1 and
                            participant2_score == 0)
                        or (participant1_score == 0.5 and
                            participant2_score == 0.5)
                    ):

                        # Si valide, les enregistre
                        match.participant1_score = participant1_score
                        match.participant2_score = participant2_score

                        match.participant1.points += participant1_score
                        match.participant2.points += participant2_score

                        # Donne le vainqueur pour chaque match
                        if (
                            match.participant1_score == 1 and
                            match.participant2_score == 0
                        ):
                            print(f"\nVainqueur : "
                                  f"{match.participant1.first_name} "
                                  f"{match.participant1.last_name}\n")
                        elif (
                            match.participant1_score == 0 and
                            match.participant2_score == 1
                        ):
                            print(f"\nVainqueur : "
                                  f"{match.participant2.first_name} "
                                  f"{match.participant2.last_name}\n")
                        elif (
                            match.participant1_score == 0.5 and
                            match.participant2_score == 0.5
                        ):
                            print("\nMatch Nul\n")
                        break
                    else:
                        print("\nErreur: Les scores doivent être : 0 pour le "
                              "perdant, 0.5 en cas de match nul et 1 pour le "
                              "vainqueur.\n")

                except ValueError:
                    print("\nErreur: Entrée non valide.")
