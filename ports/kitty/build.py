"""kitty themes."""


def theme(palette, flavour) -> str:
    terminal = flavour.terminal
    settings = [
        ("foreground", terminal["foreground"]),
        ("background", terminal["background"]),
        ("selection_foreground", terminal["selection_foreground"]),
        ("selection_background", terminal["selection_background"]),
        ("cursor", terminal["cursor"]),
        ("cursor_text_color", terminal["cursor_text"]),
        ("url_color", flavour["azurite"]),
        ("active_border_color", flavour["patina"]),
        ("inactive_border_color", flavour["line"]),
        ("bell_border_color", flavour["copper"]),
        ("active_tab_foreground", flavour["fg_strong"]),
        ("active_tab_background", flavour["bg"]),
        ("inactive_tab_foreground", flavour["fg_muted"]),
        ("inactive_tab_background", flavour["bg_dim"]),
        ("tab_bar_background", flavour["bg_dim"]),
        ("mark1_foreground", flavour["bg"]),
        ("mark1_background", flavour["patina"]),
        ("mark2_foreground", flavour["bg"]),
        ("mark2_background", flavour["copper"]),
        ("mark3_foreground", flavour["bg"]),
        ("mark3_background", flavour["bornite"]),
    ]
    settings += [(f"color{index}", color) for index, color in enumerate(flavour.ansi_list)]
    header = [
        f"## name: {flavour.title}",
        f"## author: {palette.author}",
        f"## license: {palette.license}",
        f"## upstream: {palette.homepage}/blob/main/ports/kitty/{flavour.slug}.conf",
        f"## blurb: {palette.description}",
        "",
    ]
    return "\n".join(header + [f"{key:<24}{value}" for key, value in settings]) + "\n"


def render(palette) -> dict:
    return {f"{f.slug}.conf": theme(palette, f) for f in palette.flavours.values()}
