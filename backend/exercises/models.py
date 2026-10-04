from dataclasses import dataclass

MINUS = "−"


@dataclass(frozen=True)
class Equation:
    """a·x + b = c·x + d"""

    a: int
    b: int
    c: int
    d: int

    @property
    def solution(self) -> int | None:
        if self.a == self.c or (self.d - self.b) % (self.a - self.c):
            return None
        return (self.d - self.b) // (self.a - self.c)

    def __str__(self) -> str:
        return f"{_side(self.a, self.b)} = {_side(self.c, self.d)}"


@dataclass(frozen=True)
class Exercise:
    story: str
    equation: Equation


def _signed(number: int) -> str:
    return str(number).replace("-", MINUS)


def _side(coefficient: int, constant: int) -> str:
    if coefficient == 0:
        return _signed(constant)

    text = {1: "x", -1: f"{MINUS}x"}.get(coefficient, f"{_signed(coefficient)}x")
    if constant > 0:
        text += f" + {constant}"
    elif constant < 0:
        text += f" {MINUS} {-constant}"
    return text
