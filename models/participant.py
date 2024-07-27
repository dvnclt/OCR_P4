from .player import Player


class Participant(Player):
    def __init__(self, first_name: str, last_name: str, birth_date: str,
                 chess_id: str, points: float = 0):
        super().__init__(first_name, last_name, birth_date, chess_id)
        self.points = points
        self.played_opponents = []
        self.color = None

    def to_dict(self) -> dict:
        participant_dict = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "points": self.points,
        }
        return participant_dict

    @classmethod
    def from_dict(cls, data: dict) -> 'Participant':
        return cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            chess_id=data['chess_id'],
            points=data.get('points', 0)
        )
