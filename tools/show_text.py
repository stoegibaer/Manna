#!/usr/bin/env python3
"""Print Bible text with verse numbers from the app assets.

Usage:
  python3 -I tools/show_text.py <book_nr> <chapter>[:<from>-<to>] [...]
  python3 -I tools/show_text.py 35 1 2 3          # Habakuk 1-3
  python3 -I tools/show_text.py 41 4:35-41        # Markus 4,35-41
  python3 -I tools/show_text.py --list            # book numbers and names
Option: --translation elb1905 (default)
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app/src/main/assets/bible"


def load(tid, nr):
    return json.loads((ASSETS / tid / f"{nr:02d}.json").read_text(encoding="utf-8"))["chapters"]


def main(argv):
    tid = "elbbk"
    if "--translation" in argv:
        i = argv.index("--translation"); tid = argv[i + 1]; del argv[i:i + 2]
    if argv and argv[0] == "--list":
        for b in json.loads((ASSETS / tid / "books.json").read_text(encoding="utf-8"))["books"]:
            print(f'{b["nr"]:2d} {b["name"]} ({b["abbr"]}, {b["chapters"]} Kap.)')
        return
    nr = int(argv[0]); chapters = load(tid, nr)
    for spec in argv[1:]:
        if ":" in spec:
            c, rng = spec.split(":"); a, b = (rng.split("-") + [None])[:2]
            c, a = int(c), int(a); b = int(b) if b else a
        else:
            c = int(spec); a, b = 1, len(chapters[c - 1])
        for v in range(a, b + 1):
            print(f"{c}:{v} {chapters[c - 1][v - 1]}")


if __name__ == "__main__":
    main(sys.argv[1:])
