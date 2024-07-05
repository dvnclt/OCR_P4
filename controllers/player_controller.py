from models.player import Player


class PlayerController:
    def __init__(self):
        pass

    def create_player(self, first_name, last_name, birth_date, chess_id):
        player = Player(first_name, last_name, birth_date, chess_id)
        return player
