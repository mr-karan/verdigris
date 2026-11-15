"""Write session.ansi: a terminal session with the SGR codes the real tools emit."""
from pathlib import Path

E = "\x1b["
R = E + "m"


def prompt(command: str) -> str:
    return f"{E}1;36mverdigris{R} on {E}1;35mmain{R} {E}1;32m❯{R} {command}"


LINES = [
    prompt("git status -sb"),
    f"## {E}32mmain{R}...{E}31morigin/main{R} [ahead {E}32m2{R}]",
    f" {E}31mM{R} palette.json",
    f"{E}32mA{R}  ports/zed/verdigris.json",
    f"{E}31m??{R} ports/helix/",
    "",
    prompt("python3 build.py --check"),
    "ok: 94 generated files are current, 544 contrast pairs pass",
    "",
    prompt("git log --oneline --graph -4"),
    f"* {E}33m8c41f2a{R}{E}33m ({R}{E}1;36mHEAD{R}{E}33m -> {R}{E}1;32mmain{R}{E}33m){R} feat(zed): add the theme family",
    f"* {E}33m3e9b7d0{R} feat(nvim): cover treesitter and LSP groups",
    f"{E}31m|{R}{E}32m\\{R}",
    f"{E}31m|{R} * {E}33m51d0c6e{R}{E}33m ({R}{E}1;31morigin/main{R}{E}33m){R} fix(palette): raise comment contrast",
    "",
    prompt("ls"),
    f"{E}1;34massets{R}  {E}1;34mports{R}  {E}1;34mtools{R}  {E}1;32mbuild.py{R}  Makefile  palette.json  README.md",
    "",
    prompt("git diff palette.json"),
    f"{E}1mdiff --git a/palette.json b/palette.json{R}",
    f"{E}36m@@ -14,3 +14,3 @@{R}",
    '         "line_strong": "#cdd0c7",',
    f'{E}31m-        "fg_subtle": "#77817d",{R}',
    f'{E}32m+        "fg_subtle": "#6f7975",{R}',
    "",
    prompt(""),
]

Path(__file__).with_name("session.ansi").write_text("\n".join(LINES) + "\n")
