#!/usr/bin/env python3
"""Render the README images in assets/ from the generated ports.

    python3 tools/screenshots.py            every image
    python3 tools/screenshots.py hero       only the named images

Code is highlighted by bat with the generated .tmTheme, and the terminal
session is plain ANSI mapped through the palette's 16 colours, so the images
show what the ports produce. Needs bat and chromium on PATH, and the Inter and
Commit Mono fonts.
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import palette as pal  # noqa: E402

ASSETS = ROOT / "assets"
SAMPLES = ASSETS / "samples"
SGR = re.compile(r"\x1b\[([0-9;]*)m")
SCALE = 2

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  font-family: "Inter Variable", "Inter", system-ui, sans-serif;
  font-feature-settings: "calt", "cv05", "ss03";
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  overflow: hidden;
}
pre, code, .mono { font-family: "CommitMono", ui-monospace, monospace; font-variant-ligatures: none; }
.flavour { background: var(--bg_dim); color: var(--fg); }

.window {
  background: var(--bg);
  border: 1px solid var(--line);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(var(--shadow), 0.06), 0 24px 60px -18px rgba(var(--shadow), 0.28);
  display: flex; flex-direction: column;
}
.titlebar {
  height: 38px; flex: none; position: relative;
  display: flex; align-items: center; padding: 0 14px;
  background: var(--bg_dim); border-bottom: 1px solid var(--line);
}
.dots { display: flex; gap: 7px; }
.dots i { width: 10px; height: 10px; border-radius: 50%; background: var(--line_strong); }
.titlebar .title {
  position: absolute; left: 0; right: 0; text-align: center;
  font-size: 12px; color: var(--fg_subtle); letter-spacing: 0.01em;
}
.main { display: flex; flex: 1; min-height: 0; }
.sidebar {
  width: 186px; flex: none; padding: 12px 0;
  background: var(--bg_dim); border-right: 1px solid var(--line);
  font-size: 12.5px; color: var(--fg_muted);
}
.sidebar .heading {
  padding: 0 16px 8px; font-size: 10.5px; font-weight: 600;
  letter-spacing: 0.08em; color: var(--fg_subtle);
}
.tree div { height: 25px; display: flex; align-items: center; padding-right: 14px; position: relative; }
.tree .dir { color: var(--fg); }
.tree .dir::before {
  content: ""; width: 5px; height: 5px; margin-right: 8px;
  border-right: 1.5px solid var(--fg_subtle); border-bottom: 1.5px solid var(--fg_subtle);
  transform: rotate(-45deg);
}
.tree .dir.open::before { transform: rotate(45deg) translate(-1px, -1px); }
.tree .active { background: var(--fill); color: var(--fg_strong); font-weight: 500; }
.tree .active::after {
  content: ""; position: absolute; left: 0; top: 26%; height: 48%; width: 2px; background: var(--patina);
}
.tree em { margin-left: auto; font-style: normal; font-size: 11px; font-weight: 600; }
.tree .mod { color: var(--azurite); }
.tree .new { color: var(--malachite); }

.editor { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.tabs {
  height: 36px; flex: none; display: flex; align-items: stretch;
  background: var(--bg_dim); border-bottom: 1px solid var(--line); font-size: 12.5px;
}
.tab { display: flex; align-items: center; padding: 0 16px; color: var(--fg_subtle); border-right: 1px solid var(--line); }
.tab.active { background: var(--bg); color: var(--fg_strong); margin-bottom: -1px; box-shadow: inset 0 1.5px 0 var(--patina); }
.code { flex: 1; padding: 14px 0; font-size: 13px; line-height: 21px; color: var(--fg); overflow: hidden; }
.code .line { display: flex; white-space: pre; padding-right: 16px; }
.code .ln { width: 46px; flex: none; text-align: right; padding-right: 16px; color: var(--fg_subtle); opacity: 0.72; user-select: none; }
.code .line.current { background: var(--fill_soft); }
.code .line.current .ln { color: var(--fg); opacity: 1; }
.cursor { display: inline-block; width: 2px; height: 17px; margin: 2px 0 -3px -1px; background: var(--patina); vertical-align: top; }

.panel { flex: none; border-top: 1px solid var(--line); }
.panel .heads { height: 32px; display: flex; align-items: center; gap: 18px; padding: 0 16px; font-size: 11px; letter-spacing: 0.06em; color: var(--fg_subtle); }
.panel .heads b { font-weight: 600; color: var(--fg_strong); }
.term { padding: 0 16px 14px; font-size: 12.5px; line-height: 20px; color: var(--fg); white-space: pre; }
.block { display: inline-block; width: 7.5px; height: 16px; background: var(--patina); vertical-align: -3px; }
.status {
  height: 26px; flex: none; display: flex; align-items: center; gap: 16px; padding: 0 12px;
  background: var(--bg_dim); border-top: 1px solid var(--line);
  font-size: 11.5px; color: var(--fg_muted);
}
.status .branch { color: var(--patina); font-weight: 500; }
.status .right { margin-left: auto; display: flex; gap: 16px; }

.mark { position: relative; width: 44px; height: 44px; border-radius: 50%; background: var(--copper); overflow: hidden; flex: none; }
.mark::after { content: ""; position: absolute; width: 44px; height: 44px; border-radius: 50%; left: -15px; top: 13px; background: var(--patina); }
"""


def css_vars(flavour: pal.Flavour) -> str:
    shadow = "0, 0, 0" if flavour.dark else "30, 40, 36"
    return ";".join(f"--{name}:{value}" for name, value in flavour.colors.items()) + f";--shadow:{shadow}"


def span(text: str, color: str | None, bold: bool, italic: bool, underline: bool) -> str:
    if not text:
        return ""
    styles = [f"color:{color}"] if color else []
    styles += ["font-weight:700"] if bold else []
    styles += ["font-style:italic"] if italic else []
    styles += ["text-decoration:underline"] if underline else []
    text = html.escape(text)
    return f'<span style="{";".join(styles)}">{text}</span>' if styles else text


def ansi_to_html(text: str, ansi: list) -> list:
    """One HTML string per line. 24-bit and 16-colour SGR foregrounds only."""
    lines = []
    for raw in text.rstrip("\n").split("\n"):
        out, position = [], 0
        color, bold, italic, underline = None, False, False, False
        for match in SGR.finditer(raw):
            out.append(span(raw[position : match.start()], color, bold, italic, underline))
            position = match.end()
            codes = [int(c) for c in match[1].split(";") if c] or [0]
            while codes:
                code = codes.pop(0)
                if code == 0:
                    color, bold, italic, underline = None, False, False, False
                elif code == 1:
                    bold = True
                elif code == 3:
                    italic = True
                elif code == 4:
                    underline = True
                elif code == 38 and codes[:1] == [2]:
                    color = "#%02x%02x%02x" % tuple(codes[1:4])
                    codes = codes[4:]
                elif 30 <= code <= 37:
                    color = ansi[code - 30]
                elif 90 <= code <= 97:
                    color = ansi[code - 90 + 8]
                else:
                    raise ValueError(f"unhandled SGR code {code} in {raw!r}")
        out.append(span(raw[position:], color, bold, italic, underline))
        lines.append("".join(out))
    return lines


class Bat:
    """bat with the generated themes loaded from a scratch config directory."""

    def __init__(self, scratch: Path):
        themes = scratch / "bat" / "themes"
        themes.mkdir(parents=True)
        for theme in (ROOT / "ports" / "bat").glob("*.tmTheme"):
            shutil.copy(theme, themes)
        self.env = {
            **os.environ, "COLORTERM": "truecolor",
            "BAT_CONFIG_DIR": str(scratch / "bat"), "BAT_CACHE_PATH": str(scratch / "bat-cache"),
        }
        subprocess.run(["bat", "cache", "--build"], env=self.env, check=True, capture_output=True)

    def highlight(self, flavour: pal.Flavour, sample: str) -> list:
        result = subprocess.run(
            ["bat", f"--theme={flavour.slug}", "--color=always", "--style=plain",
             "--paging=never", "--tabs=4", str(SAMPLES / sample)],
            env=self.env, check=True, capture_output=True, text=True,
        )
        return ansi_to_html(result.stdout, flavour.ansi_list)


def code_block(lines: list, current: int | None = None, first: int = 1) -> str:
    rows = []
    for number, line in enumerate(lines[first - 1 :], first):
        is_current = number == current
        cursor = '<span class="cursor"></span>' if is_current else ""
        rows.append(
            f'<div class="line{" current" if is_current else ""}">'
            f'<span class="ln">{number}</span><span>{line}{cursor}</span></div>'
        )
    return f'<pre class="code">{"".join(rows)}</pre>'


def tree(rows: list) -> str:
    items = []
    for depth, kind, name, badge in rows:
        mark = {"M": '<em class="mod">M</em>', "U": '<em class="new">U</em>'}.get(badge, "")
        indent = 16 + depth * 14 + (0 if kind.startswith("dir") else 13)
        items.append(f'<div class="{kind}" style="padding-left:{indent}px">{name}{mark}</div>')
    return f'<div class="tree">{"".join(items)}</div>'


def window(title: str, project: str, files: list, tabs: list, code: str, panel: str, status: tuple) -> str:
    tab_html = "".join(
        f'<span class="tab{" active" if index == 0 else ""}">{name}</span>' for index, name in enumerate(tabs)
    )
    language, position = status
    return f"""
<div class="window">
  <div class="titlebar"><span class="dots"><i></i><i></i><i></i></span><span class="title">{title}</span></div>
  <div class="main">
    <aside class="sidebar"><div class="heading">{project}</div>{tree(files)}</aside>
    <section class="editor">
      <div class="tabs">{tab_html}</div>
      {code}
      {panel}
    </section>
  </div>
  <div class="status"><span class="branch">main</span><span>0 errors</span><span>1 warning</span>
    <span class="right"><span>{position}</span><span>UTF-8</span><span>{language}</span></span></div>
</div>"""


def terminal_panel(lines: list) -> str:
    body = "\n".join(lines) + '<span class="block"></span>'
    return (
        '<div class="panel"><div class="heads"><b>TERMINAL</b><span>PROBLEMS</span><span>OUTPUT</span></div>'
        f'<pre class="term">{body}</pre></div>'
    )


def page(body: str, extra_css: str = "") -> str:
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{extra_css}</style></head><body>{body}</body></html>'


GO_FILES = [
    (0, "dir open", "cache", ""), (1, "file active", "cache.go", "M"), (1, "file", "cache_test.go", "U"),
    (1, "file", "lru.go", ""), (0, "dir", "cmd", ""), (0, "dir", "internal", ""),
    (0, "file", "go.mod", ""), (0, "file", "go.sum", ""), (0, "file", "Makefile", ""), (0, "file", "README.md", ""),
]
TS_FILES = [
    (0, "dir open", "src", ""), (1, "file active", "contrast.ts", "M"), (1, "file", "palette.ts", ""),
    (1, "file", "ports.ts", "U"), (0, "dir", "test", ""), (0, "file", "bun.lock", ""),
    (0, "file", "package.json", ""), (0, "file", "tsconfig.json", ""), (0, "file", "README.md", ""),
]


def session_lines(flavour: pal.Flavour, first: int, last: int) -> list:
    text = (SAMPLES / "session.ansi").read_text()
    return ansi_to_html(text, flavour.ansi_list)[first:last]


def editor_window(bat: Bat, flavour: pal.Flavour, sample: str) -> str:
    if sample == "cache.go":
        return window(
            "cache.go", "CACHE", GO_FILES, ["cache.go", "cache_test.go", "lru.go"],
            code_block(bat.highlight(flavour, sample), current=28, first=16),
            "", ("Go", "Ln 28, Col 26"),
        )
    return window(
        "contrast.ts", "VERDIGRIS", TS_FILES, ["contrast.ts", "palette.ts"],
        code_block(bat.highlight(flavour, sample), current=15),
        # The first two commands of the session, then its closing prompt.
        terminal_panel(session_lines(flavour, 0, 9) + session_lines(flavour, 25, 26)),
        ("TypeScript", "Ln 15, Col 56"),
    )


def hero(palette: pal.Palette, bat: Bat) -> tuple:
    width, height = 1200, 640
    css = f"""
.layer {{ position: absolute; inset: 0; width: {width}px; height: {height}px; }}
.layer.dark {{ clip-path: polygon(58% 0, 100% 0, 100% 100%, 44% 100%); }}
.brand {{ position: absolute; top: 54px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; }}
.brand .name {{ display: flex; align-items: center; gap: 16px; font-size: 54px; font-weight: 600; letter-spacing: -0.035em; color: var(--fg_strong); }}
.brand p {{ margin-top: 12px; font-size: 17px; color: var(--fg_muted); letter-spacing: -0.005em; }}
.layer .window {{ position: absolute; left: 110px; top: 214px; width: 980px; height: 560px; }}
"""
    layers = "".join(
        f"""<div class="layer flavour {flavour.appearance}" style="{css_vars(flavour)}">
  <div class="brand"><div class="name"><span class="mark"></span>Verdigris</div>
  <p>Weathered stone and patinated copper. A calm theme for code.</p></div>
  {editor_window(bat, flavour, "cache.go")}
</div>"""
        for flavour in (palette.light, palette.dark)
    )
    return page(layers, css), width, height


def editor(palette: pal.Palette, bat: Bat, appearance: str) -> tuple:
    flavour = palette.light if appearance == "light" else palette.dark
    code_lines = len((SAMPLES / "contrast.ts").read_text().splitlines())
    chrome = 38 + 36 + 26 + 3  # title bar, tabs, status bar, borders
    code, panel = code_lines * 21 + 28, 32 + 10 * 20 + 14
    width, height = 1200, 2 * 44 + chrome + code + panel
    css = f"""
.stage {{ width: {width}px; height: {height}px; padding: 44px 56px; }}
.stage .window {{ height: 100%; }}
"""
    body = f'<div class="stage flavour" style="{css_vars(flavour)}">{editor_window(bat, flavour, "contrast.ts")}</div>'
    return page(body, css), width, height


def terminal(palette: pal.Palette, bat: Bat) -> tuple:
    width, height = 1200, 700
    css = f"""
.half {{ position: absolute; top: 0; width: {width // 2}px; height: {height}px; padding: 40px 32px; }}
.half.dark {{ left: {width // 2}px; }}
.half .window {{ height: 100%; }}
.half .term {{ padding: 14px 18px; font-size: 12px; line-height: 19.5px; flex: 1; }}
.strip {{ display: flex; gap: 6px; padding: 0 18px 16px; }}
.strip i {{ flex: 1; height: 14px; border-radius: 4px; }}
.strip.normal {{ padding-bottom: 6px; }}
"""
    halves = []
    for flavour in (palette.light, palette.dark):
        lines = session_lines(flavour, 0, 26)
        strips = "".join(
            f'<div class="strip {name}">'
            + "".join(f'<i style="background:{c};box-shadow:inset 0 0 0 1px var(--line)"></i>' for c in colors)
            + "</div>"
            for name, colors in (("normal", flavour.ansi_list[:8]), ("bright", flavour.ansi_list[8:]))
        )
        body = "\n".join(lines) + '<span class="block"></span>'
        halves.append(
            f"""<div class="half flavour {flavour.appearance}" style="{css_vars(flavour)}"><div class="window">
  <div class="titlebar"><span class="dots"><i></i><i></i><i></i></span><span class="title">{flavour.title}</span></div>
  <pre class="term">{body}</pre>{strips}
</div></div>"""
        )
    return page("".join(halves), css), width, height


def swatches(palette: pal.Palette, bat: Bat) -> tuple:
    width, height = 1200, 770
    css = f"""
.half {{ position: absolute; top: 0; width: {width // 2}px; height: {height}px; padding: 48px 52px; background: var(--bg); }}
.half.dark {{ left: {width // 2}px; }}
h2 {{ font-size: 30px; font-weight: 600; letter-spacing: -0.025em; color: var(--fg_strong); }}
h2 small {{ margin-left: 10px; font-size: 13px; font-weight: 500; letter-spacing: 0.02em; color: var(--fg_subtle); }}
h3 {{ margin: 30px 0 14px; font-size: 10.5px; font-weight: 600; letter-spacing: 0.1em; color: var(--fg_subtle); }}
.grid {{ display: grid; gap: 16px 10px; }}
.hues {{ grid-template-columns: repeat(7, 1fr); }}
.stone {{ grid-template-columns: repeat(6, 1fr); }}
.tints {{ grid-template-columns: repeat(4, 1fr); }}
.cell {{ display: flex; flex-direction: column; align-items: flex-start; }}
.chip {{ width: 100%; height: 46px; border-radius: 10px; box-shadow: inset 0 0 0 1px rgba(var(--shadow), 0.10); position: relative; }}
.hues .chip {{ height: 58px; }}
.chip u {{ position: absolute; right: -4px; bottom: -4px; width: 22px; height: 22px; border-radius: 50%; border: 3px solid var(--bg); }}
.cell b {{ margin-top: 9px; font-size: 11.5px; font-weight: 500; color: var(--fg); letter-spacing: -0.005em; }}
.cell code {{ margin-top: 2px; font-size: 10px; color: var(--fg_subtle); }}
"""

    def cell(flavour: pal.Flavour, name: str, bright: bool = False) -> str:
        dot = f'<u style="background:{flavour[name + "_bright"]}"></u>' if bright else ""
        return (
            f'<div class="cell"><span class="chip" style="background:{flavour[name]}">{dot}</span>'
            f"<b>{name}</b><code>{flavour[name]}</code></div>"
        )

    stone = ["bg_dim", "bg", "bg_raised", "fill_soft", "fill", "line",
             "line_strong", "fg_faint", "fg_subtle", "fg_muted", "fg", "fg_strong"]
    tints = pal.WASHES + ["selection", "search"]
    halves = []
    for flavour in (palette.light, palette.dark):
        halves.append(
            f"""<div class="half flavour {flavour.appearance}" style="{css_vars(flavour)}">
  <h2>{flavour.name}<small>{flavour.appearance}</small></h2>
  <h3>COPPER</h3>
  <div class="grid hues">{"".join(cell(flavour, hue, hue != "copper") for hue in pal.HUES)}</div>
  <h3>STONE</h3>
  <div class="grid stone">{"".join(cell(flavour, name) for name in stone)}</div>
  <h3>WASHES</h3>
  <div class="grid tints">{"".join(cell(flavour, name) for name in tints)}</div>
</div>"""
        )
    return page("".join(halves), css), width, height


IMAGES = {
    "hero": hero,
    "limestone": lambda palette, bat: editor(palette, bat, "light"),
    "slate": lambda palette, bat: editor(palette, bat, "dark"),
    "terminal": terminal,
    "palette": swatches,
}


def shoot(document: str, name: str, width: int, height: int, scratch: Path) -> None:
    source = scratch / f"{name}.html"
    source.write_text(document)
    target = ASSETS / f"{name}.png"
    subprocess.run(
        ["chromium", "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
         f"--user-data-dir={scratch / 'chromium'}", f"--force-device-scale-factor={SCALE}",
         f"--window-size={width},{height}", f"--screenshot={target}", source.as_uri()],
        check=True, capture_output=True, timeout=120,
    )
    print(f"wrote {target.relative_to(ROOT)} ({width * SCALE}x{height * SCALE})")


def main() -> int:
    names = sys.argv[1:] or list(IMAGES)
    unknown = sorted(set(names) - set(IMAGES))
    if unknown:
        print(f"unknown images {unknown}; known: {', '.join(IMAGES)}", file=sys.stderr)
        return 1
    for tool in ("bat", "chromium"):
        if not shutil.which(tool):
            print(f"{tool} is not on PATH; install it to render the images", file=sys.stderr)
            return 1
    palette = pal.load()
    with tempfile.TemporaryDirectory(prefix="verdigris-") as directory:
        scratch = Path(directory)
        bat = Bat(scratch)
        for name in names:
            document, width, height = IMAGES[name](palette, bat)
            shoot(document, name, width, height, scratch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
