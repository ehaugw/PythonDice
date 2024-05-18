from typing import List, Tuple


class Dice:
    def __init__(self, rolls = None) -> None:
        if rolls is None or rolls == 0:
            rolls: List[int] = [1]

        if isinstance(rolls, int):
            rolls = [0 if i == 0 else 1 for i in range(rolls + 1)]

        self.rolls: List[int] = rolls
        self.flat: float = 0

    def __add__(self, other) -> "Dice":
        if not isinstance(other, Dice):
            other = Dice().set_flat(other)

        rolls = [0] * (len(self.rolls) + len(other.rolls) - 1)
        for self_value, self_count in enumerate(self.rolls):
            if self_count == 0: continue  # skip things that has never been rolled
            for other_value, other_count in enumerate(other.rolls):
                if other_count == 0: continue  # skip things that has never been rolled
                rolls[self_value + other_value] += self_count * other_count

        return Dice(rolls).set_flat(self.flat + other.flat)

    def set_flat(self, flat) -> "Dice":
        self.flat = flat
        return self
    
    def __mul__(self, number: int) -> "Dice":
        assert isinstance(number, int), "Rolls can only be multiplied by integers, not %s" % type(number)
        assert number >= 0, "Can't multiply Dice with negative number %s" % number
        if number == 0:
            return Dice()

        result = self
        for i in range(number - 1):
            result += self
        return result

    def average(self) -> float:
        return (
            self.flat
            + sum([self_value * self_count for self_value, self_count in enumerate(self.rolls)]) / sum(self.rolls)
        )

    def __str__(self) -> str:
        return str(self.average())

    def crit(self) -> "Dice":
        result = self * 2
        result.flat /= 2
        return result


if __name__ == "__main__":
    # test init
    roll = Dice(6)
    assert roll.flat == 0
    assert roll.rolls == [0, 1, 1, 1, 1, 1, 1]

    # test add flat
    roll += 2
    assert roll.flat == 2
    assert roll.rolls == [0, 1, 1, 1, 1, 1, 1]

    # test average
    assert roll.average() == 5.5

    # test multiply
    roll *= 2
    assert roll.flat == 4
    assert roll.average() == 11

    # test crit
    assert (Dice(6) + 1).crit().average() == 8

    # test empty init
    empty = Dice()
    assert empty.average() == 0

    # test add empty
    assert roll.average() == (roll + empty).average()

    # test add roll
    assert (Dice(6) + Dice(8)).average() == 8

    # test add Dice
    roll = Dice(6) + 1
    assert (roll + roll).average() == 9
