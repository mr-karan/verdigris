"""Helix themes. Scopes name palette colours; [palette] holds the hex values."""

# Helix scope to syntax role.
SYNTAX = {
    "attribute": "attribute", "type": "type", "type.builtin": "type", "type.enum.variant": "constant",
    "constructor": "type", "constant": "constant", "constant.builtin": "constant",
    "constant.character": "string", "constant.character.escape": "escape",
    "constant.numeric": "number", "string": "string", "string.regexp": "regex",
    "string.special": "escape", "string.special.url": "link", "string.special.symbol": "constant",
    "comment": "comment", "variable": "variable", "variable.builtin": "builtin",
    "variable.parameter": "parameter", "variable.other.member": "property", "label": "label",
    "punctuation": "punctuation", "punctuation.special": "escape", "keyword": "keyword",
    "keyword.directive": "decorator", "operator": "operator", "function": "function",
    "function.macro": "decorator", "function.special": "decorator", "tag": "tag",
    "namespace": "namespace", "markup.heading": "heading", "markup.link.url": "link",
    "markup.raw": "string",
}

# Helix scope to (fg, bg, modifiers). None leaves a field unset.
UI = {
    "special": ("patina", None, []),
    "markup.list": ("patina", None, []),
    "markup.bold": ("fg_strong", None, ["bold"]),
    "markup.italic": (None, None, ["italic"]),
    "markup.strikethrough": (None, None, ["crossed_out"]),
    "markup.link.label": ("azurite", None, []),
    "markup.link.text": ("azurite", None, []),
    "markup.quote": ("fg_muted", None, ["italic"]),
    "diff.plus": ("malachite", None, []),
    "diff.minus": ("cuprite", None, []),
    "diff.delta": ("azurite", None, []),
    "ui.background": (None, "bg", []),
    "ui.background.separator": ("line", None, []),
    "ui.text": ("fg", None, []),
    "ui.text.focus": ("patina", None, ["bold"]),
    "ui.text.inactive": ("fg_subtle", None, []),
    "ui.text.info": ("fg", None, []),
    "ui.text.directory": ("azurite", None, []),
    "ui.cursor": ("bg", "fg_muted", []),
    "ui.cursor.primary": ("bg", "patina", []),
    "ui.cursor.match": (None, "selection", ["bold"]),
    "ui.selection": (None, "fill", []),
    "ui.selection.primary": (None, "selection", []),
    "ui.cursorline.primary": (None, "fill_soft", []),
    "ui.cursorline.secondary": (None, "fill_soft", []),
    "ui.cursorcolumn.primary": (None, "fill_soft", []),
    "ui.linenr": ("fg_subtle", None, []),
    "ui.linenr.selected": ("fg", None, ["bold"]),
    "ui.gutter": (None, "bg", []),
    "ui.statusline": ("fg", "bg_dim", []),
    "ui.statusline.inactive": ("fg_subtle", "bg_dim", []),
    "ui.statusline.normal": ("bg", "patina", ["bold"]),
    "ui.statusline.insert": ("bg", "malachite", ["bold"]),
    "ui.statusline.select": ("bg", "bornite", ["bold"]),
    "ui.statusline.separator": ("line", None, []),
    "ui.bufferline": ("fg_subtle", "bg_dim", []),
    "ui.bufferline.active": ("fg_strong", "bg", ["bold"]),
    "ui.bufferline.background": (None, "bg_dim", []),
    "ui.popup": ("fg", "bg_raised", []),
    "ui.popup.info": ("fg", "bg_raised", []),
    "ui.window": ("line", None, []),
    "ui.help": ("fg", "bg_raised", []),
    "ui.menu": ("fg", "bg_raised", []),
    "ui.menu.selected": ("fg_strong", "fill", []),
    "ui.menu.scroll": ("line_strong", "bg_raised", []),
    "ui.picker.header": ("fg_muted", None, ["bold"]),
    "ui.virtual.ruler": (None, "fill_soft", []),
    "ui.virtual.whitespace": ("fg_faint", None, []),
    "ui.virtual.indent-guide": ("line", None, []),
    "ui.virtual.inlay-hint": ("fg_subtle", None, []),
    "ui.virtual.wrap": ("fg_faint", None, []),
    "ui.virtual.jump-label": ("copper", None, ["bold"]),
    "ui.highlight": (None, "fill", []),
    "ui.highlight.frameline": (None, "copper_wash", []),
    "ui.debug.breakpoint": ("cuprite", None, []),
    "ui.debug.active": ("malachite", None, []),
    "warning": ("copper", None, []),
    "error": ("cuprite", None, []),
    "info": ("azurite", None, []),
    "hint": ("patina", None, []),
    "diagnostic.unnecessary": (None, None, ["dim"]),
    "diagnostic.deprecated": (None, None, ["crossed_out"]),
}

DIAGNOSTICS = {"hint": "patina", "info": "azurite", "warning": "copper", "error": "cuprite"}


def spec(fg, bg, modifiers: list) -> str:
    if fg and not bg and not modifiers:
        return f'"{fg}"'
    parts = [f'fg = "{fg}"'] if fg else []
    parts += [f'bg = "{bg}"'] if bg else []
    # Helix has no "underline" modifier: an underline is its own table.
    if "underline" in modifiers:
        parts.append('underline = { style = "line" }')
    modifiers = [m for m in modifiers if m != "underline"]
    if modifiers:
        parts.append("modifiers = [" + ", ".join(f'"{m}"' for m in modifiers) + "]")
    return "{ " + ", ".join(parts) + " }"


def theme(palette, flavour) -> str:
    colors = set(flavour.colors)
    lines = [f"# {flavour.title}", f"# {palette.homepage}", ""]
    for scope, role in SYNTAX.items():
        style = palette.roles["syntax"][role]
        lines.append(f'"{scope}" = {spec(style["color"], None, style.get("style", "").split())}')
    lines.append("")
    for scope, (fg, bg, modifiers) in UI.items():
        assert {fg, bg} - {None} <= colors, f"{scope}: unknown colour"
        lines.append(f'"{scope}" = {spec(fg, bg, modifiers)}')
    lines.append('"diagnostic" = { underline = { style = "curl" } }')
    lines += [
        f'"diagnostic.{level}" = {{ underline = {{ color = "{color}", style = "curl" }} }}'
        for level, color in DIAGNOSTICS.items()
    ]
    lines += ["", "[palette]"]
    lines += [f'{name} = "{value}"' for name, value in flavour.colors.items()]
    return "\n".join(lines) + "\n"


def render(palette) -> dict:
    return {f"{f.slug.replace('-', '_')}.toml": theme(palette, f) for f in palette.flavours.values()}
