#!/usr/bin/env python3
"""Export every verse the reading plans use as input for the TTS server (see docs/tts-server-auftrag.md).

Usage: python3 -I tools/export_tts_input.py [--translation elbbk] [--out tts_input.json]
Collects: section refs, memory verses, prayer refs and quote refs of all plans in assets/plans/index.json (available ones).
Item id: <book 2-digit>_<chapter 3-digit>_<verse 3-digit>, e.g. 35_001_002.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app/src/main/assets"

# Pronunciation hints for names and foreign words (German reading). The TTS server may extend this list.
LEXICON = {
    "Habakuk": "Ha-ba-kuk", "Chaldäer": "Kal-dä-er", "Schigjonoth": "Schig-jo-not", "Sela": "Se-la",
    "Teman": "Te-man", "Paran": "Pa-ran", "Kuschan": "Ku-schan", "Midian": "Mi-di-an", "Scheol": "Sche-ol",
    "Elieser": "E-li-e-ser", "Morija": "Mo-ri-ja", "Pniel": "Pni-el", "Jabbok": "Jab-bok", "Isai": "I-sa-i",
    "Eliab": "E-li-ab", "Abinadab": "A-bi-na-dab", "Schamma": "Scham-ma", "Urija": "U-ri-ja",
    "Ysop": "Ü-sop", "Zion": "Zi-on", "Nebukadnezar": "Ne-bu-kad-ne-zar", "Nebusaradan": "Ne-bu-sa-ra-dan",
    "Kyrenius": "Kü-re-ni-us", "Zebedäus": "Ze-be-dä-us", "Emmaus": "Em-ma-us", "Galiläa": "Ga-li-lä-a",
    "Judäa": "Ju-dä-a", "Parther": "Par-ter", "Elamiter": "E-la-mi-ter", "Kappadozien": "Kap-pa-do-zi-en",
    "Phrygien": "Phrü-gi-en", "Pamphylien": "Pam-phü-li-en", "Kyrene": "Kü-re-ne", "Proselyten": "Pro-se-lü-ten",
    "Eloi, Eloi, lama sabachthani": "E-lo-i, E-lo-i, la-ma sa-bach-ta-ni", "Talitha kumi": "Ta-li-ta ku-mi",
    "Hephata": "Ef-fa-ta", "Boanerges": "Bo-a-ner-ges", "Gerasener": "Ge-ra-se-ner", "Dekapolis": "De-ka-po-lis",
    "Bethsaida": "Bet-sa-i-da", "Kapernaum": "Ka-per-na-um", "Gethsemane": "Get-se-ma-ne", "Golgatha": "Gol-ga-ta",
    "Bartimäus": "Bar-ti-mä-us", "Jericho": "Je-ri-cho", "Herodias": "He-ro-di-as", "Beelzebul": "Be-el-ze-bul",
    "Hosianna": "Ho-si-an-na", "Rabbuni": "Rab-bu-ni", "Abba": "Ab-ba", "Cherubim": "Che-ru-bim",
}


def ref_items(r, chapters):
    for v in range(r["from"], r["to"] + 1):
        text = chapters[r["chapter"] - 1][v - 1]
        if text.strip():
            yield f'{r["book"]:02d}_{r["chapter"]:03d}_{v:03d}', r["book"], r["chapter"], v, text


def main(argv):
    tid = argv[argv.index("--translation") + 1] if "--translation" in argv else "elbbk"
    out = pathlib.Path(argv[argv.index("--out") + 1]) if "--out" in argv else ROOT / "tts_input.json"
    index = json.loads((ASSETS / "plans/index.json").read_text(encoding="utf-8"))
    books, items = {}, {}

    def chapters(nr):
        if nr not in books:
            books[nr] = json.loads((ASSETS / f"bible/{tid}/{nr:02d}.json").read_text(encoding="utf-8"))["chapters"]
        return books[nr]

    for entry in index["plans"]:
        if not entry.get("available"): continue
        plan = json.loads((ASSETS / f'plans/{entry["id"]}.json').read_text(encoding="utf-8"))
        for s in plan["sections"]:
            refs = list(s["refs"])
            if s.get("memory_verse"): refs.append(s["memory_verse"]["ref"])
            if s.get("prayer", {}).get("ref"): refs.append(s["prayer"]["ref"])
            refs += [q["quote_ref"] for q in s.get("quiz", []) if q.get("quote_ref")]
            for r in refs:
                for iid, b, c, v, text in ref_items(r, chapters(r["book"])):
                    items[iid] = {"id": iid, "text": text, "book": b, "chapter": c, "verse": v}

    used = {k: v for k, v in LEXICON.items() if any(k in it["text"] for it in items.values())}
    data = {"translation": tid, "items": [items[k] for k in sorted(items)], "lexicon": used}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    words = sum(len(it["text"].split()) for it in items.values())
    print(f"{len(items)} Verse, {words} Wörter (≈ {words / 150:.0f} min Audio), {len(used)} Lexikon-Einträge → {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
