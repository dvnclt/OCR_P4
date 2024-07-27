from .participant import Participant
from .round import Round

from datetime import datetime
from typing import List


class Tournament:
    def __init__(self, name: str, location: str, total_rounds: int = 4):
        self.name = name
        self.location = location
        self.total_rounds = total_rounds
        self.start_datetime: datetime = None
        self.end_datetime: datetime = None
        self.description: str = None
        self.rounds: List[Round] = []
        self.participants: List[Participant] = []

    def to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'total_rounds': self.total_rounds,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'description': self.description,
            'rounds': [round.to_dict() for round in self.rounds],
            'participants': [
                participant.to_dict() for participant in self.participants
                ]
        }

    @classmethod
    def from_dict(cls, data):
        tournament = cls(
            name=data['name'],
            location=data['location'],
            total_rounds=data['total_rounds']
        )
        tournament.start_datetime = data.get('start_datetime')
        tournament.end_datetime = data.get('end_datetime')
        tournament.description = data.get('description')
        tournament.rounds = [
            Round.from_dict(round)
            for round in data.get('rounds', [])
            ]
        tournament.participants = [
            Participant.from_dict(participant)
            for participant in data.get('participants', [])
            ]
        return tournament
