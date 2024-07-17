from views.view import View

from controllers.player_controller import PlayerController
from controllers.participant_controller import ParticipantController
from controllers.match_controller import MatchController
from controllers.round_controller import RoundController
from controllers.tournament_controller import TournamentController
from controllers.data_controller import (PlayerDataController,
                                         TournamentDataController)

import sys


class MainController:
    def __init__(self):
        self.view = View()
        self.player_controller = PlayerController()
        self.participant_controller = ParticipantController()
        self.match_controller = MatchController()
        self.round_controller = RoundController()
        self.tournament_controller = TournamentController()
        self.player_data_controller = PlayerDataController()
        self.tournament_data_controller = TournamentDataController()

        self.tournament = None
        self.active_round = None

    def get_user_input(self, prompt):
        return input(prompt)

    def display_message(self, message):
        print(message)

    def main_menu(self):
        # Affiche le menu principal et demande une action à l'user
        while True:
            self.view.display_main_menu()
            choice = self.get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Affiche le menu tournoi
                self.tournament_menu()

            if choice == "2":
                pass

            if choice == "3":
                self.display_message("\nFermeture du programme.\n")
                sys.exit(0)

    def tournament_menu(self):
        # Affiche le menu tournoi et demande une action à l'user
        while True:
            self.view.display_tournament_menu()
            choice = self.get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Créer le tournoi et affiche son menu d'actions
                self.setup_tournament()
                self.tournament_action_menu()

            if choice == "2":
                self.select_tournament()

    def tournament_action_menu(self):  # A réviser
        # Affiche le menu des actions du tournoi et demande une action à l'user
        while True:
            self.view.display_tournament_actions_menu()
            choice = self.get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Créer un joueur et l'ajoute à la liste des participants
                self.setup_player()

            elif choice == "2":
                # Commence le tournoi et génère les matchs pour le round actif
                if self.tournament.start_datetime is None:
                    self.tournament.start_tournament()
                    self.display_message(
                        f"\nDébut du tournoi {self.tournament.name} : "
                        f"{self.tournament.start_datetime}."
                        )

                self.tournament_controller.generate_matches(
                    self.tournament, self.active_round
                    )

                self.display_message(f"\nNombre de matchs : "
                                     f"{len(self.active_round.matches)}"
                                     )
                self.tournament_data_controller.save_tournament(
                    self.tournament
                    )

                self.display_message(f"\nListe des matchs pour le "
                                     f"{self.active_round.name} : \n")
                for match in self.active_round.matches:
                    self.display_message(
                        f"{match.participant1.first_name} "
                        f"{match.participant1.last_name} "
                        f"{match.participant1.points} point(s)\n"
                        f"contre\n"
                        f"{match.participant2.first_name} "
                        f"{match.participant2.last_name} "
                        f"{match.participant2.points} point(s)\n"
                    )

            elif choice == "3":  # ! (en faire une méthode ?)
                # Saisie les scores des matchs

                no_registered_score = all(
                    match.participant1_score is None and
                    match.participant2_score is None for
                    match in self.active_round.matches
                )
                # Si les scores n'ont pas encore été enregistrés
                # Demande l'enregistrement
                if no_registered_score:
                    self.tournament_controller.set_scores(self.active_round)
                else:
                    # Si des scores ont déjà été enregistrés
                    # Réinitialise les scores
                    for match in self.active_round.matches:
                        match.participant1_score = None
                        match.participant2_score = None

                    # Demande à les saisir à nouveau
                    self.tournament_controller.set_scores(self.active_round)

                self.tournament_data_controller.save_tournament(
                    self.tournament
                    )

            elif choice == "4":  # ! (en faire une méthode ?)
                # Affiche le nom du round en cours et le classement actuel
                self.display_message(f"\n{self.active_round.name} en cours\n")

                self.display_message("Classement actuel : \n")
                sorted_participants = sorted(
                    self.tournament.participants, key=lambda p: p.points,
                    reverse=True
                    )
                for participant in sorted_participants:
                    self.display_message(f"{participant.first_name} "
                                         f"{participant.last_name}: "
                                         f"{participant.points} points"
                                         )

            elif choice == "5":  # !!! (en faire une méthode ?)
                # Passe au round suivant si les matchs sont terminés
                # Et si le round suivant existe

                all_matches_done = all(
                    match.participant1_score is not None and
                    match.participant2_score is not None
                    for match in self.active_round.matches
                )

                # Si tous les matchs sont terminés
                if all_matches_done:
                    # Met fin au round en cours
                    self.active_round.end_round()

                    # Passe au round suivant s'il existe
                    next_round = self.round_controller.next_round(
                        self.tournament
                        )
                    if next_round is None:
                        self.display_message("Il n'y a pas de round suivant\n")
                    else:
                        self.active_round = next_round
                        self.active_round.start_round()
                        self.display_message(f"\nLe {self.active_round.name} "
                                             f"a débuté.\n"
                                             )

                        # Affiche le classement actuel pour le nouveau round
                        # Trie les participants par ordre décroissant de points
                        self.display_message("Classement actuel : \n")
                        sorted_participants = sorted(
                            self.tournament.participants, key=lambda p:
                            p.points, reverse=True
                        )
                        for participant in sorted_participants:
                            self.display_message(
                                f"{participant.first_name} "
                                f"{participant.last_name}: "
                                f"{participant.points} points"
                            )

                else:
                    self.display_message("Les matchs ne sont pas "
                                         "encore tous terminés.\n"
                                         )

                # Sauvegarde les données du tournoi
                self.tournament_data_controller.save_tournament(
                    self.tournament)

            elif choice == "6":
                # Ajoute un round au tournoi en cours
                round_name = f"Round {self.get_user_input(
                    "Sélectionnez le numéro du nouveau round : "
                    )}"
                round = self.round_controller.create_round(round_name)
                self.tournament.rounds.append(round)

                self.tournament_data_controller.save_tournament(
                    self.tournament
                    )

            elif choice == "7":  # !!! (en faire une méthode ?)
                # Vérifie que tous les rounds ont bien été terminés
                # Si oui, mets fin au tournoi
                # Affiche le classement final

                all_rounds_done = all(round.end_round is not None for round in
                                      self.tournament.rounds
                                      )

                if all_rounds_done:  # Ne fonctionne pas
                    self.tournament.end_tournament()
                    self.display_message(f"\nTournoi terminé "
                                         f"{self.tournament.end_datetime}"
                                         )

                    self.display_message("\nClassement final : \n")
                    sorted_participants = sorted(
                        self.tournament.participants, key=lambda p: p.points,
                        reverse=True
                        )
                    for participant in sorted_participants:
                        self.display_message(f"{participant.first_name} "
                                             f"{participant.last_name}: "
                                             f"{participant.points} points"
                                             )

                self.tournament_data_controller.save_tournament(
                    self.tournament
                    )

            elif choice == "8":  # ! (en faire une méthode ?)
                # Affiche la liste des participants (ordre alphabétque)
                self.display_message("\nListe des participants : \n")

                sorted_participants = sorted(
                    self.tournament.participants, key=lambda participant:
                    (participant.last_name, participant.first_name)
                    )

                for participant in sorted_participants:
                    self.display_message(f"{participant.first_name} "
                                         f"{participant.last_name}: "
                                         f"{participant.points} point(s)"
                                         )

                self.display_message(f"\nNombre de participants : "
                                     f"{len(self.tournament.participants)})"
                                     )

            elif choice == "9":  # ! (en faire une méthode ?)
                # Affiche la liste des rounds et leurs matchs
                for round in self.tournament.rounds:
                    self.display_message(f"\n{round.name}")

                    for match in round.matches:
                        self.display_message(
                            f"\n{match.participant1.first_name} "
                            f"{match.participant1.last_name} "
                            f"{match.participant1_score}"
                            f"\ncontre"
                            f"\n{match.participant2.first_name} "
                            f"{match.participant2.last_name} "
                            f"{match.participant2_score}"
                        )
                    self.display_message(f"\nNombre de matchs : "
                                         f"{len(round.matches)}")

            elif choice == "0":
                # Option de test
                self.tournament_controller.simulate_auto_add_participants(
                    self.tournament, 9
                    )

            elif choice == "10":
                break

            else:
                self.display_message("\nErreur: Commande inconnue."
                                     "\nSélectionnez une option : "
                                     )

    def select_tournament(self):
        # Charge la liste des tournois enregistrés
        tournaments = self.tournament_data_controller.load_tournaments()

        # Si des tournois existent
        if tournaments:
            # Affiche la liste des tournois avec un numéro associé
            self.display_message(
                "\nSélectionnez un tournoi en saisisssant le numéro "
                "associé :"
                                    )
            for index, tournament in enumerate(tournaments, 1):
                self.display_message(
                    f"\n{index}. {tournament.name} - "
                    f"{tournament.location} - "
                    f"{tournament.start_datetime} - "
                    f"{tournament.end_datetime}"
                                        )
        else:
            # Sinon retourne :
            return "Aucun tournoi n'a été trouvé"

        # Demande à l'utilisateur de saisir un numéro
        while True:
            choice = int(self.get_user_input(
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

                return self.tournament_action_menu()

            else:
                print("Numéro invalide, veuillez réessayer.")

    def setup_tournament(self):
        # Configure le tournoi et le créer
        name = self.get_user_input("\nNom du tournoi : ")
        location = self.get_user_input("Lieu du tournoi : ")
        total_rounds = int(self.get_user_input(
            "Nombre de tours (4 par défaut) : ") or 4
            )
        self.tournament = self.tournament_controller.create_tournament(
            name, location, total_rounds
            )
        self.display_message(f"\nTournoi '{self.tournament.name}' créé.\n")

        # Créer le nombre de round définis
        for i in range(total_rounds):
            round_name = f"Round {i + 1}"
            round = self.round_controller.create_round(round_name)
            self.tournament.add_round(round)
            self.display_message(f"{round_name} créé.\n")

        # Sélectionne le 1er round comme round actif par défaut
        self.active_round = self.tournament.rounds[0]
        self.active_round.start_round()
        self.display_message(f"Round actuel : {self.active_round.name}\n")

        # Sauvegarde les données générées
        self.tournament_data_controller.save_tournament(self.tournament)

    def setup_player(self):
        # Configure un joueur et l'ajoute en tant que participant
        # Possibilité d'annuler en saisissant 'esc'
        while True:

            self.display_message(
                "\nSaisissez les informations demandées et "
                "validez avec 'Entrée'"
                "\nPour annuler, saisissez 'esc' et validez avec 'Entrée'"
                )

            first_name = self.get_user_input("\nPrénom : ")
            if first_name.lower() == "esc":
                self.display_message("\nAjout du joueur annulé.\n")
                break
            last_name = self.get_user_input("Nom de famille : ")
            if first_name.lower() == "esc":
                self.display_message("\nAjout du joueur annulé.\n")
                break
            birth_date = self.get_user_input(
                "Date de naissance (DD/MM/YYYY) : "
                )
            if first_name.lower() == "esc":
                self.display_message("\nAjout du joueur annulé.\n")
                break
            chess_id = self.get_user_input("Identifiant national : ")
            if first_name.lower() == "esc":
                self.display_message("\nAjout du joueur annulé.\n")
                break

            player = self.player_controller.create_player(
                first_name, last_name, birth_date, chess_id
                )

            participant = self.participant_controller.create_participant(
                player
                )

            self.tournament.add_participant(participant)
            self.display_message(f"\nJoueur '{player.first_name} "
                                 f"{player.last_name}' "
                                 f"participe au tournoi.\n")

            # Sauvegarde les données générées
            self.player_data_controller.save_players([player])
            break
