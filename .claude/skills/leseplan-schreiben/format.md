# Leseplan-Format (assets/plans/<id>.json)

Alle Texte auf Deutsch, Du-Form.

## Übersetzungsneutral (wichtig)

Die App kann die Übersetzung wechseln (Standard: Elberfelder 2019 = `elbbk`; später z. B. HfA). Deshalb:
- **Bibeltext wird nie in Freitexte kopiert.** In `summary`, `explain`, Quiz-`explain`/`hint`, `fact`, `teaser`, `try` usw. **paraphrasieren und Vers nennen** („V. 11: Ihre eigene Kraft ist ihr Gott.“ statt eines wörtlichen Zitats). Einzelne Schlüsselwörter in Anführungszeichen sind ok. Das Prüfskript warnt bei wörtlichen Zitaten ab 4 Wörtern.
- **Versangaben in deutscher Standardzählung** (wie Luther/HfA/BasisBibel/Elberfelder 2019; Psalmen mit Überschrift = Vers 1).
- **Wörtliche Texte nur mit Versangabe:** `quote` + `quote_ref` (whosaid), `memory_verse` (`ref` + `text`), `prayer.ref`. Der Text steht im Wortlaut der `basis`-Übersetzung; die App holt ihn bei anderen Übersetzungen über die Versangabe.
- **Erklärungen zu Wörtern einer bestimmten Übersetzung** (z. B. „Scheol“, „Gesicht“ = Vision) bekommen `"translation": "elbbk"` – sie erscheinen nur bei dieser Übersetzung.

```jsonc
{
  "id": "habakuk",                 // Kleinbuchstaben, = Dateiname
  "title": "Habakuk",
  "subtitle": "Warum, Gott?",      // kurze Leitfrage/Thema
  "description": "2–3 Sätze: worum geht es, warum lohnt es sich.",
  "direction": "ehrlich",          // Richtung: start | jesus | ehrlich | gerechtigkeit | hoffnung | weisheit
  "basis": "elbbk",                // Übersetzung, in deren Wortlaut quote/memory_verse.text stehen
  "stages": [                      // Etappen; am Ende jeder Etappe kommt automatisch ein Rückblick (Reihenfolge der Abschnittstitel)
    { "id": "klage", "title": "Die Klage" }
  ],
  "cards": [                       // Sammelkarten, im Plan definiert, in Abschnitten freigeschaltet
    { "id": "habakuk", "type": "person", "name": "Habakuk", "text": "max. ~400 Zeichen, sachlich", "refs": "Hab 1,1; 3,1" }
    // type: person | ort | begriff | ereignis
  ],
  "sections": [
    {
      "id": "hab-01",              // <plan-kürzel>-<nn>
      "stage": "klage",
      "refs": [ { "book": 35, "chapter": 1, "from": 1, "to": 4 } ],   // mehrere erlaubt (z. B. große Geschichte)
      "title": "Wie lange noch?",  // kurz, sachlich, kein Spoiler-Kitsch
      "summary": "1–2 Sätze, was passiert ist (für Wiedereinstieg & Rückblick).",
      "bridge": "…",               // optional: „Was dazwischen geschah“ – 1–2 Sätze, die den Sprung vom vorigen Abschnitt überbrücken (für Pläne mit Sprüngen, z. B. große Geschichte)
      "place": "jerusalem",        // optional, id aus assets/places.json
      "focus": "Achte auf …",      // optional, NUR wenn es um etwas wirklich Zentrales geht
      "quiz": [ /* 1–3 Fragen, s. u. */ ],
      "explain": [                 // Pflicht: „Versteh ich nicht“ – 1–4 Einträge
        { "q": "Was ist ein „Gesicht“?", "a": "…", "translation": "elbbk" },   // nur bei dieser Übersetzung
        { "q": "Wer sind die Chaldäer?", "a": "…" }
        // Bei echten Unterschieden zwischen Konfessionen: eigener Eintrag
        // „Wie verstehen das verschiedene Kirchen?“ – neutral, jede Sicht fair in ihren eigenen Worten.
      ],
      "cards": ["habakuk"],        // optional: hier freigeschaltete Karten
      "fact": "Wusstest du …",     // optional, überraschend + korrekt; nicht in jedem Abschnitt (~1/3)
      "teaser": "…",               // optional, Neugierfrage auf den NÄCHSTEN Abschnitt
      "memory_verse": { "ref": { "book": 35, "chapter": 2, "from": 4, "to": 4 }, "text": "Der Gerechte aber wird durch seinen Glauben leben." },
      "try": "…",                  // optional, konkrete kleine Idee für heute
      "prayer": { "ref": { "book": 19, "chapter": 13, "from": 2, "to": 2 }, "source": "Psalm 13,2" }   // Bibelwort: per ref
      // oder historisches Gebet: { "text": "…", "source": "Augustinus, Bekenntnisse I,1" }
    }
  ]
}
```

## Quiz-Typen

Für alle: `explain` (Pflicht, 1–2 Sätze mit Versangabe, wird nach der richtigen Antwort gezeigt), `hint` (Hinweis bei falscher Antwort, z. B. „Schau in Vers 6“), optional `verse` (int, Vers zum Nachschauen).

| type | Felder | Hinweise |
|---|---|---|
| `choice` | `q`, `options` (2–4), `answer` (Index) | App mischt die Optionen. Falsche Optionen plausibel, nicht albern. |
| `truefalse` | `q` (Aussage), `answer` (bool) | Gut für typische Missverständnisse. |
| `whosaid` | `quote` (wörtlich, basis-Übersetzung), `quote_ref` (Vers), `options`, `answer` | Zitat kurz (≤ 15 Wörter). |
| `order` | `q`, `items` (3–5, in RICHTIGER Reihenfolge) | App mischt. Kurze Items. |
| `error` | `q`, `text` mit genau einem `[falschen]` Wort, `fix` | Nacherzählung 1–2 Sätze; der Fehler soll inhaltlich bedeutsam sein. |
| `estimate` | `q`, `min`, `max`, `answer`, `tolerance`, `unit` | Nur bei Zahlen, die im Text stehen oder zählbar sind. |

Mischung pro Plan: überwiegend `choice`, regelmäßig die anderen Typen, nie zweimal derselbe Typ direkt hintereinander innerhalb eines Abschnitts.

## Orte (assets/places.json)

```json
{ "id": "jerusalem", "name": "Jerusalem", "lat": 31.778, "lon": 35.235, "text": "1 Satz" }
```
Neue Orte dort ergänzen (Koordinaten realistisch, gerundet auf 2–3 Nachkommastellen).

## Index (assets/plans/index.json)

Jeder Plan muss eingetragen werden: `{ "id", "title", "subtitle", "direction", "available": true }`.
