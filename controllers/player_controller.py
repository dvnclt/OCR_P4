from models.player import Player


class PlayerController:

    @staticmethod
    def create_player(first_name, last_name, birth_date, chess_id):
        player = Player(first_name, last_name, birth_date, chess_id)
        return player

    @staticmethod
    def display_player_info(player: Player):
        print(
            f"\n{player.first_name} ",
            f"{player.last_name} ",
            f"{player.birth_date} ",
            f"{player.chess_id}"
        )
