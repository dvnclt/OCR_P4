from .participant import Participant
from typing import Tuple, List


class Match:
    def __init__(self, participant1: Participant, participant2: Participant):
        self.participant1 = participant1
        self.participant2 = participant2
        self.participant1_score: float = 0
        self.participant2_score: float = 0
        self.match: Tuple[List, List] = ([self.participant1, self.participant1_score], [self.participant2, self.participant2_score])

    def results(self, participant1_score, particpant2_score):
        self.participant1_score = participant1_score
        self.participant2_score = particpant2_score

    def __repr__(self):
        return (f"{self.participant1.first_name} {self.participant1.last_name} : {self.participant1_score}\n"
                f"{self.participant2.first_name} {self.participant2.last_name} : {self.participant2_score}\n")

    def to_dict(self):
        return {
            'participant1': self.participant1.to_dict(),
            'participant1_score': self.participant1_score,
            'participant2': self.participant2.to_dict(),
            'participant2_score': self.participant2_score
        }

    @classmethod
    def from_dict(cls, data):
        match = cls(
            participant1=Participant.from_dict(data['participant1']),
            participant2=Participant.from_dict(data['participant2'])
        )
        match.participant1_score = data['participant1_score']
        match.participant2_score = data['participant2_score']
        return match
