from views import View
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from controllers.participant_controller import ParticipantController
from controllers.round_controller import RoundController

view = View()

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
                        view.display_message(f"Début du tournoi {tournament.name} : {tournament.start_date}.")

                    tournament_controller.generate_matches(tournament, active_round)
                    view.display_message(f"\nListe des matchs pour le {active_round.name} : \n\n{active_round.matches}\n"
                                         f"\nNombre de matchs : {len(active_round.matches)}")

                elif choice == "3":
                    # Enregistre les scores des participants
                    tournament_controller.set_scores(active_round)
                
                elif choice == "4":
                    # Affiche le nom du round en cours
                    view.display_message(f"Round en cours : {active_round.name}")

                elif choice == "5":
                    # Met fin au tour actuel
                    active_round.end_round()

                    # Passe au round suivant si existant
                    active_round = round_controller.next_round(tournament)
                    view.display_message(f"Round actuel : {active_round.name}\n")

                elif choice == "6":
                    if active_round.end_round() is None:
                        active_round.end_round()

                        round_name = f"Round {view.get_user_input("Sélectionnez le numéro du nouveau round : ")}"
                        round = round_controller.create_round(round_name)
                        tournament.rounds.append(round)

                        active_round = tournament.rounds[-1]
                        view.display_message(f"{active_round.name} créé.\nRound actuel : {active_round.name}\n")

                elif choice == "8":
                    view.display_message("Liste des joueurs et points : ")
                    for participant in tournament.participants:
                        view.display_message(f"{participant.first_name} {participant.last_name}: {participant.points}")

                elif choice == "0":
                    # Option de test
                    tournament_controller.simulate_auto_add_participants(tournament, 10)

