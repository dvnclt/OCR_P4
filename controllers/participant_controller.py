from models.participant import Participant
from models.player import Player

from utils import display_message


class ParticipantController:

    @staticmethod
    def create_participant(player: Player) -> Participant:
        participant = Participant(
            player.first_name, player.last_name,
            player.birth_date, player.chess_id
            )
        return participant

    @staticmethod
    def display_participant_info(participant: Participant):
        display_message(f"{participant.first_name} "
                        f"{participant.last_name}: "
                        f"{participant.points} point(s)"
                        )
