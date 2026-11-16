---
name: leseplan-schreiben
description: Schreibt einen neuen Leseplan (Abschnitte, Quizze, Erklärungen, Karten) für die ADHS-freundliche Bibel-App „Manna“. Verwenden, wenn ein Leseplan erstellt, erweitert oder überarbeitet werden soll, z. B. „Schreib den Leseplan Amos“.
---

# Leseplan schreiben

Ein Leseplan führt Menschen mit ADHS in kurzen Sinnabschnitten durch einen wertvollen Bibeltext. Nach jedem Abschnitt gibt es ein sofortiges Erfolgserlebnis (Quiz). Qualität geht vor Menge. Ein Plan, der kitschig, belehrend oder sachlich falsch ist, schadet mehr als gar keiner.

Lies zuerst **`format.md`** in diesem Ordner (Datenformat) und `docs/KONZEPT.md` (Abschnitte 1, 4 und 6).

## Ablauf

1. **Text vollständig lesen**, bevor du irgendetwas schreibst:
   `python3 -I tools/show_text.py <buch_nr> <kapitel> …` (Buchnummern: `--list`).
2. **Plan entwerfen und dem Nutzer kurz vorlegen:**
   - Welche Texte gehören hinein? Nicht zwingend alles; wichtige, aussagekräftige Stellen haben Vorrang vor Vollständigkeit.
   - Etappen und Sinnabschnitte mit 5–12 Versen, die nicht mitten in einer Szene oder einem Gedanken enden.
   - Einen Satz pro Abschnitt, worum es geht.
3. **Ausarbeiten** in `app/src/main/assets/plans/<id>.json`. Den Plan in `assets/plans/index.json` eintragen, neue Orte in `assets/places.json`.
4. **Prüfen:** `python3 -I tools/validate_plan.py app/src/main/assets/plans/<id>.json --review`. Alle Fehler beheben. Dann jeden Abschnitt im Review-Ausdruck gegen den Text lesen: Ist jede Antwort wirklich aus dem Text belegbar? Ist jede falsche Option wirklich falsch?
5. **Selbstkritik-Durchgang** mit den Qualitätsregeln unten, Abschnitt für Abschnitt. Lieber ein optionales Feld streichen als ein mittelmäßiges behalten.
6. Am Ende dem Nutzer berichten: Anzahl der Abschnitte, Karten und Fragen sowie die Stellen, bei denen du unsicher warst.

## Qualitätsregeln

**Ton**
- Erwachsen und ehrlich, mit Du-Ansprache, warm, aber nüchtern. Die Leser sind Jugendliche und Erwachsene.
- **Kein Kitsch:** keine Emojis, keine Herzchen-Sprache, keine Superlative („wunderschön“, „unglaublich kraftvoll“), kein „Gott liebt dich so sehr!!“. Auch keine Predigt und keine Moral mit erhobenem Zeigefinger.
- Keine Scham: nie „Du solltest …“ oder „Hast du etwa …?“. Formulierungen laden ein, statt Forderungen zu stellen.
- **Nicht predigen, nichts nahelegen.** Karten, Erklärungen, Fakten und „Heute ausprobieren“ vermitteln nichts, was man nicht selbst im Text finden kann. Gib sachliche Informationen (Wortbedeutung, Hintergrund, wie verschiedene Traditionen lesen) und stelle gute Fragen. Ziehe keine Schlussfolgerung für den Leser („Das zeigt uns …“, „Hier wird deutlich …“, „Gott will damit sagen …“). Die Verständnisarbeit macht der Leser. Im Zweifel: Satz streichen oder als offene Frage formulieren.
- **Sichtweisen von Gläubigen:** Die Pläne sind für Gläubige. Zeige, wie andere Gläubige und Traditionen einen Text verstehen. Die historisch-kritische Sicht wird nicht als eigene Position dargestellt. Sachliche Informationen (Datierung, Textgeschichte, Handschriften) bleiben erlaubt.
- **Endzeit:** Die Leser kommen meist mit einer dispensationalistischen Sicht. Ziel ist, andere Verständnisse kennenzulernen, besonders den Amillenialismus. Zeige, wo die vertraute Sicht eine Deutung ist, und stelle die anderen fair und gründlich daneben.

**Neugierfragen (`teaser`)**
- Sie sollen auch Bibelkenner neugierig machen. Also keine offensichtlichen Floskeln wie „Was wird wohl passieren?“, sondern eine echte Spannung, ein überraschendes Detail oder eine offene Frage.
- Sie verraten nicht die Pointe des nächsten Abschnitts.

**„Achte auf …“ (`focus`)**
- Nur, wenn es um etwas Zentrales geht, also höchstens in jedem dritten Abschnitt.

**Quiz**
- Gefragt wird nur nach **Wichtigem**: Handlung, Aussage, Wendepunkt. Nebensächliche Details („Welche Farbe …?“) kommen höchstens vor, wenn sie Bedeutung tragen.
- Jede richtige Antwort muss **aus dem Abschnitt belegbar** sein. `explain` nennt den Vers.
- Falsche Optionen sind plausibel, aber eindeutig falsch, und nie lächerlich.
- Bei Deutungsfragen nicht abfragen, was jemand „glauben soll“. Abgefragt wird, was im Text steht.
- Abwechslung bei den Typen (siehe `format.md`).

**Erklärungen (`explain`)**
- Schwierige Wörter erklären, besonders die alte Sprache der Elberfelder 1905: „Jehova“, „Pardel“, „Hindin“, „verdolmetscht“. Dazu historischer Hintergrund und Zusammenhang.
- Kurz halten: 1–4 Sätze pro Eintrag.
- **Konfessionen:** Gibt es echte Unterschiede im Verständnis (z. B. zwischen katholisch, orthodox, evangelisch-landeskirchlich und freikirchlich), dann alle Sichtweisen fair und neutral nennen, jede in ihren eigenen Worten. Keine Sicht wird als „die richtige“ dargestellt. Die Zielgruppe ist freikirchlich geprägt und soll andere Verständnisse kennenlernen. Wo es Gemeinsamkeiten gibt (z. B. die Gemeinsame Erklärung zur Rechtfertigungslehre von 1999), diese nennen.
- Bei unsicheren wissenschaftlichen Fragen (Datierung, Autorschaft, Textgeschichte) den Stand ehrlich und knapp darstellen („wahrscheinlich“, „umstritten“).

**Brücken (`bridge`)**
- Nur in Plänen, die Sprünge machen. 1–2 sachliche Sätze: Was geschah zwischen dem vorigen und diesem Abschnitt (Zeit, Ort, Personen)? Keine Deutung, kein Spoiler des aktuellen Abschnitts.

**Karten (`cards`)**
- Personen, Orte, Begriffe und Ereignisse, die für das Verständnis wichtig sind, mit sachlichem Text (≤ 400 Zeichen).
- Ohne Emoji. Pro Plan etwa 6–15 Karten.

**„Wusstest du?“ (`fact`)**
- Überraschend, korrekt und relevant. Etwa jeder dritte Abschnitt bekommt eins.
- Keine Fakten, die du nicht sicher weißt.

**Gebet (`prayer`)**
- **Nur Bibelworte** (z. B. Ps 13,2; Mk 9,24) oder **historische Gebete** (z. B. Augustinus, Bonhoeffer, alte Kirchengebete) mit Quellenangabe.
- Niemals selbst formulierte Gebete. Selten einsetzen, etwa in jedem vierten Abschnitt, und nur, wo es wirklich passt.
- Historische Gebete nur gemeinfrei (Autor seit über 70 Jahren tot) oder in eigener Übersetzung eines alten Originals.

**„Heute ausprobieren“ (`try`)**
- Konkret, klein und in unter 5 Minuten machbar, nicht moralisierend.
- Nur, wo es sich natürlich aus dem Text ergibt.

## Sachliche Sorgfalt

- Prüfe Namen, Zahlen und Abläufe im Text nach, statt dich auf dein Gedächtnis zu verlassen. Das Prüfskript kontrolliert nur Format und Zitate, nicht die Inhalte.
- Bei Paralleltexten (z. B. Markus und Matthäus) nur abfragen, was im **gelesenen** Text steht.
