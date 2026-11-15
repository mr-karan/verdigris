"""WezTerm colour schemes (TOML files for color_scheme_dirs)."""


def strings(values: list) -> str:
    return "[\n" + "".join(f'    "{value}",\n' for value in values) + "]"


def table(name: str, pairs: list) -> str:
    return "\n".join([f"[{name}]"] + [f'{key} = "{value}"' for key, value in pairs]) + "\n"


def tab(name: str, background: str, foreground: str) -> str:
    return table(f"colors.tab_bar.{name}", [("bg_color", background), ("fg_color", foreground)])


def theme(palette, flavour) -> str:
    terminal = flavour.terminal
    colors = "\n".join([
        "[colors]",
        f'foreground = "{terminal["foreground"]}"',
        f'background = "{terminal["background"]}"',
        f'cursor_bg = "{terminal["cursor"]}"',
        f'cursor_fg = "{terminal["cursor_text"]}"',
        f'cursor_border = "{terminal["cursor"]}"',
        f'selection_fg = "{terminal["selection_foreground"]}"',
        f'selection_bg = "{terminal["selection_background"]}"',
        f'scrollbar_thumb = "{flavour["line_strong"]}"',
        f'split = "{flavour["line"]}"',
        f'compose_cursor = "{flavour["copper"]}"',
        f'visual_bell = "{flavour["fill"]}"',
        f"ansi = {strings(flavour.ansi_list[:8])}",
        f"brights = {strings(flavour.ansi_list[8:])}",
    ]) + "\n"
    tables = [
        colors,
        table("colors.tab_bar", [("background", flavour["bg_dim"]), ("inactive_tab_edge", flavour["line"])]),
        tab("active_tab", flavour["bg"], flavour["fg_strong"]),
        tab("inactive_tab", flavour["bg_dim"], flavour["fg_muted"]),
        tab("inactive_tab_hover", flavour["fill"], flavour["fg"]),
        tab("new_tab", flavour["bg_dim"], flavour["fg_muted"]),
        tab("new_tab_hover", flavour["fill"], flavour["fg"]),
        table("metadata", [
            ("name", flavour.title), ("author", palette.author), ("origin_url", palette.homepage),
        ]),
    ]
    return "\n".join(tables)


def render(palette) -> dict:
    return {f"{f.slug}.toml": theme(palette, f) for f in palette.flavours.values()}
