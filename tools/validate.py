#!/usr/bin/env python3
"""Load every generated port in the tool it is for.

    python3 tools/validate.py            run every check whose tool is on PATH
    python3 tools/validate.py --online   also fetch Zed's schema from zed.dev

A check passes only if the real tool accepts the file and reports the
palette's colours back. A missing tool is a skip, never a pass. On NixOS:

    nix shell nixpkgs#neovim nixpkgs#helix nixpkgs#kitty nixpkgs#wezterm \\
      nixpkgs#alacritty nixpkgs#delta nixpkgs#vsce -c python3 tools/validate.py

Set VSCODE_APP to VS Code's resources/app directory to check colour ids.
"""

import fcntl
import json
import os
import plistlib
import pty
import re
import select
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time
import tomllib
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import palette as pal  # noqa: E402

PORTS = ROOT / "ports"
SAMPLE = ROOT / "assets" / "samples" / "cache.go"
ZED_SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"


class Skip(Exception):
    pass


class Failure(Exception):
    pass


def need(*tools: str) -> None:
    missing = [tool for tool in tools if not shutil.which(tool)]
    if missing:
        raise Skip(f"{', '.join(missing)} not on PATH")


def run(command: list, env: dict | None = None, cwd: Path | None = None, stdin: str | None = None) -> str:
    result = subprocess.run(
        command, env={**os.environ, **(env or {})}, cwd=cwd, input=stdin,
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise Failure(f"{' '.join(map(str, command[:3]))} exited {result.returncode}: {(result.stderr or result.stdout).strip()[:300]}")
    return result.stdout + result.stderr


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def truecolor(text: str, layer: int) -> set:
    """Colours of 24-bit SGR sequences: layer 38 is foreground, 48 background."""
    return {"#%02x%02x%02x" % tuple(map(int, m)) for m in re.findall(rf"{layer};2;(\d+);(\d+);(\d+)", text)}


def check_parse(p: pal.Palette, scratch: Path) -> str:
    counts = {"json": 0, "toml": 0, "tmTheme": 0}
    for path in sorted(PORTS.rglob("*")):
        if path.suffix == ".json":
            json.loads(path.read_text())
            counts["json"] += 1
        elif path.suffix == ".toml":
            tomllib.loads(path.read_text())
            counts["toml"] += 1
        elif path.suffix == ".tmTheme":
            plistlib.loads(path.read_bytes())
            counts["tmTheme"] += 1
    return ", ".join(f"{n} {kind}" for kind, n in counts.items()) + " files parse"


def check_ghostty(p: pal.Palette, scratch: Path) -> str:
    need("ghostty")
    themes = scratch / "ghostty" / "themes"
    themes.mkdir(parents=True)
    for flavour in p.flavours.values():
        shutil.copy(PORTS / "ghostty" / flavour.slug, themes)
    env = {"XDG_CONFIG_HOME": str(scratch)}
    config = scratch / "ghostty" / "config"
    for flavour in p.flavours.values():
        config.write_text(f"theme = {flavour.slug}\n")
        run(["ghostty", "+validate-config"], env)
        shown = run(["ghostty", "+show-config"], env)
        for line in (f"background = {flavour['bg']}", f"cursor-color = {flavour['patina']}",
                     f"palette = 1={flavour.ansi['red']}", f"palette = 15={flavour.ansi['bright_white']}"):
            expect(line in shown, f"{flavour.slug}: `{line}` missing from +show-config")
    config.write_text(f"theme = light:{p.light.slug},dark:{p.dark.slug}\n")
    run(["ghostty", "+validate-config"], env)
    return "+validate-config accepts both themes and the light:dark pair"


def check_kitty(p: pal.Palette, scratch: Path) -> str:
    need("kitty")
    script = (
        "import sys; from kitty.config import load_config; o = load_config(sys.argv[-1]); "
        "h = lambda c: '#%02x%02x%02x' % (c.red, c.green, c.blue); "
        "print('RESULT', h(o.background), h(o.foreground), h(o.cursor), h(o.color1), h(o.color15))"
    )
    for flavour in p.flavours.values():
        path = PORTS / "kitty" / f"{flavour.slug}.conf"
        out = run(["kitty", "+runpy", f"import sys; sys.argv = ['kitty', {str(path)!r}]; exec({script!r})"],
                  {"KITTY_CONFIG_DIRECTORY": str(scratch / "kitty")})
        want = f"RESULT {flavour['bg']} {flavour['fg']} {flavour['patina']} {flavour.ansi['red']} {flavour.ansi['bright_white']}"
        expect(want in out, f"{flavour.slug}: kitty parsed {out.strip()[-120:]}, wanted {want}")
        expect("Ignoring unknown config key" not in out, f"{flavour.slug}: kitty ignored a key: {out.strip()[:200]}")
    return "kitty's load_config reads both themes"


def check_alacritty(p: pal.Palette, scratch: Path) -> str:
    need("alacritty")
    for flavour in p.flavours.values():
        run(["alacritty", "migrate", "--dry-run", "--config-file", str(PORTS / "alacritty" / f"{flavour.slug}.toml")])
    return "`alacritty migrate --dry-run` parses both files (keys are not checked by a running Alacritty)"


def check_wezterm(p: pal.Palette, scratch: Path) -> str:
    need("wezterm")
    config = scratch / "wezterm.lua"
    lines = ['local wezterm = require "wezterm"']
    for flavour in p.flavours.values():
        path = PORTS / "wezterm" / f"{flavour.slug}.toml"
        lines.append(
            f'do local c, m = wezterm.color.load_scheme("{path}") '
            'print("RESULT " .. m.name .. " " .. c.background .. " " .. c.cursor_bg .. " " .. c.ansi[2] .. " " .. c.brights[8]) end'
        )
    lines.append(f'return {{ color_scheme_dirs = {{ "{PORTS / "wezterm"}" }}, color_scheme = "{p.dark.title}" }}')
    config.write_text("\n".join(lines))
    out = run(["wezterm", "--config-file", str(config), "show-keys"])
    for flavour in p.flavours.values():
        want = f"RESULT {flavour.title} {flavour['bg']} {flavour['patina']} {flavour.ansi['red']} {flavour.ansi['bright_white']}"
        expect(want in out, f"{flavour.slug}: wezterm.color.load_scheme did not report `{want}`")
    expect("ERROR" not in out, f"wezterm reported an error: {out[:300]}")
    return "wezterm.color.load_scheme reads both schemes, and the scheme resolves by name"


def check_windows_terminal(p: pal.Palette, scratch: Path) -> str:
    schemes = json.loads((PORTS / "windows-terminal" / "verdigris.json").read_text())["schemes"]
    want = {"name", "background", "foreground", "cursorColor", "selectionBackground"}
    want |= {color for name in ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
             for color in (name, "bright" + name.capitalize())}
    for scheme in schemes:
        expect(set(scheme) == want, f"{scheme.get('name')}: keys differ from the scheme schema: {sorted(set(scheme) ^ want)}")
    return "structure only: both schemes carry exactly the documented keys (no Windows host to load them)"


def check_fzf(p: pal.Palette, scratch: Path) -> str:
    need("fzf", "bash")
    for flavour in p.flavours.values():
        out = run(["bash", "-c", f'unset FZF_DEFAULT_OPTS; . "{PORTS / "fzf" / (flavour.slug + ".sh")}"; printf "alpha\\nbeta\\n" | fzf --filter=alp'])
        expect(out.strip() == "alpha", f"{flavour.slug}: fzf returned {out!r}")
    return "fzf accepts the --color options of both flavours"


def bat_environment(scratch: Path) -> dict:
    themes = scratch / "bat" / "themes"
    themes.mkdir(parents=True, exist_ok=True)
    for theme in (PORTS / "bat").glob("*.tmTheme"):
        shutil.copy(theme, themes)
    env = {"BAT_CONFIG_DIR": str(scratch / "bat"), "BAT_CACHE_PATH": str(scratch / "cache" / "bat"), "COLORTERM": "truecolor"}
    run(["bat", "cache", "--build"], env)
    return env


def check_bat(p: pal.Palette, scratch: Path) -> str:
    need("bat")
    env = bat_environment(scratch)
    for flavour in p.flavours.values():
        out = run(["bat", f"--theme={flavour.slug}", "--color=always", "--style=plain", "--paging=never", str(SAMPLE)], env)
        used = truecolor(out, 38)
        stray = used - set(flavour.colors.values())
        expect(not stray, f"{flavour.slug}: bat emitted colours outside the palette: {sorted(stray)}")
        for role in ("keyword", "string", "comment", "function", "type", "number"):
            expect(flavour.syntax[role].color in used, f"{flavour.slug}: no token got the {role} colour")
    return "bat highlights Go with both themes, using only palette colours"


def check_delta(p: pal.Palette, scratch: Path) -> str:
    need("delta", "bat")
    bat_environment(scratch)
    home = scratch / "delta-home"
    home.mkdir()
    (home / ".gitconfig").write_text(f"[include]\n\tpath = {PORTS / 'bat' / 'verdigris.gitconfig'}\n")
    diff = "".join([
        "diff --git a/cache.go b/cache.go\n--- a/cache.go\n+++ b/cache.go\n@@ -1,2 +1,2 @@\n",
        ' package cache\n-const ttl = 5 * time.Minute\n+const ttl = 10 * time.Minute\n',
    ])
    env = {"HOME": str(home), "XDG_CACHE_HOME": str(scratch / "cache"), "XDG_CONFIG_HOME": str(home), "COLORTERM": "truecolor"}
    for flavour in p.flavours.values():
        out = run(["delta", "--features", flavour.slug, "--paging=never"], env, stdin=diff)
        backgrounds = truecolor(out, 48)
        for wash in ("cuprite_wash", "malachite_wash"):
            expect(flavour[wash] in backgrounds, f"{flavour.slug}: delta did not use {wash}")
        expect(flavour.syntax["keyword"].color in truecolor(out, 38), f"{flavour.slug}: delta did not use the syntax theme")
    return "delta applies both features and the syntax theme to a diff"


def check_nvim(p: pal.Palette, scratch: Path) -> str:
    need("nvim")
    script = scratch / "check.lua"
    script.write_text("""
local hex = function(n) return n and string.format("#%06x", n) or "nil" end
for _, bg in ipairs({ "light", "dark" }) do
  vim.o.background = bg
  vim.cmd.colorscheme("verdigris")
  local hl = function(name) return vim.api.nvim_get_hl(0, { name = name, link = false }) end
  local n = hl("Normal")
  print(string.format("RESULT %s %s %s %s %s %s %s", bg, hex(n.bg), hex(n.fg), hex(hl("@keyword").fg),
    hex(hl("Comment").fg), tostring(hl("Comment").italic), vim.g.terminal_color_1))
  local theme = dofile(vim.env.VERDIGRIS_PORT .. "/lua/lualine/themes/verdigris.lua")
  print("LUALINE " .. bg .. " " .. theme.normal.a.bg)
end
""")
    port = PORTS / "nvim"
    env = {name: str(scratch / "nvim" / name) for name in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME")}
    out = run(["nvim", "--headless", "-u", "NONE", "--cmd", f"set rtp^={port}", "-l", str(script)],
              {**env, "VERDIGRIS_PORT": str(port)})
    for flavour in p.flavours.values():
        want = (f"RESULT {flavour.appearance} {flavour['bg']} {flavour['fg']} {flavour.syntax['keyword'].color} "
                f"{flavour.syntax['comment'].color} true {flavour.ansi['red']}")
        expect(want in out, f"{flavour.appearance}: nvim reported {out.strip()[:300]}, wanted {want}")
        expect(f"LUALINE {flavour.appearance} {flavour['patina']}" in out, f"{flavour.appearance}: lualine theme did not load")
    return "`:colorscheme verdigris` loads for both backgrounds, and the lualine theme loads"


def helix_session(config_home: Path) -> tuple:
    """Open the sample in Helix inside a pty, quit, and return (screen text, log text)."""
    log = config_home / "hx.log"
    pid, fd = pty.fork()
    if pid == 0:
        os.environ.update(XDG_CONFIG_HOME=str(config_home), TERM="xterm-256color", COLORTERM="truecolor")
        os.execvp("hx", ["hx", "-vv", "--log", str(log), str(SAMPLE)])
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
    # Helix stops reading keys while it shuts down. A blocking write would then
    # wait on a full pty forever, so the quit keys are best effort.
    os.set_blocking(fd, False)
    screen, start, next_quit, running = b"", time.monotonic(), 1.5, True
    try:
        while running and time.monotonic() - start < 10:
            if select.select([fd], [], [], 0.2)[0]:
                try:
                    screen += os.read(fd, 65536)
                except BlockingIOError:
                    pass
                except OSError:
                    break
            if time.monotonic() - start > next_quit:
                next_quit += 0.5
                try:
                    os.write(fd, b"\x1b:q!\r")
                except BlockingIOError:
                    pass
                except OSError:
                    break
            running = os.waitpid(pid, os.WNOHANG)[0] == 0
    finally:
        if running:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        os.close(fd)
    return screen.decode(errors="replace"), log.read_text() if log.exists() else ""


def check_helix(p: pal.Palette, scratch: Path) -> str:
    need("hx")
    home = scratch / "helix-home"
    themes = home / "helix" / "themes"
    themes.mkdir(parents=True)
    for theme in (PORTS / "helix").glob("*.toml"):
        shutil.copy(theme, themes)
    # Only the theme is under test, so Helix starts no language server.
    (home / "helix" / "languages.toml").write_text('[[language]]\nname = "go"\nlanguage-servers = []\n')
    for flavour in p.flavours.values():
        name = flavour.slug.replace("-", "_")
        (home / "helix" / "config.toml").write_text(f'theme = "{name}"\n')
        screen, log = helix_session(home)
        problems = [line for line in log.splitlines() if "theme" in line.lower() and ("WARN" in line or "ERROR" in line)]
        if problems:
            raise Failure(f"{name}: Helix logged {problems[0][:200]}")
        expect(flavour["bg"] in truecolor(screen, 48), f"{name}: Helix did not paint the theme background")
        expect(flavour.syntax["keyword"].color in truecolor(screen, 38), f"{name}: Helix did not use the keyword colour")
    return "Helix loads both themes without a theme warning and paints their colours"


def vscode_app() -> Path:
    if os.environ.get("VSCODE_APP"):
        return Path(os.environ["VSCODE_APP"])
    need("code")
    for parent in Path(shutil.which("code")).resolve().parents:
        for candidate in (parent / "resources" / "app", parent / "lib" / "vscode" / "resources" / "app"):
            if candidate.is_dir():
                return candidate
    raise Skip("cannot find VS Code's resources/app from `code`; set VSCODE_APP")


def check_vscode_colors(p: pal.Palette, scratch: Path) -> str:
    app = vscode_app()
    bundle = (app / "out" / "vs" / "workbench" / "workbench.desktop.main.js").read_text(errors="replace")
    contributed = {
        color["id"]
        for manifest in app.glob("extensions/*/package.json")
        for color in json.loads(manifest.read_text()).get("contributes", {}).get("colors", [])
    }
    total = 0
    for theme in sorted((PORTS / "vscode" / "themes").glob("*.json")):
        keys = set(json.loads(theme.read_text())["colors"])
        unknown = sorted(key for key in keys if f'"{key}"' not in bundle and key not in contributed)
        expect(not unknown, f"{theme.name}: colour ids this VS Code does not define: {unknown}")
        total = len(keys)
    return f"all {total} workbench colour ids exist in this VS Code"


def check_vscode_install(p: pal.Palette, scratch: Path) -> str:
    need("vsce", "code")
    vsix = scratch / "verdigris.vsix"
    run(["vsce", "package", "--out", str(vsix)], cwd=PORTS / "vscode")
    names = set(zipfile.ZipFile(vsix).namelist())
    for flavour in p.flavours.values():
        expect(f"extension/themes/{flavour.slug}-color-theme.json" in names, f"{flavour.slug} missing from the VSIX")
    expect("extension/build.py" not in names, "build.py leaked into the VSIX")
    profile = ["--extensions-dir", str(scratch / "code-extensions"), "--user-data-dir", str(scratch / "code-data")]
    run(["code", *profile, "--install-extension", str(vsix)])
    listed = run(["code", *profile, "--list-extensions", "--show-versions"])
    expect(f"verdigris@{p.version}" in listed, f"extension not listed after install: {listed.strip()[-200:]}")
    return "vsce packages the extension and `code --install-extension` installs it in a scratch profile"


def check_zed(p: pal.Palette, scratch: Path, online: bool) -> str:
    if not online:
        raise Skip("pass --online to fetch Zed's theme schema")
    with urllib.request.urlopen(urllib.request.Request(ZED_SCHEMA, headers={"User-Agent": "theme-validator"}), timeout=30) as response:
        schema = json.load(response)
    family = json.loads((PORTS / "zed" / "verdigris.json").read_text())
    try:
        import jsonschema
    except ImportError:
        jsonschema = None
    if jsonschema:
        errors = list(jsonschema.Draft7Validator(schema).iter_errors(family))
        expect(not errors, f"schema errors: {[error.message[:120] for error in errors[:3]]}")
    allowed = set(schema["definitions"]["ThemeStyleContent"]["properties"])
    for theme in family["themes"]:
        unknown = sorted(set(theme["style"]) - allowed)
        expect(not unknown, f"{theme['name']}: style keys not in Zed's schema: {unknown}")
        expect(theme["appearance"] in ("light", "dark"), f"{theme['name']}: bad appearance")
    how = "validates against" if jsonschema else "uses only style keys from"
    return f"the theme family {how} Zed's v0.2.0 schema (not loaded in Zed itself)"


def check_pygments(p: pal.Palette, scratch: Path) -> str:
    try:
        import pygments
        from pygments.formatters import TerminalTrueColorFormatter
        from pygments.lexers import GoLexer
    except ImportError:
        raise Skip("pygments is not importable by this python") from None
    sys.path.insert(0, str(PORTS / "pygments"))
    import pygments_verdigris

    for flavour in p.flavours.values():
        style = getattr(pygments_verdigris, flavour.title.replace(" ", "") + "Style")
        out = pygments.highlight(SAMPLE.read_text(), GoLexer(), TerminalTrueColorFormatter(style=style))
        used = truecolor(out, 38)
        stray = used - set(flavour.colors.values())
        expect(not stray, f"{flavour.slug}: Pygments emitted colours outside the palette: {sorted(stray)}")
        expect(flavour.syntax["keyword"].color in used, f"{flavour.slug}: keyword colour unused")
    return f"Pygments {pygments.__version__} highlights Go with both styles, using only palette colours"


def check_t3code(p: pal.Palette, scratch: Path) -> str:
    theme = json.loads((PORTS / "t3code" / "verdigris.json").read_text())
    expect(theme["colors"]["accent"] == p.light["patina"], "light accent is not the palette's patina")
    expect(theme["variants"]["dark"]["accent"] == p.dark["patina"], "dark accent is not the palette's patina")
    expect(len(theme["colors"]) == 61 and len(theme["variants"]["dark"]) == 61, "not 61 roles per mode")
    return "structure only: T3's limits are asserted by ports/t3code/build.py (not loaded in T3 Code)"


def main() -> int:
    online = "--online" in sys.argv[1:]
    palette = pal.load()
    checks = [
        ("parse", check_parse), ("t3code", check_t3code), ("ghostty", check_ghostty), ("kitty", check_kitty),
        ("alacritty", check_alacritty), ("wezterm", check_wezterm), ("windows-terminal", check_windows_terminal),
        ("fzf", check_fzf), ("bat", check_bat), ("delta", check_delta), ("nvim", check_nvim),
        ("helix", check_helix), ("vscode colours", check_vscode_colors), ("vscode install", check_vscode_install),
        ("zed", lambda p, s: check_zed(p, s, online)), ("pygments", check_pygments),
    ]
    failed = 0
    for name, check in checks:
        with tempfile.TemporaryDirectory(prefix="verdigris-validate-") as directory:
            try:
                status, detail = "PASS", check(palette, Path(directory))
            except Skip as skip:
                status, detail = "SKIP", str(skip)
            except (Failure, subprocess.TimeoutExpired, OSError, ValueError, KeyError) as error:
                status, detail = "FAIL", f"{type(error).__name__}: {error}"
                failed += 1
        print(f"{status}  {name:<17} {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
