

class Player:
    def __init__(self, first_name: str, last_name: str, birth_date: str, chess_id: str):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.chess_id = chess_id

    def __repr__(self):
        return (f"Player : last_name='{self.last_name}', first_name='{self.first_name}', birth_date='{self.birth_date}', national_id='{self.chess_id}'")

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'chess_id': self.chess_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
