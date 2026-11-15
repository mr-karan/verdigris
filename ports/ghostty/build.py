"""Ghostty themes."""


def theme(palette, flavour) -> str:
    terminal = flavour.terminal
    lines = [f"# {flavour.title}", f"# {palette.homepage}", ""]
    lines += [f"palette = {index}={color}" for index, color in enumerate(flavour.ansi_list)]
    lines += [
        f"background = {terminal['background']}",
        f"foreground = {terminal['foreground']}",
        f"cursor-color = {terminal['cursor']}",
        f"cursor-text = {terminal['cursor_text']}",
        f"selection-background = {terminal['selection_background']}",
        f"selection-foreground = {terminal['selection_foreground']}",
        f"split-divider-color = {flavour['line']}",
    ]
    return "\n".join(lines) + "\n"


def render(palette) -> dict:
    return {f.slug: theme(palette, f) for f in palette.flavours.values()}
