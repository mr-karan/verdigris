"""Generate the Verdigris T3 Code theme file and check it against T3's limits.

Verdigris: weathered stone and patinated copper. Neutrals carry a faint
grey-green cast, the accent is the blue-green of copper patina, and bare
copper is the one warm note (warnings, search matches).

Run: python3 -I verdigris.py out.json
"""

import json
import re
import sys

NAME = "Verdigris"

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

# Limestone: a soft grey-green paper, never white.
LIGHT = {
    "canvas": "#f3f3ee", "chrome": "#ebece6",
    "toolbar": "#f3f3ee", "toolbarForeground": "#2a322f", "toolbarBorder": "#dddfd7",
    "toolbarControl": "#fafaf7", "toolbarControlForeground": "#2a322f", "toolbarControlHover": "#e5e7e0",
    "surface": "#f7f7f3", "surfaceRaised": "#fbfbf8", "surfaceOverlay": "#fcfcfa",
    "text": "#1e2523", "textMuted": "#5c6763",
    "border": "#dddfd7", "input": "#cdd0c7", "focus": "#2c6e64",
    "accent": "#2c6e64", "accentForeground": "#f6fbf9",
    "secondary": "#e6e8e1", "secondaryForeground": "#2a322f",
    "muted": "#ecede7", "mutedForeground": "#5c6763",
    "placeholder": "#77817d", "secondaryLabel": "#4e5955", "iconMuted": "#77817d",
    "error": "#a8423f", "errorForeground": "#fffaf8", "errorSurface": "#f5e5e1",
    "warning": "#8f5226", "warningForeground": "#fffaf5", "warningSurface": "#f4e9db",
    "update": "#3d628a", "updateForeground": "#f8fbfe", "updateSurface": "#e3eaf1",
    "accentSurface": "#dcebe6", "accentSurfaceForeground": "#1f564d",
    "messageSurface": "#e8eae3", "messageForeground": "#1e2523",
    "messageAction": "#dfe1d9", "messageActionForeground": "#2a322f", "messageActionHover": "#d5d8cf",
    "codeBackground": "#eaebe5", "codeForeground": "#252d2a",
    "searchMatchBackground": "#f0d9bb", "searchMatchForeground": "#2a1c0e",
    "searchMatchActiveBackground": "#cf9160", "searchMatchActiveForeground": "#1d1206",
    "sidebar": "#ebece6", "sidebarForeground": "#2a322f", "sidebarMutedForeground": "#586360",
    "sidebarControlSurface": "#e3e5de", "sidebarRowHover": "#e3e5de",
    "sidebarRowActive": "#dcdfd7", "sidebarRowSelected": "#d9e6e1", "sidebarBorder": "#dddfd7",
    "terminalBackground": "#eff0ea", "terminalForeground": "#252d2a", "terminalCursor": "#2c6e64",
    "terminalSelection": "#cde0d9", "terminalScrollbar": "#cdd0c7", "terminalScrollbarHover": "#b7bbb1",
}

# Patina at night: deep green-grey slate, never black.
DARK = {
    "canvas": "#151a19", "chrome": "#111615",
    "toolbar": "#151a19", "toolbarForeground": "#c6cfcb", "toolbarBorder": "#252d2b",
    "toolbarControl": "#1b2120", "toolbarControlForeground": "#d0d7d3", "toolbarControlHover": "#232b29",
    "surface": "#191f1e", "surfaceRaised": "#1e2524", "surfaceOverlay": "#222a28",
    "text": "#dde3df", "textMuted": "#8e9a96",
    "border": "#29312f", "input": "#323b39", "focus": "#82c3b4",
    "accent": "#82c3b4", "accentForeground": "#0b1b17",
    "secondary": "#222a28", "secondaryForeground": "#d0d7d3",
    "muted": "#1b2120", "mutedForeground": "#8a9692",
    "placeholder": "#727e7a", "secondaryLabel": "#9ea9a5", "iconMuted": "#75827d",
    "error": "#e38d86", "errorForeground": "#230c0a", "errorSurface": "#2e1c1a",
    "warning": "#d9a377", "warningForeground": "#221306", "warningSurface": "#2c231a",
    "update": "#8fb2d8", "updateForeground": "#0a1522", "updateSurface": "#1a2530",
    "accentSurface": "#1a2d29", "accentSurfaceForeground": "#a5d8cb",
    "messageSurface": "#1f2625", "messageForeground": "#dde3df",
    "messageAction": "#262e2c", "messageActionForeground": "#c9d1cd", "messageActionHover": "#2e3735",
    "codeBackground": "#101514", "codeForeground": "#d0d7d3",
    "searchMatchBackground": "#523a24", "searchMatchForeground": "#f6e7d6",
    "searchMatchActiveBackground": "#d9a377", "searchMatchActiveForeground": "#221306",
    "sidebar": "#111615", "sidebarForeground": "#c0c9c5", "sidebarMutedForeground": "#87938f",
    "sidebarControlSurface": "#181e1d", "sidebarRowHover": "#181e1d",
    "sidebarRowActive": "#1d2423", "sidebarRowSelected": "#1a2925", "sidebarBorder": "#1c2221",
    "terminalBackground": "#101514", "terminalForeground": "#d0d7d3", "terminalCursor": "#82c3b4",
    "terminalSelection": "#26403a", "terminalScrollbar": "#2b3432", "terminalScrollbarHover": "#3a4543",
}

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
  --vg-accent: #2c6e64; --vg-copper: #8f5226; --vg-line: #dddfd7; --vg-line-soft: #e6e8e1;
  --vg-ink: #1e2523; --vg-quiet: #5c6763; --vg-chip: #e6e8e1;
  --vg-wash: rgba(44, 110, 100, 0.045);
  --vg-shadow: 0 1px 2px rgba(30, 40, 36, 0.05), 0 10px 28px -6px rgba(30, 40, 36, 0.10);
  --vg-lift: 0 1px 2px rgba(30, 40, 36, 0.04), 0 4px 14px -4px rgba(30, 40, 36, 0.07);
}
.dark {
  --vg-accent: #82c3b4; --vg-copper: #d9a377; --vg-line: #29312f; --vg-line-soft: #212827;
  --vg-ink: #dde3df; --vg-quiet: #8e9a96; --vg-chip: #232b29;
  --vg-wash: rgba(130, 195, 180, 0.035);
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


def luminance(color: str) -> float:
    channels = (int(color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


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


def contrast_table() -> list:
    failures = []
    print(f"{'pair':<30}{"fg on bg":<58}{'min':>5}{'light':>8}{'dark':>8}")
    for fg, bg, minimum, label in PAIRS:
        ratios = [contrast(p[fg], p[bg]) for p in (LIGHT, DARK)]
        flags = ["" if r >= minimum else "!" for r in ratios]
        print(f"{label:<30}{fg + " / " + bg:<58}{minimum:>5.1f}"
              f"{ratios[0]:>7.2f}{flags[0] or ' '}{ratios[1]:>7.2f}{flags[1] or ' '}")
        for mode, ratio in zip(("light", "dark"), ratios):
            if ratio < minimum:
                failures.append(f"{mode}: {label} ({fg} on {bg}) is {ratio:.2f}, needs {minimum}")
    return failures


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python3 -I verdigris.py out.json")
    check_palette("light", LIGHT)
    check_palette("dark", DARK)
    assert len(ROLES) == 61 and len(set(ROLES)) == 61, len(ROLES)
    assert len(NAME) <= 48
    check_css(CSS)
    failures = contrast_table()
    if failures:
        sys.exit("contrast failures:\n  " + "\n  ".join(failures))
    theme = {
        "version": 1, "name": NAME, "appearance": "light",
        "colors": LIGHT, "variants": {"dark": DARK}, "css": CSS,
    }
    out = json.dumps(theme, indent=2) + "\n"
    size = len(out.encode())
    assert size <= 32 * 1024, f"file is {size} bytes"
    with open(sys.argv[1], "w") as f:
        f.write(out)
    print(f"\n{NAME}: {len(ROLES)} roles per mode, css {len(CSS)} chars, file {size} bytes -> {sys.argv[1]}")


main()
