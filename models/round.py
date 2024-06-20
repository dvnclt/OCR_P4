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
