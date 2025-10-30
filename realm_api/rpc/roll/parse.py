"""Parse segments from roll command arguments"""

# stdlib
from re import compile

# local
from realm_schema import ConstantModifier, DiceRoll, RollSegment

roll_regex = compile(
    r"^(?P<all>"
    r"(?P<num>\d*)"
    r"d(?P<die>\d+)"
    r"(?P<fun>!\d*|k[hl]\d*)?"
    r")"
    r"(>(?P<min>\d+))?"
    r"(<(?P<max>\d+))?"
    r"(x(?P<batch>\d+))?"
)
"""Regex pattern for initial roll"""

addl_roll_regex = compile(
    r"(?P<all>"
    r"(?P<op>[-+])"
    r"(?P<num>\d*)"
    r"(d(?P<die>\d+)(?P<fun>!\d*|k[hl]\d*)?)?"
    r")"
    r"(>(?P<min>\d+))?"
    r"(<(?P<max>\d+))?"
    r"(x(?P<batch>\d+))?"
)
"""Regex pattern for additional modifier rolls/constants"""


class ParsedRoll(list[list[RollSegment]]):
    max: int | None = None
    min: int | None = None


def parse_segments(roll: str) -> ParsedRoll:
    """Parse a roll formula string into a list of RollSegment objects."""

    batches = ParsedRoll()

    # strip all whitespace
    roll = roll.replace(" ", "")

    # parse first roll
    first = roll_regex.match(roll)
    assert first
    first = first.groupdict()

    # parse variable number of mods
    mods = [r.groupdict() for r in addl_roll_regex.finditer(roll)]

    batch = int(first["batch"] or 1)
    batches.max = int(first["max"]) if first["max"] else None
    batches.min = int(first["min"]) if first["min"] else None

    for m in mods:
        if m["batch"]:
            batch = int(m["batch"])

        if m["max"]:
            batches.max = int(m["max"])

        if m["min"]:
            batches.min = int(m["min"])

    for _ in range(batch):
        segments: list[RollSegment] = [
            DiceRoll(
                raw=first["all"],
                dice=int(first["num"] or "1"),
                faces=int(first["die"]),
                extra=first["fun"],
            )
        ]

        for mod in mods:
            if mod["die"]:
                segments.append(
                    DiceRoll(
                        raw=mod["all"],
                        negative=mod["op"] == "-",
                        dice=int(mod["num"] or "1"),
                        faces=int(mod["die"]),
                        extra=mod["fun"],
                    )
                )
            else:
                segments.append(
                    ConstantModifier(
                        raw=mod["all"],
                        negative=mod["op"] == "-",
                        number=int(mod["num"]),
                    )
                )

        batches.append(segments)

    return batches
