# Konzept: Bibel-App für Menschen mit ADHS

> Stand: 16.11.2026 · Status: **Entwurf zur Freigabe**
> Arbeitstitel: **Manna** („jeden Tag genug für heute“, vgl. 2. Mose 16). Name ist noch offen.

## 1. Ziel

Menschen mit ADHS und Problemen bei der Umsetzung von Vorhaben (Executive Dysfunction) soll es **so leicht wie möglich** fallen, regelmäßig und mit Gewinn die Bibel zu lesen. Die App senkt die Hürde zum Anfangen auf das Minimum, belohnt sofort und beschämt nie. Dabei bleibt sie inhaltlich ernstzunehmend.

**Leitprinzipien**
1. **Anfangen ist das Schwerste.** Darum ein Tipp bis zum Text und als Tagesminimum nur 1 Vers.
2. **Sofortiges Erfolgserlebnis.** Nach jedem kurzen Sinnabschnitt gibt es Feedback, nicht erst am Ende (Delay Aversion).
3. **Keine Scham.** Die App zeigt keine Streaks, die reißen, keine Zähler, die sinken, und keine Strafen für Fehler.
4. **Wenig Auswahl.** Es gibt immer einen klaren nächsten Schritt, keine Entscheidungslähmung.
5. **Qualität vor Menge.** Der Fokus liegt auf wichtigen, aussagekräftigen Texten statt auf Durchlesen. Nichts darf kitschig wirken.
6. **Konfessionsübergreifend.** Wo Konfessionen unterschiedlich verstehen, werden die Sichtweisen neutral genannt. Die Zielgruppe ist zunächst eine freikirchliche Jugendgruppe, die auch andere Verständnisse kennenlernen soll.

## 2. Recherche-Grundlage (Kurzfassung)

| Erkenntnis | Evidenz | Umsetzung |
|---|---|---|
| Delay Aversion: Späte Belohnung und spätes Feedback motivieren bei ADHS kaum (Sonuga-Barke) | gut | Quiz und Belohnung nach jedem Abschnitt |
| Kurze Abschnitte senken die Überforderung | plausibel | Sinnabschnitte von ca. 5–12 Versen |
| Rückblick über den ganzen Text hilft bei ADHS mehr als Abfragen pro Abschnitt (Stern & Halamish 2023) | eine Studie | zusätzlich Kapitel- bzw. Etappen-Rückblick |
| Streaks lösen nach einer Unterbrechung oft Scham und Abbruch aus | umstritten | Wochenziel und nur wachsende Zähler |
| Vorlesen beim Mitlesen wird als Stütze erlebt | qualitativ | Vorlesen mit Mitlese-Markierung |
| Wenn-dann-Pläne und Erinnerungen | bei Kindern belegt | Gewohnheits-Anker, Plan B, Erinnerungen |
| Verteilte Wiederholung (Spaced Repetition) | allgemein gut belegt | „Erinnerst du dich?“-Fragen |
| Vorab-Fragen lenken die Aufmerksamkeit | allgemein belegt | „Achte auf …“, nur bei Wichtigem |

## 3. Übersetzung

- **Start: Elberfelder 1905** (gemeinfrei, offline, liegt bereits vor).
- Die Übersetzung ist **austauschbar** (eigene Schnittstelle `TextProvider`). Eine moderne Übersetzung (BasisBibel, HfA) ist später nur über eine offizielle API oder mit Erlaubnis des Verlags möglich.
- Quizfragen beziehen sich auf den **Inhalt**, nicht auf den Wortlaut, und funktionieren deshalb mit jeder Übersetzung.

## 4. Lesepläne

### Struktur
```
Die große Geschichte (für alle zuerst)
        ↓
„Wohin als Nächstes?“  → wenige Richtungen
  • Jesus kennenlernen       → Markus · (Bergpredigt) · (…)
  • Ehrlich mit Gott         → Habakuk · (Psalmen für schwere Tage) · (Hiob)
  • Gerechtigkeit & Treue    → (Amos) · (Hosea) · (Micha)
  • Hoffnung & Trost         → (Jesaja 40–55) · (…)
  • Sinn & Weisheit          → (Prediger) · (…)
        ↓
pro Richtung höchstens 3 Pläne
```
Pläne in Klammern sind „bald verfügbar“. Sie sind sichtbar, aber nicht wählbar, damit man nicht erschlagen wird.

### Version 1
| Plan | Inhalt | Umfang (geschätzt) |
|---|---|---|
| **Die große Geschichte** | der rote Faden der Bibel von der Schöpfung bis zur neuen Schöpfung, mit Etappen-Rückblicken | ca. 40 Abschnitte |
| **Markus** | Jesus kennenlernen | ca. 80 Abschnitte |
| **Habakuk** | Warum, Gott? Ein Prophet streitet mit Gott | ca. 8 Abschnitte |

Die Lesepläne werden mit einem **wiederverwendbaren Skill** geschrieben (`.claude/skills/leseplan-schreiben/`). Er enthält das Format, Qualitätsregeln gegen Kitsch, Regeln für die Neutralität zwischen Konfessionen und ein Prüfskript, das alle Versangaben und Antworten gegen den Bibeltext abgleicht.

### Inhalt pro Abschnitt
| Feld | Pflicht | Beschreibung |
|---|---|---|
| Bibelstelle(n) | ✓ | eine oder mehrere Versbereiche (die große Geschichte springt) |
| Titel | ✓ | kurz und sachlich |
| Zusammenfassung | ✓ | 1–2 Sätze für den Wiedereinstieg und die Rückblicke |
| Ort | – | für die Mini-Karte |
| „Achte auf …“ | – | nur wenn es um etwas wirklich Wichtiges geht |
| Quiz | ✓ | 1–3 Fragen |
| Erklärungen („Versteh ich nicht“) | ✓ | vorab geschrieben: Begriffe, Hintergrund, ggf. „So verstehen es verschiedene Konfessionen“ |
| Karten | – | Personen, Orte und Begriffe, die freigeschaltet werden |
| „Wusstest du?“ | – | Überraschungs-Hintergrundwissen, nicht bei jedem Abschnitt |
| Neugierfrage | – | macht neugierig auf den nächsten Abschnitt; darf für Bibelkenner nicht offensichtlich oder kitschig sein |
| Merkvers | – | für das Merkvers-Spiel |
| „Heute ausprobieren“ | – | eine kleine, konkrete Idee für den Alltag |
| Gebetswort | – | **nur** Bibelworte (z. B. Mk 9,24) oder Gebete aus der Kirchengeschichte, keine selbst formulierten Gebete; selten und nur, wo es passt |

## 5. Ablauf einer Lese-Session

```
App öffnen
  → [nach längerer Pause] Wiedereinstieg: „Schön, dass du da bist“ + was bisher geschah
  → Energie-Check:  wenig Kraft → 1 Vers · normal → 1 Abschnitt · viel → bis zum Etappen- bzw. Kapitelende
  → [optional] 1 „Erinnerst du dich?“-Frage
  → Vorbereitung: Ort auf der Mini-Karte, ggf. „Achte auf …“
  → Lesen: Vollansicht oder Fokusmodus Vers für Vers (abschaltbar), Vorlesen mit Markierung
  → Quiz: sofortiges Feedback, bei Fehlern Hinweis und Versstelle, nochmal versuchen
  → Belohnung: Senfkorn wächst, ggf. neue Karte oder „Wusstest du?“
  → [Kapitel- oder Etappenende] Rückblick: Ereignisse ordnen
  → Ein-Tipp-Reflexion (überspringbar) · ggf. „Heute ausprobieren“ · ggf. Gebetswort
  → Stoppsignal: „Für heute geschafft ✓“, darunter klein „Noch einer?“ und die Neugierfrage
```

- **Ein-Knopf-Start:** Der Startbildschirm hat einen großen Knopf, der zum nächsten Abschnitt führt. Kein Menü steht im Weg.
- **Tagesminimum = 1 Vers.** „Wenig Kraft“ zeigt genau einen Vers, das gilt als geschafft.
- **Nicht stören** (optional): Während der Session werden Benachrichtigungen stummgeschaltet. Dafür muss man einmal eine Berechtigung erteilen.

## 6. Erfolgserlebnis und Motivation

- **Quiz-Typen:** Multiple Choice, Wahr/Falsch, „Wer hat’s gesagt?“, Reihenfolge sortieren, „Finde den Fehler“ (falsches Wort in einer Nacherzählung antippen), Schätzfrage mit Schieberegler. Emoji-Rätsel gibt es nicht.
- **Kein Punktabzug.** Bei einem Fehler kommen Hinweis und Versstelle, dann ein neuer Versuch.
- **Feedback:** Vibration, Ton und Konfetti, einzeln und leicht abschaltbar.
- **Senfkorn** (vgl. Mk 4,30–32): Es wächst mit jedem Abschnitt zum Baum und schrumpft nie.
- **Sammelalbum:** schön gestaltete Karten zu Personen, Orten, Begriffen und Ereignissen, die Sammellust wecken. Keine Glücksspiel-Mechanik.
- **„Wusstest du?“-Karten** tauchen unvorhersehbar auf.
- **Merkvers-Spiel:** Wörter in der richtigen Reihenfolge antippen.
- **Verteilte Wiederholung:** Beantwortete Fragen kommen nach etwa 1, 3, 7 und 21 Tagen wieder.
- **Wochenziel statt Streak**, z. B. 4 von 7 Tagen, frei wählbar. Es zählen nur Werte, die wachsen („47 Abschnitte gelesen“).
- **Ausdrücklich nicht dabei:** Fortschrittsbalken, Level oder Titel, Ranglisten.

## 7. Erinnerungen und Gewohnheit

- **Gewohnheits-Anker beim ersten Start:** „Nach dem ___ lese ich“ (Auswahl oder eigener Text) und eine Uhrzeit.
- **Plan B:** „Wenn ich es verpasse, dann ___“.
- **Erinnerungen ab der Anker-Uhrzeit stündlich, bis das Tagesminimum erfüllt ist:**
  - Die **erste** Erinnerung enthält eine Quizfrage („Erinnerst du dich?“) mit Antwortknöpfen. Ein Tipp öffnet die App mit Ergebnis und dem nächsten Abschnitt.
  - Die **folgenden** zeigen die Neugierfrage zum nächsten Abschnitt mit den Knöpfen **[1 Vers lesen ✓]** und **[Weiterlesen →]**.
- **Ruhezeit:** einstellbar, Standard bis 22:00 Uhr.
- **„Heute bewusst aussetzen“** ohne Vorwurf; Erinnerungen sind generell abschaltbar.
- **Lernen:** Nach etwa 2 Wochen schlägt die App vor, die Erinnerung zur tatsächlichen Lesezeit zu verschieben.

## 8. Lesehilfen

- **Fokusmodus Vers für Vers:** Der aktuelle Vers ist hell, der Rest gedimmt, ein Tipp führt weiter. Abschaltbar.
- **Vorlesen mit Mitlese-Markierung:**
  - Für die Lesepläne gibt es **vorab erzeugte Audios** von deinem KI-Server (Auftrag siehe `docs/tts-server-auftrag.md`). Sie werden mit der App ausgeliefert und funktionieren offline, ein Audio pro Vers.
  - Beim freien Lesen und als Ersatz dient die Android-Systemstimme.
- **Personen-, Orts- und Begriffskarten:** Ein Tipp auf ein markiertes Wort zeigt eine kurze Beschreibung ohne Emoji. Dieselben Karten erscheinen im Sammelalbum.
- **Mini-Karte „Wo sind wir?“:** eine schlichte, selbst gezeichnete Karte des alten Israel und seiner Umgebung.
- **„Versteh ich nicht“:** vorab geschriebene Erklärungen pro Abschnitt, keine Live-KI.

## 9. Weiteres

- **Ein-Tipp-Reflexion:** Auswahl-Chips wie „hat mich getröstet“, „fordert mich heraus“, „verstehe ich noch nicht“ oder „will ich mir merken“, optional mit eigenem Text. Alles wird in einem privaten Tagebuch gesammelt.
- **Lieblingsverse speichern** (ohne Hintergrundbild-Funktion).
- **Freies Lesen** in der ganzen Bibel mit Fokusmodus und Systemstimme, ohne Quiz.
- **Anzeige:** Schriftgröße, Zeilenabstand, gut lesbare Schrift (z. B. Atkinson Hyperlegible), Dunkelmodus; alles umschaltbar.
- **Ruhiger Modus:** keine Animationen, kein Ton.

## 10. Später / bewusst nicht in Version 1

| Funktion | Status |
|---|---|
| Gruppenfunktion und gemeinsam lesen (Jugendgruppe, anonymisiert) | **später**, braucht einen sicheren Server |
| Homescreen-Widget mit einer tiefen Grundfrage | später |
| Moderne Übersetzung | später, über API oder Lizenz |
| Weitere Pläne (Psalmen, Amos, Hosea, Jesaja, Prediger, Bergpredigt …) | laufend, mit dem Skill |
| Spaziergang-Modus (nur Audio), Fortschrittsbalken, Level/Titel, Emoji-Rätsel | **nein** |

## 11. Technik

- **Kotlin + Jetpack Compose (Material 3)**, minSdk 26. Die Versionen stammen aus dem funktionierenden `cardManager`-Projekt (AGP 9.4.1, Kotlin 2.4.21, Compose BOM 2026.09.00).
- **Room** für Fortschritt, Antworten, Wiederholungs-Queue, Karten, Tagebuch und Favoriten; **DataStore** für Einstellungen.
- **Inhalte** liegen als JSON in `assets/`: der Bibeltext pro Buch und die Lesepläne. Audio-Pakete (Ogg Opus) liegen pro Leseplan in `assets/audio/`.
- **Erinnerungen** über AlarmManager und Notifications mit Aktionsknöpfen; eine Neuplanung nach einem Neustart ist vorgesehen.
- **Media3 (ExoPlayer)** für die Audios; Android `TextToSpeech` als Ersatz.
- **Komplett offline**, kein Tracking, keine Konten.
- **Verteilung** zunächst als APK für den privaten Gebrauch.

## 12. Etappen

| Etappe | Inhalt | Ergebnis |
|---|---|---|
| **M1** | Grundgerüst, Bibeltext, Session-Ablauf, Lesen inkl. Fokusmodus, alle Quiz-Typen, Senfkorn, Stoppsignal, Skill und **Habakuk** als ersten Plan | Ein Plan ist komplett durchspielbar |
| **M2** | **Die große Geschichte**, Planauswahl (Richtungen), Karten, Sammelalbum, Mini-Karte, „Versteh ich nicht“, Rückblicke | Das Kernerlebnis steht |
| **M3** | Erinnerungen (Quiz in der Benachrichtigung), Anker, Plan B, Lernen, Wiederholung, Wochenziel, Wiedereinstieg, Energie-Check, Nicht stören | Hilfe beim Dranbleiben |
| **M4** | Audios einbinden, **Markus**, Reflexion, Tagebuch, Favoriten, freies Lesen, Merkvers-Spiel, Einstellungen | Version 1 komplett |

## 13. Noch offen

- **App-Name:** „Manna“ ist ein Vorschlag.
- **Markus komplett (ca. 80 Abschnitte) oder als „Best of“?** Empfehlung: komplett, weil Markus kurz und durchgehend erzählend ist.

## 14. Ideen für weitere Lesepläne (zur späteren Besprechung)

Vom Nutzer am 16.11.2026 vorgeschlagen, noch nicht entschieden:

- **Der Himmel** – was die Bibel über Himmel, Ewigkeit und neue Schöpfung sagt (und was nicht).
- **Rechtfertigung vor Gott** – wie wird der Mensch vor Gott gerecht? (Abraham, Habakuk 2,4, Römer, Galater, Jakobus; mit fairer Darstellung der konfessionellen Unterschiede, vgl. Gemeinsame Erklärung 1999).
- **Die unsichtbare Welt** – Details der geistlichen Welt, z. B. die Sicht von Dr. Michael Heiser („The Unseen Realm“: himmlischer Rat, Söhne Gottes, Mächte und Gewalten). Achtung: eine bestimmte wissenschaftliche Deutung – im Plan als solche kennzeichnen und andere Sichtweisen nennen.
- **Bibel im Alltag** – Lesepläne zu sehr relevanten modernen Lebensbereichen mit praktischer Anwendung (z. B. Arbeit, Geld, Beziehungen, Social Media, Angst, Erschöpfung, Konflikte).

### Entscheidung vom 16.11.2026: Plan-Katalog Runde 2

Drei neue Richtungen: **Glauben verstehen**, **Schwierige Fragen**, **Leben**.

Aufgenommen (Reihenfolge offen, außer den nächsten vier): Wie liest man die Bibel?, Gottes Bünde, Warum das Kreuz?, Rechtfertigung, Dreieinigkeit, Heiliger Geist, Gemeinde, Himmel/Tod/neue Schöpfung, Gericht und Hölle, Offenbarung, Unsichtbare Welt, Texte die man lieber überspringt, Gewalt im AT, Texte des Schreckens, Macht und Missbrauch, Wenn die Seele nicht mehr kann, Klagelieder, Körper/Liebe/Sexualität, Sabbat/Ruhe, Vergebung, Bibel im Alltag (Reihe von Mini-Plänen), Christ und Staat, Fremde und Flüchtlinge, Schöpfung bewahren, Die vergessenen Frauen. Nicht aufgenommen: „Jesus war Jude“ als eigener Plan.

Als Nächstes: **Wie liest man die Bibel?**, **Texte, die man lieber überspringt**, **Die Offenbarung ohne Angst**, **Die unsichtbare Welt**.

**Neue Idee (16.11.2026, Nutzer):** Plan **„Mit Gott leben“** (Richtung Leben): biblisch erarbeiten, wie (Alltags-)Leben und Beziehung mit Gott aussehen kann, soll oder muss – was Gott wichtig ist, was Menschen ausmacht, die „Freunde Gottes“ genannt werden (Abraham, Mose, die Jünger in Joh 15). Ziel: ein Gefühl dafür bekommen, wie man mit Gott in Beziehung lebt. Nur Bibeltext; Karten und Erklärungen führen zum Text hin, geben Kontext und stellen Fragen – kein Predigen.

**Endzeit:** Die Leser kommen in der Regel mit einer dispensationalistischen Sicht. Das ist ihr Vorwissen, nicht die Sicht, die der Plan vertritt. Ziel ist, andere Verständnisse kennenzulernen, besonders den Amillenialismus (daneben historischer Prämillenialismus, Postmillenialismus, Präterismus). Der Plan zeigt, wo die vertraute Sicht eine Deutung ist, und stellt die anderen fair und gründlich daneben.

**Ton (Nutzerwunsch):** nicht predigen. Karten, Erklärungen und Fragen vermitteln nichts, was man nicht selbst im Text finden kann. Gute Fragen zum Text stellen, sachliche Informationen geben, wo sie helfen, keine Bedeutung nahelegen, die nicht eindeutig im Text steht. Die Verständnisarbeit macht der Leser.

**Sichtweisen:** Die Pläne sind für Gläubige. Gezeigt wird, wie andere Gläubige und Traditionen einen Text verstehen. Die historisch-kritische Sicht wird nicht als eigene Position dargestellt.
