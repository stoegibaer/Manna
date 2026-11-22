# Manna – Bibel in Häppchen

Eine Android-App (und Web-App fürs iPhone), die Menschen mit ADHS und Schwierigkeiten bei der Umsetzung von Vorhaben (Executive Dysfunction) das Bibellesen so leicht wie möglich machen soll: kurze Sinnabschnitte, sofortiges Erfolgserlebnis durch Quizfragen, keine Strafen, keine reißenden Streaks.

> Privates Projekt, nicht im Play Store. Konzept und Entscheidungen: [`docs/KONZEPT.md`](docs/KONZEPT.md)

## Funktionen

- **Lesen in Sinnabschnitten** (5–12 Verse) mit Fokusmodus (Vers für Vers) und Erklärungen („Versteh ich nicht“)
- **Sechs Quiz-Typen** nach jedem Abschnitt – Fehler kosten nichts
- **Belohnung:** ein wachsender Garten aus zwölf biblischen Bäumen am Strom des Lebens, danach Baum des Lebens und goldene Stadt; Sammelkarten, Konfetti/Ton/Haptik (abschaltbar), Etappen-Rückblick
- **Lesepläne:** *Die große Geschichte* (44 Abschnitte, Start für alle), *Habakuk*; Auswahl nach Richtungen
- **Mini-Karte** „Wo sind wir?“
- **Updates direkt in der App** (abschaltbar), APK aus den GitHub-Releases
- **Gewohnheit:** Tagesminimum 1 Vers, Wenn-dann-Anker, Plan B, stündliche Erinnerung bis gelesen wurde (erste mit Quizfrage), „Heute aussetzen“, Wochenziel statt Streak, verteilte Wiederholung, Wiedereinstieg nach Pausen, „Nicht stören“ beim Lesen

## Bauen

```bash
./gradlew assembleDebug          # APK: app/build/outputs/apk/debug/app-debug.apk
./gradlew testDebugUnitTest      # Unit-Tests
```

## Veröffentlichen (Android)

Die App sucht selbst nach Updates: Sie fragt bei GitHub nach dem neuesten Release und installiert nach einem Tippen dessen APK.
Ein neues Release braucht deshalb immer eine signierte APK (`keystore.properties` muss vorhanden sein):

```bash
# versionCode und versionName in app/build.gradle.kts erhöhen, committen, pushen
./gradlew assembleRelease
cp app/build/outputs/apk/release/app-release.apk manna-X.Y.Z.apk
gh release create vX.Y.Z manna-X.Y.Z.apk --title "Manna X.Y.Z" --notes "…"
```

Der Tag muss zur `versionName` passen (`v0.2.3` ↔ `0.2.3`). Die Testversion („Manna (Test)“) sucht nicht nach Updates.

## Web-App für iPhone (PWA)

`web/` enthält dieselbe App als Web-App (Svelte + TypeScript), vor allem für iPhone-Nutzer:
**https://stoegibaer.github.io/Manna/** – in Safari öffnen, Teilen → „Zum Home-Bildschirm“.
Sie nutzt die Inhalte aus `app/src/main/assets` direkt (keine Kopie im Repo), funktioniert offline und
speichert alles nur auf dem Gerät. Keine Erinnerungen, kein „Nicht stören“, keine Vibration.
Sicherungen sind mit der Android-App austauschbar.

```bash
cd web
npm install
npm run dev        # http://localhost:5173 (Vorschau des Gartens: ?debugTree=200)
npm run check      # Typprüfung
npm test           # Unit-Tests
npm run build      # nach web/dist
```

Jeder Push auf `main`, der `web/` oder die Inhalte ändert, veröffentlicht die Web-App automatisch
(`.github/workflows/web.yml`). Installierte Apps bieten dann „Neu laden“ an.

## Lesepläne schreiben

Mit dem Claude-Code-Skill [`leseplan-schreiben`](.claude/skills/leseplan-schreiben/SKILL.md) (Format, Qualitätsregeln, konfessionelle Neutralität). Prüfen:

```bash
python3 -I tools/validate_plan.py app/src/main/assets/plans/<id>.json --review
```

## Quellen und Lizenzen

- **Bibeltext:** Elberfelder Übersetzung, Edition bibelkommentare.de. © 2019 Verbreitung des christlichen Glaubens e.V., lizenziert unter [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Bezogen über [ebible.org](https://ebible.org/Scriptures/details.php?id=deuelbbk) / [bible.helloao.org](https://bible.helloao.org). Der Wortlaut ist unverändert; beim Import wurden nur fehlende Leerzeichen an Fußnoten-Stellen ergänzt (`tools/build_bible_assets.py`).
- **Kartendaten:** [Natural Earth](https://www.naturalearthdata.com/) (gemeinfrei), aufbereitet mit `tools/build_map.py`.
- **Inhalte der Lesepläne** (Fragen, Erklärungen, Karten): eigene Texte dieses Projekts.
