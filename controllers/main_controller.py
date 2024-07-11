from views.view import View
from player_controller import PlayerController
from participant_controller import ParticipantController
from match_controller import MatchController
from round_controller import RoundController
from tournament_controller import TournamentController


class MainController:
    def __init__(self):
        self.view = View()
        self.player_controller = PlayerController()
        self.participant_controller = ParticipantController()
        self.match_controller = MatchController()
        self.round_controller = RoundController()
        self.tournament_controller = TournamentController()

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def display_message(message):
        print(message)

    def main_menu(self):
        while True:
            self.view.display_main_menu()
            choice = self.get_user_input("\nSélectionnez une option : ")
            if choice == "1":
                self.view.display_tournament_menu()
                choice = self.view.get_user_input("Sélectionnez une option : ")
            # A terminer

while True:
    # Affiche le menu principal et demande une action à l'utilisateur
    view.display_main_menu()
    choice = view.get_user_input("Sélectionnez une option : ")

    if choice == "1":
        # Affiche le menu tournoi et demande une action à l'utilisateur
        view.display_tournament_menu()
        choice = view.get_user_input("Sélectionnez une option : ")

        if choice == "1":
            # Créer un tournoi et les rounds définis. Sélectionne le premier round comme round actif
            name = view.get_user_input("\nNom du tournoi : ")
            location = view.get_user_input("Lieu du tournoi : ")
            total_rounds = int(view.get_user_input("Nombre de tours (4 par défaut) : ") or 4)

            tournament_controller = TournamentController()
            tournament = tournament_controller.create_tournament(name, location, total_rounds)
            view.display_message(f"\nTournoi '{tournament.name}' créé.\n")

            round_controller = RoundController()
            for i in range(total_rounds):
                round_name = f"Round {i + 1}"
                round = round_controller.create_round(round_name)
                tournament.add_round(round)
                view.display_message(f"{round_name} créé.\n")

            active_round = tournament.rounds[0]
            view.display_message(f"Round actuel : {active_round.name}\n")

            while True:
                # Affiche le menu des actions de tournoi et demande une action à l'utilisateur
                view.display_tournament_actions_menu()
                choice = view.get_user_input("Sélectionnez une option : ")

                if choice == "1":
                    # Créer un nouveau joueur et l'ajoute au tournoi en tant que participant
                    # A améliorer pour vérifier d'abord l'existence du joueur dans la DB
                    first_name = view.get_user_input("\nPrénom : ")
                    last_name = view.get_user_input("Nom de famille : ")
                    birth_date = view.get_user_input("Date de naissance (DD/MM/YYYY) : ")
                    chess_id = view.get_user_input("Identifiant national : ")

                    player_controller = PlayerController()
                    player = player_controller.create_player(first_name, last_name, birth_date, chess_id)

                    participant_controller = ParticipantController()
                    participant = participant_controller.create_participant(player)

                    tournament.add_participant(participant)
                    view.display_message(f"\nJoueur '{player.first_name} {player.last_name}' participe au tournoi.\n")

                elif choice == "2":
                    # Si le tournoi n'a pas déjà commencé, le commence et génère les matchs pour le round en cours
                    if tournament.start_date is None:
                        tournament.start_tournament()
                        view.display_message(f"\nDébut du tournoi {tournament.name} : {tournament.start_date}.")

                    tournament_controller.generate_matches(tournament, active_round)

                    view.display_message(f"\nListe des matchs pour le {active_round.name} : \n")
                    for match in active_round.matches:
                        view.display_message(
                            f"{match.participant1.first_name} {match.participant1.last_name} {match.participant1.points} point(s)\n"
                            f"contre\n"
                            f"{match.participant2.first_name} {match.participant2.last_name} {match.participant2.points} point(s)\n"
                        )

                    view.display_message(f"\nNombre de matchs : {len(active_round.matches)}")

                elif choice == "3":
                    # Vérifie si les scores ont déjà été saisis
                    # Si non, enregistre les scores
                    # Si oui, réinitialise la précédente saisie et en enregistre une nouvelle

                    no_registered_score = all(match.participant1_score is None and match.participant2_score is None for match in active_round.matches)

                    if no_registered_score:
                        tournament_controller.set_scores(active_round)
                    else:  # Ne fonctionne pas - Changer d'approche, il semble que les scores ne sont jamais None
                        for match in active_round.matches:
                            match.participant1_score = None
                            match.participant2_score = None
                        tournament_controller.set_scores(active_round)

                elif choice == "4":
                    # Affiche le nom du round en cours et le classement actuel
                    view.display_message(f"\n{active_round.name} en cours\n")

                    view.display_message("Classement actuel : \n")
                    sorted_participants = sorted(tournament.participants, key=lambda p: p.points, reverse=True)
                    for participant in sorted_participants:
                        view.display_message(f"{participant.first_name} {participant.last_name}: {participant.points} points")

                elif choice == "5":
                    # Vérifie que les tous les matchs sont terminés
                    # Si oui, met fin au round en cours et passe au suivant
                    # Affiche le classement actuel pour le nouveau round

                    all_matches_done = all(match.participant1_score is not None and match.participant2_score is not None for match in active_round.matches)

                    if all_matches_done:
                        active_round.end_round()
                    else: # Ne fonctionne pas - Changer d'approche, il semble que les scores ne sont jamais None
                        view.display_message(f"Les matchs ne sont pas terminés")

                    if active_round.end_round is not None:
                        next_round = round_controller.next_round(tournament)
                        if next_round is None:
                            view.display_message("Il n'y a pas de round suivant\n")
                        else:
                            active_round = next_round
                            view.display_message(f"\nLe {active_round.name} a débuté.\n")

                        view.display_message("Classement actuel : \n")
                        sorted_participants = sorted(tournament.participants, key=lambda p: p.points, reverse=True)
                        for participant in sorted_participants:
                            view.display_message(f"{participant.first_name} {participant.last_name}: {participant.points} points")

                elif choice == "6":
                    round_name = f"Round {view.get_user_input("Sélectionnez le numéro du nouveau round : ")}"
                    round = round_controller.create_round(round_name)
                    tournament.rounds.append(round)

                elif choice == "7":
                    # Vérifie que tous les rounds ont bien été terminés
                    # Mets fin au tournoi 
                    # Affiche le classement final

                    all_rounds_done = all(round.end_round is not None for round in tournament.rounds)

                    if all_rounds_done:  # Ne fonctionne pas - Changer d'approche, il semble que les round.end_round ne sont jamais None
                        tournament.end_tournament()
                        view.display_message(f"\nTournoi terminé {tournament.end_date}")

                        view.display_message("\nClassement final : \n")
                        sorted_participants = sorted(tournament.participants, key=lambda p: p.points, reverse=True)
                        for participant in sorted_participants:
                            view.display_message(f"{participant.first_name} {participant.last_name}: {participant.points} points")

                elif choice == "8":
                    view.display_message("\nListe des participants : \n")

                    sorted_participants = sorted(tournament.participants, key=lambda participant: (participant.last_name, participant.first_name))

                    for participant in sorted_participants:
                        view.display_message(f"{participant.first_name} {participant.last_name}: {participant.points} point(s)")

                    view.display_message(f"\nNombre de participants : {len(tournament.participants)})")

                elif choice == "9":
                    for round in tournament.rounds:
                        view.display_message(
                            f"\n{round.name}")
                        for match in round.matches:
                            view.display_message(
                                f"\n{match.participant1.first_name} {match.participant1.last_name} {match.participant1_score}"
                                f"\ncontre"
                                f"\n{match.participant2.first_name} {match.participant2.last_name} {match.participant2_score}"
                            )
                        view.display_message(f"\nNombre de matchs : {len(round.matches)}")

                elif choice == "0":
                    # Option de test
                    tournament_controller.simulate_auto_add_participants(tournament, 9)
