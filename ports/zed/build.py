"""Zed theme family: both flavours in one file."""

import json

from palette import ANSI, mix

TRANSPARENT = "#00000000"
SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"

# Zed capture name to (syntax role, or palette colour prefixed with "=").
SYNTAX = {
    "attribute": "attribute", "boolean": "constant", "comment": "comment", "comment.doc": "comment",
    "constant": "constant", "constructor": "type", "embedded": "variable", "enum": "type",
    "function": "function", "hint": "=fg_subtle", "keyword": "keyword", "label": "label",
    "link_text": "link", "link_uri": "link", "namespace": "namespace", "number": "number",
    "operator": "operator", "predictive": "=fg_subtle", "preproc": "decorator", "primary": "variable",
    "property": "property", "property.json_key": "key", "punctuation": "punctuation",
    "punctuation.bracket": "punctuation", "punctuation.delimiter": "punctuation",
    "punctuation.list_marker": "=patina", "punctuation.markup": "=fg_muted",
    "punctuation.special": "escape", "selector": "attribute", "selector.pseudo": "attribute",
    "string": "string", "string.escape": "escape", "string.regex": "regex",
    "string.special": "escape", "string.special.symbol": "constant", "tag": "tag",
    "text.literal": "string", "title": "heading", "type": "type", "variable": "variable",
    "variable.special": "builtin", "variant": "constant",
}


def syntax(f) -> dict:
    styles = {}
    for capture, target in SYNTAX.items():
        if target.startswith("="):
            styles[capture] = {"color": f[target[1:]], "font_style": None, "font_weight": None}
            continue
        style = f.syntax[target]
        styles[capture] = {
            "color": style.color,
            "font_style": "italic" if style.italic else None,
            "font_weight": 700 if style.bold else None,
        }
    styles["emphasis"] = {"color": f["fg"], "font_style": "italic", "font_weight": None}
    styles["emphasis.strong"] = {"color": f["fg_strong"], "font_style": None, "font_weight": 700}
    return dict(sorted(styles.items()))


def style(f) -> dict:
    def a(name: str, alpha: float) -> str:
        return f[name] + f"{round(alpha * 255):02x}"

    def status(name: str, color: str, background: str) -> dict:
        return {name: f[color], f"{name}.background": f[background], f"{name}.border": a(color, 0.4)}

    def quiet(name: str) -> dict:
        return {name: f["fg_subtle"], f"{name}.background": f["bg"], f"{name}.border": f["line"]}

    hues = ["patina", "copper", "azurite", "bornite", "malachite", "brass", "cuprite"]
    colors = {
        "accents": [f[hue] for hue in hues],
        "background": f["bg_dim"],
        "background.appearance": "opaque",
        "border": f["line"],
        "border.variant": f["line"],
        "border.focused": a("patina", 0.6),
        "border.selected": f["patina"],
        "border.transparent": TRANSPARENT,
        "border.disabled": f["line"],
        "elevated_surface.background": f["bg_raised"],
        "surface.background": f["bg_dim"],
        "element.background": f["fill"],
        "element.hover": f["line"],
        "element.active": f["line_strong"],
        "element.selected": f["line"],
        "element.disabled": f["fill_soft"],
        "drop_target.background": a("patina", 0.15),
        "ghost_element.background": TRANSPARENT,
        "ghost_element.hover": a("fg", 0.06),
        "ghost_element.active": a("fg", 0.11),
        "ghost_element.selected": a("fg", 0.08),
        "ghost_element.disabled": TRANSPARENT,
        "text": f["fg"],
        "text.muted": f["fg_muted"],
        "text.placeholder": f["fg_subtle"],
        "text.disabled": f["fg_subtle"],
        "text.accent": f["patina"],
        "icon": f["fg"],
        "icon.muted": f["fg_muted"],
        "icon.disabled": f["fg_faint"],
        "icon.placeholder": f["fg_subtle"],
        "icon.accent": f["patina"],
        "status_bar.background": f["bg_dim"],
        "title_bar.background": f["bg_dim"],
        "title_bar.inactive_background": f["bg_dim"],
        "toolbar.background": f["bg"],
        "tab_bar.background": f["bg_dim"],
        "tab.inactive_background": f["bg_dim"],
        "tab.active_background": f["bg"],
        "search.match_background": a("copper", 0.3),
        "panel.background": f["bg_dim"],
        "panel.focused_border": a("patina", 0.6),
        "panel.indent_guide": f["line"],
        "panel.indent_guide_hover": f["line_strong"],
        "panel.indent_guide_active": f["line_strong"],
        "pane.focused_border": TRANSPARENT,
        "pane_group.border": f["line"],
        "scrollbar.thumb.background": a("fg_subtle", 0.25),
        "scrollbar.thumb.hover_background": a("fg_subtle", 0.4),
        "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": TRANSPARENT,
        "editor.foreground": f["fg"],
        "editor.background": f["bg"],
        "editor.gutter.background": f["bg"],
        "editor.subheader.background": f["bg_dim"],
        "editor.active_line.background": f["fill_soft"],
        "editor.highlighted_line.background": f["fill"],
        "editor.line_number": a("fg_subtle", 0.75),
        "editor.active_line_number": f["fg"],
        "editor.invisible": f["fg_faint"],
        "editor.wrap_guide": f["line"],
        "editor.active_wrap_guide": f["line_strong"],
        "editor.indent_guide": f["line"],
        "editor.indent_guide_active": f["line_strong"],
        "editor.document_highlight.read_background": a("patina", 0.14),
        "editor.document_highlight.write_background": a("patina", 0.22),
        "editor.document_highlight.bracket_background": a("patina", 0.2),
        "terminal.background": f.terminal["background"],
        "terminal.foreground": f.terminal["foreground"],
        "terminal.bright_foreground": f["fg_strong"],
        "terminal.dim_foreground": f["fg_muted"],
        "terminal.ansi.background": f.terminal["background"],
        "link_text.hover": f["patina"],
        **status("conflict", "bornite", "fill_soft"),
        **status("created", "malachite", "malachite_wash"),
        **status("deleted", "cuprite", "cuprite_wash"),
        **status("error", "cuprite", "cuprite_wash"),
        **status("info", "azurite", "azurite_wash"),
        **status("modified", "azurite", "azurite_wash"),
        **status("renamed", "patina", "patina_wash"),
        **status("success", "malachite", "malachite_wash"),
        **status("warning", "copper", "copper_wash"),
        **quiet("hidden"),
        **quiet("hint"),
        **quiet("ignored"),
        **quiet("predictive"),
        **quiet("unreachable"),
        "players": [{"cursor": f["patina"], "background": f["patina"], "selection": f["selection"]}]
        + [{"cursor": f[hue], "background": f[hue], "selection": a(hue, 0.24)} for hue in hues[1:]],
        "syntax": syntax(f),
    }
    for name in ANSI:
        colors[f"terminal.ansi.{name}"] = f.ansi[name]
    # Zed's dim colours are the normal ones stepped toward the background.
    for name in ANSI[:8]:
        colors[f"terminal.ansi.dim_{name}"] = mix(f.ansi[name], f.terminal["background"], 0.35)
    return colors


def render(palette) -> dict:
    family = {
        "$schema": SCHEMA,
        "name": palette.name,
        "author": palette.author,
        "themes": [
            {"name": f.title, "appearance": f.appearance, "style": style(f)}
            for f in palette.flavours.values()
        ],
    }
    return {"verdigris.json": json.dumps(family, indent=2) + "\n"}
