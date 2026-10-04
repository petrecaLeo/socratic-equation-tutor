import re


def _number(answer: int) -> str:
    digits = str(abs(answer))
    # O número tem que estar inteiro: o 5 não pode ser pedaço de 15, de 5,5 nem de −5.
    after = r"(?!\d|[.,]\d)"
    if answer < 0:
        return rf"[-−]\s*{digits}{after}"
    return rf"(?<![-−\d]){digits}{after}"


def leak_pattern(answer: int) -> re.Pattern:
    number = _number(answer)
    forms = [
        rf"\bx\s*(?:=|vale|é|equals|is)\s*(?:igual\s+a\s+)?{number}",
        rf"\b(?:resposta|answer)(?:\s+(?:certa|correta|final|correct))?\s*(?:é|is|:|=)\s*(?:x\s*=\s*)?{number}",
    ]
    return re.compile("|".join(forms), re.IGNORECASE)
