from views import View
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController

view = View()

while True:
    view.display_main_menu()
    choice = view.get_user_input("Sélectionnez une option : ")

    if choice == "1":
        view.display_tournament_menu()
        choice = view.get_user_input("Sélectionnez une option : ")

        if choice == "1":
            name = view.get_user_input("\nNom du tournoi : ")
            location = view.get_user_input("Lieu du tournoi : ")
            total_rounds = int(view.get_user_input("Nombre de tours (4 par défaut) : ") or 4)

            tournament_controller = TournamentController()
            tournament = tournament_controller.create_tournament(name, location, total_rounds)
            view.display_message(f"\nTournoi '{tournament.name}' créé avec succès.\n")

            round_controller = RoundController()
            for i in range(total_rounds):
                round_name = f"Round {i + 1}"
                round = round_controller.create_round(round_name)
                tournament.add_round(round)
                view.display_message(f"{round_name} créé.\n")

            while True:
                view.display_tournament_actions_menu()
                choice = view.get_user_input("Sélectionnez une option : ")

                if choice == "1":
                    # A améliorer pour vérifier d'abord l'existence du joueur dans la DB
                    first_name = view.get_user_input("\nPrénom : ")
                    last_name = view.get_user_input("Nom de famille : ")
                    birth_date = view.get_user_input("Date de naissance (DD/MM/YYYY) : ")
                    chess_id = view.get_user_input("Identifiant national : ")

                    player_controller = PlayerController()
                    player = player_controller.add_player(first_name, last_name, birth_date, chess_id)
                    tournament.add_player(player)
                    view.display_message(f"\nJoueur '{player.first_name} {player.last_name}' ajouté avec succès.\n")

                if choice == "2":
                    tournament.start_tournament()
                    view.display_message(f"Le tournoi {tournament.name} a commencé : {tournament.start_date}.")

                if choice == "0":
                    tournament_controller.simulate_auto_add_players(tournament, 20)
                    tournament_controller.generate_matches(tournament, round)
                    view.display_message(f"liste des match pour le {round.name} : \n{round.matches}\n"
                                         f"Nombre de matchs : {len(round.matches)}")
