

class View:
    @staticmethod
    def display_main_menu():
        print("\nChess Club Tournament Tool\n")
        print("Saisissez le numéro associé à l'action souhaitée et validez avec 'Entrée'.\n")
        print("1 : Menu des tournois")
        print("2 : Menu des rapports")
        print("3 : Quitter le programme\n")

    @staticmethod
    def display_tournament_menu():
        print("\nMenu des tournois\n")
        print("\n1 : Créer un tournoi")
        print("2 : Sélectionner un tournoi existant")
        print("3 : Retour au menu principal\n")

    @staticmethod
    def display_tournament_actions_menu():
        print("\nMenu des actions de tournois\n")
        print("1 : Ajouter un joueur")
        print("2 : Démarrer le tournoi")
        print("3 : Générer les matchs")
        print("4 : Saisir les résultats")
        print("5 : Afficher le round en cours")
        print("6 : Ajouter un round et le démarrer")
        print("7 : Terminer le round")
        print("8 : Terminer le tournoi")
        print("9 : Afficher la liste des participants")
        print("10 : Afficher la liste des rounds")
        print("11 : Retour au menu principal\n")

    @staticmethod
    def display_report_menu():
        print("\n1 : Afficher la liste des tournois")
        print("2 : Afficher la liste des joueurs enregistrés")
        print("3 : Retour au menu principal")

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def display_message(message):
        print(message)
