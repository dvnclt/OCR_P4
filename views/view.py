

class View:
    @staticmethod
    def get_user_input(prompt):  # Del
        return input(prompt)

    @staticmethod
    def display_message(message):  # Del
        print(message)

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
        print("\nMenu des actions du tournoi\n")
        print("1 : Ajouter un participant")
        print("2 : Générer les matchs")
        print("3 : Saisir les résultats")
        print("4 : Afficher le round en cours et le classement actuel")
        print("5 : Terminer le round en cours et commencer le suivant")
        print("6 : Ajouter un round")
        print("7 : Terminer le tournoi")
        print("8 : Afficher la liste des participants")
        print("9 : Afficher la liste des rounds")
        print("10 : Retour au menu principal\n")

    @staticmethod
    def display_report_menu():
        print("\n1 : Afficher la liste des tournois")
        print("2 : Afficher la liste des joueurs enregistrés")
        print("3 : Retour au menu principal")
