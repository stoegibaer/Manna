# Manna – Bibel in Häppchen

Eine Android-App, die Menschen mit ADHS und Schwierigkeiten bei der Umsetzung von Vorhaben (Executive Dysfunction) das Bibellesen so leicht wie möglich machen soll: kurze Sinnabschnitte, sofortiges Erfolgserlebnis durch Quizfragen, keine Strafen, keine reißenden Streaks.

> Privates Projekt, nicht im Play Store. Konzept und Entscheidungen: [`docs/KONZEPT.md`](docs/KONZEPT.md)

## Funktionen

- **Lesen in Sinnabschnitten** (5–12 Verse) mit Fokusmodus (Vers für Vers) und Erklärungen („Versteh ich nicht“)
- **Sechs Quiz-Typen** nach jedem Abschnitt – Fehler kosten nichts
- **Belohnung:** wachsendes Senfkorn, Sammelkarten, Konfetti/Ton/Haptik (abschaltbar), Etappen-Rückblick
- **Lesepläne:** *Die große Geschichte* (44 Abschnitte, Start für alle), *Habakuk*; Auswahl nach Richtungen
- **Mini-Karte** „Wo sind wir?“
- **Gewohnheit:** Tagesminimum 1 Vers, Wenn-dann-Anker, Plan B, stündliche Erinnerung bis gelesen wurde (erste mit Quizfrage), „Heute aussetzen“, Wochenziel statt Streak, verteilte Wiederholung, Wiedereinstieg nach Pausen, „Nicht stören“ beim Lesen

## Bauen

```bash
./gradlew assembleDebug          # APK: app/build/outputs/apk/debug/app-debug.apk
./gradlew testDebugUnitTest      # Unit-Tests
```

## Lesepläne schreiben

Mit dem Claude-Code-Skill [`leseplan-schreiben`](.claude/skills/leseplan-schreiben/SKILL.md) (Format, Qualitätsregeln, konfessionelle Neutralität). Prüfen:

```bash
python3 -I tools/validate_plan.py app/src/main/assets/plans/<id>.json --review
```

## Quellen und Lizenzen

- **Bibeltext:** Elberfelder Übersetzung, Edition bibelkommentare.de. © 2019 Verbreitung des christlichen Glaubens e.V., lizenziert unter [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Bezogen über [ebible.org](https://ebible.org/Scriptures/details.php?id=deuelbbk) / [bible.helloao.org](https://bible.helloao.org). Der Wortlaut ist unverändert; beim Import wurden nur fehlende Leerzeichen an Fußnoten-Stellen ergänzt (`tools/build_bible_assets.py`).
- **Kartendaten:** [Natural Earth](https://www.naturalearthdata.com/) (gemeinfrei), aufbereitet mit `tools/build_map.py`.
- **Inhalte der Lesepläne** (Fragen, Erklärungen, Karten): eigene Texte dieses Projekts.
