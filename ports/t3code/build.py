"""T3 Code theme, checked against T3's limits.

Verdigris: weathered stone and patinated copper. Neutrals carry a faint
grey-green cast, the accent is the blue-green of copper patina, and bare
copper is the one warm note (warnings, search matches).

Run from the repository root: python3 build.py t3code
"""

import json
import re

from palette import contrast, rgb

ROLES = """
canvas chrome toolbar toolbarForeground toolbarBorder toolbarControl
toolbarControlForeground toolbarControlHover surface surfaceRaised
surfaceOverlay text textMuted border input focus accent accentForeground
secondary secondaryForeground muted mutedForeground placeholder secondaryLabel
iconMuted error errorForeground errorSurface warning warningForeground
warningSurface update updateForeground updateSurface accentSurface
accentSurfaceForeground messageSurface messageForeground messageAction
messageActionForeground messageActionHover codeBackground codeForeground
searchMatchBackground searchMatchForeground searchMatchActiveBackground
searchMatchActiveForeground sidebar sidebarForeground sidebarMutedForeground
sidebarControlSurface sidebarRowHover sidebarRowActive sidebarRowSelected
sidebarBorder terminalBackground terminalForeground terminalCursor
terminalSelection terminalScrollbar terminalScrollbarHover
""".split()

# Roles both flavours take from palette.json.
SHARED = {
    "canvas": "bg", "chrome": "bg_dim", "toolbar": "bg",
    "surfaceRaised": "bg_raised",
    "text": "fg_strong", "textMuted": "fg_muted",
    "border": "line", "input": "line_strong", "focus": "patina", "accent": "patina",
    "secondary": "fill", "muted": "fill_soft",
    "error": "cuprite", "errorSurface": "cuprite_wash",
    "warning": "copper", "warningSurface": "copper_wash",
    "update": "azurite", "updateSurface": "azurite_wash",
    "accentSurface": "patina_wash",
    "messageForeground": "fg_strong", "codeForeground": "fg",
    "searchMatchBackground": "search",
    "sidebar": "bg_dim",
    "terminalForeground": "fg", "terminalCursor": "patina",
    "terminalSelection": "selection", "terminalScrollbarHover": "fg_faint",
}

# The rest is tuned per flavour. A name is a palette.json colour; a hex is a
# tint only T3's chrome needs, so it lives here and not in the palette.

# Limestone: a soft grey-green paper, never white.
LIGHT = {
    "toolbarForeground": "#2a322f", "toolbarBorder": "line",
    "toolbarControl": "#fafaf7", "toolbarControlForeground": "#2a322f", "toolbarControlHover": "#e5e7e0",
    "surface": "#f7f7f3", "surfaceOverlay": "#fcfcfa",
    "accentForeground": "#f6fbf9",
    "secondaryForeground": "#2a322f", "mutedForeground": "fg_muted",
    "placeholder": "#77817d", "secondaryLabel": "#4e5955", "iconMuted": "#77817d",
    "errorForeground": "#fffaf8", "warningForeground": "#fffaf5", "updateForeground": "#f8fbfe",
    "accentSurfaceForeground": "#1f564d",
    "messageSurface": "#e8eae3",
    "messageAction": "#dfe1d9", "messageActionForeground": "#2a322f", "messageActionHover": "#d5d8cf",
    "codeBackground": "#eaebe5",
    "searchMatchForeground": "#2a1c0e",
    "searchMatchActiveBackground": "#cf9160", "searchMatchActiveForeground": "#1d1206",
    "sidebarForeground": "#2a322f", "sidebarMutedForeground": "#586360",
    "sidebarControlSurface": "#e3e5de", "sidebarRowHover": "#e3e5de",
    "sidebarRowActive": "#dcdfd7", "sidebarRowSelected": "#d9e6e1", "sidebarBorder": "line",
    "terminalBackground": "#eff0ea", "terminalScrollbar": "line_strong",
}

# Slate: deep green-grey, never black.
DARK = {
    "toolbarForeground": "#c6cfcb", "toolbarBorder": "#252d2b",
    "toolbarControl": "fill_soft", "toolbarControlForeground": "fg", "toolbarControlHover": "#232b29",
    "surface": "#191f1e", "surfaceOverlay": "fill",
    "accentForeground": "#0b1b17",
    "secondaryForeground": "fg", "mutedForeground": "#8a9692",
    "placeholder": "#727e7a", "secondaryLabel": "#9ea9a5", "iconMuted": "fg_subtle",
    "errorForeground": "#230c0a", "warningForeground": "#221306", "updateForeground": "#0a1522",
    "accentSurfaceForeground": "#a5d8cb",
    "messageSurface": "#1f2625",
    "messageAction": "#262e2c", "messageActionForeground": "#c9d1cd", "messageActionHover": "#2e3735",
    "codeBackground": "#101514",
    "searchMatchForeground": "#f6e7d6",
    "searchMatchActiveBackground": "copper", "searchMatchActiveForeground": "#221306",
    "sidebarForeground": "#c0c9c5", "sidebarMutedForeground": "#87938f",
    "sidebarControlSurface": "#181e1d", "sidebarRowHover": "#181e1d",
    "sidebarRowActive": "#1d2423", "sidebarRowSelected": "#1a2925", "sidebarBorder": "#1c2221",
    "terminalBackground": "#101514", "terminalScrollbar": "#2b3432",
}

# @flavour.colour@ is a palette.json colour, @flavour.colour.rgb@ its channels.
CSS = """
/* Verdigris: stone and copper patina. Only T3's documented stable selectors. */
:root {
  --vg-sans: "Inter Variable", "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --vg-mono: "CommitMono", "JetBrainsMono Nerd Font", "JetBrains Mono", ui-monospace, monospace;
  /* T3's own font tokens: the rest of the UI follows without per-element rules. */
  --font-sans: var(--vg-sans);
  --font-mono: var(--vg-mono);
}
:root:not(.dark) {
  --vg-accent: @light.patina@; --vg-copper: @light.copper@; --vg-line: @light.line@; --vg-line-soft: @light.fill@;
  --vg-ink: @light.fg_strong@; --vg-quiet: @light.fg_muted@; --vg-chip: @light.fill@;
  --vg-wash: rgba(@light.patina.rgb@, 0.045);
  --vg-shadow: 0 1px 2px rgba(30, 40, 36, 0.05), 0 10px 28px -6px rgba(30, 40, 36, 0.10);
  --vg-lift: 0 1px 2px rgba(30, 40, 36, 0.04), 0 4px 14px -4px rgba(30, 40, 36, 0.07);
}
.dark {
  --vg-accent: @dark.patina@; --vg-copper: @dark.copper@; --vg-line: @dark.line@; --vg-line-soft: #212827;
  --vg-ink: @dark.fg_strong@; --vg-quiet: @dark.fg_muted@; --vg-chip: #232b29;
  --vg-wash: rgba(@dark.patina.rgb@, 0.035);
  --vg-shadow: 0 1px 2px rgba(0, 0, 0, 0.35), 0 14px 34px -8px rgba(0, 0, 0, 0.45);
  --vg-lift: 0 1px 2px rgba(0, 0, 0, 0.3), 0 6px 18px -6px rgba(0, 0, 0, 0.35);
}

::selection { background: color-mix(in srgb, var(--vg-accent) 26%, transparent); }

/* Conversation: a barely-there patina wash behind the first messages. */
[data-workspace-area="conversation"] {
  background-image: linear-gradient(180deg, var(--vg-wash), transparent 320px);
}
[data-chat-header] { border-bottom: 1px solid var(--vg-line-soft) !important; }

/* Prose */
.chat-markdown, .composer-tiptap, [data-user-message-bubble] {
  font-family: var(--vg-sans);
  font-feature-settings: "calt", "cv05", "ss03";
  font-optical-sizing: auto;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}
.chat-markdown { line-height: 1.65; letter-spacing: -0.003em; }
.composer-tiptap { line-height: 1.6; }
.chat-markdown h1, .chat-markdown h2, .chat-markdown h3, .chat-markdown h4 {
  font-weight: 600; letter-spacing: -0.014em; line-height: 1.3;
}
.chat-markdown strong { font-weight: 600; }
.chat-markdown a {
  color: var(--vg-accent);
  text-decoration: underline;
  text-decoration-color: color-mix(in srgb, var(--vg-accent) 35%, transparent);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  transition: text-decoration-color 140ms ease;
}
.chat-markdown a:hover { text-decoration-color: var(--vg-accent); }
.chat-markdown blockquote {
  border-left: 2px solid color-mix(in srgb, var(--vg-accent) 45%, transparent);
  color: var(--vg-quiet);
}
.chat-markdown hr { border-color: var(--vg-line-soft); }
.chat-markdown thead th { font-weight: 600; color: var(--vg-quiet); }

/* Code */
.chat-markdown code, .chat-markdown pre, .chat-markdown-codeblock, .composer-tiptap code {
  font-family: var(--vg-mono) !important;
  font-feature-settings: normal;
  font-variant-ligatures: none;
  letter-spacing: 0;
}
.chat-markdown :not(pre) > code {
  font-size: 0.875em;
  padding: 0.12em 0.36em;
  border-radius: 5px;
  border: 1px solid var(--vg-line-soft);
  background: var(--vg-chip);
}
.chat-markdown pre { line-height: 1.55; font-size: 0.86em; }
.chat-markdown-codeblock {
  border: 1px solid var(--vg-line) !important;
  border-radius: 10px !important;
  overflow: hidden;
}

/* Messages */
[data-user-message-bubble] {
  border: 1px solid var(--vg-line-soft) !important;
  border-radius: 14px !important;
  line-height: 1.6;
}

/* Quoted response in a user message: a pull quote with a patina rail.
   Not on T3's stable list: the card is the bubble's link with data-thread-find-ignore. */
[data-user-message-bubble] a[data-thread-find-ignore] {
  background: var(--vg-wash) !important;
  border-left: 2px solid color-mix(in srgb, var(--vg-accent) 55%, transparent);
  border-radius: 2px 8px 8px 2px !important;
  padding: 7px 12px 8px !important;
  font-size: 0.8125rem !important;
  line-height: 1.55;
  color: var(--vg-quiet) !important;
  transition: background-color 140ms ease, border-color 140ms ease;
}
[data-user-message-bubble] a[data-thread-find-ignore]:hover {
  background: color-mix(in srgb, var(--vg-accent) 9%, transparent) !important;
  border-left-color: var(--vg-accent);
}
[data-user-message-bubble] a[data-thread-find-ignore] mark {
  background: color-mix(in srgb, var(--vg-accent) 14%, transparent) !important;
  color: var(--vg-ink) !important;
  border-radius: 3px;
  padding: 1px 3px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}

/* Composer: a quiet floating card; the edge turns to patina on focus. */
[data-slot="composer-host"] {
  border-radius: 16px !important;
  box-shadow: var(--vg-lift);
  transition: box-shadow 180ms ease, border-color 180ms ease;
}
[data-slot="composer-host"]:focus-within {
  border-color: color-mix(in srgb, var(--vg-accent) 50%, var(--vg-line)) !important;
  box-shadow: var(--vg-lift), 0 0 0 3px color-mix(in srgb, var(--vg-accent) 12%, transparent);
}

/* Sidebar: the open thread gets a short patina tick, not a full bar. */
[data-thread-item] [aria-current]:not([aria-current="false"]) {
  background-image: linear-gradient(var(--vg-accent), var(--vg-accent));
  background-repeat: no-repeat;
  background-size: 2px 52%;
  background-position: left center;
  font-weight: 500;
}
[data-slot="project-monogram"] svg { border-radius: 6px; }

/* Cards and floating surfaces: hairline plus one soft shadow. */
[data-thread-details-card] {
  border-radius: 12px !important;
  border-color: var(--vg-line) !important;
}
[data-slot="menu-popup"], [data-slot="popover-popup"], [data-slot="dialog-popup"] {
  border: 1px solid var(--vg-line) !important;
  box-shadow: var(--vg-shadow) !important;
}
[data-slot="menu-popup"], [data-slot="popover-popup"] { border-radius: 10px !important; }
[data-slot="dialog-popup"] { border-radius: 14px !important; }
[data-slot="tooltip-popup"] { border-radius: 6px !important; letter-spacing: 0.005em; }
[data-thread-terminal-drawer] { border-top: 1px solid var(--vg-line) !important; }

/* Controls */
[data-slot="button"] { border-radius: 8px; transition: background-color 120ms ease, border-color 120ms ease, color 120ms ease; }
[data-slot="input"], [data-slot="select-trigger"] { border-radius: 8px; }
[data-slot="input"]:focus-visible, [data-slot="select-trigger"]:focus-visible {
  border-color: color-mix(in srgb, var(--vg-accent) 55%, var(--vg-line)) !important;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--vg-accent) 14%, transparent) !important;
  outline: none;
}
:focus-visible { outline-color: color-mix(in srgb, var(--vg-accent) 70%, transparent); }
svg.lucide { stroke-width: 1.6; }

/* Scrollbars: thin and neutral, patina only while hovered. */
[data-slot="scroll-area-thumb"] { border-radius: 999px; }
[data-slot="scroll-area-scrollbar"]:hover [data-slot="scroll-area-thumb"] {
  background: color-mix(in srgb, var(--vg-accent) 45%, transparent) !important;
}
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background-color: color-mix(in srgb, var(--vg-quiet) 30%, transparent);
  border: 3px solid transparent; background-clip: padding-box; border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background-color: color-mix(in srgb, var(--vg-accent) 50%, transparent); }

@media (prefers-reduced-motion: reduce) {
  [data-slot="composer-host"], [data-slot="button"], .chat-markdown a { transition: none; }
}
""".strip() + "\n"

# Mirrors packages/shared/src/themeCss.ts at db2cc20.
FETCHES = re.compile(r"image-set\(|\bsrc\(", re.I)
URL_NOT_LOCAL = re.compile(r"url\((?![ \t\n\f\r]*[\"']?(?:data:|#))", re.I)
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")

# (foreground role, background role, minimum ratio, label)
BODY, UI = 4.5, 3.0
PAIRS = [
    ("text", "canvas", BODY, "body text"),
    ("text", "surface", BODY, "text on surface"),
    ("text", "surfaceRaised", BODY, "text on raised"),
    ("text", "surfaceOverlay", BODY, "text on overlay"),
    ("textMuted", "canvas", BODY, "muted text"),
    ("textMuted", "surface", BODY, "muted on surface"),
    ("mutedForeground", "muted", BODY, "muted fg on muted"),
    ("secondaryLabel", "canvas", BODY, "secondary label"),
    ("secondaryForeground", "secondary", BODY, "secondary button"),
    ("toolbarForeground", "toolbar", BODY, "toolbar"),
    ("toolbarControlForeground", "toolbarControl", BODY, "toolbar control"),
    ("toolbarControlForeground", "toolbarControlHover", BODY, "toolbar control hover"),
    ("messageForeground", "messageSurface", BODY, "user message"),
    ("messageActionForeground", "messageAction", BODY, "message action"),
    ("messageActionForeground", "messageActionHover", BODY, "message action hover"),
    ("codeForeground", "codeBackground", BODY, "code block"),
    ("terminalForeground", "terminalBackground", BODY, "terminal"),
    ("terminalForeground", "terminalSelection", BODY, "terminal selection"),
    ("sidebarForeground", "sidebar", BODY, "sidebar"),
    ("sidebarForeground", "sidebarRowHover", BODY, "sidebar row hover"),
    ("sidebarForeground", "sidebarRowSelected", BODY, "sidebar open thread"),
    ("sidebarMutedForeground", "sidebar", BODY, "sidebar muted"),
    ("sidebarMutedForeground", "sidebarRowSelected", BODY, "sidebar muted, open thread"),
    ("accent", "canvas", BODY, "accent as link text"),
    ("accentForeground", "accent", BODY, "accent button"),
    ("accentSurfaceForeground", "accentSurface", BODY, "accent surface"),
    ("error", "canvas", BODY, "error text"),
    ("error", "errorSurface", BODY, "error on its surface"),
    ("errorForeground", "error", BODY, "error button"),
    ("warning", "canvas", BODY, "warning text"),
    ("warning", "warningSurface", BODY, "warning on its surface"),
    ("warningForeground", "warning", BODY, "warning button"),
    ("update", "canvas", BODY, "update text"),
    ("update", "updateSurface", BODY, "update on its surface"),
    ("updateForeground", "update", BODY, "update button"),
    ("searchMatchForeground", "searchMatchBackground", BODY, "search match"),
    ("searchMatchActiveForeground", "searchMatchActiveBackground", BODY, "search match, active"),
    ("placeholder", "canvas", UI, "placeholder (ui)"),
    ("placeholder", "surfaceRaised", UI, "placeholder in composer (ui)"),
    ("iconMuted", "canvas", UI, "muted icon (ui)"),
    ("focus", "canvas", UI, "focus ring (ui)"),
    ("terminalCursor", "terminalBackground", UI, "terminal cursor (ui)"),
]


def check_palette(name: str, palette: dict) -> None:
    missing, extra = set(ROLES) - set(palette), set(palette) - set(ROLES)
    assert not missing and not extra, f"{name}: missing {sorted(missing)}, extra {sorted(extra)}"
    bad = {k: v for k, v in palette.items() if not HEX.match(v)}
    assert not bad, f"{name}: not #rrggbb: {bad}"


def check_css(css: str) -> None:
    code = re.sub(r"/\*[\s\S]*?\*/", "", css)
    assert "\\" not in css, "backslash in css"
    assert "@import" not in code.lower(), "@import in css"
    assert "@font-face" not in code.lower(), "@font-face in css"
    assert not FETCHES.search(code), "image-set( or src( in css"
    assert not URL_NOT_LOCAL.search(code), "non-local url() in css"
    assert code.count("{") == code.count("}"), "unbalanced braces in css"
    assert len(css) <= 20_000, f"css is {len(css)} chars"


def contrast_failures(light: dict, dark: dict) -> list:
    failures = []
    for fg, bg, minimum, label in PAIRS:
        for mode, colors in (("light", light), ("dark", dark)):
            ratio = contrast(colors[fg], colors[bg])
            if ratio < minimum:
                failures.append(f"{mode}: {label} ({fg} on {bg}) is {ratio:.2f}, needs {minimum}")
    return failures


def resolve(name: str, flavour, tints: dict) -> dict:
    assert not set(SHARED) & set(tints), f"{name}: defined twice: {sorted(set(SHARED) & set(tints))}"
    colors = {
        role: ref if ref.startswith("#") else flavour[ref]
        for role, ref in {**SHARED, **tints}.items()
    }
    check_palette(name, colors)
    return {role: colors[role] for role in ROLES}


def fill_css(css: str, palette) -> str:
    def color(match: re.Match) -> str:
        value = getattr(palette, match[1])[match[2]]
        return ", ".join(map(str, rgb(value))) if match[3] else value

    return re.sub(r"@(light|dark)\.(\w+?)(\.rgb)?@", color, css)


def render(palette) -> dict:
    light, dark = resolve("light", palette.light, LIGHT), resolve("dark", palette.dark, DARK)
    css = fill_css(CSS, palette)
    assert len(ROLES) == 61 and len(set(ROLES)) == 61, len(ROLES)
    assert len(palette.name) <= 48
    check_css(css)
    failures = contrast_failures(light, dark)
    if failures:
        raise SystemExit("t3code contrast failures:\n  " + "\n  ".join(failures))
    theme = {
        "version": 1, "name": palette.name, "appearance": "light",
        "colors": light, "variants": {"dark": dark}, "css": css,
    }
    out = json.dumps(theme, indent=2) + "\n"
    size = len(out.encode())
    assert size <= 32 * 1024, f"file is {size} bytes"
    return {"verdigris.json": out}
