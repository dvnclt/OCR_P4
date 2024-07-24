from controllers.main_controller import MainController

if __name__ == "__main__":
    run = MainController()
    run.main_menu()

"""
Important :
    - Optimiser maincontroller

Bugs :
Chargement tournoi, meme si scores ont déjà été saisi
    Il faut les saisir à nouveau pour passer au round suivant

Améliorations:
    - Vérifier le format des inputs pour chaque saisie
    - Vérifier qu'un numéro de round n'existe pas déjà pour éviter
        la duplication des rounds


Accessoire :
    - is_first plutot que name *
    - Indiquer les méthodes publiques et privées
"""
