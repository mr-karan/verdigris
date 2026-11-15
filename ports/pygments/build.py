"""Pygments styles, installable as a package that registers both by name."""

MODULE = "pygments_verdigris"

# Pygments token to syntax role.
TOKENS = {
    "Comment": "comment", "Comment.Preproc": "decorator", "Comment.PreprocFile": "string",
    "Keyword": "keyword", "Keyword.Constant": "constant", "Keyword.Type": "type",
    "Operator": "operator", "Operator.Word": "keyword", "Punctuation": "punctuation",
    "Name": "variable", "Name.Function": "function", "Name.Function.Magic": "function",
    "Name.Builtin": "function", "Name.Builtin.Pseudo": "builtin", "Name.Class": "type",
    "Name.Exception": "type", "Name.Decorator": "decorator", "Name.Constant": "constant",
    "Name.Namespace": "namespace", "Name.Tag": "tag", "Name.Attribute": "attribute",
    "Name.Label": "label", "Name.Entity": "constant", "Name.Property": "property",
    "Name.Variable.Magic": "builtin",
    "String": "string", "String.Doc": "comment", "String.Escape": "escape",
    "String.Interpol": "escape", "String.Regex": "regex", "String.Symbol": "constant",
    "Number": "number",
    "Generic.Heading": "heading", "Generic.Subheading": "heading",
}

# Pygments token to (palette colour, style words).
PLAIN = {
    "Token": ("fg", ""), "Whitespace": ("fg_faint", ""), "Error": ("cuprite", ""),
    "Generic.Deleted": ("cuprite", ""), "Generic.Inserted": ("malachite", ""),
    "Generic.Error": ("cuprite", ""), "Generic.Traceback": ("cuprite", ""),
    "Generic.Prompt": ("fg_subtle", ""), "Generic.Output": ("fg_muted", ""),
    "Generic.Emph": ("fg", "italic"), "Generic.Strong": ("fg_strong", "bold"),
    "Generic.EmphStrong": ("fg_strong", "bold italic"),
}


def style_class(flavour) -> str:
    rules = {token: f"{words} {flavour[color]}".strip() for token, (color, words) in PLAIN.items()}
    for token, role in TOKENS.items():
        style = flavour.syntax[role]
        words = [word for word in ("bold", "italic", "underline") if getattr(style, word)]
        # A child token inherits its parent's italics unless it says otherwise.
        words += [] if style.italic else ["noitalic"]
        rules[token] = " ".join(words + [style.color])
    body = "\n".join(f'        {token}: "{rule}",' for token, rule in rules.items())
    name = flavour.title.replace(" ", "")
    return f'''class {name}Style(Style):
    """{flavour.title}: the {flavour.appearance} flavour."""

    name = "{flavour.slug}"
    background_color = "{flavour["bg"]}"
    highlight_color = "{flavour["fill_soft"]}"
    line_number_color = "{flavour["fg_subtle"]}"
    line_number_background_color = "{flavour["bg"]}"
    line_number_special_color = "{flavour["fg"]}"
    line_number_special_background_color = "{flavour["fill_soft"]}"
    styles = {{
{body}
    }}
'''


def module(palette) -> str:
    head = f'''"""{palette.name} for Pygments. Generated from palette.json: edit that, then run build.py.

{palette.homepage}
"""

from pygments.style import Style
from pygments.token import (
    Comment, Error, Generic, Keyword, Name, Number, Operator, Punctuation, String, Token, Whitespace,
)

'''
    return head + "\n\n".join(style_class(f) for f in palette.flavours.values())


def project(palette) -> str:
    entries = "\n".join(
        f'{f.slug} = "{MODULE}:{f.title.replace(" ", "")}Style"' for f in palette.flavours.values()
    )
    return f'''[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "pygments-verdigris"
version = "{palette.version}"
description = "{palette.description}"
readme = "README.md"
license = {{ text = "{palette.license}" }}
authors = [{{ name = "{palette.author}" }}]
requires-python = ">=3.8"
dependencies = ["pygments>=2.11"]

[project.urls]
Homepage = "{palette.homepage}"

[project.entry-points."pygments.styles"]
{entries}

[tool.setuptools]
py-modules = ["{MODULE}"]
'''


def render(palette) -> dict:
    return {f"{MODULE}.py": module(palette), "pyproject.toml": project(palette)}
