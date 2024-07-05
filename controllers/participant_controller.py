from models.participant import Participant
from models.player import Player


class ParticipantController:
    def __init__(self):
        pass

    def create_participant(self, player: Player) -> Participant:
        participant = Participant(player.first_name, player.last_name, player.birth_date, player.chess_id)
        return participant
