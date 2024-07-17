from models.player import Player


class PlayerController:

    @staticmethod
    def create_player(first_name, last_name, birth_date, chess_id):
        player = Player(first_name, last_name, birth_date, chess_id)
        return player
