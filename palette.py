"""The Verdigris palette: load palette.json, resolve roles, check contrast.

Every port renders from the Palette built here, so a colour is defined once.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEX = re.compile(r"^#[0-9a-f]{6}$")

ANSI = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
]
TERMINAL = [
    "background", "foreground", "cursor", "cursor_text",
    "selection_background", "selection_foreground",
]
SEMANTIC = ["error", "warning", "info", "hint", "success", "added", "modified", "removed"]
SYNTAX = [
    "comment", "keyword", "operator", "punctuation", "function", "string",
    "escape", "regex", "number", "constant", "type", "variable", "parameter",
    "property", "key", "namespace", "tag", "attribute", "decorator", "builtin",
    "label", "heading", "link",
]
STYLES = {"italic", "bold", "underline"}


class PaletteError(Exception):
    """palette.json is malformed. The message names what to fix."""


@dataclass(frozen=True)
class Style:
    color: str
    italic: bool = False
    bold: bool = False
    underline: bool = False


@dataclass(frozen=True)
class Flavour:
    key: str
    name: str
    appearance: str
    colors: dict
    terminal: dict
    ansi: dict
    semantic: dict
    syntax: dict

    def __getitem__(self, color: str) -> str:
        return self.colors[color]

    @property
    def slug(self) -> str:
        return f"verdigris-{self.key}"

    @property
    def title(self) -> str:
        return f"Verdigris {self.name}"

    @property
    def dark(self) -> bool:
        return self.appearance == "dark"

    @property
    def ansi_list(self) -> list:
        return [self.ansi[name] for name in ANSI]


@dataclass(frozen=True)
class Palette:
    name: str
    version: str
    description: str
    author: str
    license: str
    homepage: str
    notes: dict
    flavours: dict

    @property
    def light(self) -> Flavour:
        return self._by_appearance("light")

    @property
    def dark(self) -> Flavour:
        return self._by_appearance("dark")

    def _by_appearance(self, appearance: str) -> Flavour:
        return next(f for f in self.flavours.values() if f.appearance == appearance)


def _exact_keys(where: str, got, want) -> None:
    missing, extra = set(want) - set(got), set(got) - set(want)
    if missing or extra:
        raise PaletteError(f"{where}: missing {sorted(missing)}, unknown {sorted(extra)}")


def _resolve(where: str, colors: dict, name: str) -> str:
    if name not in colors:
        raise PaletteError(f"{where}: '{name}' is not a colour in flavours.*.colors")
    return colors[name]


def _flavour(key: str, raw: dict, roles: dict, names: list) -> Flavour:
    colors = raw["colors"]
    _exact_keys(f"flavours.{key}.colors", colors, names)
    for name, value in colors.items():
        if not HEX.match(value):
            raise PaletteError(f"flavours.{key}.colors.{name}: '{value}' is not lowercase #rrggbb")
    if raw["appearance"] not in ("light", "dark"):
        raise PaletteError(f"flavours.{key}.appearance must be 'light' or 'dark'")

    def group(name: str) -> dict:
        return {role: _resolve(f"roles.{name}.{role}", colors, ref) for role, ref in roles[name].items()}

    syntax = {}
    for role, spec in roles["syntax"].items():
        styles = set(spec.get("style", "").split())
        if styles - STYLES:
            raise PaletteError(f"roles.syntax.{role}.style: unknown {sorted(styles - STYLES)}")
        syntax[role] = Style(
            _resolve(f"roles.syntax.{role}", colors, spec["color"]),
            **{style: True for style in styles},
        )
    return Flavour(
        key=key, name=raw["name"], appearance=raw["appearance"], colors=dict(colors),
        terminal=group("terminal"), ansi=group("ansi"), semantic=group("semantic"), syntax=syntax,
    )


def load(path: Path = ROOT / "palette.json") -> Palette:
    raw = json.loads(path.read_text())
    roles = raw["roles"]
    _exact_keys("roles.ansi", roles["ansi"], ANSI)
    _exact_keys("roles.terminal", roles["terminal"], TERMINAL)
    _exact_keys("roles.semantic", roles["semantic"], SEMANTIC)
    _exact_keys("roles.syntax", roles["syntax"], SYNTAX)
    names = list(next(iter(raw["flavours"].values()))["colors"])
    _exact_keys("notes", raw["notes"], names)
    flavours = {key: _flavour(key, value, roles, names) for key, value in raw["flavours"].items()}
    if sorted(f.appearance for f in flavours.values()) != ["dark", "light"]:
        raise PaletteError("flavours: need exactly one light and one dark flavour")
    return Palette(
        name=raw["name"], version=raw["version"], description=raw["description"],
        author=raw["author"], license=raw["license"], homepage=raw["homepage"],
        notes=raw["notes"], flavours=flavours,
    )


def rgb(color: str) -> tuple:
    return tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))


def mix(base: str, toward: str, amount: float) -> str:
    """A tint between two palette colours, for formats with no alpha channel."""
    channels = (round(b + (t - b) * amount) for b, t in zip(rgb(base), rgb(toward)))
    return "#%02x%02x%02x" % tuple(channels)


def luminance(color: str) -> float:
    channels = (c / 255 for c in rgb(color))
    r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    """WCAG 2 contrast ratio, from 1 to 21."""
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# WCAG AA for body text, a floor for quiet text, and the AA bar for UI parts.
TEXT, QUIET, UI = 4.5, 3.5, 3.0

HUES = ["patina", "copper", "cuprite", "azurite", "malachite", "brass", "bornite"]
BRIGHTS = [f"{hue}_bright" for hue in HUES if hue != "copper"]
WASHES = [f"{hue}_wash" for hue in ("patina", "copper", "cuprite", "azurite", "malachite")]
# Everything code or prose can sit on.
GROUNDS = ["bg", "bg_dim", "bg_raised", "fill_soft", "fill"]

# (minimum, foreground colours, background colours, what the pair is)
COLOR_RULES = [
    (TEXT, ["fg_strong", "fg"], GROUNDS + WASHES + ["selection", "search"], "text"),
    (TEXT, ["fg_muted"], GROUNDS, "muted text"),
    (TEXT, HUES + BRIGHTS, GROUNDS + WASHES, "hue as text"),
    (UI, HUES, ["selection"], "hue on a selection"),
    (QUIET, ["fg_subtle"], ["bg", "bg_dim", "fill_soft"], "quiet text"),
    # A button or a status bar segment: the background colour as text on a hue.
    (TEXT, ["bg", "bg_dim"], HUES, "label on a hue"),
]

# Roles that are allowed to be quiet; every other syntax and ANSI role is body text.
QUIET_SYNTAX = {"comment"}
QUIET_ANSI = {"bright_black"}
# ANSI black is a background shade in both flavours, so it is never text on bg.
ANSI_BACKGROUND = {"black"}


@dataclass(frozen=True)
class Pair:
    flavour: str
    label: str
    fg: str
    bg: str
    minimum: float
    ratio: float

    @property
    def ok(self) -> bool:
        return self.ratio >= self.minimum


def contrast_pairs(palette: Palette) -> list:
    """Every checked pair, in a stable order."""
    pairs = []
    for flavour in palette.flavours.values():
        def add(label: str, fg: str, bg: str, minimum: float) -> None:
            pairs.append(Pair(flavour.key, label, fg, bg, minimum, contrast(fg, bg)))

        for minimum, fgs, bgs, what in COLOR_RULES:
            for fg in fgs:
                for bg in bgs:
                    add(f"{what}: {fg} on {bg}", flavour[fg], flavour[bg], minimum)
        for role, style in flavour.syntax.items():
            minimum = QUIET if role in QUIET_SYNTAX else TEXT
            for bg in ("bg", "bg_dim", "fill_soft"):
                add(f"syntax {role} on {bg}", style.color, flavour[bg], minimum)
        background = flavour.terminal["background"]
        for name in ANSI:
            if name in ANSI_BACKGROUND:
                continue
            minimum = QUIET if name in QUIET_ANSI else TEXT
            add(f"ansi {name} on terminal background", flavour.ansi[name], background, minimum)
        add("ansi white on black", flavour.ansi["white"], flavour.ansi["black"], TEXT)
        add("terminal foreground", flavour.terminal["foreground"], background, TEXT)
        add("terminal foreground on selection", flavour.terminal["selection_foreground"],
            flavour.terminal["selection_background"], TEXT)
        add("terminal cursor", flavour.terminal["cursor"], background, UI)
        add("text under the cursor", flavour.terminal["cursor_text"], flavour.terminal["cursor"], TEXT)
    return pairs


def contrast_failures(palette: Palette) -> list:
    return [
        f"{p.flavour}: {p.label} is {p.ratio:.2f}, needs {p.minimum} ({p.fg} on {p.bg})"
        for p in contrast_pairs(palette) if not p.ok
    ]
