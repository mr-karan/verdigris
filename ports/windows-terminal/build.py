"""Windows Terminal colour schemes, as a JSON fragment."""

import json

from palette import ANSI


def camel(name: str) -> str:
    head, *rest = name.replace("magenta", "purple").split("_")
    return head + "".join(part.capitalize() for part in rest)


def scheme(flavour) -> dict:
    terminal = flavour.terminal
    colors = {
        "name": flavour.title,
        "background": terminal["background"],
        "foreground": terminal["foreground"],
        "cursorColor": terminal["cursor"],
        "selectionBackground": terminal["selection_background"],
    }
    colors.update({camel(name): flavour.ansi[name] for name in ANSI})
    return colors


def render(palette) -> dict:
    fragment = {"schemes": [scheme(f) for f in palette.flavours.values()]}
    return {"verdigris.json": json.dumps(fragment, indent=2) + "\n"}
