"""Alacritty colour schemes (TOML, Alacritty 0.13 and later)."""

from palette import ANSI


def table(name: str, pairs: list) -> str:
    return "\n".join([f"[{name}]"] + [f'{key} = "{value}"' for key, value in pairs]) + "\n"


def theme(palette, flavour) -> str:
    terminal = flavour.terminal
    names = ANSI[:8]
    tables = [
        table("colors.primary", [
            ("background", terminal["background"]),
            ("foreground", terminal["foreground"]),
            ("dim_foreground", flavour["fg_muted"]),
            ("bright_foreground", flavour["fg_strong"]),
        ]),
        table("colors.cursor", [("text", terminal["cursor_text"]), ("cursor", terminal["cursor"])]),
        table("colors.vi_mode_cursor", [("text", flavour["bg"]), ("cursor", flavour["copper"])]),
        table("colors.selection", [
            ("text", terminal["selection_foreground"]),
            ("background", terminal["selection_background"]),
        ]),
        table("colors.search.matches", [("foreground", flavour["fg_strong"]), ("background", flavour["search"])]),
        table("colors.search.focused_match", [("foreground", flavour["bg"]), ("background", flavour["copper"])]),
        table("colors.hints.start", [("foreground", flavour["bg"]), ("background", flavour["copper"])]),
        table("colors.hints.end", [("foreground", flavour["bg"]), ("background", flavour["azurite"])]),
        table("colors.footer_bar", [("foreground", flavour["fg"]), ("background", flavour["fill"])]),
        table("colors.normal", [(name, flavour.ansi[name]) for name in names]),
        table("colors.bright", [(name, flavour.ansi[f"bright_{name}"]) for name in names]),
    ]
    return f"# {flavour.title}\n# {palette.homepage}\n\n" + "\n".join(tables)


def render(palette) -> dict:
    return {f"{f.slug}.toml": theme(palette, f) for f in palette.flavours.values()}
