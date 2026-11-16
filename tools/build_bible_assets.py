#!/usr/bin/env python3
"""Convert a Bible translation JSON into compact per-book app assets.

Supported sources:
  - getbible.net v2 (e.g. https://api.getbible.net/v2/elberfelder1905.json)
  - bible.helloao.org complete.json (e.g. https://bible.helloao.org/api/deu_elbbk/complete.json)

Usage: python3 -I tools/build_bible_assets.py <source.json> <translation_id> [--name "..."] [--license "..."]
Output: app/src/main/assets/bible/<translation_id>/<NN>.json  ({"chapters": [[verse, ...], ...]})
        app/src/main/assets/bible/<translation_id>/books.json
"""
import json, re, sys, pathlib

BOOKS = [
    ("1. Mose", "1Mo"), ("2. Mose", "2Mo"), ("3. Mose", "3Mo"), ("4. Mose", "4Mo"), ("5. Mose", "5Mo"),
    ("Josua", "Jos"), ("Richter", "Ri"), ("Rut", "Rut"), ("1. Samuel", "1Sam"), ("2. Samuel", "2Sam"),
    ("1. Könige", "1Kön"), ("2. Könige", "2Kön"), ("1. Chronik", "1Chr"), ("2. Chronik", "2Chr"),
    ("Esra", "Esr"), ("Nehemia", "Neh"), ("Ester", "Est"), ("Hiob", "Hiob"), ("Psalmen", "Ps"),
    ("Sprüche", "Spr"), ("Prediger", "Pred"), ("Hoheslied", "Hld"), ("Jesaja", "Jes"), ("Jeremia", "Jer"),
    ("Klagelieder", "Klgl"), ("Hesekiel", "Hes"), ("Daniel", "Dan"), ("Hosea", "Hos"), ("Joel", "Joel"),
    ("Amos", "Am"), ("Obadja", "Obd"), ("Jona", "Jona"), ("Micha", "Mi"), ("Nahum", "Nah"),
    ("Habakuk", "Hab"), ("Zefanja", "Zef"), ("Haggai", "Hag"), ("Sacharja", "Sach"), ("Maleachi", "Mal"),
    ("Matthäus", "Mt"), ("Markus", "Mk"), ("Lukas", "Lk"), ("Johannes", "Joh"), ("Apostelgeschichte", "Apg"),
    ("Römer", "Röm"), ("1. Korinther", "1Kor"), ("2. Korinther", "2Kor"), ("Galater", "Gal"),
    ("Epheser", "Eph"), ("Philipper", "Phil"), ("Kolosser", "Kol"), ("1. Thessalonicher", "1Thess"),
    ("2. Thessalonicher", "2Thess"), ("1. Timotheus", "1Tim"), ("2. Timotheus", "2Tim"), ("Titus", "Tit"),
    ("Philemon", "Phlm"), ("Hebräer", "Hebr"), ("Jakobus", "Jak"), ("1. Petrus", "1Petr"),
    ("2. Petrus", "2Petr"), ("1. Johannes", "1Joh"), ("2. Johannes", "2Joh"), ("3. Johannes", "3Joh"),
    ("Judas", "Jud"), ("Offenbarung", "Offb"),
]

def clean(t: str) -> str:
    t = t.strip()
    t = re.sub(r"\s+([.,;:!?])", r"\1", t)      # "erlischt ." -> "erlischt."
    t = re.sub(r",(?=[^\s\d\"'])", ", ", t)      # "dreißig-,und" -> "dreißig-, und"
    t = re.sub(r"\s{2,}", " ", t)
    return t

def helloao_verse(parts):
    """Join helloao verse content. Footnote markers sit between words without spaces – put the space back."""
    out = ""
    for p in parts:
        if isinstance(p, dict):
            if "text" in p: p = p["text"]
            elif "lineBreak" in p: p = " "
            else: p = None  # footnote marker
        if p is None:
            out += "\x00"
            continue
        out += "\x01" + p  # \x01 marks a boundary between content parts (e.g. before words of Jesus)
    # a removed footnote between two non-space characters is a word boundary unless punctuation follows
    out = re.sub(r"(?<=\S)\x00+(?=\x01?[^\s.,;:!?)\]»“\x00\x01])", " ", out)
    out = out.replace("\x00", "")
    # part boundaries (e.g. before/after words of Jesus) between two words or after punctuation need a space:
    # "sprach:Dies", "lieb?Petrus", "undzieht", "Korban(das", ")sei"
    out = re.sub(r"(?<=[:;,.!?)A-Za-zÄÖÜäöüß])\x01(?=[A-Za-zÄÖÜäöüß(„])", " ", out)
    out = out.replace("\x01", "")
    out = re.sub(r"\s+\)", ")", out)  # "geworden )" -> "geworden)"
    out = re.sub(r"\)(?=[A-Za-zÄÖÜäöüß])", ") ", out)  # ")wie" -> ") wie"
    return re.sub(r"(\s*\*)+\s*$", "", out)  # stanza/book dividers in Psalms (Ps 119, end of Psalter books)


# Known defects in the source text: (translation, book, chapter, verse) -> corrected verse
FIXES = {
    ("elbbk", 54, 2, 10): "sondern was Frauen geziemt, die sich zur Gottesfurcht bekennen, durch gute Werke.",
}


def read_books(data):
    """Yield (nr, [[verse text, ...] per chapter]) for both source formats."""
    if "translation" in data and isinstance(data.get("books"), list) and data["books"] and "order" in data["books"][0]:
        for b in sorted(data["books"], key=lambda x: x["order"]):
            chapters = []
            for ch in b["chapters"]:
                verses = {x["number"]: helloao_verse(x["content"]) for x in ch["chapter"]["content"] if x.get("type") == "verse"}
                chapters.append([verses.get(n, "") for n in range(1, max(verses) + 1)])
            yield b["order"], chapters
    else:
        for b in sorted(data["books"], key=lambda x: x["nr"]):
            yield b["nr"], [[v["text"] for v in sorted(ch["verses"], key=lambda v: v["verse"])]
                            for ch in sorted(b["chapters"], key=lambda c: c["chapter"])]


def main(src, tid, name=None, license_=None):
    data = json.load(open(src, encoding="utf-8"))
    out = pathlib.Path(__file__).resolve().parent.parent / "app/src/main/assets/bible" / tid
    out.mkdir(parents=True, exist_ok=True)
    books = []
    for nr, raw in read_books(data):
        chapters = [[clean(v) for v in ch] for ch in raw]
        for (t, b, c, v), text in FIXES.items():
            if t == tid and b == nr: chapters[c - 1][v - 1] = text
        (out / f"{nr:02d}.json").write_text(json.dumps({"chapters": chapters}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        name, abbr = BOOKS[nr - 1]
        books.append({"nr": nr, "name": name, "abbr": abbr, "chapters": len(chapters)})
    tr = data.get("translation")
    default_name = tr.get("name", tid) if isinstance(tr, dict) else (tr or tid)
    (out / "books.json").write_text(json.dumps({"id": tid, "name": name or default_name,
        "license": license_ or data.get("distribution_license", ""), "books": books}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(books)} books to {out}")

if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    main(a[0], a[1], opt("--name"), opt("--license"))
