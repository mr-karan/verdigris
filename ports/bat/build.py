"""TextMate .tmTheme files for bat, delta and Sublime Text, plus delta styles."""

import plistlib
import uuid

import textmate
from palette import TEXT, contrast, mix

# How far a word-level diff highlight moves from the line wash toward its hue.
EMPHASIS = 0.16


def tm_theme(palette, flavour) -> str:
    settings = [{
        "settings": {
            "background": flavour["bg"],
            "foreground": flavour["fg"],
            "caret": flavour["patina"],
            "lineHighlight": flavour["fill_soft"],
            "selection": flavour["selection"],
            "invisibles": flavour["fg_faint"],
            "guide": flavour["line"],
            "stackGuide": flavour["line"],
            "activeGuide": flavour["line_strong"],
            "gutter": flavour["bg"],
            "gutterForeground": flavour["fg_subtle"],
            "findHighlight": flavour["search"],
            "findHighlightForeground": flavour["fg_strong"],
            "accent": flavour["patina"],
            "misspelling": flavour["cuprite"],
        }
    }]
    for label, scopes, style in textmate.rules(flavour):
        rule = {"foreground": style.color}
        if textmate.font_style(style):
            rule["fontStyle"] = textmate.font_style(style)
        settings.append({"name": label, "scope": ", ".join(scopes), "settings": rule})
    theme = {
        "name": flavour.title,
        "author": palette.author,
        "comment": palette.homepage,
        "colorSpaceName": "sRGB",
        "semanticClass": f"theme.{flavour.appearance}.{flavour.slug.replace('-', '_')}",
        "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, f"{palette.homepage}#{flavour.slug}")),
        "settings": settings,
    }
    return plistlib.dumps(theme, sort_keys=False).decode()


def delta_feature(flavour) -> str:
    minus_emph = mix(flavour["cuprite_wash"], flavour["cuprite"], EMPHASIS)
    plus_emph = mix(flavour["malachite_wash"], flavour["malachite"], EMPHASIS)
    for emph in (minus_emph, plus_emph):
        assert contrast(flavour["fg"], emph) >= TEXT, f"{flavour.key}: text on diff emphasis {emph}"
    lines = [
        f'[delta "{flavour.slug}"]',
        f"\t{'dark' if flavour.dark else 'light'} = true",
        f"\tsyntax-theme = {flavour.slug}",
        f'\tminus-style = syntax "{flavour["cuprite_wash"]}"',
        f'\tminus-emph-style = syntax "{minus_emph}"',
        f'\tplus-style = syntax "{flavour["malachite_wash"]}"',
        f'\tplus-emph-style = syntax "{plus_emph}"',
        f'\tline-numbers-minus-style = "{flavour["cuprite"]}"',
        f'\tline-numbers-plus-style = "{flavour["malachite"]}"',
        f'\tline-numbers-zero-style = "{flavour["fg_subtle"]}"',
        f'\tline-numbers-left-style = "{flavour["line"]}"',
        f'\tline-numbers-right-style = "{flavour["line"]}"',
        f'\tfile-style = "{flavour["fg_strong"]}" bold',
        f'\tfile-decoration-style = "{flavour["line"]}" ul',
        '\thunk-header-style = file line-number syntax',
        f'\thunk-header-file-style = "{flavour["fg_muted"]}"',
        f'\thunk-header-line-number-style = "{flavour["copper"]}"',
        f'\thunk-header-decoration-style = "{flavour["line"]}" box',
        f'\tcommit-style = "{flavour["patina"]}" bold',
        f'\tcommit-decoration-style = "{flavour["line"]}" ul',
        f'\tblame-palette = "{flavour["bg"]}" "{flavour["bg_dim"]}" "{flavour["fill_soft"]}" "{flavour["fill"]}"',
        f'\tmerge-conflict-ours-diff-header-style = "{flavour["azurite"]}" bold',
        f'\tmerge-conflict-theirs-diff-header-style = "{flavour["bornite"]}" bold',
        '\tmerge-conflict-begin-symbol = "~"',
        '\tmerge-conflict-end-symbol = "~"',
    ]
    return "\n".join(lines) + "\n"


def render(palette) -> dict:
    files = {f"{f.slug}.tmTheme": tm_theme(palette, f) for f in palette.flavours.values()}
    files["verdigris.gitconfig"] = "\n".join(delta_feature(f) for f in palette.flavours.values())
    return files
