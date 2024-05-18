from typing import List, Tuple
from dice import Dice


class Outcome:
    def __init__(self, outcomes = None) -> None:
        if outcomes is None:
            outcomes = []
        self.outcomes: List[Tuple[int, Dice]] = outcomes

    def __add__(self, other: "Outcome") -> "Outcome":
        return Outcome([[1 for self_outcome in self.outcomes] for other_outcome in other.outcomes])
