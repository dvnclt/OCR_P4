from controllers.main_controller import MainController

if __name__ == "__main__":
    run = MainController()
    run.main_menu()

"""
Todo list :

is_first plutot que name

Ajouter la fonction d'attribution des couleurs

Cohérence :
    Terminer le tournoi mets fin au round en cours
        Si tournoi terminé, ne peut plus afficher les rounds en cours
    Si le 1er round a commencé, on ne devrait plus pouvoir ajouter de joueur
    Si les matchs n'ont pas été générés, on ne devrait pas pouvoir saisir de score
    On ne peut pas générer de matchs si pas assez de joueur

Finir de nettoyer

Ajouter la fonctionnalité description

Lors du chargement d'un tournoi, active round est bien le dernier round actif.
Mais lorsque je veux passer au round suivant
le round suivant est le deuxième round dans tous les cas
Donc le passage au round suivant par du principe qu'on est toujours d'abord au 1er round
"""
