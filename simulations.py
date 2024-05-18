import re

from dice import Dice
from utilities import every_nth, from_breakpoint, proficiency, heaviside, dc_beat_count


def kayrel(
    level: int,
    weapon: Dice,
    rounds: int,
    strength: int,
    sentinel: bool,
) -> Dice:

    dueling = 2
    weapon += dueling + strength

    if level < 3:
        base_rogue = weapon
    else:
        base_rogue = rogue(
            level=level - 2,
            weapon=weapon,
            rounds=1,
            strength=strength,
            sentinel=sentinel,

            total_level=level
        )

    warlock_level = heaviside(level, 2)
    hex = Dice(6) * warlock_level
    return (hex + base_rogue + proficiency(level) * warlock_level) * rounds


def rogue(
    level: int,
    weapon: Dice,
    rounds: int,
    strength: int,
    sentinel: bool,

    total_level: int = 0,
) -> Dice:
    if total_level == 0:
        total_level = level

    weapon += strength

    sneak_attack: Dice = Dice(6) * every_nth(level, 1, 2)
    booming_blade: Dice = Dice(8) * every_nth(total_level, 5, 6)

    action: Dice = weapon + booming_blade
    once_per_turn: Dice = sneak_attack

    per_sentinel = weapon + sneak_attack
    per_round: Dice = action + once_per_turn + per_sentinel * int(sentinel)

    return per_round * rounds


def fighter(
    level: int,
    weapon: Dice,
    rounds: int,
    strength: int,
    sentinel: bool,
) -> Dice:

    weapon += strength
    action: Dice = weapon * from_breakpoint(level, [1, 5, 11, 20])

    per_sentinel = weapon
    per_round = action + per_sentinel * int(sentinel)
    return per_round * rounds


def warlock(
    level: int,
    weapon: Dice,
    rounds: int,
    charisma: int,
) -> Dice:

    hex: Dice = Dice(6)
    hexblade_curse = proficiency(level)
    agonizing_blast = charisma
    eldritch_blast: Dice = weapon + agonizing_blast + hex

    attacks = from_breakpoint(level, [1, 5, 11, 17])
    action: Dice = eldritch_blast * attacks

    return action * rounds + hexblade_curse * attacks * (rounds - 1)


def classic_ranger(
    level: int,
    weapon: Dice,
    rounds: int,
    strength: int,
    sentinel: bool,

    use_horde_breaker: int = 0
) -> Dice:

    dueling = 2 * heaviside(level, 2)
    weapon += dueling + strength

    hunters_mark: Dice = Dice(6) * heaviside(level, 2)
    base_attack: Dice = weapon + hunters_mark

    attacks = from_breakpoint(level, [1, 5]) + heaviside(level, 3) * use_horde_breaker
    action: Dice = base_attack * attacks

    per_sentinel = weapon
    per_round = action + per_sentinel * int(sentinel)
    return per_round * rounds


def mundane_ranger(
    level: int,
    weapon: Dice,
    rounds: int,
    strength: int,
    wisdom: int,
    sentinel: bool,

    wisdom_save_bonus: int,

    use_horde_breaker: int = 0
) -> Dice:

    dueling = 2 * heaviside(level, 2)
    weapon += dueling + strength

    base_attack: Dice = weapon

    attacks = from_breakpoint(level, [1, 5]) + heaviside(level, 3) * use_horde_breaker
    action: Dice = base_attack * attacks

    wound = Dice(4) * heaviside(level, 2)

    wound_lifetime = 20.0 / dc_beat_count(8 + proficiency(level) + wisdom, wisdom_save_bonus)


    wound_ticks = int(rounds * (rounds + 1) / 2)

    per_sentinel = weapon
    per_round = action + per_sentinel * int(sentinel)
    return per_round * rounds + wound * int(wound_ticks * attacks)

def gandalf(
    level: int,
    weapon: Dice,
    rounds: int,
    dexterity: int,
    sentinel: bool,
) -> Dice:
    paladin_level = 2
    wizard_level = level - paladin_level

    weapon += dexterity

    base_attack: Dice = weapon
    booming_blade = weapon + Dice(8) * from_breakpoint(level, [5, 11, 17])

    action = booming_blade + base_attack * heaviside(wizard_level, 6)

    per_sentinel = weapon
    per_round = action + per_sentinel * int(sentinel)
    return per_round * rounds

def str_list_of_dice(dice_list):
    return re.sub(r"[\[\]']", "", str([str(d) for d in dice_list]))
    

if __name__ == "__main__":

    max_rounds = 4
    sentinel: bool = True

    #attacker
    primary_stat: int = 4
    secondary_stat: int = 3
    longsword_1h = Dice(8) + 2 + Dice(6)

    #defender
    wisdom_save_bonus = 5

    for level in (1, 2, 3, 5, 6, 7, 8, 9, 11):
        print("_")
        print("LEVEL: %s" % level)
        print("Round: %s" % re.sub(r"[\[\]']", "", str(list(range(1, max_rounds + 1)))))

        print("Kayrel:" , str_list_of_dice([
            kayrel(
                level=level,
                weapon=longsword_1h,
                rounds=r,
                strength=primary_stat,
                sentinel=sentinel,
            )
            for r in range(1, max_rounds + 1)
        ]))

        print("Rogue:" , str_list_of_dice([
            rogue(
                level=level,
                weapon=longsword_1h,
                rounds=r,
                strength=primary_stat,
                sentinel=sentinel,
            )
            for r in range(1, max_rounds + 1)
        ]))

        print("Warlock:", str_list_of_dice([
            warlock(
                level=level,
                weapon=Dice(10),
                charisma=primary_stat,
                rounds=r,
            )
            for r in range(1, max_rounds + 1)
        ]))

        print("Classic_Ranger:", str_list_of_dice([
            classic_ranger(
                level=level,
                weapon=longsword_1h,
                rounds=r,
                strength=primary_stat,
                sentinel=sentinel,
            )
            for r in range(1, max_rounds + 1)
        ]))

        print("Mundane_Ranger:", str_list_of_dice([
            mundane_ranger(
                level=level,
                weapon=longsword_1h,
                rounds=r,
                strength=primary_stat,
                wisdom=secondary_stat,
                sentinel=sentinel,
        
                wisdom_save_bonus=wisdom_save_bonus
            )
            for r in range(1, max_rounds + 1)
        ]))

        print("Gandalf:", str_list_of_dice([
            gandalf(
                level=level,
                weapon=longsword_1h,
                rounds=r,
                dexterity=primary_stat,
                sentinel=sentinel,
            )
            for r in range(1, max_rounds + 1)
        ]))
