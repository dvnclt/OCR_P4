from .match import Match
from datetime import datetime


class Round:
    def __init__(self, name: str):
        self.name = name
        self.start_datetime = None
        self.end_datetime = None
        self.matches = []

    def start_round(self):
        # A transferer
        self.start_datetime = datetime.now().isoformat()

    def end_round(self):
        # A transferer
        self.end_datetime = datetime.now().isoformat()

    def add_match(self, match: Match):
        # A transferer
        self.matches.append(match)

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
