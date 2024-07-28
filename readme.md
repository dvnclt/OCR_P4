# Chess Club Tournament Tool

## Description

Ce projet est un outil pour la gestion des tournois d'échecs. Il permet de créer et de gérer des tournois, d'ajouter des participants, de générer des matchs, et de consulter des rapports sur les joueurs et tournois.

## Structure du Projet

Le projet est divisé en plusieurs composants :

- **`main.py`** : Point d'entrée de l'application.
- **`controllers/`** : Contient les contrôleurs qui gèrent la logique de l'application.
- **`views/`** : Contient les vues qui affichent les menus et les informations à l'utilisateur.
- **`utils.py`** : Contient des fonctions utilitaires pour obtenir des entrées utilisateur et afficher des messages.

### Fichiers et Dossiers

#### `main.py`

Point d'entrée de l'application. Il initialise le contrôleur principal et lance le menu principal.

#### `controllers/`

- **`main_controller.py`** : Contient le contrôleur principal qui coordonne les différents contrôleurs et gère les menus de l'application.
- **`player_controller.py`** : Gère les opérations liées aux joueurs.
- **`participant_controller.py`** : Gère les opérations liées aux participants dans les tournois.
- **`round_controller.py`** : Gère les opérations liées aux rounds des tournois.
- **`tournament_controller.py`** : Gère les opérations liées aux tournois.
- **`report_controller.py`** : Gère la génération de rapports.
- **`data_controller.py`** : Contient les contrôleurs pour les données des joueurs et des tournois.

#### `views/`

- **`view.py`** : Contient la classe `View` avec des méthodes statiques pour afficher les menus à l'utilisateur.

#### `utils.py`

Contient des fonctions utilitaires :

- **`get_user_input(prompt)`** : Demande une entrée utilisateur avec le prompt spécifié.
- **`display_message(message)`** : Affiche le message spécifié.

## Menus et Options

### Menu Principal

Affiche les options suivantes :

1. **Menu des tournois**
2. **Menu des rapports**
3. **Quitter le programme**

### Menu des Tournois

Affiche les options suivantes :

1. **Créer un tournoi**
2. **Sélectionner un tournoi existant**
3. **Retour au menu principal**

### Menu des Actions du Tournoi

Affiche les options suivantes :

1. **Ajouter un participant**
2. **Générer les matchs**
3. **Saisir les résultats**
4. **Afficher le round en cours et le classement actuel**
5. **Terminer le round en cours et commencer le suivant**
6. **Ajouter un round**
7. **Terminer le tournoi**
8. **Afficher la liste des participants**
9. **Afficher la liste des rounds et des matchs**
10. **Entrer la description du tournoi**
11. **Retour au menu principal**

### Menu des Rapports

Affiche les options suivantes :

1. **Afficher la liste des joueurs enregistrés**
2. **Afficher la liste des tournois**
3. **Retour au menu principal**

## Description des Classes et Méthodes

### `controllers/main_controller.py`

Gère les menus principaux ainsi que les actions associées aux tournois et aux rapports.

### `views/view.py`

Contient la classe `View` avec des méthodes statiques pour afficher les différents menus :

- **`display_main_menu()`** : Affiche le menu principal.
- **`display_tournament_menu()`** : Affiche le menu des tournois.
- **`display_tournament_actions_menu()`** : Affiche le menu des actions du tournoi.
- **`display_report_menu()`** : Affiche le menu des rapports.

### `utils.py`

Fournit des fonctions utilitaires pour l'entrée utilisateur et l'affichage des messages :

- **`get_user_input(prompt)`** : Obtenir une entrée utilisateur.
- **`display_message(message)`** : Afficher un message à l'utilisateur.

## Lancer le Programme

Pour lancer le programme, suivez les étapes ci-dessous selon votre système d'exploitation.

### Prérequis

Python

### Instructions pour Windows

1. Ouvrez l'invite de commandes (CMD) ou PowerShell.
2. Naviguez jusqu'au répertoire contenant le fichier `main.py`.
3. Exécutez le programme avec la commande suivante :
   ```bash
   python main.py

### Instructions pour MacOS et Linux

1. Ouvrez le terminal.
2. Naviguez jusqu'au répertoire contenant le fichier `main.py`.
3. Exécutez le programme avec la commande suivante :
   ```bash
   python main.py