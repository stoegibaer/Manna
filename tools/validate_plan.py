#!/usr/bin/env python3
"""Validate a reading plan JSON against the format and the Bible text.

Usage:
  python3 -I tools/validate_plan.py app/src/main/assets/plans/habakuk.json
  python3 -I tools/validate_plan.py <plan.json> --review   # also print text + questions per section
Exit code 1 if errors were found. Warnings do not fail.
Format: .claude/skills/leseplan-schreiben/format.md
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app/src/main/assets"
CARD_TYPES = {"person", "ort", "begriff", "ereignis"}
QUIZ_TYPES = {"choice", "truefalse", "whosaid", "order", "error", "estimate"}
KITSCH = ["❤", "♥", "🙏", "✨", "wunderschön", "herzlich", "kuschel", "liebevoll umarmt", "zuckersüß", "magisch"]

errors, warnings = [], []
_bible = {}


def err(where, msg): errors.append(f"✗ {where}: {msg}")
def warn(where, msg): warnings.append(f"⚠ {where}: {msg}")


BASIS = "elbbk"  # overwritten by plan["basis"]


def book(nr, tid=None):
    tid = tid or BASIS
    if nr not in _bible:
        p = ASSETS / "bible" / tid / f"{nr:02d}.json"
        _bible[nr] = json.loads(p.read_text(encoding="utf-8"))["chapters"] if p.exists() else None
    return _bible[nr]


def norm(s):
    return re.sub(r"[^\wäöüß]+", " ", s.lower()).strip()


def ref_text(r):
    ch = book(r["book"])
    return " ".join(ch[r["chapter"] - 1][v - 1] for v in range(r["from"], r["to"] + 1))


def check_ref(where, r):
    for k in ("book", "chapter", "from", "to"):
        if not isinstance(r.get(k), int):
            err(where, f"ref braucht int '{k}': {r}"); return False
    ch = book(r["book"])
    if ch is None:
        err(where, f"Buch {r['book']} nicht gefunden"); return False
    if not 1 <= r["chapter"] <= len(ch):
        err(where, f"Kapitel {r['chapter']} existiert nicht in Buch {r['book']}"); return False
    n = len(ch[r["chapter"] - 1])
    if not (1 <= r["from"] <= r["to"] <= n):
        err(where, f"Verse {r['from']}-{r['to']} ungültig (Kapitel hat {n})"); return False
    return True


def check_text_fields(where, obj, keys):
    for k in keys:
        v = obj.get(k)
        if isinstance(v, str):
            low = v.lower()
            for kw in KITSCH:
                if kw in low:
                    warn(where, f"möglicher Kitsch in '{k}': enthält '{kw}'")


def check_quiz(where, q, section_text):
    t = q.get("type")
    if t not in QUIZ_TYPES:
        err(where, f"unbekannter Quiz-Typ {t!r}"); return
    if not q.get("explain"):
        err(where, "explain fehlt (Erklärung nach der Antwort)")
    if not q.get("hint"):
        warn(where, "hint fehlt (Hinweis bei falscher Antwort)")
    if t in ("choice", "whosaid"):
        opts = q.get("options", [])
        if not 2 <= len(opts) <= 4: err(where, "options: 2-4 Einträge")
        if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(opts): err(where, "answer: gültiger Index nötig")
        if len(set(opts)) != len(opts): err(where, "options doppelt")
        if t == "choice" and not q.get("q"): err(where, "q fehlt")
        if t == "whosaid":
            quote, qr = q.get("quote", ""), q.get("quote_ref")
            if not quote: err(where, "quote fehlt")
            if not qr: err(where, "quote_ref fehlt (Vers des Zitats – damit die App es in jeder Übersetzung zeigen kann)")
            elif check_ref(where, qr) and norm(quote) not in norm(ref_text(qr)):
                err(where, f"Zitat steht nicht wörtlich in quote_ref ({BASIS}): {quote!r}")
    elif t == "truefalse":
        if not q.get("q"): err(where, "q (Aussage) fehlt")
        if not isinstance(q.get("answer"), bool): err(where, "answer muss true/false sein")
    elif t == "order":
        items = q.get("items", [])
        if not 3 <= len(items) <= 5: err(where, "items: 3-5 Einträge in richtiger Reihenfolge")
        if len(set(items)) != len(items): err(where, "items doppelt")
    elif t == "error":
        text = q.get("text", "")
        marks = re.findall(r"\[([^\]]+)\]", text)
        if len(marks) != 1: err(where, "text braucht genau ein [falsches Wort] in eckigen Klammern")
        elif " " in marks[0].strip(): err(where, "das markierte falsche Wort muss ein einzelnes Wort sein")
        if not q.get("fix"): err(where, "fix (richtiges Wort) fehlt")
    elif t == "estimate":
        for k in ("min", "max", "answer"):
            if not isinstance(q.get(k), int): err(where, f"{k} muss int sein")
        if all(isinstance(q.get(k), int) for k in ("min", "max", "answer")):
            if not q["min"] <= q["answer"] <= q["max"]: err(where, "answer liegt nicht zwischen min und max")
        if not isinstance(q.get("tolerance", 0), int): err(where, "tolerance muss int sein")


def check_quotes(where, obj, keys, text):
    """Free texts must not quote the Bible verbatim – the wording differs between translations."""
    if not text: return
    for k in keys:
        v = obj.get(k)
        if not isinstance(v, str): continue
        for m in re.findall(r"„([^“]+)“", v):
            if len(m.split()) >= 4 and norm(m) in norm(text):
                warn(where, f"wörtliches Bibelzitat in '{k}' ({m[:40]}…) – paraphrasieren und Vers nennen")


def main(path, review):
    global BASIS
    plan = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    pid = plan.get("id", "?")
    BASIS = plan.get("basis", BASIS)
    if not (ASSETS / "bible" / BASIS).exists(): err(pid, f"basis-Übersetzung '{BASIS}' nicht in assets/bible")
    for k in ("id", "title", "subtitle", "description", "direction", "sections"):
        if not plan.get(k): err(pid, f"Plan-Feld '{k}' fehlt")
    cards = {c["id"]: c for c in plan.get("cards", [])}
    for c in plan.get("cards", []):
        if c.get("type") not in CARD_TYPES: err(f"card {c.get('id')}", f"type muss einer von {CARD_TYPES} sein")
        if not c.get("name") or not c.get("text"): err(f"card {c.get('id')}", "name/text fehlt")
        if len(c.get("text", "")) > 400: warn(f"card {c.get('id')}", "Kartentext > 400 Zeichen, kürzen")
    places = {}
    pf = ASSETS / "places.json"
    if pf.exists():
        places = {p["id"]: p for p in json.loads(pf.read_text(encoding="utf-8"))["places"]}
    used_cards, ids = set(), set()
    stages = plan.get("stages", [])
    stage_ids = {s["id"] for s in stages}
    for i, s in enumerate(plan.get("sections", [])):
        sid = s.get("id", f"#{i}")
        if sid in ids: err(sid, "doppelte Abschnitts-ID")
        ids.add(sid)
        for k in ("title", "summary", "refs", "quiz", "explain"):
            if not s.get(k): err(sid, f"Pflichtfeld '{k}' fehlt")
        ok = all(check_ref(sid, r) for r in s.get("refs", []))
        text = " ".join(ref_text(r) for r in s.get("refs", [])) if ok else ""
        nverses = sum(r["to"] - r["from"] + 1 for r in s.get("refs", [])) if ok else 0
        if ok and not 3 <= nverses <= 16: warn(sid, f"{nverses} Verse – Ziel sind ca. 5-12")
        if not 1 <= len(s.get("quiz", [])) <= 3: err(sid, "1-3 Quizfragen pro Abschnitt")
        for j, q in enumerate(s.get("quiz", [])):
            check_quiz(f"{sid} quiz[{j}]", q, text)
            check_text_fields(f"{sid} quiz[{j}]", q, ("q", "explain", "hint"))
        for e in s.get("explain", []):
            if not e.get("q") or not e.get("a"): err(sid, "explain-Einträge brauchen q und a")
            if not e.get("translation"): check_quotes(sid + " explain", e, ("a",), text)
        for j, q in enumerate(s.get("quiz", [])):
            check_quotes(f"{sid} quiz[{j}]", q, ("q", "explain", "hint", "text"), text)
        check_quotes(sid, s, ("summary", "bridge", "focus", "teaser", "fact", "try"), text)
        for c in s.get("cards", []):
            used_cards.add(c)
            if c not in cards: err(sid, f"Karte '{c}' ist nicht im Plan definiert")
        if s.get("place") and places and s["place"] not in places: err(sid, f"Ort '{s['place']}' fehlt in places.json")
        if stages and s.get("stage") not in stage_ids: err(sid, f"stage '{s.get('stage')}' unbekannt")
        mv = s.get("memory_verse")
        if mv:
            if check_ref(f"{sid} memory_verse", mv.get("ref", {})):
                if norm(mv.get("text", "")) not in norm(ref_text(mv["ref"])): err(sid, "memory_verse.text steht nicht wörtlich im Vers")
            if len(mv.get("text", "").split()) > 16: warn(sid, "Merkvers > 16 Wörter – für das Spiel zu lang")
        pr = s.get("prayer")
        if pr:
            if not pr.get("source"): err(sid, "prayer braucht source")
            if not pr.get("text") and not pr.get("ref"): err(sid, "prayer braucht ref (Bibelwort) oder text (historisches Gebet)")
            if pr.get("ref"): check_ref(f"{sid} prayer", pr["ref"])
        check_text_fields(sid, s, ("title", "summary", "focus", "teaser", "fact", "try", "bridge"))
        if s.get("bridge") and len(s["bridge"]) > 320: warn(sid, "bridge > 320 Zeichen – kürzer fassen")
        if s.get("prayer") and s["prayer"].get("text"): check_text_fields(sid, s["prayer"], ("text",))
        if review:
            print(f"\n══ {sid} · {s.get('title')} ══")
            for r in s.get("refs", []):
                ch = book(r["book"])
                for v in range(r["from"], r["to"] + 1):
                    print(f"  {r['chapter']}:{v} {ch[r['chapter'] - 1][v - 1]}")
            for q in s.get("quiz", []):
                print(f"  ? [{q['type']}] {q.get('q') or q.get('quote') or q.get('text')}")
                if "options" in q: print(f"    → {q['options'][q['answer']]}  (von {q['options']})")
                if q["type"] == "truefalse": print(f"    → {q['answer']}")
                if q["type"] == "order": print(f"    → {q['items']}")
                if q["type"] == "error": print(f"    → richtig: {q.get('fix')}")
                if q["type"] == "estimate": print(f"    → {q['answer']} ±{q.get('tolerance', 0)}")
    for c in cards:
        if c not in used_cards: warn(f"card {c}", "wird in keinem Abschnitt freigeschaltet")
    for st in stages:
        n = sum(1 for s in plan["sections"] if s.get("stage") == st["id"])
        if n < 3: warn(f"stage {st['id']}", f"nur {n} Abschnitte – Rückblick braucht ≥3")
    idx = ASSETS / "plans" / "index.json"
    if idx.exists() and pid not in [p["id"] for p in json.loads(idx.read_text(encoding="utf-8"))["plans"]]:
        warn(pid, "Plan ist nicht in assets/plans/index.json eingetragen")
    print()
    for w in warnings: print(w)
    for e in errors: print(e)
    print(f"\n{pid}: {len(plan.get('sections', []))} Abschnitte, {len(cards)} Karten – {len(errors)} Fehler, {len(warnings)} Warnungen")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], "--review" in a)
