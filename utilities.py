from typing import List


def dc_beat_count(dc: int, bonus: int) -> int:
    return max(min(21 + bonus - dc, 20), 0)


def proficiency(level: int) -> int:
    return 2 + every_nth(level, 5, 4)


def every_nth(current: int, start: int, step: int) -> int:
    return from_breakpoint(current, list(range(start, 21, step)))


def heaviside(breaker: int, breakpoint: int) -> int:
    return int(breaker >= breakpoint)

    
def from_breakpoint(breaker: int, breakpoints: List[int]) -> int:
    """
    from_breakpoint(11, [1, 5, 11, 17]) -> 3
    """
    return sum([breaker >= breakpoint for breakpoint in breakpoints])


if __name__ == "__main__":
    assert heaviside(1,2) == 0
    assert heaviside(2,2) == 1

    assert from_breakpoint(-1, [0]) == 0
    assert from_breakpoint(0, [1]) == 0
    assert from_breakpoint(1, [1]) == 1
    assert from_breakpoint(1, [1, 5]) == 1
    assert from_breakpoint(4, [1, 5]) == 1
    assert from_breakpoint(5, [1, 5]) == 2

    # implicitly tests every_nth and from_breakpoint
    assert proficiency(1) == 2
    assert proficiency(4) == 2
    assert proficiency(5) == 3
    assert proficiency(8) == 3
    assert proficiency(9) == 4

    # outcomes_that_saves
    assert dc_beat_count(21, 0) == 0
    assert dc_beat_count(20, 0) == 1
    assert dc_beat_count(20, 1) == 2
    assert dc_beat_count(20, 4) == 5
    assert dc_beat_count(16, 4) == 9
    assert dc_beat_count(22, 0) == 0
    assert dc_beat_count(0, 0) == 20
    assert dc_beat_count(0, 1) == 20
