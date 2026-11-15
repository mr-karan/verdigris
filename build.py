#!/usr/bin/env python3
"""Render every Verdigris port from palette.json.

    python3 build.py              regenerate every port
    python3 build.py ghostty zed  regenerate the named ports
    python3 build.py --check      fail if a committed file is out of date
    python3 build.py --contrast   print every checked contrast pair

A port is a directory ports/<name>/ with a build.py that defines
render(palette) and returns {file name: text}. Files are written next to it.
Contrast is checked before anything is written.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

import palette as pal

ROOT = Path(__file__).resolve().parent
PORTS = ROOT / "ports"


def port_names() -> list:
    return sorted(p.parent.name for p in PORTS.glob("*/build.py"))


def render_port(name: str, palette: pal.Palette) -> dict:
    """Absolute path to rendered text for one port."""
    source = PORTS / name / "build.py"
    spec = importlib.util.spec_from_file_location(f"verdigris_port_{name.replace('-', '_')}", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {PORTS / name / file: text for file, text in module.render(palette).items()}


def print_contrast(palette: pal.Palette) -> None:
    for pair in pal.contrast_pairs(palette):
        flag = " " if pair.ok else "!"
        print(f"{pair.flavour:<10}{pair.ratio:6.2f}{flag} min {pair.minimum:<4} {pair.label}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ports", nargs="*", help="ports to render (default: all)")
    parser.add_argument("--check", action="store_true", help="write nothing; fail on stale files")
    parser.add_argument("--contrast", action="store_true", help="print every contrast pair")
    args = parser.parse_args()

    try:
        palette = pal.load()
    except pal.PaletteError as error:
        print(f"palette.json: {error}", file=sys.stderr)
        return 1
    if args.contrast:
        print_contrast(palette)
    failures = pal.contrast_failures(palette)
    if failures:
        print("contrast regressions, fix the colours in palette.json:", file=sys.stderr)
        print("\n".join(f"  {line}" for line in failures), file=sys.stderr)
        return 1

    known = port_names()
    unknown = sorted(set(args.ports) - set(known))
    if unknown:
        print(f"unknown ports {unknown}; known: {', '.join(known)}", file=sys.stderr)
        return 1

    targets = {}
    for name in args.ports or known:
        targets.update(render_port(name, palette))

    stale = [path for path, text in targets.items() if not path.exists() or path.read_text() != text]
    if args.check:
        if stale:
            print("out of date, run `python3 build.py`:", file=sys.stderr)
            print("\n".join(f"  {path.relative_to(ROOT)}" for path in stale), file=sys.stderr)
            return 1
        print(f"ok: {len(targets)} generated files are current, {len(pal.contrast_pairs(palette))} contrast pairs pass")
        return 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text := targets[path])
        print(f"wrote {path.relative_to(ROOT)} ({len(text.encode())} bytes)")
    print(f"{len(targets)} files, {len(stale)} changed, {len(pal.contrast_pairs(palette))} contrast pairs pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
