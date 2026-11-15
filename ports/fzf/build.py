"""fzf colours, as a shell and a fish snippet per flavour."""


def colors(flavour) -> list:
    spec = [
        ("fg", "fg"), ("bg", "bg"), ("hl", "patina"),
        ("fg+", "fg_strong"), ("bg+", "fill"), ("hl+", "patina"),
        ("gutter", "bg"), ("query", "fg"), ("disabled", "fg_subtle"),
        ("info", "fg_subtle"), ("prompt", "patina"), ("pointer", "copper"),
        ("marker", "malachite"), ("spinner", "copper"), ("header", "azurite"),
        ("border", "line_strong"), ("label", "fg_muted"),
        ("separator", "line"), ("scrollbar", "line_strong"),
    ]
    pairs = [f"{key}:{flavour[color]}" for key, color in spec]
    return ["--color=" + ",".join(pairs[index : index + 6]) for index in range(0, len(pairs), 6)]


def render(palette) -> dict:
    files = {}
    for flavour in palette.flavours.values():
        header = f"# {flavour.title} for fzf\n# {palette.homepage}\n"
        options = " \\\n  ".join(colors(flavour))
        files[f"{flavour.slug}.sh"] = (
            f'{header}export FZF_DEFAULT_OPTS="${{FZF_DEFAULT_OPTS:-}} \\\n  {options}"\n'
        )
        files[f"{flavour.slug}.fish"] = (
            f'{header}set -gx FZF_DEFAULT_OPTS "$FZF_DEFAULT_OPTS \\\n  {options}"\n'
        )
    return files
