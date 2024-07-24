from views.view import View

from controllers.player_controller import PlayerController
from controllers.participant_controller import ParticipantController
from controllers.round_controller import RoundController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from controllers.data_controller import (PlayerDataController,
                                         TournamentDataController)

from utils import display_message, get_user_input

import sys


class MainController:
    def __init__(self):
        self.view = View()
        self.player_controller = PlayerController()
        self.participant_controller = ParticipantController()
        self.round_controller = RoundController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()
        self.player_data_controller = PlayerDataController()
        self.tournament_data_controller = TournamentDataController()

    def main_menu(self):
        # Affiche le menu principal et demande une action à l'user
        while True:
            self.view.display_main_menu()
            choice = get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Affiche le menu tournoi
                self.tournament_menu()

            if choice == "2":
                self.report_menu()

            if choice == "3":
                display_message("\nFermeture du programme.\n")
                sys.exit(0)

    def tournament_menu(self):
        # Affiche le menu tournoi et demande une action à l'user
        while True:
            self.view.display_tournament_menu()
            choice = get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Créer le tournoi et affiche son menu d'actions
                self.tournament_controller.setup_tournament()
                if not self.tournament_controller.setup_tournament:
                    self.tournament_menu()

            if choice == "2":
                self.tournament_controller.select_tournament()
                if self.tournament_controller.select_tournament:
                    self.tournament_action_menu()

            if choice == "3":
                self.main_menu()

    def tournament_action_menu(self):
        # Affiche le menu des actions du tournoi et demande une action à l'user
        while True:
            self.view.display_tournament_actions_menu()
            choice = get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Créer un joueur et l'ajoute à la liste des participants
                self.tournament_controller.setup_player()

            elif choice == "2":
                # Commence le tournoi et génère les matchs pour le round actif
                self.tournament_controller.generate_matches()

            elif choice == "3":
                # Saisie les scores des matchs
                self.tournament_controller.set_scores()

            elif choice == "4":
                # Affiche le nom du round en cours et le classement actuel
                self.tournament_controller.get_current_round()

            elif choice == "5":
                # Met fin au round en cours et passe au suivant
                self.tournament_controller.get_next_round()

            elif choice == "6":
                # Ajoute un round au tournoi en cours
                self.tournament_controller.add_round()

            elif choice == "7":
                # Termine le dernier round et le tournoi
                self.tournament_controller.end_tournament()

            elif choice == "8":
                # Affiche la liste des participants (ordre alphabétque)
                self.tournament_controller.display_participants_list()

            elif choice == "9":
                # Affiche la liste des rounds et leurs matchs
                self.tournament_controller.display_rounds_list()

            elif choice == "10":
                self.tournament_controller.set_description()

            elif choice == "0":
                # Option de test
                self.tournament_controller.auto_add_participants(9)

            elif choice == "11":
                # Retourne au menu principal
                break

            else:
                display_message("\nErreur: Commande inconnue."
                                "\nSélectionnez une option : "
                                )

    def report_menu(self):
        while True:
            self.view.display_report_menu()
            choice = get_user_input("\nSélectionnez une option : ")

            if choice == "1":
                # Affiche la liste des joueurs
                self.report_controller.display_players_list()

            elif choice == "2":
                # Affiche la liste des tournois
                self.report_controller.display_tournaments_list()

            elif choice == "3":
                # Retour au menu précédent
                break
