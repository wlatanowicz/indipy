import re


def children(value, child_class):
    if value is None:
        return []
    for ch in value:
        if not isinstance(ch, child_class):
            raise ValueError(
                "Child node has to be of type %s, %s given",
                child_class.__name__,
                ch.__class__.__name__,
            )
    return value


def dictionary(value, dictionary_class):
    if value not in dictionary_class.__dict__.values():
        raise ValueError(
            'Invalid value: "%s" not found in %s', value, dictionary_class.__name__
        )
    return value


def number(value):
    regexps = (
        r"^\-?\d+$",  # int
        r"^\-?\d+\.\d+$",
        r"^\-?\d+\.$",
        r"^\-?\.\d+$",  # float
        r"^\-?\d+:\d{2}$",  # :mm
        r"^\-?\d+:\d{2}\.\d+$",  # :mm.m
        r"^\-?\d+:\d{2}:\d{2}$",  # :mm:ss
        r"^\-?\d+:\d{2}:\d{2}\.\d+$",  # :mm:ss.s
    )
    if value is None:
        return None

    if not any([re.match(r, str(value)) for r in regexps]):
        raise ValueError("Invalid value for number: %s", value)

    return value
