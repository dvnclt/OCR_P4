from .match import Match

from datetime import datetime


class Round:
    def __init__(self, name: str):
        self.name = name
        self.start_datetime = datetime.now().isoformat()
        self.end_datetime = None
        self.matches = []

    def add_match(self, match: Match):
        self.matches.append(match)

    def end_round(self):
        self.end_datetime = datetime.now().isoformat()

    def __repr__(self):
        matches_str = "\n".join(map(str, self.matches))
        return (f"Liste des matchs pour le tour '{self.name}' :\n\n"
                f"{matches_str}\n"
                f"Date et heure du début du tour : {self.start_datetime}\n"
                f"Date et heure de fin du tour : {self.end_datetime}\n")

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
