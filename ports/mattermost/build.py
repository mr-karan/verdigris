"""Mattermost custom themes: one JSON per flavour, pasted into Settings."""

import json

SPEC = {
    "sidebarTeamBarBg": "bg_dim",
    "sidebarBg": "bg_dim",
    "sidebarHeaderBg": "bg_dim",
    "sidebarHeaderTextColor": "fg_strong",
    "sidebarText": "fg_muted",
    "sidebarUnreadText": "fg_strong",
    "sidebarTextHoverBg": "fill",
    "sidebarTextActiveBorder": "patina",
    "sidebarTextActiveColor": "fg_strong",
    "onlineIndicator": "malachite",
    "awayIndicator": "copper",
    "dndIndicator": "cuprite",
    "mentionBg": "patina",
    "mentionBj": "patina",
    "mentionColor": "bg",
    "centerChannelBg": "bg",
    "centerChannelColor": "fg",
    "newMessageSeparator": "copper",
    "linkColor": "patina",
    "buttonBg": "patina",
    "buttonColor": "bg",
    "errorTextColor": "cuprite",
    "mentionHighlightBg": "search",
    "mentionHighlightLink": "fg_strong",
}

# Mattermost offers four fixed code themes and none take custom colours.
CODE_THEME = {"light": "github", "dark": "monokai"}


def render(palette) -> dict:
    files = {}
    for flavour in palette.flavours.values():
        theme = {key: flavour[color] for key, color in sorted(SPEC.items())}
        theme["codeTheme"] = CODE_THEME[flavour.appearance]
        files[f"{flavour.slug}.json"] = json.dumps(theme, indent=2) + "\n"
    return files
