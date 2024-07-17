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

    def add_participant(self, participant: Participant):
        # A transférer
        self.participants.append(participant)
        self.participants.sort(key=lambda participant: participant.last_name)

    def add_round(self, round: Round):
        # A Transférer
        self.rounds.append(round)

    def current_round_name(self) -> str:
        # A Transférer
        if self.rounds:
            return self.rounds[-1].name
        return None

    def set_description(self, description: str):
        # A Transférer
        self.description = description

    def start_tournament(self):
        # A Transférer
        self.start_datetime = datetime.now().isoformat()

    def end_tournament(self):
        # A Transférer
        self.end_datetime = datetime.now().isoformat()

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
