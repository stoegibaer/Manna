# Auftrag für Claude Code auf dem LLM-Server: Vorlese-Audios erzeugen

> Diesen gesamten Text (ab „Prompt“) in Claude Code auf dem LLM-Server einfügen.
> Die Eingabedatei `tts_input.json` erzeugt das BibleApp-Projekt (`tools/export_tts_input.py`, folgt in Etappe M4) und kopierst du vorher auf den Server.

---

## Prompt

Ich entwickle eine Android-Bibel-App für Menschen mit ADHS. Die App liest Bibeltexte vor und markiert dabei den aktuellen Vers. Du sollst auf diesem Server mit der **besten hier verfügbaren deutschen TTS-Stimme** die Audiodateien dafür erzeugen. Welche TTS-Software installiert ist, ändert sich oft. Schau also selbst nach, was vorhanden ist und funktioniert, und wähle das Beste für natürliches Deutsch. Der Text ist die Elberfelder Bibel von 1905 und gemeinfrei.

### Eingabe
Die Datei `tts_input.json` hat dieses Format:
```json
{
  "translation": "elb1905",
  "items": [
    { "id": "35_001_001", "text": "Der Ausspruch, welchen Habakuk, der Prophet, geschaut hat.", "book": 35, "chapter": 1, "verse": 1 }
  ],
  "lexicon": { "Habakuk": "Ha-ba-kuk", "Chaldäer": "Kal-dä-er" }
}
```
- Jedes Item ist **genau ein Bibelvers**. Die `id` lautet `<Buch 2-stellig>_<Kapitel 3-stellig>_<Vers 3-stellig>`, wobei Buch 1–66 der evangelischen Reihenfolge folgt.
- Der Text ist bereits bereinigt. Versnummern und Überschriften werden **nicht** vorgelesen.
- `lexicon` enthält Ausspracheregeln für biblische Namen und Fremdwörter (auch aramäische Zitate wie „Talitha kumi“ oder „Eloi, Eloi, lama sabachthani“). Setze sie so um, wie es die gewählte Engine erlaubt (Phoneme, SSML oder eine phonetische Umschreibung nur für die Synthese). Ergänze die Liste, wenn dir weitere Wörter auffallen, die falsch ausgesprochen werden, und liefere die ergänzte Liste mit zurück.

### Anforderungen an die Stimme
- **Eine einzige, gleichbleibende Stimme** für alle Verse, ruhig, warm und natürlich. Bitte nicht theatralisch, nicht predigthaft und kein Nachrichtensprecher-Ton.
- Normales Lesetempo (ca. 140–160 Wörter pro Minute) mit natürlicher Betonung, auch bei wörtlicher Rede in Anführungszeichen.
- Alte Schreibweisen wie „daß“, „Weib“, „verdolmetscht“ oder „Jesaias“ ganz normal aussprechen.

### Ausgabe
- Ordner `out/<translation>/` mit **einer Datei pro Vers**: `out/elb1905/<id>.ogg`.
- Format **Ogg Opus, mono, 48 kHz, ca. 32 kbit/s**.
- **Lautheit** auf ca. −16 LUFS integriert normalisieren (True Peak ≤ −1,5 dBTP), z. B. per `ffmpeg loudnorm` in zwei Durchgängen.
- **Stille** am Anfang und Ende auf ca. 80–120 ms kürzen. Die App setzt die Pausen zwischen den Versen selbst.
- Datei `out/<translation>/manifest.json`:
```json
{
  "translation": "elb1905",
  "engine": "<Software + Modell + Version>",
  "voice": "<Stimmenname/-ID>",
  "generated": "<ISO-Datum>",
  "items": {
    "35_001_001": {
      "file": "35_001_001.ogg",
      "duration_ms": 4210,
      "words": [ { "w": "Der", "start_ms": 90, "end_ms": 240 } ]
    }
  }
}
```
  - `words` (Zeitstempel pro Wort) ist **optional**. Liefere sie, wenn die Engine sie mitliefert oder wenn eine Ausrichtung zwischen Audio und Text (z. B. WhisperX oder ein anderes Alignment-Verfahren) zuverlässig klappt. Sonst lass das Feld weg.

### Ablauf
1. **Zuerst nur 3 Probe-Verse** erzeugen: `35_001_002`, `35_003_017` und einen Vers mit wörtlicher Rede. Zeig mir, wo die Dateien liegen, und **warte auf mein OK zur Stimme**, bevor du alles erzeugst.
2. Das Skript soll **fortsetzbar** sein: Bereits erzeugte Dateien werden übersprungen. Ein Abbruch darf keine kaputten Dateien hinterlassen, also zuerst in eine temporäre Datei schreiben und dann umbenennen.
3. **Qualitätsprüfung:** Falls Whisper oder ein anderes Spracherkennungsmodell verfügbar ist, transkribiere jede Datei zurück und vergleiche sie mit dem Text. Verse mit deutlicher Abweichung (z. B. Wortfehlerrate über 15 %), abgeschnittenen Enden, Wiederholungen oder Halluzinationen werden automatisch bis zu 2-mal neu erzeugt. Was danach noch auffällig ist, kommt in `out/<translation>/report.md` (ID, Text, Transkript, Problem).
4. Am Ende erstellst du ein Archiv `tts_<translation>_<Datum>.tar.gz` mit `out/`, der ergänzten Lexikon-Liste und dem Report.
5. Leg das Skript inklusive kurzer README (verwendete Engine, Aufruf, Abhängigkeiten) in einem eigenen Ordner ab, damit ich es später für neue Lesepläne wieder laufen lassen kann. Bei neuen Lieferungen soll es mit derselben Stimme dazu passend weiter erzeugen.

### Zusammenfassung am Schluss
Nenne mir:
- die verwendete Engine und Stimme
- Anzahl erzeugter Verse, Gesamtdauer und Gesamtgröße
- ob Wort-Zeitstempel dabei sind
- wie viele Verse im Report stehen
- den Pfad zum Archiv
