"""Helpers for writing reading plans as Python (see .claude/skills/leseplan-schreiben/format.md).

In a plan script:
    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from planlib import *
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def R(b, c, f, t=None): return {"book": b, "chapter": c, "from": f, "to": t or f}


def _opt(d, **kw):
    for k, v in kw.items():
        if v is not None: d[k] = v
    return d


def choice(q, options, verse=None, hint=None, explain=""):
    """options[0] is the right answer – the app shuffles."""
    return _opt({"type": "choice", "q": q, "options": options, "answer": 0, "explain": explain}, hint=hint, verse=verse)


def tf(q, answer, verse=None, hint=None, explain=""):
    return _opt({"type": "truefalse", "q": q, "answer": answer, "explain": explain}, hint=hint, verse=verse)


def who(quote, ref, options, explain, hint="Wer spricht hier mit wem?"):
    """options[0] is the speaker."""
    return {"type": "whosaid", "quote": quote, "quote_ref": ref, "options": options, "answer": 0, "hint": hint, "explain": explain}


def order(q, items, explain, hint="Lies den Abschnitt noch einmal von oben."):
    return {"type": "order", "q": q, "items": items, "hint": hint, "explain": explain}


def error(text, fix, verse, explain, hint=None):
    return {"type": "error", "q": "Finde den Fehler in der Nacherzählung.", "text": text, "fix": fix, "verse": verse,
            "hint": hint or f"Lies Vers {verse}.", "explain": explain}


def estimate(q, lo, hi, answer, unit, explain, verse=None, hint=None, tol=0):
    return _opt({"type": "estimate", "q": q, "min": lo, "max": hi, "answer": answer, "tolerance": tol, "unit": unit, "explain": explain},
                hint=hint, verse=verse)


def E(q, a, translation=None): return _opt({"q": q, "a": a}, translation=translation)


def MV(ref, text): return {"ref": ref, "text": text}


class PlanBuilder:
    def __init__(self, id, prefix, title, subtitle, description, direction, stages, cards, basis="elbbk"):
        self.plan = {
            "id": id, "title": title, "subtitle": subtitle, "description": description, "direction": direction, "basis": basis,
            "stages": [{"id": i, "title": t} for i, t in stages],
            "cards": [{"id": i, "type": t, "name": n, "text": x, "refs": r} for i, t, n, x, r in cards],
            "sections": [],
        }
        self.prefix = prefix

    def sec(self, stage, refs, title, summary, quiz, explain, **kw):
        d = {"id": f"{self.prefix}-{len(self.plan['sections']) + 1:02d}", "stage": stage, "refs": refs, "title": title, "summary": summary}
        for k in ("bridge", "place", "focus"):
            if k in kw: d[k] = kw.pop(k)
        d["quiz"] = quiz
        d["explain"] = explain
        if "try_" in kw: kw["try"] = kw.pop("try_")
        d.update(kw)
        self.plan["sections"].append(d)

    def write(self):
        out = ROOT / f"app/src/main/assets/plans/{self.plan['id']}.json"
        out.write_text(json.dumps(self.plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out} ({len(self.plan['sections'])} sections)")
