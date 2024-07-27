from .match import Match


class Round:
    def __init__(self, name: str):
        self.name = name
        self.start_datetime = None
        self.end_datetime = None
        self.matches = []
        self.is_completed = False

    def to_dict(self):
        return {
            'name': self.name,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'matches': [match.to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data):
        round = cls(name=data['name'])
        round.start_datetime = data['start_datetime']
        round.end_datetime = data.get('end_datetime')
        round.matches = [Match.from_dict(match) for match in data['matches']]
        return round
