from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.data_controller import (PlayerDataController,
                                         TournamentDataController)

from utils import get_user_input, display_message


class ReportController:
    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()

        self.tournament = None

    def display_tournament_info(self):
        display_message("\nInformations du tournoi :")
        print(
            f"\nname : {self.tournament.name}",
            f"\nlocation : {self.tournament.location}",
            f"\ntotal_rounds : {self.tournament.total_rounds}",
            f"\nstart_datetime : {self.tournament.start_datetime}",
            f"\nend_datetime : {self.tournament.end_datetime}",
            f"\ndescription : {self.tournament.description}"
            )

    def display_players_list(self):
        players = PlayerDataController.load_players()

        if players:
            display_message("\nListe des joueurs :")
            for player in players:
                PlayerController.display_player_info(player)
        else:
            display_message("Erreur: Aucun joueur trouvé")
            return

    def display_tournaments_list(self):
        # Charge la liste des tournois enregistrés
        tournaments = TournamentDataController.load_tournaments()
        # Si des tournois existent
        if tournaments:
            # Affiche la liste des tournois avec un numéro associé
            display_message(
                "\nSélectionnez un tournoi en saisisssant le numéro associé :"
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

        # Demande à l'utilisateur de saisir un numéro - 1
        while True:
            try:
                choice_input = get_user_input(
                    "Entrez le numéro du tournoi : "
                    "\nPour annuler, saisissez 'esc' et validez avec 'Entrée'"
                    "\n"
                    )
                choice = int(choice_input) - 1

                if 0 <= choice < len(tournaments):
                    self.tournament = tournaments[choice]
                    self.tournament_controller.tournament = self.tournament
                    self.display_tournament_options()

                    return True

                elif choice_input.lower() == "esc":
                    display_message("\nSélection du tournoi annulée.\n")
                    return False

                else:
                    display_message("Numéro invalide, veuillez réessayer.")
                    continue

            except ValueError:
                display_message(
                    "\nErreur: Saisie invalide. Indiquez un numéro de tournoi"
                )
                break

    def display_tournament_options(self):
        while True:
            # Affiche les options du tournoi
            display_message("\nQue souhaitez-vous faire ?\n"
                            "1. Afficher les informations du tournoi\n"
                            "2. Afficher la liste des participants\n"
                            "3. Afficher la liste des rounds\n"
                            "4. Retour à la liste des tournois")

            # Demande à l'utilisateur de choisir une option
            choice = (get_user_input(""))

            if choice == "1":
                # Affiche les informations du tournoi
                self.display_tournament_info()

            elif choice == "2":
                self.tournament_controller.display_participants_list()

            elif choice == "3":
                self.tournament_controller.display_rounds_list()

            elif choice == "4":
                self.display_tournaments_list()
                break
            else:
                display_message("Erreur: Choix invalide, veuillez réessayer.")
