"""fish syntax colours: one theme with a [light] and a [dark] section.

fish picks the section that matches the terminal background.
"""

SPEC = [
    ("fish_color_normal", "fg"),
    ("fish_color_command", "patina"),
    ("fish_color_keyword", "patina"),
    ("fish_color_param", "fg"),
    ("fish_color_option", "fg_muted"),
    ("fish_color_quote", "malachite"),
    ("fish_color_escape", "brass"),
    ("fish_color_operator", "copper"),
    ("fish_color_redirection", "bornite"),
    ("fish_color_end", "fg_muted"),
    ("fish_color_error", "cuprite"),
    ("fish_color_comment", "fg_subtle"),
    ("fish_color_autosuggestion", "fg_subtle"),
    ("fish_color_cwd", "patina"),
    ("fish_color_cwd_root", "cuprite"),
    ("fish_color_user", "malachite"),
    ("fish_color_host", "fg_muted"),
    ("fish_color_host_remote", "brass"),
    ("fish_color_status", "cuprite"),
    ("fish_color_search_match", "--background={search}"),
    ("fish_color_selection", "--background={selection}"),
    ("fish_color_valid_path", "--underline"),
    ("fish_color_history_current", "--bold"),
    ("fish_color_cancel", "-r"),
    ("fish_pager_color_completion", "fg"),
    ("fish_pager_color_description", "fg_subtle"),
    ("fish_pager_color_prefix", "{patina} --bold --underline"),
    ("fish_pager_color_progress", "{bg} --background={patina}"),
    ("fish_pager_color_selected_background", "--background={fill}"),
]


def value(flavour, spec: str) -> str:
    # fish reads "#" in a theme file as the start of a comment.
    if spec.startswith("-") or "{" in spec:
        return spec.format(**{k: v.lstrip("#") for k, v in flavour.colors.items()})
    return flavour[spec].lstrip("#")


def render(palette) -> dict:
    lines = ["# name: Verdigris", f"# url: {palette.homepage}"]
    for flavour in (palette.light, palette.dark):
        lines.append(f"[{flavour.appearance}]")
        lines.append(f"# preferred_background: {flavour['bg'].lstrip('#')}")
        lines += [f"{name} {value(flavour, spec)}" for name, spec in SPEC]
    return {"verdigris.theme": "\n".join(lines) + "\n"}
