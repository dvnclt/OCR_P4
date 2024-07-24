from .participant import Participant
from typing import Tuple, List


class Match:
    def __init__(self, participant1: Participant, participant2: Participant):
        self.participant1 = participant1
        self.participant2 = participant2
        self.participant1_score = None
        self.participant2_score = None
        self.match: Tuple[List, List] = (
            [self.participant1, self.participant1_score],
            [self.participant2, self.participant2_score]
            )

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
