from models.round import Round


class RoundController:
    def create_round(self, name):
        round = Round(name)
        return round
