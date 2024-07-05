from .player import Player


class Participant(Player):
    def __init__(self, first_name: str, last_name: str, birth_date: str, chess_id: str):
        super().__init__(first_name, last_name, birth_date, chess_id)
        self.points = 0
        self.played_opponents = set()

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "points": self.points,
            "played_opponents": self.played_opponents
        }

    @classmethod
    def from_dict(cls, data):
        pass
