"""Generated documentation: the README's palette and contrast tables, and the
swatch images those tables use."""

import re

import palette as pal

STONE = [
    "bg_dim", "bg", "bg_raised", "fill_soft", "fill", "line", "line_strong",
    "fg_faint", "fg_subtle", "fg_muted", "fg", "fg_strong",
]
TINTS = pal.WASHES + ["selection", "search"]


def swatch(color: str) -> str:
    # A mid-grey edge keeps a pale swatch visible on a light page and a dark one on a dark page.
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">'
        f'<rect x="0.5" y="0.5" width="19" height="19" rx="5" fill="{color}" stroke="#808080" stroke-opacity="0.35"/>'
        "</svg>\n"
    )


def cell(flavour: pal.Flavour, name: str) -> str:
    image = f"assets/swatches/{flavour.key}/{name}.svg"
    return f'<img src="{image}" width="16" height="16" alt=""> `{flavour[name]}`'


def table(palette: pal.Palette, names: list) -> str:
    flavours = list(palette.flavours.values())
    head = "| Colour | " + " | ".join(f.name for f in flavours) + " | Used for |"
    rule = "| --- | " + " | ".join("---" for _ in flavours) + " | --- |"
    rows = [
        f"| `{name}` | " + " | ".join(cell(f, name) for f in flavours) + f" | {palette.notes[name]} |"
        for name in names
    ]
    return "\n".join([head, rule, *rows])


def palette_section(palette: pal.Palette) -> str:
    return "\n\n".join([
        "### Copper",
        table(palette, pal.HUES),
        "### Stone",
        table(palette, STONE),
        "<details>\n<summary>Bright variants and washes</summary>",
        table(palette, pal.BRIGHTS),
        table(palette, TINTS),
        "</details>",
    ])


def contrast_section(palette: pal.Palette) -> str:
    flavours = list(palette.flavours.values())
    rows = [
        ("Text", "fg", pal.TEXT), ("Emphasis", "fg_strong", pal.TEXT), ("Muted text", "fg_muted", pal.TEXT),
        ("Comments", "fg_subtle", pal.QUIET),
    ] + [(f"`{hue}`", hue, pal.TEXT) for hue in pal.HUES]
    lines = [
        "| On the editor background | Minimum | " + " | ".join(f.name for f in flavours) + " |",
        "| --- | --- | " + " | ".join("---" for _ in flavours) + " |",
    ]
    for label, name, minimum in rows:
        ratios = " | ".join(f"{pal.contrast(f[name], f['bg']):.2f}" for f in flavours)
        lines.append(f"| {label} | {minimum} | {ratios} |")
    pairs = pal.contrast_pairs(palette)
    body = [p for p in pairs if p.minimum == pal.TEXT]
    worst = " and ".join(
        f"{min(p.ratio for p in body if p.flavour == f.key):.2f} in {f.name}" for f in flavours
    )
    lines.append("")
    lines.append(
        f"The build checks {len(pairs)} pairs. The lowest ratio among the {len(body)} "
        f"body-text pairs is {worst}."
    )
    return "\n".join(lines)


def fill(readme: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!-- {name}:start -->\n)(?:.*?\n)?(<!-- {name}:end -->)", re.S)
    if not pattern.search(readme):
        raise SystemExit(f"README.md: add the markers <!-- {name}:start --> and <!-- {name}:end -->")
    return pattern.sub(lambda match: f"{match[1]}\n{content}\n\n{match[2]}", readme)


def render(palette: pal.Palette) -> dict:
    files = {
        pal.ROOT / "assets" / "swatches" / flavour.key / f"{name}.svg": swatch(color)
        for flavour in palette.flavours.values()
        for name, color in flavour.colors.items()
    }
    readme = (pal.ROOT / "README.md").read_text()
    readme = fill(readme, "palette", palette_section(palette))
    readme = fill(readme, "contrast", contrast_section(palette))
    files[pal.ROOT / "README.md"] = readme
    return files
