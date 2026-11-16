#!/usr/bin/env python3
"""Source for the reading plan "Die große Geschichte" (generates assets/plans/grosse-geschichte.json).

Edit here, then: python3 -I tools/plans/grosse_geschichte.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/grosse-geschichte.json --review
"""
import json, pathlib

def R(b, c, f, t=None): return {"book": b, "chapter": c, "from": f, "to": t or f}
def choice(q, options, verse=None, hint=None, explain=""):
    d = {"type": "choice", "q": q, "options": options, "answer": 0, "explain": explain}
    if hint: d["hint"] = hint
    if verse: d["verse"] = verse
    return d
def tf(q, answer, verse=None, hint=None, explain=""):
    d = {"type": "truefalse", "q": q, "answer": answer, "explain": explain}
    if hint: d["hint"] = hint
    if verse: d["verse"] = verse
    return d
def who(quote, ref, options, explain, hint="Wer spricht hier mit wem?"):
    return {"type": "whosaid", "quote": quote, "quote_ref": ref, "options": options, "answer": 0, "hint": hint, "explain": explain}
def order(q, items, explain, hint="Lies den Abschnitt noch einmal von oben."):
    return {"type": "order", "q": q, "items": items, "hint": hint, "explain": explain}
def error(text, fix, verse, explain, hint=None):
    return {"type": "error", "q": "Finde den Fehler in der Nacherzählung.", "text": text, "fix": fix, "verse": verse,
            "hint": hint or f"Lies Vers {verse}.", "explain": explain}
def estimate(q, lo, hi, answer, unit, explain, verse=None, hint=None, tol=0):
    d = {"type": "estimate", "q": q, "min": lo, "max": hi, "answer": answer, "tolerance": tol, "unit": unit, "explain": explain}
    if hint: d["hint"] = hint
    if verse: d["verse"] = verse
    return d
def E(q, a, translation=None):
    d = {"q": q, "a": a}
    if translation: d["translation"] = translation
    return d
def MV(ref, text): return {"ref": ref, "text": text}

CARDS = [
    ("adam-eva", "person", "Adam und Eva", "Die ersten Menschen der Bibel. „Adam“ heißt auf Hebräisch einfach „Mensch“ und klingt an „adama“ (Erdboden) an; „Eva“ (Chawwa) erinnert an „Leben“. Ihre Geschichte erzählt, wer der Mensch ist: Gottes Ebenbild – und einer, der sich von Gott abwendet.", "1Mo 1–3"),
    ("noah", "person", "Noah", "Er findet Gnade vor Gott, als die Welt voller Gewalt ist. Nach der Flut schließt Gott mit ihm und allem Leben einen Bund: Nie wieder soll eine Flut alles vernichten. Das Zeichen dafür ist der Bogen in den Wolken.", "1Mo 6–9"),
    ("bund", "begriff", "Bund", "Eine feste, verbindliche Beziehung, die Gott mit Menschen eingeht – mit Noah, Abraham, Israel am Sinai, David. Die Propheten kündigen einen „neuen Bund“ an (Jer 31). Jesus nimmt das beim letzten Mahl auf. „Testament“ ist das lateinische Wort für Bund.", "1Mo 9; 2Mo 19–24; Jer 31,31"),
    ("abraham", "person", "Abraham", "Stammvater Israels, zuerst Abram genannt. Auf Gottes Wort hin verlässt er seine Heimat und vertraut einer Zusage, deren Erfüllung er selbst kaum erlebt. Juden, Christen und Muslime berufen sich auf ihn.", "1Mo 12–25"),
    ("jakob", "person", "Jakob / Israel", "Enkel Abrahams. Ein Mensch mit Ecken: Er betrügt seinen Bruder Esau und wird selbst betrogen. Am Jabbok ringt er mit Gott und erhält den Namen Israel. Seine zwölf Söhne werden die Stammväter der zwölf Stämme.", "1Mo 25–50"),
    ("josef", "person", "Josef", "Lieblingssohn Jakobs, von seinen Brüdern als Sklave nach Ägypten verkauft. Dort steigt er zum zweitmächtigsten Mann des Landes auf und rettet in einer Hungersnot seine Familie. Seine Geschichte zeigt, wie Gott aus Bösem Gutes machen kann.", "1Mo 37–50"),
    ("mose", "person", "Mose", "Als Säugling vor dem Tod gerettet, wächst er am Hof des Pharao auf. Gott beruft ihn am brennenden Dornbusch, Israel aus der Sklaverei zu führen. Am Sinai empfängt er die Gebote. Das versprochene Land sieht er nur noch von fern.", "2Mo – 5Mo"),
    ("zehn-worte", "begriff", "Die Zehn Worte", "Die Zehn Gebote, auf Hebräisch „die zehn Worte“ (daher „Dekalog“). Sie beginnen nicht mit einer Forderung, sondern mit einer Erinnerung: Gott hat sein Volk aus der Sklaverei befreit. Sie stehen zweimal in der Bibel.", "2Mo 20,1–17; 5Mo 5,6–21"),
    ("david", "person", "David", "Hirtenjunge aus Bethlehem, später König Israels (um 1000 v. Chr.) und Dichter vieler Psalmen. Er macht Jerusalem zur Hauptstadt. Die Bibel zeigt ihn mit großen Stärken und schwerer Schuld. Gott verspricht ihm einen Nachkommen, dessen Herrschaft kein Ende hat.", "1Sam 16 – 1Kön 2"),
    ("messias", "begriff", "Messias / Christus", "Hebräisch „Maschiach“, griechisch „Christos“: der Gesalbte. Gesalbt wurden Könige und Priester. Nach dem Ende des Königtums hofften viele auf einen kommenden König aus Davids Familie. Christen bekennen Jesus als diesen Messias – daher der Name „Christus“.", "2Sam 7; Jes 9; Mk 8,29"),
    ("elia", "person", "Elia", "Prophet im Nordreich Israel (9. Jh. v. Chr.) unter König Ahab und Königin Isebel. Er kämpft gegen die Verehrung des Gottes Baal. Nach seinem größten Sieg bricht er zusammen und will sterben – und Gott begegnet ihm ganz leise.", "1Kön 17 – 2Kön 2"),
    ("exil", "ereignis", "Das Babylonische Exil", "587/586 v. Chr. erobern die Babylonier Jerusalem, zerstören den Tempel und verschleppen viele Menschen nach Babylon. Rund 50 Jahre später erlaubt der Perserkönig Kyrus die Rückkehr. In dieser Krise wurden viele Texte der Bibel gesammelt und neu gelesen.", "2Kön 25; Ps 137; Esra 1"),
    ("reich-gottes", "begriff", "Reich Gottes", "Das zentrale Thema der Predigt Jesu. Gemeint ist kein Gebiet, sondern Gottes Herrschaft: wo Gott regiert, wird das Leben heil. Mit Jesus ist es angebrochen und doch noch nicht vollendet. Matthäus sagt meist „Reich der Himmel“ – aus Ehrfurcht vor dem Wort „Gott“.", "Mk 1,15; Mt 5,3"),
    ("petrus", "person", "Petrus", "Fischer vom See Genezareth, eigentlich Simon. Jesus nennt ihn Petrus, „Fels“. Er bekennt Jesus als Messias, verleugnet ihn aber in der Nacht der Verhaftung dreimal. Nach Ostern wird er Sprecher der ersten Gemeinde. Nach alter Überlieferung starb er in Rom.", "Mk 1,16; Joh 21; Apg 2"),
    ("kreuz", "ereignis", "Die Kreuzigung", "Die grausamste römische Hinrichtungsart, vor allem für Sklaven und Aufständische. Jesus wurde um das Jahr 30 n. Chr. unter dem Statthalter Pontius Pilatus vor Jerusalem gekreuzigt. Für Christen ist das Kreuz zum Zeichen geworden, dass Gott selbst Leid und Schuld trägt.", "Mk 15; Lk 23"),
    ("auferstehung", "ereignis", "Die Auferstehung", "Am dritten Tag nach der Kreuzigung finden Frauen das Grab leer; danach begegnet der Auferstandene vielen Jüngern. Für die ersten Christen ist das der Kern des Glaubens (1Kor 15,3–8). Gefeiert wird es an Ostern – und an jedem Sonntag.", "Lk 24; 1Kor 15"),
    ("heiliger-geist", "begriff", "Heiliger Geist", "Gottes Gegenwart und Kraft, die Menschen erfüllt und verändert. Schon am Anfang schwebt Gottes Geist über dem Wasser (1Mo 1,2). Jesus verspricht ihn seinen Jüngern; an Pfingsten kommt er auf sie. Christen bekennen ihn als dritte Person des dreieinigen Gottes.", "1Mo 1,2; Apg 1,8; Apg 2"),
    ("pfingsten", "ereignis", "Pfingsten", "Ursprünglich das jüdische Wochenfest (Schawuot), 50 Tage nach Passa – „Pfingsten“ kommt vom griechischen „pentekoste“, der fünfzigste. An diesem Fest kommt der Heilige Geist auf die Jünger. Es gilt als Geburtstag der Kirche.", "Apg 2"),
    ("paulus", "person", "Paulus", "Jüdischer Gelehrter aus Tarsus, zuerst Verfolger der Christen. Nach seiner Begegnung mit dem Auferstandenen vor Damaskus wird er zum wichtigsten Missionar der frühen Kirche. 13 Briefe im Neuen Testament tragen seinen Namen; bei einigen ist umstritten, ob er sie selbst schrieb.", "Apg 9; Röm; 1Kor"),
    ("neue-schoepfung", "begriff", "Neue Schöpfung", "Das Ziel der großen Geschichte: Gott macht Himmel und Erde neu und wohnt selbst bei den Menschen. Die Bibel endet, wo sie begann – mit einem Baum des Lebens und einem Strom (Offb 22,1–2) –, aber jetzt in einer Stadt voller Menschen.", "Jes 65,17; Offb 21–22"),
]

STAGES = [("anfang", "Der Anfang"), ("verheissung", "Die Verheißung"), ("befreiung", "Befreiung und Bund"), ("koenige", "Könige"),
          ("exil", "Propheten und Exil"), ("jesus", "Jesus"), ("kreuz", "Kreuz und Auferstehung"), ("gemeinde", "Die Gemeinde und das Ziel")]

S = []
def sec(stage, refs, title, summary, quiz, explain, **kw):
    d = {"id": f"gg-{len(S) + 1:02d}", "stage": stage, "refs": refs, "title": title, "summary": summary}
    for k in ("bridge", "place", "focus"):
        if k in kw: d[k] = kw.pop(k)
    d["quiz"] = quiz
    d["explain"] = explain
    d.update(kw)
    S.append(d)

# ───────────────────────── 1 · Der Anfang ─────────────────────────
sec("anfang", [R(1, 1, 1, 5), R(1, 1, 26, 31)], "Am Anfang",
    "Gott schafft durch sein Wort Licht aus der Finsternis. Den Menschen schafft er als sein Bild – Mann und Frau – und am Ende ist alles sehr gut.",
    bridge="Die Bibel ist eine Bibliothek aus 66 Büchern, geschrieben über mehr als tausend Jahre. Und doch erzählt sie eine zusammenhängende Geschichte. Sie beginnt ganz am Anfang.",
    focus="Achte darauf, was Gott über den Menschen sagt – und was über alles am Ende.",
    quiz=[
        choice("Wie schafft Gott in diesen Versen?", ["Er spricht – und es geschieht", "Er kämpft gegen ein Ungeheuer", "Er formt alles aus Lehm", "Er bittet die Engel um Hilfe"],
               3, "Schau, wie Vers 3 beginnt.", "V. 3: Gott spricht, und es wird Licht. Sein Wort genügt."),
        tf("Gott schafft den Menschen als sein Bild – als Mann und Frau.", True, 27, "Lies Vers 27.",
           "V. 27: Beide, Mann und Frau, sind Gottes Ebenbild. Die Würde des Menschen hängt nicht an Geschlecht, Leistung oder Herkunft."),
    ],
    explain=[
        E("Was heißt „Bild Gottes“?", "Im Alten Orient stellten Könige Statuen von sich auf, um zu zeigen: Hier regiere ich. Die Bibel sagt: Jeder Mensch ist so ein Bild – Gottes Stellvertreter in der Welt, mit Würde und Verantwortung für die Schöpfung."),
        E("Sind das sieben echte Tage?", "Darüber denken Christen verschieden. Manche lesen die Schöpfungstage wörtlich als 24-Stunden-Tage (verbreitet in manchen Freikirchen). Viele andere – darunter die katholische Kirche, die meisten evangelischen Landeskirchen und viele Freikirchen – lesen 1. Mose 1 als kunstvoll gebauten Text, der sagt, wer die Welt geschaffen hat und warum, nicht in welcher Zeit. Einig sind sich alle: Die Welt ist kein Zufall, sondern Gottes gute Schöpfung."),
        E("Warum spricht Gott in der Mehrzahl (V. 26)?", "Jüdische Ausleger sehen darin oft eine feierliche Redeform oder Gottes Hofstaat aus Engeln. Christen haben darin seit der Alten Kirche auch einen Hinweis auf den dreieinigen Gott gesehen."),
    ],
    memory_verse=MV(R(1, 1, 27), "Und Gott schuf den Menschen in seinem Bild, im Bild Gottes schuf er ihn"),
    fact="Das hebräische Wort für „schaffen“ (bara) hat in der Bibel immer Gott als Subjekt. Menschen können vieles machen – „schaffen“ in diesem Sinn kann nur Gott.",
    teaser="Ein Garten, zwei besondere Bäume und ein einziges Verbot.",
    prayer={"ref": R(19, 8, 4, 5), "source": "Psalm 8,4–5"})

sec("anfang", [R(1, 2, 7, 9), R(1, 2, 15, 18), R(1, 2, 21, 25)], "Der Mensch im Garten",
    "Gott formt den Menschen aus Erde und haucht ihm Leben ein. Er gibt ihm einen Garten, eine Aufgabe, ein Verbot – und ein Gegenüber.",
    bridge="Kapitel 2 erzählt die Erschaffung des Menschen ein zweites Mal – diesmal ganz nah, wie mit Gottes eigenen Händen.",
    quiz=[
        error("Gott setzte den Menschen in den Garten Eden, um ihn zu bebauen und zu [beherrschen].", "bewahren", 15,
              "V. 15: bebauen und bewahren – der Mensch soll den Garten pflegen und schützen, nicht ausbeuten."),
        choice("Was ist laut Gott „nicht gut“?", ["Dass der Mensch allein ist", "Dass der Mensch vom Baum isst", "Dass der Garten keine Mauer hat", "Dass die Tiere keine Namen haben"],
               18, "Vers 18.", "V. 18: Zum ersten Mal ist etwas nicht gut: das Alleinsein. Der Mensch ist auf Beziehung hin geschaffen."),
    ],
    explain=[
        E("Warum aus Staub?", "Im Hebräischen ein Wortspiel: „Adam“ (Mensch) wird aus der „adama“ (Erdboden) geformt. Der Mensch gehört zur Erde – und lebt doch erst durch Gottes Atem (V. 7)."),
        E("Was heißt „Hilfe“ hier?", "Das hebräische Wort „ezer“ meint keine untergeordnete Gehilfin. Es wird sonst oft für Gott selbst gebraucht, der Israel hilft (z. B. Ps 121,1–2). Gemeint ist ein Gegenüber auf Augenhöhe."),
        E("Welche zwei Bäume stehen in der Mitte?", "Der Baum des Lebens und der Baum der Erkenntnis des Guten und Bösen (V. 9). „Gut und Böse erkennen“ meint wohl: selbst bestimmen wollen, was gut ist – unabhängig von Gott."),
    ],
    cards=["adam-eva"],
    fact="Wo Eden lag, weiß niemand. 1. Mose 2 nennt vier Flüsse, darunter Euphrat und Tigris – das weist nach Mesopotamien, in den heutigen Irak.",
    teaser="Die erste Frage, die in der Bibel gestellt wird, kommt nicht von Gott.")

sec("anfang", [R(1, 3, 1, 13)], "Der Bruch",
    "Die Schlange sät Misstrauen gegen Gott. Die Menschen essen vom verbotenen Baum, verstecken sich – und schieben die Schuld weiter.",
    focus="Achte darauf, wie sich die Beziehungen verändern – zu Gott und untereinander.",
    quiz=[
        who("Hat Gott wirklich gesagt", R(1, 3, 1), ["Die Schlange", "Die Frau", "Adam", "Gott"],
            "V. 1: Die erste Frage der Bibel stellt die Schlange – und sie zielt auf Misstrauen gegenüber Gott.", "Wer beginnt das Gespräch?"),
        order("In welcher Reihenfolge passiert es?",
              ["Die Schlange stellt Gottes Wort in Frage", "Die Frau isst und gibt dem Mann", "Sie merken, dass sie nackt sind", "Sie verstecken sich vor Gott", "Gott ruft: Wo bist du?"],
              "V. 1–9: Vom Zweifel zum Essen, von der Scham zum Verstecken – und dann sucht Gott den Menschen."),
        choice("Wie antworten Adam und die Frau auf Gottes Fragen?", ["Jeder schiebt die Schuld weiter", "Sie bitten sofort um Vergebung", "Sie schweigen", "Sie laufen aus dem Garten"],
               12, "Vers 12–13.", "V. 12–13: Der Mann zeigt auf die Frau (und auf Gott, der sie ihm gegeben hat), die Frau auf die Schlange."),
    ],
    explain=[
        E("Wer ist die Schlange?", "Der Text sagt nur: ein Tier, listiger als alle anderen. Spätere Texte deuten sie auf den Teufel (z. B. Offb 12,9). Auffällig: Die Bibel erklärt nicht, woher das Böse kommt – sie zeigt, wie es wirkt."),
        E("Wie verstehen das verschiedene Kirchen?", "Die westlichen Kirchen (katholisch und evangelisch) sprechen von „Erbsünde“: Seit diesem Bruch ist jeder Mensch von der Sünde geprägt und kann sich nicht selbst befreien. Die orthodoxe Kirche spricht lieber von „Ursünde“: Wir erben nicht Adams Schuld, wohl aber die Folgen – Sterblichkeit und eine Neigung zum Bösen. Einig sind sich alle: Der Mensch braucht Gottes Hilfe."),
        E("Warum fragt Gott „Wo bist du?“", "Gott weiß, wo der Mensch ist. Die Frage ist eine Einladung, sich zu zeigen und ehrlich zu werden – der erste Schritt zurück."),
    ],
    teaser="Gott spricht ein Urteil – und tut danach etwas Überraschendes für die beiden.")

sec("anfang", [R(1, 3, 14, 24)], "Draußen vor dem Garten",
    "Die Folgen: Mühe, Schmerz, ein gestörtes Miteinander und der Tod. Doch Gott macht den Menschen Kleider – und kündigt an, dass die Schlange nicht das letzte Wort behält.",
    quiz=[
        choice("Was tut Gott, bevor er die Menschen aus dem Garten schickt?", ["Er macht ihnen Kleider aus Fell", "Er nimmt ihnen die Sprache", "Er verflucht die Frau", "Er baut ihnen ein Haus"],
               21, "Vers 21.", "V. 21: Gott selbst kleidet sie – ein Zeichen der Fürsorge mitten im Gericht."),
        tf("Gott verflucht in diesem Abschnitt Adam und Eva selbst.", False, 17, "Wer oder was genau wird verflucht (V. 14 und 17)?",
           "V. 14 und 17: Verflucht werden die Schlange und der Erdboden – nicht die Menschen."),
    ],
    explain=[
        E("Was bedeutet Vers 15?", "Zwischen den Nachkommen der Frau und der Schlange soll Feindschaft sein; einer wird der Schlange den Kopf zertreten. Christen haben das seit der Alten Kirche als erste Ankündigung des Siegs Jesu über das Böse gelesen („Protevangelium“). Jüdische Ausleger lesen es meist allgemeiner: als dauernden Kampf des Menschen mit dem Bösen."),
        E("Ist das eine Strafe für alle Zeit?", "V. 16–19 beschreiben, wie die Welt nun ist: mühsam, schmerzvoll, mit Machtgefällen zwischen Mann und Frau. Viele Ausleger betonen: Das beschreibt die gebrochene Welt – es schreibt sie nicht als Gottes Ideal vor."),
        E("Warum die Cherubim?", "Cherubim sind himmlische Wächterwesen. Sie bewachen den Weg zum Baum des Lebens (V. 24). Der Weg zurück ist versperrt – ab jetzt erzählt die Bibel, wie Gott selbst einen neuen Weg öffnet. Ganz am Ende taucht der Baum des Lebens wieder auf (Offb 22,2)."),
    ],
    teaser="Die Menschheit gerät aus den Fugen – und Gott ist darüber nicht kalt, sondern im Herzen getroffen.")

sec("anfang", [R(1, 6, 5, 8), R(1, 9, 11, 16)], "Neuanfang mit Noah",
    "Gott sieht die Bosheit der Menschen, und es schmerzt ihn. Er rettet Noah durch die Flut und schließt danach einen Bund mit allem Leben: Nie wieder eine Flut. Das Zeichen ist der Bogen in den Wolken.",
    bridge="Außerhalb des Gartens geht es bergab: Kain erschlägt seinen Bruder Abel, und die Gewalt breitet sich aus (1. Mose 4–6).",
    quiz=[
        error("Das Zeichen des Bundes ist ein [Stern] in den Wolken.", "Bogen", 13, "9,13: Gott setzt seinen Bogen in die Wolken.", "Lies Vers 13 in Kapitel 9."),
        tf("Gott reagiert auf die Bosheit der Menschen mit kalter Gleichgültigkeit.", False, 6, "Lies Vers 6 in Kapitel 6.",
           "6,6: Es reut Gott, und es schmerzt ihn bis ins Herz. Die Bibel zeigt einen Gott, der leidet, wenn Menschen Böses tun."),
        choice("Mit wem schließt Gott nach der Flut seinen Bund?", ["Mit Noah, seinen Nachkommen und allen Lebewesen", "Nur mit Noah", "Nur mit Israel", "Mit den Engeln"],
               12, "Lies 9,12–16.", "9,12–16: Der Bund gilt Noah, seinen Nachkommen und allen Lebewesen auf der Erde."),
    ],
    explain=[
        E("Ist die Flut eine historische Geschichte?", "Flutgeschichten gibt es in vielen Kulturen des Alten Orients, etwa im babylonischen Gilgamesch-Epos. Manche Christen lesen die Sintflut als weltweites historisches Ereignis, andere als Erinnerung an eine regionale Katastrophe oder als theologische Erzählung. Die Bibel setzt einen eigenen Akzent: Gott leidet am Bösen – und bindet sich danach selbst mit einem Versprechen."),
        E("Was ist ein Bund?", "Eine feste, verbindliche Beziehung mit Zusagen. Hier verpflichtet sich Gott einseitig, ohne Bedingungen. Der Bogen erinnert nicht die Menschen, sondern Gott selbst an sein Versprechen (9,15–16)."),
    ],
    cards=["noah", "bund"],
    fact="Das hebräische Wort für den Regenbogen (qeschet) ist dasselbe wie für den Kriegsbogen. Manche Ausleger sehen darin ein Bild: Gott hängt seine Waffe an den Himmel.",
    teaser="Einem einzelnen Mann wird ein Satz gesagt, der die ganze Weltgeschichte betreffen soll.")

# ───────────────────────── 2 · Die Verheißung ─────────────────────────
sec("verheissung", [R(1, 12, 1, 9)], "Abraham: Geh!",
    "Gott ruft Abram, alles hinter sich zu lassen, und verspricht: Ich will dich segnen – und durch dich alle Völker. Abram geht nach Kanaan.",
    bridge="Nach der Flut verteilen sich die Völker über die Erde (1. Mose 10–11). Dann richtet sich der Blick auf einen einzigen Mann in der Stadt Haran: Abram.",
    place="sichem",
    focus="Achte darauf, wer am Ende durch Abram gesegnet werden soll.",
    quiz=[
        estimate("Wie alt ist Abram, als er aufbricht?", 20, 120, 75, "Jahre", "V. 4: 75 Jahre – Gott beginnt etwas Neues mit einem Mann, der eigentlich schon alt ist.", 4, "Vers 4 verrät es.", tol=5),
        choice("Wer soll durch Abram gesegnet werden?", ["Alle Geschlechter der Erde", "Nur seine Familie", "Nur die Bewohner Kanaans", "Nur die Könige"],
               3, "Vers 3.", "V. 3: Der Segen ist kein Selbstzweck – durch Abram sollen alle Völker gesegnet werden."),
    ],
    explain=[
        E("Wo liegt Haran?", "Eine Handelsstadt im Norden Mesopotamiens (heute Südosttürkei). Abrams Familie kam ursprünglich aus Ur im Süden (1Mo 11,31). Von Haran nach Kanaan sind es rund 600 Kilometer – mit Herden eine Reise von Wochen."),
        E("Warum baut Abram Altäre?", "Ein Altar war ein Ort der Anbetung und des Opfers. Abram markiert damit: Dieses Land gehört dem Gott, der ihn gerufen hat – obwohl dort noch die Kanaaniter wohnen (V. 6–8)."),
    ],
    cards=["abraham"],
    fact="Juden, Christen und Muslime berufen sich auf Abraham als Stammvater des Glaubens – deshalb spricht man von den „abrahamitischen Religionen“.",
    teaser="Abram wartet und wartet auf den versprochenen Sohn. Dann zeigt Gott ihm den Nachthimmel.")

sec("verheissung", [R(1, 15, 1, 6)], "Zähl die Sterne",
    "Abram klagt: Ich habe kein Kind. Gott führt ihn hinaus unter den Sternenhimmel: So zahlreich werden deine Nachkommen sein. Abram glaubt – und Gott rechnet es ihm als Gerechtigkeit an.",
    bridge="Jahre vergehen. Abram lebt im Land und wird reich – aber er hat noch immer kein Kind.",
    quiz=[
        choice("Was soll Abram zählen?", ["Die Sterne", "Den Sand am Meer", "Seine Herden", "Die Völker der Erde"],
               5, "Vers 5.", "V. 5: Zähl die Sterne, wenn du kannst – so viele werden deine Nachkommen sein."),
        tf("Abram hat keine Zweifel und stellt Gott keine Fragen.", False, 2, "Lies Vers 2–3.",
           "V. 2–3: Abram spricht offen aus, was ihn quält. Glaube und ehrliche Fragen schließen sich in der Bibel nicht aus."),
    ],
    explain=[
        E("Was heißt „zur Gerechtigkeit rechnen“?", "Abram hat nichts geleistet – er vertraut nur Gottes Zusage. Und Gott sagt: Das macht ihn gerecht, also richtig mit Gott verbunden (V. 6). Paulus greift diesen Vers auf (Röm 4,3; Gal 3,6)."),
        E("Wer ist Elieser von Damaskus?", "Ein Verwalter in Abrams Haushalt. Ohne eigenes Kind wäre er nach damaligem Recht der Erbe gewesen (V. 2–3)."),
    ],
    memory_verse=MV(R(1, 15, 6), "Und er glaubte dem HERRN; und er rechnete es ihm zur Gerechtigkeit."),
    teaser="Endlich ist der Sohn da. Und dann verlangt Gott etwas Unbegreifliches.")

sec("verheissung", [R(1, 22, 1, 14)], "Abraham und Isaak",
    "Gott stellt Abraham auf die Probe: Er soll Isaak opfern. Abraham geht – und im letzten Moment hält Gott ihn zurück. Ein Widder wird an Isaaks Stelle geopfert.",
    bridge="Gott hält Wort: Sara bekommt im hohen Alter einen Sohn, Isaak (1. Mose 21). Abram heißt inzwischen Abraham – „Vater vieler Völker“.",
    place="jerusalem",
    focus="Achte auf die Frage, die Isaak unterwegs stellt.",
    quiz=[
        order("Bring die Ereignisse in die richtige Reihenfolge.",
              ["Abraham sattelt früh am Morgen seinen Esel", "Isaak trägt das Holz", "Isaak fragt nach dem Schaf", "Der Engel ruft vom Himmel", "Abraham opfert einen Widder"],
              "V. 3–13."),
        choice("Was antwortet Abraham auf Isaaks Frage nach dem Schaf?", ["Gott wird es sich selbst aussuchen", "Wir kaufen unterwegs eins", "Du bist das Opfer", "Er schweigt"],
               8, "Vers 8.", "V. 8: Gott wird selbst für das Opfer sorgen – und so kommt es auch (V. 13–14)."),
    ],
    explain=[
        E("Wie kann Gott so etwas verlangen?", "Die Geschichte ist eine der schwersten der Bibel. Im Umfeld Israels gab es Kinderopfer; diese Erzählung endet ausdrücklich damit, dass Gott kein Kinderopfer will. Juden nennen sie „Akeda“, die Bindung Isaaks, und lesen sie als Geschichte äußersten Vertrauens. Christen sehen darin auch ein Vorausbild: Gott selbst gibt seinen Sohn (vgl. Röm 8,32)."),
        E("Wo liegt Morija?", "Die Bibel verbindet den Berg Morija später mit dem Tempelberg in Jerusalem (2. Chronik 3,1). Wo Abraham fast seinen Sohn opfert, wird später der Tempel stehen."),
    ],
    fact="Abraham gibt dem Ort einen Namen, der bedeutet: Gott sieht vor, Gott sorgt (V. 14). Das lateinische Wort für „vorhersehen, vorsorgen“ ist „providere“ – daher kommt der Begriff „Providenz“, Vorsehung.",
    teaser="Abrahams Enkel ist ein Betrüger auf der Flucht – und in einer Nacht kämpft er mit einem Unbekannten.")

sec("verheissung", [R(1, 32, 25, 31)], "Jakob ringt mit Gott",
    "In der Nacht vor der Begegnung mit Esau ringt ein Unbekannter mit Jakob bis zum Morgen. Jakob lässt nicht los, bis er gesegnet wird. Er bekommt einen neuen Namen: Israel.",
    bridge="Isaak bekommt Zwillinge, Esau und Jakob. Jakob erschleicht sich den Segen seines Bruders und flieht (1. Mose 27–28). Zwanzig Jahre später kehrt er zurück – und Esau kommt ihm mit 400 Männern entgegen.",
    place="pniel",
    quiz=[
        who("Ich lasse dich nicht los, du habest mich denn gesegnet", R(1, 32, 27), ["Jakob", "Der Unbekannte", "Esau", "Isaak"],
            "V. 27: Jakob, der sich den Segen früher erschlichen hat, bittet jetzt offen darum."),
        choice("Welchen neuen Namen bekommt Jakob?", ["Israel", "Abraham", "Pniel", "Juda"],
               29, "Vers 29.", "V. 29: Israel – sinngemäß „der mit Gott ringt“. Das ganze Volk wird nach ihm benannt."),
    ],
    explain=[
        E("Mit wem ringt Jakob?", "Der Text sagt zuerst: ein Mann (V. 25). Am Ende sagt Jakob, er habe Gott von Angesicht gesehen (V. 31). Hosea 12,4–5 spricht von einem Engel. Die Geschichte lässt das bewusst geheimnisvoll."),
        E("Warum hinkt Jakob danach?", "Die Begegnung mit Gott verändert ihn – sichtbar und für immer. Er geht gesegnet, aber verwundet weiter (V. 32). Viele haben darin ein Bild für echten Glauben gesehen: nicht unverletzt, aber nicht mehr allein."),
    ],
    cards=["jakob"],
    fact="Bis heute trägt der Staat Israel den Namen, den Jakob in dieser Nacht bekommt.",
    teaser="Jakobs Lieblingssohn wird von den eigenen Brüdern verkauft. Jahre später liegt ihr Leben in seiner Hand.")

sec("verheissung", [R(1, 50, 15, 21)], "Josef: Gott wendet es zum Guten",
    "Nach Jakobs Tod fürchten die Brüder Josefs Rache. Josef weint und vergibt: Ihr hattet Böses vor, Gott aber hat es zum Guten gewendet.",
    bridge="Die Brüder verkaufen Josef als Sklaven nach Ägypten. Nach Jahren im Gefängnis wird er dort zum zweitmächtigsten Mann des Landes und rettet in einer Hungersnot auch seine Familie. Jakob zieht mit allen nach Ägypten (1. Mose 37–47).",
    place="aegypten",
    focus="Achte darauf, wie Josef auf die Angst seiner Brüder reagiert.",
    quiz=[
        error("Josef sagt: Ihr hattet Böses gegen mich im Sinn; Gott aber wollte es [bestrafen].", "gut machen", 20,
              "V. 20: Gott hatte im Sinn, es gut zu machen – um viele Menschen am Leben zu erhalten."),
        choice("Was tut Josef, als die Brüder um Vergebung bitten?", ["Er weint und tröstet sie", "Er lässt sie gefangen nehmen", "Er schickt sie zurück nach Kanaan", "Er verlangt eine Entschädigung"],
               17, "Lies Vers 17 und 21.", "V. 17 und 21: Josef weint, beruhigt sie und verspricht, für sie und ihre Kinder zu sorgen."),
    ],
    explain=[
        E("Hat Jakob das wirklich befohlen?", "Davon wird vorher nichts erzählt. Viele Ausleger vermuten, dass die Brüder die Botschaft aus Angst erfunden haben (V. 16–17). Josef geht darauf gar nicht ein – er vergibt trotzdem."),
        E("Heißt das, Gott wollte das Böse?", "Josef sagt nicht, das Böse sei gut gewesen. Die Brüder bleiben verantwortlich. Aber Gott war stärker als ihre Pläne und hat daraus Rettung gemacht."),
    ],
    cards=["josef"],
    teaser="Generationen später ist aus Jakobs Familie ein großes Volk geworden – und Ägypten hat Angst davor.")

# ───────────────────────── 3 · Befreiung und Bund ─────────────────────────
sec("befreiung", [R(2, 3, 1, 14)], "Der brennende Dornbusch",
    "Gott erscheint Mose in einem Dornbusch, der brennt und nicht verbrennt. Er hat das Elend seines Volkes gesehen und schickt Mose zum Pharao. Auf die Frage nach seinem Namen antwortet Gott: Ich bin, der ich bin.",
    bridge="Rund 400 Jahre später: Die Nachkommen Jakobs sind in Ägypten zu einem großen Volk geworden – und der Pharao hat sie zu Sklaven gemacht. Mose, als Baby gerettet und am Hof aufgewachsen, musste nach einem Totschlag fliehen (2. Mose 1–2).",
    place="horeb",
    focus="Achte darauf, was Gott über das Leiden seines Volkes sagt.",
    quiz=[
        who("Wer bin ich, dass ich zu dem Pharao gehen", R(2, 3, 11), ["Mose", "Aaron", "Jethro", "Der Pharao"],
            "V. 11: Mose fühlt sich zu klein für den Auftrag. Gottes Antwort: Ich werde mit dir sein (V. 12)."),
        choice("Was sagt Gott über sein Volk in Ägypten?", ["Er hat ihr Elend gesehen und ihr Schreien gehört", "Sie sind selbst schuld an ihrer Lage", "Sie sollen geduldig bleiben", "Er hat sie vergessen"],
               7, "Vers 7.", "V. 7–8: Gott sieht, hört und kennt ihre Schmerzen – und kommt herab, um sie zu retten."),
    ],
    explain=[
        E("Was bedeutet „Ich bin, der ich bin“?", "Gott nennt seinen Namen JHWH und deutet ihn (V. 14). Das Hebräische lässt mehrere Übersetzungen zu: „Ich bin, der ich bin“, „Ich werde sein, der ich sein werde“ oder „Ich bin da“. Gemeint ist: Gott lässt sich nicht festlegen – aber er ist verlässlich da."),
        E("Warum soll Mose die Schuhe ausziehen?", "Der Ort ist heilig, weil Gott dort ist (V. 5). Schuhe auszuziehen war ein Zeichen der Ehrfurcht – in vielen Kulturen bis heute."),
    ],
    cards=["mose"],
    fact="Der Berg heißt hier Horeb; an anderen Stellen heißt derselbe Berg Sinai. Wo genau er liegt, weiß man nicht.",
    teaser="Das Volk ist frei – und steht nach wenigen Tagen mit dem Rücken zum Meer.")

sec("befreiung", [R(2, 14, 10, 14), R(2, 14, 21, 22), R(2, 14, 30, 31)], "Durchs Meer",
    "Eingeschlossen zwischen Meer und ägyptischem Heer bekommt Israel Panik. Mose sagt: Fürchtet euch nicht – der HERR wird für euch kämpfen. Gott teilt das Meer, und Israel zieht hindurch.",
    bridge="Nach zehn Plagen lässt der Pharao Israel ziehen. In der Nacht des Aufbruchs feiert Israel das erste Passa (2. Mose 5–13). Doch dann bereut der Pharao es und jagt ihnen mit seinem Heer nach.",
    place="schilfmeer",
    quiz=[
        choice("Wie reagiert das Volk, als die Ägypter kommen?", ["Es bekommt Angst und macht Mose Vorwürfe", "Es betet ruhig", "Es greift zu den Waffen", "Es schickt Unterhändler"],
               11, "Lies Vers 10–12.", "V. 10–12: Große Angst – sie wünschen sich sogar zurück in die Sklaverei."),
        error("Mose sagt: Der HERR wird für euch kämpfen, und ihr werdet [laut] sein.", "still", 14,
              "V. 14: Gott kämpft – und das Volk darf still werden."),
        tf("Gott trocknet das Meer mit einem starken Ostwind, die ganze Nacht hindurch.", True, 21, "Lies Vers 21.",
           "V. 21: Gott wirkt durch einen Ostwind, die ganze Nacht lang – ein Wunder mit den Mitteln der Natur."),
    ],
    explain=[
        E("Welches Meer war das?", "Hebräisch heißt es „Jam Suf“, wörtlich „Schilfmeer“. Ob damit ein See im Norden des heutigen Golfs von Suez, ein Seitenarm oder das Rote Meer selbst gemeint ist, ist unsicher."),
        E("Was ist das Passa?", "Das Fest der Befreiung aus Ägypten. In der letzten Nacht vor dem Auszug aß Israel ein Lamm und strich sein Blut an die Türpfosten (2. Mose 12). Juden feiern Passa bis heute – und Jesus stirbt an einem Passafest."),
    ],
    memory_verse=MV(R(2, 14, 14), "Der HERR wird für euch kämpfen, und ihr werdet stille sein."),
    try_="Wenn dir heute etwas über den Kopf wächst: Sag dir Vers 14 einmal halblaut vor.",
    teaser="In der Wüste bekommt das befreite Volk zehn Worte – und das erste ist gar kein Gebot.")

sec("befreiung", [R(2, 20, 1, 17)], "Die Zehn Worte",
    "Gott stellt sich vor als der, der Israel aus der Sklaverei befreit hat. Dann gibt er zehn Worte für ein Leben in Freiheit: Gott allein vertrauen, seinen Namen ehren, ruhen, die Eltern ehren und Leben, Ehe, Eigentum und Wahrheit schützen.",
    bridge="Nach drei Monaten in der Wüste kommt Israel an den Berg Sinai. Gott bietet dem Volk einen Bund an (2. Mose 19).",
    place="horeb",
    focus="Achte auf Vers 2: Was sagt Gott, bevor das erste Gebot kommt?",
    quiz=[
        choice("Womit beginnen die Zehn Worte?", ["Mit der Erinnerung an die Befreiung aus Ägypten", "Mit einer Drohung", "Mit dem Gebot, nicht zu töten", "Mit einer Liste von Opfern"],
               2, "Vers 2.", "V. 2: Erst kommt die Befreiung, dann kommen die Gebote. Sie sind Regeln für Befreite – damit sie nicht wieder unfrei werden."),
        tf("Am Sabbat sollen nur die Israeliten ruhen, Knechte und Fremde aber weiterarbeiten.", False, 10, "Lies Vers 10.",
           "V. 10: Auch Knechte, Mägde, Fremde und sogar die Tiere sollen ruhen. Der Ruhetag schützt die Schwächsten."),
    ],
    explain=[
        E("Warum zählen Kirchen die Gebote unterschiedlich?", "Der Bibeltext nennt keine Nummern. Katholiken und Lutheraner zählen nach Augustinus: Das Bilderverbot gehört zum ersten Gebot, das Begehren wird in zwei Gebote geteilt. Reformierte, Orthodoxe und die meisten Freikirchen zählen das Bilderverbot als eigenes zweites Gebot und das Begehren als eines. Im Judentum gilt schon Vers 2 als erstes „Wort“. Der Inhalt ist überall derselbe."),
        E("Sabbat oder Sonntag?", "Der Sabbat ist der siebte Tag, unser Samstag. Juden halten ihn bis heute. Die meisten Christen feiern seit der frühen Kirche den Sonntag als Tag der Auferstehung Jesu; einige, etwa die Siebenten-Tags-Adventisten, halten am Samstag fest."),
        E("Was heißt „eifernder Gott“?", "Das Wort beschreibt eine leidenschaftliche Liebe, die keine Konkurrenz duldet – wie in einer Ehe. Die Strafe reicht bis ins dritte und vierte Glied, die Güte aber auf Tausende (V. 5–6): Gottes Güte ist viel größer als sein Zorn.", "elbbk"),
    ],
    cards=["zehn-worte"],
    fact="Die Bibel nennt sie nie „die Zehn Gebote“, sondern „die zehn Worte“ (2. Mose 34,28). Daher kommt der Fachbegriff „Dekalog“.",
    teaser="Mose bleibt 40 Tage auf dem Berg. Unten wird das Volk ungeduldig.")

sec("befreiung", [R(2, 32, 1, 8), R(2, 34, 5, 7)], "Das goldene Kalb – und Gottes Name",
    "Während Mose auf dem Berg ist, lässt sich das Volk ein goldenes Kalb machen und bricht den Bund fast sofort. Doch Gott erneuert ihn und zeigt sein Wesen: barmherzig, gnädig, langsam zum Zorn und groß an Güte.",
    bridge="Mose steigt auf den Berg, um von Gott die Gebote auf Steintafeln zu empfangen. Er bleibt vierzig Tage dort (2. Mose 24,18).",
    place="horeb",
    quiz=[
        who("mache uns einen Gott, der vor uns hergehe", R(2, 32, 1), ["Das Volk", "Aaron", "Mose", "Der Pharao"],
            "32,1: Das Volk drängt Aaron. Ohne Mose fühlen sie sich verloren und wollen etwas Sichtbares."),
        choice("Wie beschreibt Gott sich selbst in Kapitel 34?", ["Barmherzig, gnädig und langsam zum Zorn", "Streng und unnahbar", "Gleichgültig gegenüber Schuld", "Gerecht, aber ohne Gnade"],
               6, "Lies 34,6–7.", "34,6–7: Barmherzig und gnädig, langsam zum Zorn, groß an Güte und Treue – und doch nimmt er Schuld ernst. Diese Selbstbeschreibung wird im Alten Testament immer wieder zitiert."),
    ],
    explain=[
        E("Warum ein Kalb?", "Stierbilder waren in Israels Umwelt Symbole für Kraft und Fruchtbarkeit. Bemerkenswert: Aaron ruft ein Fest für den HERRN aus (32,5). Das Volk will Gott nicht ersetzen – es will ihn sichtbar und verfügbar machen. Genau das verbietet das Bilderverbot."),
        E("Was passiert zwischen Kapitel 32 und 34?", "Mose zerbricht die Tafeln, tritt bei Gott für das Volk ein und bittet, Gottes Herrlichkeit sehen zu dürfen (2. Mose 32,19–33,23). Dann schreibt er die Gebote auf zwei neue Tafeln."),
    ],
    memory_verse=MV(R(2, 34, 6), "barmherzig und gnädig, langsam zum Zorn und groß an Güte und Wahrheit"),
    teaser="Vierzig Jahre Wüste später steht Israel an der Grenze des Landes. Mose hält seine letzte Rede.")

sec("befreiung", [R(5, 6, 4, 9), R(5, 30, 15, 20)], "Wähle das Leben",
    "Das Herz des Glaubens Israels: Der HERR ist einer – liebe ihn mit allem, was du hast, und gib es weiter. Am Ende stellt Mose das Volk vor die Wahl: Leben oder Tod, Segen oder Fluch. Wähle das Leben!",
    bridge="Israel bleibt 40 Jahre in der Wüste, bis eine neue Generation herangewachsen ist. In den Ebenen Moabs, kurz vor dem Einzug ins Land, erinnert Mose das Volk an alles, was Gott gesagt hat.",
    place="moab",
    quiz=[
        choice("Womit soll Israel Gott lieben?", ["Mit ganzem Herzen, ganzer Seele und ganzer Kraft", "Vor allem mit Opfern", "Vor allem am Sabbat", "Mit Worten, nicht mit Taten"],
               5, "Lies 6,5.", "6,5: Mit allem, was man ist und hat."),
        tf("Mose sagt: Ob ihr leben werdet, ist reiner Zufall.", False, 19, "Lies 30,19.",
           "30,19: Mose stellt das Volk vor eine echte Entscheidung – und rät eindeutig: Wähle das Leben."),
    ],
    explain=[
        E("Was ist das „Schma Israel“?", "„Höre, Israel“ – hebräisch „Schma Jisrael“. Es ist bis heute das zentrale Bekenntnis des Judentums und wird morgens und abends gebetet. Fromme Juden befestigen diese Worte in einer kleinen Kapsel am Türpfosten (Mesusa) – so wie es 6,9 sagt."),
        E("Kann man Liebe befehlen?", "Im Alten Orient meinte „lieben“ in Verträgen auch: treu sein, sich verbindlich zur Seite stellen. Gemeint ist mehr als ein Gefühl – eine Entscheidung, die das ganze Leben prägt."),
    ],
    memory_verse=MV(R(5, 30, 19), "So wähle das Leben, damit du lebest"),
    fact="Jesus nennt 6,4–5 das wichtigste Gebot – und stellt ein zweites daneben: Liebe deinen Nächsten wie dich selbst (Mk 12,29–31).",
    try_="Schreib dir einen Bibelvers, der dir wichtig ist, auf einen Zettel und kleb ihn an deine Tür oder deinen Spiegel – wie in 6,9.",
    teaser="Israel will einen König wie alle anderen Völker. Gott sucht sich einen aus, den niemand auf dem Zettel hatte.")

# ───────────────────────── 4 · Könige ─────────────────────────
sec("koenige", [R(9, 16, 1, 13)], "David wird gesalbt",
    "Gott schickt den Propheten Samuel nach Bethlehem, um einen Sohn Isais zum König zu salben. Nicht der Älteste und Stattlichste wird es, sondern der Jüngste, der draußen die Schafe hütet: David.",
    bridge="Unter Josua kommt Israel ins Land. Es folgen Jahrhunderte unter „Richtern“, dann will das Volk einen König. Der erste, Saul, scheitert an seinem Ungehorsam (Josua bis 1. Samuel 15).",
    place="bethlehem",
    focus="Achte auf Vers 7: Worauf schaut Gott?",
    quiz=[
        estimate("Wie viele Söhne lässt Isai an Samuel vorbeigehen, bevor David geholt wird?", 1, 12, 7, "Söhne",
                 "V. 10: Sieben Söhne – und keiner ist der Richtige. David, der Jüngste, war nicht einmal eingeladen.", 10, "Vers 10."),
        choice("Worauf sieht Gott laut Vers 7?", ["Auf das Herz", "Auf die Größe", "Auf das Alter", "Auf die Herkunft"],
               7, "Vers 7.", "V. 7: Der Mensch sieht auf das Äußere, Gott aber sieht auf das Herz."),
    ],
    explain=[
        E("Was bedeutet „salben“?", "Öl wurde auf den Kopf gegossen – ein Zeichen, dass Gott jemanden für eine Aufgabe auswählt und ausrüstet. Das hebräische Wort für „Gesalbter“ ist „Maschiach“ – Messias."),
        E("Warum hat Samuel Angst?", "Saul ist noch König. Einen neuen König zu salben, wäre Hochverrat (V. 2). David wird erst viele Jahre später, nach Sauls Tod, wirklich König."),
    ],
    cards=["david"],
    memory_verse=MV(R(9, 16, 7), "der Mensch sieht auf das Äußere, aber der HERR sieht auf das Herz"),
    teaser="David ist König, hat Jerusalem erobert und will Gott ein Haus bauen. Gott dreht den Spieß um.")

sec("koenige", [R(10, 7, 8, 16)], "Ein Haus für immer",
    "Durch den Propheten Nathan sagt Gott: Nicht du baust mir ein Haus – ich baue dir eins. Ein Nachkomme Davids soll regieren, und sein Königtum soll für immer bestehen.",
    bridge="David besiegt Goliat, wird von Saul verfolgt und nach dessen Tod König. Er macht Jerusalem zur Hauptstadt und bringt die Bundeslade dorthin (1. Samuel 17 – 2. Samuel 6). Nun will er Gott einen Tempel bauen.",
    place="jerusalem",
    quiz=[
        error("Gott sagt David: Ich will dir ein [Heer] machen, und dein Thron soll fest sein auf ewig.", "Haus", 11,
              "V. 11 und 16: Gott baut David ein Haus – gemeint ist eine Königsfamilie, eine Dynastie, die nicht endet.", "Lies Vers 11 und 16."),
        tf("Gott verspricht, dass Davids Nachkommen niemals Fehler machen werden.", False, 14, "Lies Vers 14–15.",
           "V. 14–15: Gott rechnet mit Fehlern und wird zurechtweisen – aber seine Güte wird nicht weichen."),
    ],
    explain=[
        E("Wer ist der Nachkomme?", "Zunächst Davids Sohn Salomo, der den Tempel baut. Doch das Königtum endet 587 v. Chr. Darum hofften viele auf einen kommenden Sohn Davids, den Messias. Das Neue Testament sieht diese Zusage in Jesus erfüllt, der „Sohn Davids“ genannt wird."),
        E("Was ist ein „Haus“ hier?", "Das Wort hat zwei Bedeutungen: Gebäude (David will einen Tempel bauen) und Familie (Gott verspricht eine Dynastie). Dieses Wortspiel ist der Kern der Geschichte."),
    ],
    cards=["messias"],
    fact="Das Neue Testament beginnt mit genau diesem Gedanken: Matthäus 1,1 nennt Jesus Christus den „Sohn Davids“.",
    teaser="Der König, dem Gott so viel versprochen hat, wird zum Ehebrecher und Mörder.")

sec("koenige", [R(10, 12, 1, 13)], "„Du bist der Mann!“",
    "Der Prophet Nathan erzählt David von einem Reichen, der einem Armen sein einziges Lamm wegnimmt. David ist empört – und Nathan sagt: Du bist der Mann! David bekennt seine Schuld.",
    bridge="David schläft mit Batseba, der Frau seines Offiziers Uria. Als sie schwanger wird, lässt David Uria gezielt im Krieg sterben (2. Samuel 11).",
    place="jerusalem",
    focus="Achte darauf, wie David auf die Geschichte reagiert, bevor er merkt, dass es um ihn geht.",
    quiz=[
        who("Du bist der Mann", R(10, 12, 7), ["Nathan", "David", "Uria", "Batseba"],
            "V. 7: Nathan hält dem König den Spiegel vor – mit großem Mut. Er hätte dafür sterben können."),
        choice("Was hatte der arme Mann in Nathans Geschichte?", ["Ein einziges kleines Lamm", "Eine kleine Herde", "Einen Weinberg", "Gar nichts"],
               3, "Vers 3.", "V. 3: Ein einziges Lamm, das er liebte wie eine Tochter."),
        tf("David versucht, sich herauszureden.", False, 13, "Lies Vers 13.",
           "V. 13: David bekennt schlicht, dass er gegen Gott gesündigt hat. Und Nathan sagt ihm Vergebung zu."),
    ],
    explain=[
        E("Was hatte David getan?", "Er nahm sich die Frau eines anderen und ließ ihren Mann töten, um es zu vertuschen (2. Samuel 11). Als König hatte er alle Macht – viele Ausleger sprechen deshalb heute von Machtmissbrauch. Die Bibel verschweigt das nicht, auch nicht bei ihrem größten König."),
        E("Warum erzählt Nathan eine Geschichte?", "Eine direkte Anklage hätte David vielleicht abgewehrt. Über den Mann in der Geschichte urteilt er selbst – und spricht so sein eigenes Urteil (V. 5–6)."),
    ],
    teaser="Nach dieser Begegnung entsteht eines der ehrlichsten Gebete der Bibel.")

sec("koenige", [R(19, 51, 3, 14)], "Schaffe mir ein reines Herz",
    "David bittet um Erbarmen, bekennt seine Schuld ohne Ausrede und bittet Gott um ein neues, reines Herz und die Freude, gerettet zu sein.",
    bridge="Die Überschrift von Psalm 51 verbindet ihn mit genau diesem Moment: David, nachdem der Prophet Nathan bei ihm war.",
    place="jerusalem",
    quiz=[
        choice("Worum bittet David vor allem?", ["Um ein reines Herz und einen neuen Geist", "Um den Sieg über seine Feinde", "Dass niemand von seiner Schuld erfährt", "Um ein langes Leben"],
               12, "Vers 12.", "V. 12: Er will nicht nur der Strafe entgehen, sondern innerlich neu werden."),
        tf("David schiebt die Schuld auf andere.", False, 5, "Lies Vers 5–6.",
           "V. 5–6: Er nennt seine Schuld beim Namen. Kein Wort über Batseba oder die Umstände."),
    ],
    explain=[
        E("Was ist Ysop?", "Eine Pflanze, deren Zweige bei Reinigungsriten zum Besprengen dienten (2. Mose 12,22). David bittet: Reinige du mich (V. 9)."),
        E("„In Sünde geboren“ – was heißt Vers 7?", "David sagt: Meine Schuld ist kein Ausrutscher, sie reicht tief. In der westlichen Kirche wurde der Vers zu einem Beleg für die Lehre von der Erbsünde; jüdische und viele andere Ausleger lesen ihn als poetischen Ausdruck tiefer Reue."),
        E("Warum andere Versnummern?", "Deutsche Bibeln zählen die Überschrift eines Psalms mit. Darum steht die Bitte um ein reines Herz hier in Vers 12 – in englischen Bibeln in Vers 10."),
    ],
    memory_verse=MV(R(19, 51, 12), "Schaffe mir, Gott, ein reines Herz, und erneuere in meinem Innern einen festen Geist!"),
    teaser="Nach David zerbricht das Reich. Im Norden kämpft ein Prophet allein gegen alle – und bricht dann zusammen.")

sec("koenige", [R(11, 19, 3, 8), R(11, 19, 11, 13)], "Elia: Es ist genug",
    "Elia flieht in die Wüste, ist am Ende und will sterben. Ein Engel weckt ihn: Steh auf, iss. Am Berg Horeb begegnet ihm Gott – nicht im Sturm, im Erdbeben oder im Feuer, sondern in einem leisen Säuseln.",
    bridge="Nach Salomo zerbricht das Reich in Israel (Norden) und Juda (Süden). Im Norden lässt König Ahab den Gott Baal verehren. Der Prophet Elia tritt ihm entgegen und besiegt auf dem Karmel die Baalspropheten (1. Kön 12–18). Nun will Königin Isebel ihn töten.",
    place="horeb",
    focus="Achte darauf, was Gott zuerst für den erschöpften Elia tut.",
    quiz=[
        who("Es ist genug", R(11, 19, 4), ["Elia", "Der Engel", "Isebel", "Ahab"],
            "V. 4: Elia ist völlig erschöpft und will nicht mehr leben. Die Bibel nimmt das ernst."),
        choice("Was tut der Engel für Elia?", ["Er weckt ihn und gibt ihm Essen und Wasser", "Er tadelt ihn für seine Angst", "Er schickt ihn sofort zurück", "Er nimmt ihn mit in den Himmel"],
               7, "Lies Vers 5–7.", "V. 5–7: Zweimal: Steh auf und iss. Gottes erste Antwort auf Elias Verzweiflung ist Brot, Wasser und Schlaf – keine Predigt."),
        error("Gott war nicht im Wind, nicht im Erdbeben und nicht im Feuer. Danach kam der Ton eines leisen [Donners].", "Säuselns", 12,
              "V. 12: Nach Sturm, Erdbeben und Feuer kommt etwas ganz Leises."),
    ],
    explain=[
        E("Geht es Elia wie bei einer Depression?", "Die Bibel benutzt keine modernen Begriffe. Aber sie beschreibt einen Menschen nach enormer Anspannung, der völlig leer ist, sich wertlos fühlt und sterben will (V. 4). Gott wirft ihm das nicht vor. Wenn es dir selbst so geht: Sprich mit jemandem darüber – mit Freunden, in der Gemeinde, mit Ärzten oder der Telefonseelsorge (0800 111 0 111, kostenlos, rund um die Uhr)."),
        E("Was ist das „leise Säuseln“?", "Wörtlich etwa: „eine Stimme dünnen Schweigens“. Sturm, Erdbeben und Feuer waren klassische Zeichen einer Gotteserscheinung – doch Gott kommt ganz leise. Er ist größer als unsere Erwartungen."),
    ],
    cards=["elia"],
    try_="Wenn du gerade erschöpft bist: Iss etwas, trink etwas, schlaf. Bei Elia ist das Gottes erste Antwort.",
    teaser="Die Propheten sagen Unbequemes: Gott hat genug von euren Gottesdiensten.")

# ───────────────────────── 5 · Propheten und Exil ─────────────────────────
sec("exil", [R(30, 5, 21, 24), R(33, 6, 6, 8)], "Was Gott wirklich will",
    "Durch Amos sagt Gott: Eure Feste und Lieder will ich nicht – lasst Recht und Gerechtigkeit strömen wie Wasser. Micha fasst zusammen, was Gott vom Menschen will: Recht tun, Güte lieben und demütig mit Gott leben.",
    bridge="Im 8. Jahrhundert v. Chr. geht es Israel wirtschaftlich gut – aber die Reichen beuten die Armen aus, und die Gottesdienste sind prächtig. Da treten Propheten wie Amos und Micha auf.",
    place="bethel",
    quiz=[
        choice("Was soll laut Amos fließen wie ein Bach?", ["Recht und Gerechtigkeit", "Das Blut der Opfer", "Wein für die Feste", "Gold für den Tempel"],
               24, "Amos 5,24.", "Am 5,24: Recht und Gerechtigkeit sollen strömen wie ein Bach, der nie austrocknet."),
        tf("Micha sagt: Gott will vor allem teure Opfer.", False, 8, "Lies Micha 6,6–8.",
           "Mi 6,6–8: Weder Tausende Widder noch Ströme von Öl – Gott will Recht, Güte und Demut."),
    ],
    explain=[
        E("Ist Gott gegen Gottesdienste?", "Nein – gegen Gottesdienste, die mit Unrecht im Alltag einhergehen. Lieder und Opfer ohne Gerechtigkeit nennt er Lärm (Am 5,23)."),
        E("Wer waren Amos und Micha?", "Amos war Viehzüchter aus Tekoa in Juda, der im Nordreich predigte (Am 1,1; 7,14). Micha stammte aus einem Dorf in Juda. Beide wirkten im 8. Jahrhundert v. Chr. und stellten sich auf die Seite der Armen."),
    ],
    memory_verse=MV(R(33, 6, 8), "Recht zu üben und Güte zu lieben und demütig zu wandeln mit deinem Gott"),
    fact="Martin Luther King zitierte Amos 5,24 in seiner berühmten Rede „I Have a Dream“ (1963).",
    teaser="Die Warnungen verhallen. Dann kommt der Tag, den niemand für möglich gehalten hat.")

sec("exil", [R(12, 25, 8, 12)], "Jerusalem fällt",
    "Die Babylonier unter Nebukadnezar erobern Jerusalem. Tempel, Königspalast und Häuser werden verbrannt, die Mauern niedergerissen, die meisten Menschen nach Babylon verschleppt.",
    bridge="722 v. Chr. erobern die Assyrer das Nordreich Israel. Juda im Süden hält sich noch über hundert Jahre – trotz der Warnungen von Propheten wie Jeremia. Dann kommen die Babylonier.",
    place="jerusalem",
    quiz=[
        choice("Was geschieht mit dem Tempel?", ["Er wird verbrannt", "Er wird zu einem Palast umgebaut", "Er bleibt verschont", "Er wird nach Babylon gebracht"],
               9, "Vers 9.", "V. 9: Das Haus des HERRN wird niedergebrannt – das Zentrum des Glaubens Israels."),
        tf("Alle Menschen werden nach Babylon gebracht.", False, 12, "Lies Vers 12.",
           "V. 12: Die Ärmsten des Landes bleiben zurück, um Weinberge und Äcker zu bestellen."),
    ],
    explain=[
        E("Wann war das?", "Im Jahr 587 oder 586 v. Chr. (die Forschung schwankt um ein Jahr). Juden gedenken der Zerstörung bis heute am Fastentag Tischa beAv."),
        E("Warum ist das so schlimm?", "Land, König und Tempel – alles, was Gottes Zusagen sichtbar gemacht hatte, ist verloren. Viele fragten: Hat Gott uns verlassen? Gilt sein Versprechen an David noch? Viele Texte der Bibel ringen mit diesen Fragen."),
    ],
    cards=["exil"],
    teaser="In Babylon sollen die Verschleppten fröhliche Lieder singen. Sie können es nicht.")

sec("exil", [R(19, 137, 1, 6)], "An den Flüssen Babels",
    "Die Gefangenen sitzen an den Flüssen Babylons und weinen. Ihre Bewacher verlangen Lieder aus Zion. Doch wie soll man in der Fremde Gottes Lieder singen? Sie schwören: Jerusalem vergessen wir nie.",
    bridge="Die Verschleppten leben nun in Babylon, fast 900 Kilometer Luftlinie von Jerusalem entfernt.",
    place="babylon",
    quiz=[
        choice("Was tun die Gefangenen mit ihren Instrumenten?", ["Sie hängen sie an die Weiden", "Sie spielen für die Babylonier", "Sie zerbrechen sie", "Sie verkaufen sie"],
               2, "Vers 2.", "V. 2: Sie hängen ihre Lauten in die Bäume – zum Singen ist ihnen nicht zumute."),
        tf("Die Babylonier verlangen, dass die Gefangenen Lieder aus Zion singen.", True, 3, "Lies Vers 3.",
           "V. 3: Ihre Bewacher wollen Unterhaltung – die heiligen Lieder werden zum Spott."),
    ],
    explain=[
        E("Was ist Zion?", "Ursprünglich der Hügel in Jerusalem mit Davids Burg, später der Tempelberg und schließlich ein Name für ganz Jerusalem – den Ort, an dem Gott wohnt."),
        E("Und die harten Verse am Ende?", "Der Psalm endet mit Rachewünschen gegen Babylon (V. 7–9), die wir hier nicht gelesen haben. Sie sind roh und verstörend. Die Bibel zeigt damit: Man darf auch Hass und Schmerz vor Gott bringen – statt sie selbst in die Tat umzusetzen."),
    ],
    fact="Den Anfang dieses Psalms kennen viele aus dem Song „Rivers of Babylon“ (The Melodians 1970, Boney M. 1978).",
    teaser="Ein Prophet schreibt den Verschleppten einen Brief. Sein Rat ist überraschend alltäglich.")

sec("exil", [R(24, 29, 4, 14)], "Sucht der Stadt Bestes",
    "Jeremia schreibt den Verschleppten: Baut Häuser, gründet Familien, sucht das Wohl der Stadt und betet für sie. Nach siebzig Jahren wird Gott euch zurückbringen. Er hat Gedanken des Friedens über euch.",
    bridge="Schon einige Jahre vor dem Fall Jerusalems waren erste Gruppen nach Babylon verschleppt worden. Falsche Propheten versprachen ihnen eine schnelle Rückkehr. An sie schreibt der Prophet Jeremia einen Brief.",
    place="babylon",
    focus="Achte darauf, wofür die Verschleppten beten sollen.",
    quiz=[
        estimate("Nach wie vielen Jahren will Gott die Verschleppten zurückbringen?", 1, 100, 70, "Jahren",
                 "V. 10: Nach siebzig Jahren – also nicht bald, sondern nach einem Menschenleben.", 10, "Vers 10.", tol=2),
        choice("Wofür sollen die Verschleppten beten?", ["Für den Frieden der Stadt, in der sie leben", "Für den Untergang Babylons", "Für eine schnelle Flucht", "Nur für sich selbst"],
               7, "Vers 7.", "V. 7: Sie sollen für das Wohl der fremden Stadt beten – denn deren Frieden ist auch ihr Frieden."),
    ],
    explain=[
        E("Warum siebzig Jahre?", "Eine runde Zahl für ein Menschenleben. Tatsächlich erlaubte der Perserkönig Kyrus 539/538 v. Chr. die Rückkehr – etwa 60 Jahre nach der ersten Verschleppung."),
        E("Gilt Vers 11 mir?", "Zunächst gilt er dem verschleppten Volk in einer ganz konkreten Lage. Viele Christen beziehen ihn trotzdem auch auf sich – weil er zeigt, wie Gott zu Menschen steht: mit Gedanken des Friedens, nicht des Unheils."),
    ],
    memory_verse=MV(R(24, 29, 11), "Gedanken des Friedens und nicht zum Unglück, um euch Ausgang und Hoffnung zu gewähren"),
    try_="Tu heute etwas Kleines für den Ort, an dem du lebst – für Nachbarn, Mitbewohner oder deine Straße.",
    teaser="Ein anderer Prophet sieht ein Tal voller Knochen. Gott fragt ihn: Können die wieder leben?")

sec("exil", [R(26, 37, 1, 14)], "Die toten Gebeine",
    "Hesekiel sieht ein Tal voller verdorrter Knochen. Auf Gottes Wort fügen sie sich zusammen, bekommen Sehnen, Fleisch und Haut – und als Gottes Atem kommt, werden sie lebendig. Gott sagt: Das ist Israel. Ich hole euch aus euren Gräbern.",
    bridge="Unter den Verschleppten in Babylon lebt der Priester und Prophet Hesekiel. Viele dort haben die Hoffnung aufgegeben.",
    place="babylon",
    quiz=[
        order("In welcher Reihenfolge geschieht es?",
              ["Die Knochen rücken zusammen", "Sehnen, Fleisch und Haut kommen darüber", "Der Atem kommt in sie", "Sie stehen auf – ein großes Heer"],
              "V. 7–10: Erst die Form, dann der Atem. Ohne Gottes Atem bleiben sie tot.", "Lies Vers 7–10."),
        choice("Wofür stehen die Knochen?", ["Für das ganze Volk Israel", "Für die Feinde Israels", "Für die Toten der Sintflut", "Für die Propheten"],
               11, "Vers 11.", "V. 11: Die Gebeine sind das Haus Israel, das sagt: Unsere Hoffnung ist verloren."),
    ],
    explain=[
        E("Atem, Wind, Geist?", "Das hebräische Wort „ruach“ bedeutet alles drei: Atem, Wind und Geist. Der Text spielt damit: Der Wind aus den vier Himmelsrichtungen wird zum Lebensatem – und Gott sagt: Ich gebe euch meinen Geist (V. 14)."),
        E("Geht es um Auferstehung?", "Zunächst ist es ein Bild für die Wiederherstellung des Volkes nach dem Exil. Später haben Juden und Christen darin auch einen Hinweis auf die Auferstehung der Toten gesehen."),
    ],
    fact="Der Spiritual „Dem Bones“ („Ezekiel connected dem dry bones“) erzählt genau diese Vision.",
    teaser="Ein Unbekannter wird verachtet, geschlagen und getötet – und gerade so wird er zur Rettung für viele.")

sec("exil", [R(23, 53, 1, 7)], "Der leidende Knecht",
    "Der Knecht ist unscheinbar, verachtet und voller Schmerzen. Man hielt ihn für von Gott gestraft – doch er trug unsere Schuld. Durch seine Wunden sind wir geheilt. Wie ein Lamm schweigt er.",
    bridge="Im Buch Jesaja gibt es Lieder über einen geheimnisvollen „Knecht Gottes“ (Jes 42; 49; 50; 52–53). Das bekannteste beginnt mit einer Frage.",
    quiz=[
        choice("Was trug der Knecht laut Vers 4–5?", ["Unsere Leiden und unsere Schuld", "Die Krone des Königs", "Die Tafeln des Gesetzes", "Die Opfer für den Tempel"],
               5, "Lies Vers 4–5.", "V. 4–5: Er trägt unsere Leiden und wird wegen unserer Schuld verwundet – zu unserem Frieden."),
        error("Er wurde misshandelt, aber er [protestierte] laut – wie ein Lamm, das zur Schlachtung geführt wird.", "schwieg", 7,
              "V. 7: Er tut seinen Mund nicht auf – wie ein Lamm."),
    ],
    explain=[
        E("Wer ist der Knecht?", "Darüber wird seit über 2000 Jahren nachgedacht. Jüdische Ausleger sehen im Knecht meist das leidende Volk Israel selbst. Christen haben in ihm von Anfang an Jesus erkannt – das Neue Testament zitiert Jesaja 53 mehrfach (z. B. Apg 8,32–35; 1. Petr 2,22–25). Der Text selbst nennt keinen Namen."),
        E("Wann wurde das geschrieben?", "Viele Forscher ordnen Jesaja 40–55 der Zeit des Exils zu, andere dem Propheten Jesaja selbst im 8. Jh. v. Chr. Sicher ist: Der Text ist Jahrhunderte älter als Jesus."),
    ],
    memory_verse=MV(R(23, 53, 5), "durch seine Striemen ist uns Heilung geworden"),
    fact="In Qumran am Toten Meer wurde eine vollständige Jesaja-Rolle gefunden, die etwa aus dem 2. Jahrhundert v. Chr. stammt – mit Kapitel 53 fast gleichlautend wie in unseren Bibeln.",
    teaser="Gott kündigt einen neuen Bund an. Diesmal nicht auf Steintafeln.")

sec("exil", [R(24, 31, 31, 34)], "Ein neuer Bund",
    "Gott verspricht einen neuen Bund. Sein Gesetz wird er nicht auf Stein, sondern ins Herz schreiben. Alle werden ihn kennen, vom Kleinsten bis zum Größten, und er wird ihre Schuld vergeben.",
    bridge="Mitten in der Katastrophe kündigt Jeremia nicht nur Gericht an, sondern auch eine Zukunft.",
    place="jerusalem",
    quiz=[
        error("Gott sagt: Ich werde mein Gesetz auf neue [Steintafeln] schreiben.", "ihr Herz", 33,
              "V. 33: Gottes Wille soll nicht mehr nur von außen kommen, sondern von innen."),
        choice("Was wird Gott nach Vers 34 mit der Schuld tun?", ["Vergeben und nicht mehr daran denken", "Sie auf die Kinder übertragen", "Sie gegen gute Taten aufrechnen", "Sie aufschreiben"],
               34, "Vers 34.", "V. 34: Er vergibt – und denkt nicht mehr daran."),
    ],
    explain=[
        E("Was war am alten Bund falsch?", "Nicht Gottes Gebote waren schlecht – das Volk hat den Bund gebrochen (V. 32). Der neue Bund setzt tiefer an: beim Herzen."),
        E("Altes und Neues Testament", "„Testament“ ist das lateinische Wort für Bund. Jesus greift diese Verheißung beim letzten Mahl auf (Lk 22,20) – daher heißt der zweite Teil der Bibel „Neues Testament“. Wichtig: Es ersetzt das Alte nicht, sondern führt es weiter."),
    ],
    memory_verse=MV(R(24, 31, 33), "Ich werde mein Gesetz in ihr Inneres legen und werde es auf ihr Herz schreiben"),
    teaser="Johannes beginnt sein Evangelium mit denselben Worten wie die Bibel selbst.")

# ───────────────────────── 6 · Jesus ─────────────────────────
sec("jesus", [R(43, 1, 1, 5), R(43, 1, 14)], "Das Wort wurde Mensch",
    "Johannes beginnt sein Evangelium wie 1. Mose: Im Anfang war das Wort. Durch das Wort ist alles geworden, in ihm ist Leben und Licht. Und das Wort wurde Mensch und wohnte unter uns.",
    bridge="Ab 538 v. Chr. kehren viele Juden zurück und bauen den Tempel wieder auf. Es folgen Jahrhunderte unter Persern, Griechen und Römern. Viele warten auf den Messias.",
    focus="Achte darauf, mit welchen Worten das beginnt – du kennst sie aus dem allerersten Abschnitt.",
    quiz=[
        choice("Womit beginnt das Johannesevangelium?", ["Mit denselben Worten wie die Bibel: Im Anfang", "Mit Jesu Geburt in Bethlehem", "Mit dem Stammbaum Jesu", "Mit Johannes dem Täufer"],
               1, "Vers 1.", "V. 1: Im Anfang – wie 1. Mose 1,1. Johannes erzählt Jesus als Neuanfang der Schöpfung."),
        tf("Dass das Wort „Fleisch“ wird, heißt: Gott wurde ein echter Mensch.", True, 14, "Lies Vers 14.",
           "V. 14: Fleisch meint verletzlich, sterblich, ganz Mensch. Gott wohnt nicht mehr nur im Tempel, sondern unter uns."),
    ],
    explain=[
        E("Wer ist „das Wort“?", "Griechisch „Logos“: Wort, Sinn, Vernunft. Jüdische Leser hörten darin Gottes schöpferisches Wort aus 1. Mose 1, griechische die Vernunft hinter der Welt. Johannes sagt: Dieses Wort ist eine Person – Jesus (V. 14–17)."),
        E("Was heißt „wohnte unter uns“?", "Wörtlich: Er „zeltete“ unter uns. Das erinnert an das Zelt der Begegnung, in dem Gott in der Wüste bei Israel wohnte (2. Mose 40,34)."),
    ],
    memory_verse=MV(R(43, 1, 14), "Und das Wort wurde Fleisch und wohnte unter uns"),
    teaser="Ein römischer Kaiser ordnet eine Volkszählung an – und setzt damit eine schwangere Frau in Bewegung.")

sec("jesus", [R(42, 2, 1, 14)], "Die Geburt",
    "Wegen einer Volkszählung reisen Josef und Maria nach Bethlehem. Dort kommt Jesus zur Welt und wird in eine Krippe gelegt. Engel verkünden Hirten auf dem Feld: Euch ist heute der Retter geboren.",
    bridge="Ein Engel kündigt Maria in Nazareth an, dass sie den Sohn Gottes zur Welt bringen wird (Lk 1,26–38).",
    place="bethlehem",
    quiz=[
        order("Bring die Ereignisse in die richtige Reihenfolge.",
              ["Kaiser Augustus ordnet eine Einschreibung an", "Josef und Maria reisen nach Bethlehem", "Jesus wird geboren und in eine Krippe gelegt", "Ein Engel erscheint den Hirten", "Viele Engel loben Gott"],
              "V. 1–14."),
        choice("Wem wird die Geburt zuerst verkündet?", ["Hirten auf dem Feld", "Dem König Herodes", "Den Priestern im Tempel", "Den Weisen aus dem Osten"],
               8, "Lies Vers 8–11.", "V. 8–11: Hirten – einfache Leute ohne Ansehen – hören die Nachricht als Erste. Die Weisen kommen bei Matthäus vor."),
    ],
    explain=[
        E("Warum Bethlehem?", "Bethlehem ist die Stadt Davids (V. 4). Der Prophet Micha hatte angekündigt, dass dort ein Herrscher für Israel geboren wird (Mi 5,1)."),
        E("Wie sehen die Kirchen Maria?", "Alle Kirchen ehren Maria als Mutter Jesu. Katholische und orthodoxe Christen verehren sie besonders und bitten sie um ihre Fürsprache. Evangelische und freikirchliche Christen sehen in ihr vor allem ein Vorbild des Glaubens und richten ihre Gebete allein an Gott."),
    ],
    fact="Kaiser Augustus ließ sich als Friedensbringer feiern. Eine Inschrift aus dem Jahr 9 v. Chr. nennt seinen Geburtstag den Beginn einer „frohen Botschaft“ für die Welt. Lukas verwendet für Jesus bewusst ähnliche Worte.",
    teaser="Rund 30 Jahre später tritt Jesus öffentlich auf. Sein erster Satz fasst alles zusammen.")

sec("jesus", [R(41, 1, 14, 20)], "Die Zeit ist erfüllt",
    "Jesus verkündet in Galiläa: Die Zeit ist erfüllt, das Reich Gottes ist nahe – kehrt um und glaubt. Er ruft vier Fischer, und sie lassen alles stehen und folgen ihm.",
    bridge="Jesus wächst in Nazareth auf. Mit etwa 30 Jahren lässt er sich von Johannes dem Täufer im Jordan taufen (Mk 1,9–11; Lk 3,23).",
    place="see-genezareth",
    quiz=[
        choice("Was sagt Jesus zu den Fischern?", ["Folgt mir – ich mache euch zu Menschenfischern", "Fangt mehr Fische für die Armen", "Verkauft eure Boote", "Geht nach Jerusalem"],
               17, "Vers 17.", "V. 17: Ihr Können bleibt – aber es bekommt ein neues Ziel: Menschen."),
        tf("Jakobus und Johannes nehmen ihren Vater mit.", False, 20, "Lies Vers 20.",
           "V. 20: Sie lassen ihren Vater Zebedäus mit den Tagelöhnern im Boot zurück."),
    ],
    explain=[
        E("Was heißt „Buße tun“?", "Das griechische Wort „metanoia“ meint Umdenken, die Richtung ändern. Es geht nicht um Selbstbestrafung, sondern darum, sich Gott zuzuwenden."),
        E("Was ist das „Reich Gottes“?", "Kein Land, sondern Gottes Herrschaft: Wo Gott regiert, wird das Leben heil. Mit Jesus ist es nahe gekommen – in seinen Worten und Taten bricht es an."),
    ],
    cards=["reich-gottes", "petrus"],
    teaser="Auf einem Berg erklärt Jesus, wer wirklich glücklich ist. Seine Liste ist eine Provokation.")

sec("jesus", [R(40, 5, 1, 12)], "Die Seligpreisungen",
    "Auf einem Berg nennt Jesus die glücklich, die arm im Geist sind, trauern, sanft sind, nach Gerechtigkeit hungern, barmherzig, reinen Herzens und Friedensstifter sind – und die, die deswegen verfolgt werden.",
    bridge="Jesus zieht durch Galiläa, heilt Kranke und lehrt. Große Mengen folgen ihm (Mt 4,23–25).",
    place="see-genezareth",
    focus="Achte darauf, wen Jesus glücklich nennt – und ob du das selbst so sehen würdest.",
    quiz=[
        choice("Was wird den Friedensstiftern versprochen?", ["Sie werden Söhne Gottes heißen", "Sie werden das Land erben", "Sie werden getröstet", "Sie werden Gott schauen"],
               9, "Vers 9.", "V. 9: Wer Frieden stiftet, zeigt Gottes Wesen – so wie Kinder ihren Eltern ähneln."),
        tf("Jesus nennt die Trauernden glücklich.", True, 4, "Lies Vers 4.",
           "V. 4: Nicht weil Trauer gut wäre – sondern weil Gott sie trösten wird."),
    ],
    explain=[
        E("Was heißt „glückselig“?", "Das griechische Wort „makarios“ meint: Wohl dir! Gesegnet bist du! Jesus beschreibt keine Pflichten, sondern spricht Menschen etwas zu, die nach menschlichen Maßstäben eher Verlierer sind."),
        E("„Arm im Geist“?", "Gemeint sind Menschen, die wissen, dass sie vor Gott nichts vorzuweisen haben und auf ihn angewiesen sind. Lukas überliefert dieselbe Seligpreisung kürzer: Glückselig ihr Armen (Lk 6,20)."),
    ],
    memory_verse=MV(R(40, 5, 9), "Glückselig die Friedensstifter, denn sie werden Söhne Gottes heißen."),
    teaser="Ein Sohn wünscht seinem Vater praktisch den Tod. Was der Vater dann tut, erzählt Jesus als Gleichnis.")

sec("jesus", [R(42, 15, 11, 24)], "Der verlorene Sohn",
    "Ein Sohn lässt sich sein Erbe auszahlen, verprasst alles und landet bei den Schweinen. Er kehrt um, um als Tagelöhner zu arbeiten. Doch der Vater läuft ihm entgegen, umarmt ihn und feiert ein Fest: Er war tot und lebt wieder.",
    bridge="Fromme Kritiker beschweren sich, dass Jesus mit Zöllnern und Sündern isst. Er antwortet mit drei Geschichten über Verlorenes, das gefunden wird (Lk 15,1–3).",
    quiz=[
        order("Bring die Geschichte in die richtige Reihenfolge.",
              ["Der Sohn lässt sich sein Erbe auszahlen", "Er verprasst alles in einem fernen Land", "Er hütet Schweine und hungert", "Er macht sich auf den Weg nach Hause", "Der Vater läuft ihm entgegen"],
              "V. 12–20."),
        who("Vater, ich habe gesündigt gegen den Himmel und vor dir", R(42, 15, 18), ["Der jüngere Sohn", "Der Vater", "Der ältere Sohn", "Ein Knecht"],
            "V. 18 und 21: Er hat sich den Satz zurechtgelegt. Den Teil mit dem Tagelöhner lässt der Vater ihn gar nicht mehr sagen."),
    ],
    explain=[
        E("Warum ist die Bitte um das Erbe so schlimm?", "Ein Erbe bekommt man nach dem Tod des Vaters. Wer es vorher fordert, sagt sinngemäß: Du bist für mich gestorben."),
        E("Warum ist das Laufen des Vaters so auffällig?", "Ein älterer Mann lief im Orient nicht – das galt als würdelos. Der Vater wartet nicht auf eine Entschuldigung, sondern rennt dem Sohn entgegen (V. 20). So, sagt Jesus, ist Gott."),
        E("Und der ältere Bruder?", "Die Geschichte geht weiter (V. 25–32): Der ältere Sohn ärgert sich über das Fest. Das Gleichnis bleibt offen – geht er mit hinein? Damit spricht Jesus seine frommen Kritiker an."),
    ],
    memory_verse=MV(R(42, 15, 24), "war verloren und ist gefunden worden"),
    prayer={"text": "Du hast uns auf dich hin geschaffen, und unruhig ist unser Herz, bis es ruht in dir.", "source": "Augustinus, Bekenntnisse I,1 (um 400)"},
    teaser="Zwei Jünger wollen die besten Plätze neben Jesus. Seine Antwort stellt alle Machtverhältnisse auf den Kopf.")

sec("jesus", [R(41, 10, 35, 45)], "Nicht bedient werden, sondern dienen",
    "Jakobus und Johannes wollen die Ehrenplätze in Jesu Herrlichkeit. Die anderen ärgern sich. Jesus erklärt: Bei euch soll es anders sein als bei den Mächtigen – wer groß sein will, soll dienen. Er selbst ist gekommen, um zu dienen und sein Leben zu geben.",
    bridge="Jesus ist mit seinen Jüngern auf dem Weg nach Jerusalem. Schon zum dritten Mal kündigt er an, dass er dort leiden und sterben wird (Mk 10,32–34).",
    quiz=[
        choice("Worum bitten Jakobus und Johannes?", ["Um die Plätze rechts und links neben Jesus", "Um Geld für die Reise", "Um die Heilung ihres Vaters", "Darum, in Galiläa bleiben zu dürfen"],
               37, "Vers 37.", "V. 37: Sie wollen die Ehrenplätze, wenn Jesus herrscht."),
        error("Jesus sagt: Wer unter euch groß werden will, soll euer [Anführer] sein.", "Diener", 43,
              "V. 43–44: Größe zeigt sich im Dienen."),
    ],
    explain=[
        E("Was sind „Kelch“ und „Taufe“?", "Bilder für das Leiden, das Jesus bevorsteht (V. 38). Jakobus wurde später tatsächlich als Erster der Zwölf hingerichtet (Apg 12,2)."),
        E("Was heißt „Lösegeld für viele“?", "Mit Lösegeld kaufte man Gefangene oder Sklaven frei. Jesus deutet seinen Tod so: Er gibt sein Leben, damit andere frei werden (V. 45). „Viele“ meint im hebräischen Sprachgebrauch die große Menge – alle."),
    ],
    memory_verse=MV(R(41, 10, 45), "nicht gekommen, um bedient zu werden, sondern um zu dienen"),
    try_="Tu heute jemandem einen kleinen Dienst, ohne dass er davon erfährt.",
    teaser="Am letzten Abend nimmt Jesus Brot und Wein und gibt ihnen eine neue Bedeutung.")

# ───────────────────────── 7 · Kreuz und Auferstehung ─────────────────────────
sec("kreuz", [R(42, 22, 14, 20)], "Das letzte Mahl",
    "Beim Passamahl nimmt Jesus Brot und sagt: Das ist mein Leib, für euch gegeben. Dann den Kelch: der neue Bund in meinem Blut. Tut dies zu meinem Gedächtnis.",
    bridge="Jesus zieht unter Jubel in Jerusalem ein und vertreibt die Händler aus dem Tempel. Die religiöse Führung beschließt, ihn zu töten; Judas, einer der Zwölf, bietet an, ihn auszuliefern (Lk 19–22).",
    place="jerusalem",
    focus="Achte auf das Wort „Bund“ – du kennst es schon aus der großen Geschichte.",
    quiz=[
        error("Jesus nahm Brot, dankte, brach es und sagte: Das ist mein Leib, der für euch [gebrochen] wird.", "gegeben", 19,
              "V. 19: mein Leib, der für euch gegeben wird."),
        choice("Wie nennt Jesus den Kelch?", ["Den neuen Bund in seinem Blut", "Den Kelch des Zorns", "Den Kelch der Freude", "Den Kelch der Väter"],
               20, "Vers 20.", "V. 20: Der neue Bund – Jesus nimmt die Verheißung aus Jeremia 31 auf."),
    ],
    explain=[
        E("Wie verstehen das die Kirchen?", "Alle feiern dieses Mahl, verstehen es aber verschieden. Katholiken: Brot und Wein werden wirklich Leib und Blut Christi (Wandlung). Orthodoxe: Christus ist wirklich gegenwärtig – ein Geheimnis, das man nicht erklärt. Lutheraner: Christus ist in, mit und unter Brot und Wein gegenwärtig. Reformierte: Christus ist geistlich gegenwärtig. Viele Freikirchen: ein Gedächtnismahl, bei dem man sich an Jesu Tod erinnert und Gemeinschaft feiert."),
        E("Was ist das Passamahl?", "Das Festessen zur Erinnerung an die Befreiung aus Ägypten (2. Mose 12). Jesus deutet es neu: Jetzt geht es um eine Befreiung durch seinen Tod."),
    ],
    fact="Abendmahl, Eucharistie (griechisch „Danksagung“), Kommunion, Herrenmahl, Brotbrechen – dieses Mahl hat viele Namen, fast alle aus dem Neuen Testament oder der frühen Kirche.",
    teaser="Am nächsten Mittag wird es dunkel über dem ganzen Land.")

sec("kreuz", [R(41, 15, 33, 39)], "Der Tod",
    "Von Mittag bis drei Uhr ist es finster. Jesus schreit: Mein Gott, mein Gott, warum hast du mich verlassen? – und stirbt. Der Vorhang im Tempel zerreißt, und ein römischer Hauptmann bekennt: Dieser Mensch war wirklich Gottes Sohn.",
    bridge="In der Nacht wird Jesus im Garten Gethsemane verhaftet. Petrus verleugnet ihn dreimal. Der römische Statthalter Pontius Pilatus lässt ihn kreuzigen, obwohl er keine klare Schuld erkennen kann (Mk 14–15).",
    place="jerusalem",
    quiz=[
        who("Wahrhaftig, dieser Mensch war Gottes Sohn", R(41, 15, 39), ["Der römische Hauptmann", "Petrus", "Pilatus", "Ein Priester"],
            "V. 39: Ausgerechnet der Römer, der die Hinrichtung beaufsichtigt, spricht das Bekenntnis aus."),
        choice("Was geschieht im Tempel, als Jesus stirbt?", ["Der Vorhang zerreißt von oben nach unten", "Das Feuer auf dem Altar erlischt", "Die Tore öffnen sich von selbst", "Die Priester fliehen"],
               38, "Vers 38.", "V. 38: Der Vorhang trennte das Allerheiligste ab. Er zerreißt von oben – wie von Gott selbst."),
    ],
    explain=[
        E("Warum ruft Jesus diesen Satz?", "Es ist der Anfang von Psalm 22 – einem Gebet, das in tiefster Verlassenheit beginnt und in Vertrauen endet. Jesus erlebt Gottverlassenheit und betet sie trotzdem zu Gott."),
        E("Sechste und neunte Stunde?", "Man zählte die Stunden ab Sonnenaufgang (etwa 6 Uhr). Die sechste Stunde ist also Mittag, die neunte etwa 15 Uhr."),
        E("Warum musste Jesus sterben?", "Historisch: Die religiöse Führung sah in ihm einen Gotteslästerer, Rom einen möglichen Aufrührer. Theologisch deutet das Neue Testament seinen Tod mit vielen Bildern: Lösegeld, Opfer, Sieg über das Böse, Gottes Liebe bis zum Äußersten. Die Kirchen gewichten diese Bilder unterschiedlich, halten aber gemeinsam fest: Er starb für uns."),
    ],
    cards=["kreuz"],
    prayer={"text": "Wenn ich einmal soll scheiden, so scheide nicht von mir; wenn ich den Tod soll leiden, so tritt du dann herfür. Wenn mir am allerbängsten wird um das Herze sein, so reiß mich aus den Ängsten kraft deiner Angst und Pein.",
            "source": "Paul Gerhardt, „O Haupt voll Blut und Wunden“ (1656)"},
    teaser="Am dritten Tag gehen Frauen zum Grab, um einen Toten zu salben.")

sec("kreuz", [R(42, 24, 1, 12)], "Er ist nicht hier",
    "Am Sonntagmorgen finden Frauen das Grab offen und leer. Zwei Männer in leuchtenden Kleidern fragen: Was sucht ihr den Lebendigen bei den Toten? Er ist auferstanden. Die Apostel halten es für Gerede – Petrus läuft hin und staunt.",
    bridge="Josef von Arimathäa legt Jesus in ein Felsengrab. Dann beginnt der Sabbat, an dem man nicht arbeiten darf (Lk 23,50–56).",
    place="jerusalem",
    quiz=[
        who("Was sucht ihr den Lebendigen unter den Toten", R(42, 24, 5), ["Zwei Männer in strahlenden Kleidern", "Maria Magdalene", "Petrus", "Jesus selbst"],
            "V. 4–5: Die Frage enthält schon die Antwort: Er ist kein Toter."),
        choice("Wie reagieren die Apostel auf den Bericht der Frauen?", ["Sie halten ihn für Geschwätz", "Sie feiern sofort", "Sie gehen alle zum Grab", "Sie melden es den Priestern"],
               11, "Vers 11.", "V. 11: Es kommt ihnen vor wie leeres Gerede. Die ersten Zeugen der Auferstehung sind Frauen – und man glaubt ihnen zunächst nicht."),
        tf("Petrus findet im Grab nur die Leinentücher.", True, 12, "Lies Vers 12.",
           "V. 12: Die Tücher liegen da, der Leib nicht. Petrus geht verwundert nach Hause."),
    ],
    explain=[
        E("Warum ist wichtig, dass es Frauen waren?", "Das Zeugnis von Frauen galt damals vor Gericht wenig. Hätte jemand die Geschichte erfunden, hätte er wohl Männer als erste Zeugen gewählt. Viele Historiker sehen darin einen Hinweis, dass hier eine alte Erinnerung bewahrt wurde."),
        E("Was heißt Auferstehung?", "Nicht die Rückkehr ins alte Leben, sondern ein neues, verwandeltes Leben, über das der Tod keine Macht mehr hat. Für die ersten Christen war sie der Kern des Glaubens (1. Kor 15,14)."),
    ],
    cards=["auferstehung"],
    teaser="Zwei Jünger gehen enttäuscht nach Hause. Ein Fremder begleitet sie – und sie erkennen ihn erst ganz am Ende.")

sec("kreuz", [R(42, 24, 28, 35)], "Emmaus",
    "In Emmaus laden die beiden Jünger den Fremden ein zu bleiben. Als er das Brot bricht, erkennen sie Jesus – und er verschwindet. Sie laufen sofort zurück nach Jerusalem.",
    bridge="Am selben Tag wandern zwei Jünger nach Emmaus. Ein Unbekannter schließt sich ihnen an und erklärt ihnen unterwegs die Schriften (Lk 24,13–27).",
    place="emmaus",
    quiz=[
        who("Brannte nicht unser Herz in uns", R(42, 24, 32), ["Die beiden Jünger", "Die Elf in Jerusalem", "Jesus", "Petrus"],
            "V. 32: Im Rückblick merken sie, was unterwegs schon in ihnen passiert war."),
        choice("Woran erkennen sie Jesus?", ["Am Brechen des Brotes", "An seinen Wunden", "An seiner Stimme", "An seinem Gewand"],
               35, "Lies Vers 30–31 und 35.", "V. 30–31 und 35: Als er das Brot bricht – wie beim letzten Mahl."),
    ],
    explain=[
        E("Warum erkennen sie ihn nicht früher?", "Lukas sagt nur, dass ihre Augen gehalten waren (V. 16). Die Geschichte zeigt: Den Auferstandenen erkennt man nicht einfach mit den Augen, sondern in der Begegnung – in den Schriften und im gemeinsamen Mahl."),
        E("Wo lag Emmaus?", "Das ist unbekannt. Lukas nennt eine Entfernung von 60 Stadien, gut 11 Kilometer, von Jerusalem (V. 13); mehrere Orte kommen in Frage."),
    ],
    fact="Die Bitte der beiden an den Fremden, bei ihnen zu bleiben, weil es Abend wird (V. 29), ist zu einem bekannten Abendgebet geworden – unter anderem vertont von Johann Sebastian Bach (Kantate BWV 6).",
    try_="Iss heute eine Mahlzeit ohne Bildschirm – mit jemandem zusammen, wenn das geht.",
    teaser="Petrus hatte Jesus dreimal verleugnet. Jetzt fragt Jesus ihn dreimal etwas.")

sec("kreuz", [R(43, 21, 15, 19)], "„Liebst du mich?“",
    "Nach dem Frühstück fragt Jesus Petrus dreimal: Hast du mich lieb? Petrus wird traurig, antwortet aber jedes Mal: Du weißt es. Jesus gibt ihm den Auftrag, seine Schafe zu weiden – und sagt: Folge mir nach.",
    bridge="Der Auferstandene begegnet seinen Jüngern mehrfach. Eines Morgens am See Genezareth hat er für sie gekocht – Fisch über einem Kohlenfeuer (Joh 21,1–14).",
    place="see-genezareth",
    quiz=[
        estimate("Wie oft fragt Jesus Petrus, ob er ihn liebt?", 1, 7, 3, "Mal",
                 "V. 15–17: Dreimal – so oft, wie Petrus ihn verleugnet hatte.", 17, "Lies Vers 15–17 noch einmal."),
        choice("Welchen Auftrag bekommt Petrus?", ["Für Jesu Schafe sorgen", "Einen Tempel bauen", "Ein Evangelium schreiben", "Zurück zum Fischen gehen"],
               17, "Vers 15–17.", "V. 15–17: Petrus soll sich um die Menschen kümmern, die zu Jesus gehören."),
    ],
    explain=[
        E("Warum dreimal?", "Petrus hatte Jesus in der Nacht der Verhaftung dreimal verleugnet – an einem Kohlenfeuer (Joh 18,18.25–27). Jetzt, wieder an einem Kohlenfeuer, darf er dreimal seine Liebe aussprechen. Jesus stellt ihn wieder her, ohne ihn bloßzustellen."),
        E("Wie verstehen das die Kirchen?", "Die katholische Kirche sieht in diesem Auftrag (zusammen mit Mt 16,18) eine Grundlage für das Amt des Papstes als Nachfolger des Petrus. Orthodoxe, evangelische und freikirchliche Christen sehen darin vor allem die persönliche Wiederherstellung des Petrus und einen Auftrag an alle, die in der Gemeinde Verantwortung tragen."),
        E("Was bedeuten Vers 18–19?", "Jesus deutet an, wie Petrus sterben wird. Nach alter Überlieferung wurde er um 64–67 n. Chr. in Rom gekreuzigt."),
    ],
    teaser="Jesus verabschiedet sich – und gibt einen Auftrag, der bis ans Ende der Welt reicht.")

# ───────────────────────── 8 · Die Gemeinde und das Ziel ─────────────────────────
sec("gemeinde", [R(44, 1, 6, 11)], "Bis an das Ende der Erde",
    "Die Jünger fragen, ob Jesus jetzt das Reich für Israel wiederherstellt. Er antwortet: Ihr werdet die Kraft des Heiligen Geistes empfangen und meine Zeugen sein – bis an das Ende der Erde. Dann wird er in den Himmel aufgenommen.",
    bridge="Lukas schreibt nach seinem Evangelium einen zweiten Band: die Apostelgeschichte. Vierzig Tage lang zeigt sich der Auferstandene seinen Jüngern (Apg 1,3).",
    place="jerusalem",
    quiz=[
        order("Wohin sollen die Zeugen gehen? In der Reihenfolge von Vers 8:", ["Jerusalem", "Judäa und Samaria", "Bis an das Ende der Erde"],
              "V. 8: Von der Stadt über das Land bis zu allen Völkern – das ist auch der Aufbau der ganzen Apostelgeschichte.", "Vers 8."),
        who("Männer von Galiläa, was steht ihr", R(44, 1, 11), ["Zwei Männer in weißen Kleidern", "Jesus", "Petrus", "Die Mutter Jesu"],
            "V. 10–11: Nicht in den Himmel starren – er kommt wieder, und bis dahin gibt es zu tun."),
    ],
    explain=[
        E("Was ist die „Himmelfahrt“?", "Jesus wird von einer Wolke verhüllt (V. 9) – in der Bibel ein Zeichen für Gottes Gegenwart. „Himmel“ meint hier nicht einen Ort über den Wolken, sondern Gottes Wirklichkeit. Gefeiert wird das an Christi Himmelfahrt, 40 Tage nach Ostern."),
        E("Was heißt „Zeuge“?", "Ein Zeuge erzählt, was er selbst erlebt hat. Das griechische Wort „martys“ bekam später auch die Bedeutung „Märtyrer“ – weil viele Zeugen für ihr Zeugnis starben."),
    ],
    cards=["heiliger-geist"],
    teaser="Zehn Tage später: ein Brausen, Feuer und Menschen aus aller Welt, die plötzlich ihre eigene Sprache hören.")

sec("gemeinde", [R(44, 2, 1, 13)], "Pfingsten",
    "Am Pfingstfest kommt der Heilige Geist wie Sturm und Feuer auf die Jünger. Sie reden in anderen Sprachen, und Pilger aus vielen Völkern hören Gottes große Taten in ihrer eigenen Sprache. Manche staunen, andere spotten: Die sind betrunken.",
    bridge="Die Jünger warten in Jerusalem, wie Jesus es ihnen gesagt hat. Es ist das jüdische Wochenfest, und Pilger aus vielen Ländern sind in der Stadt.",
    place="jerusalem",
    quiz=[
        choice("Was hören die Pilger?", ["Gottes große Taten in ihrer eigenen Sprache", "Eine Predigt auf Hebräisch", "Lieder aus dem Tempel", "Nur unverständliche Laute"],
               11, "Lies Vers 6–11.", "V. 6–11: Jeder hört sie in seiner Muttersprache – Gottes Botschaft gilt allen Völkern."),
        tf("Alle Zuhörer sind sofort begeistert.", False, 13, "Lies Vers 13.",
           "V. 13: Manche spotten, die Jünger seien betrunken."),
    ],
    explain=[
        E("Wie verstehen das die Kirchen?", "Alle Kirchen glauben, dass der Heilige Geist bis heute wirkt. Pfingstkirchen und die charismatische Bewegung erwarten auch heute Gaben wie Zungenrede und Prophetie und betonen ein besonderes Erfülltwerden mit dem Geist. Andere Kirchen sehen die Sprachen von Pfingsten als einmaliges Zeichen am Anfang und betonen das stille Wirken des Geistes in Glaube, Liebe und Sakramenten. Dazwischen gibt es viele Haltungen."),
        E("Was hat das mit dem Turmbau zu Babel zu tun?", "In 1. Mose 11 verwirrt Gott die Sprachen, und die Menschen zerstreuen sich. An Pfingsten werden Menschen vieler Sprachen durch eine Botschaft verbunden. Viele Ausleger sehen darin eine bewusste Umkehrung."),
    ],
    cards=["pfingsten"],
    fact="In Vers 9–11 werden Menschen aus 15 Völkern und Regionen genannt – vom heutigen Iran bis nach Rom.",
    teaser="Petrus predigt – und am Ende entsteht eine Gemeinschaft, die die Stadt verändert.")

sec("gemeinde", [R(44, 2, 37, 47)], "Die erste Gemeinde",
    "Die Zuhörer fragen: Was sollen wir tun? Petrus ruft zu Umkehr und Taufe. Dreitausend schließen sich an. Die Gemeinde bleibt bei der Lehre der Apostel, in der Gemeinschaft, beim Brotbrechen und im Gebet – und teilt ihren Besitz.",
    bridge="Petrus erklärt der Menge, was geschehen ist: Jesus, der gekreuzigt wurde, hat Gott auferweckt (Apg 2,14–36).",
    place="jerusalem",
    focus="Achte auf die vier Dinge, bei denen die Gemeinde bleibt (V. 42).",
    quiz=[
        estimate("Wie viele Menschen kommen an diesem Tag dazu?", 0, 10000, 3000, "Menschen", "V. 41: Etwa dreitausend.", 41, "Vers 41.", tol=500),
        choice("Wobei bleiben die ersten Christen beständig?", ["Lehre, Gemeinschaft, Brotbrechen und Gebet", "Fasten, Opfer, Wallfahrt und Almosen", "Lesen, Singen, Wandern und Feiern", "Predigt, Mission, Spenden und Bauen"],
               42, "Vers 42.", "V. 42: Die Lehre der Apostel, die Gemeinschaft, das Brotbrechen und die Gebete."),
    ],
    explain=[
        E("Wie verstehen die Kirchen die Taufe?", "Katholische, orthodoxe, landeskirchliche und viele andere Kirchen taufen auch Säuglinge: Die Taufe ist Gottes Geschenk, das dem eigenen Glauben vorausgeht. Baptisten und viele andere Freikirchen taufen nur Menschen, die selbst ihren Glauben bekennen: Die Taufe ist die Antwort auf Gottes Ruf. Beide Seiten berufen sich auf das Neue Testament."),
        E("Haben die ersten Christen alles geteilt?", "V. 44–45 erzählt, dass sie Besitz verkauften und nach Bedarf verteilten. Das war freiwillig (vgl. Apg 5,4). Es zeigt, wie sehr der Glaube ihr ganzes Leben verändert hat."),
    ],
    try_="Schreib heute einem Menschen aus deiner Gemeinde oder Gruppe eine kurze Nachricht.",
    teaser="Der gefährlichste Gegner der jungen Gemeinde ist unterwegs, um in Damaskus Christen zu verhaften.")

sec("gemeinde", [R(44, 9, 1, 9)], "Saulus vor Damaskus",
    "Saulus will die Christen in Damaskus verhaften. Unterwegs umstrahlt ihn ein Licht, er stürzt und hört: Warum verfolgst du mich? Ich bin Jesus. Blind wird er nach Damaskus geführt. Drei Tage isst und trinkt er nichts.",
    bridge="Die Gemeinde wächst, aber auch der Widerstand. Stephanus wird gesteinigt; dabei ist ein junger Mann namens Saulus (Apg 7–8).",
    place="damaskus",
    quiz=[
        who("Wer bist du, Herr", R(44, 9, 5), ["Saulus", "Hananias", "Petrus", "Ein Begleiter"],
            "V. 5: Saulus fragt – und die Antwort stellt sein ganzes Leben auf den Kopf."),
        choice("Wen verfolgt Saulus laut der Stimme?", ["Jesus selbst", "Nur die Apostel", "Den Hohenpriester", "Die Römer"],
               5, "Lies Vers 4–5.", "V. 4–5: Wer die Christen verfolgt, verfolgt Jesus selbst. So eng verbindet er sich mit seinen Leuten."),
        tf("Saulus ist nach der Begegnung drei Tage blind.", True, 9, "Lies Vers 9.",
           "V. 9: Drei Tage ohne Sehen, Essen und Trinken. Dann besucht ihn Hananias (V. 10–19)."),
    ],
    explain=[
        E("Saulus oder Paulus?", "Saulus war sein jüdischer Name, Paulus sein römischer. Er wurde nicht wegen der Bekehrung umbenannt – die Apostelgeschichte nennt ihn ab Kapitel 13 einfach mit seinem römischen Namen, als er unter Nichtjuden wirkt."),
        E("Ist das eine Bekehrung?", "Paulus selbst spricht von einer Berufung (Gal 1,15–16): Er hat nicht die Religion gewechselt, sondern als Jude erkannt, dass Jesus der Messias ist – und wurde zum Apostel für die Völker."),
    ],
    cards=["paulus"],
    fact="„Vom Saulus zum Paulus werden“ ist eine deutsche Redewendung – obwohl die beiden Namen in der Bibel gar nichts mit der Bekehrung zu tun haben.",
    teaser="Jahre später schreibt Paulus einen Brief nach Rom, in dem einer der stärksten Sätze der Bibel steht.")

sec("gemeinde", [R(45, 8, 31, 39)], "Nichts kann uns trennen",
    "Paulus fragt: Wenn Gott für uns ist, wer kann gegen uns sein? Gott hat seinen eigenen Sohn gegeben. Nichts – weder Tod noch Leben, weder Gegenwart noch Zukunft – kann uns von Gottes Liebe trennen.",
    bridge="Paulus gründet Gemeinden im ganzen Mittelmeerraum. Um 57 n. Chr. schreibt er an die Christen in Rom, die er noch nie besucht hat, seinen längsten Brief.",
    place="rom",
    quiz=[
        choice("Was kann uns laut Paulus von der Liebe Gottes trennen?", ["Nichts", "Nur der Tod", "Nur schwere Schuld", "Zweifel"],
               39, "Lies Vers 38–39.", "V. 38–39: Paulus zählt alles auf, was ihm einfällt – und sagt: Nichts davon."),
        tf("Paulus verspricht, dass Christen kein Leid erleben werden.", False, 35, "Lies Vers 35–36.",
           "V. 35–36: Er nennt Angst, Verfolgung, Hunger, sogar das Schwert. Leid bleibt – aber es kann nicht von Gottes Liebe trennen."),
    ],
    explain=[
        E("Warum fragt Paulus so viel?", "Er schreibt wie ein Redner vor Gericht: Wer klagt an? Wer verurteilt? Und gibt selbst die Antwort: Gott spricht gerecht, Christus tritt für uns ein (V. 33–34)."),
        E("Was sind „Fürstentümer“ und „Gewalten“?", "Unsichtbare Mächte, an die man damals glaubte – Geister, Schicksalsmächte, Sterne. Paulus sagt: Auch sie haben nicht das letzte Wort."),
    ],
    memory_verse=MV(R(45, 8, 31), "Wenn Gott für uns ist, wer gegen uns?"),
    teaser="Am Ende der Bibel sieht Johannes etwas, das zusammenführt, was mit einem Garten begann.")

sec("gemeinde", [R(66, 21, 1, 7)], "Alles neu",
    "Johannes sieht einen neuen Himmel und eine neue Erde und das neue Jerusalem. Gott wohnt bei den Menschen. Er wischt jede Träne ab; Tod, Trauer und Schmerz sind vorbei. Gott sagt: Siehe, ich mache alles neu.",
    bridge="Gegen Ende des 1. Jahrhunderts werden Christen im Römischen Reich verfolgt. Johannes, verbannt auf die Insel Patmos, sieht in Visionen, wohin Gottes Geschichte führt (Offb 1,9).",
    place="patmos",
    focus="Achte darauf, wo Gott am Ende wohnt.",
    quiz=[
        choice("Wo wohnt Gott am Ende?", ["Bei den Menschen", "Weit über dem Himmel", "Nur im Tempel", "In einer anderen Welt ohne Menschen"],
               3, "Vers 3.", "V. 3: Gottes Zelt ist bei den Menschen. Was im Garten Eden begann, wird vollendet."),
        error("Gott wird jede Träne abwischen, und das [Licht] wird nicht mehr sein, noch Trauer, noch Schmerz.", "der Tod", 4,
              "V. 4: Der Tod wird nicht mehr sein."),
    ],
    explain=[
        E("Wie liest man die Offenbarung?", "Die Offenbarung ist voller Bilder und Symbole, die Christen sehr verschieden deuten: als Blick auf die Zeit des Römischen Reiches, als Fahrplan der Endzeit oder als zeitlose Bilder für den Kampf zwischen Gut und Böse. Bei diesem Kapitel sind sich fast alle einig: Am Ende steht nicht die Zerstörung, sondern Gottes neue Welt."),
        E("Was heißt Alpha und Omega?", "Der erste und der letzte Buchstabe des griechischen Alphabets (V. 6) – wie „von A bis Z“. Gott steht am Anfang und am Ende der Geschichte."),
        E("Warum gibt es kein Meer mehr?", "Für Menschen der Antike war das Meer ein Bild für Chaos und Bedrohung. Dass es nicht mehr ist (V. 1), heißt: Nichts bedroht mehr das Leben."),
    ],
    cards=["neue-schoepfung"],
    memory_verse=MV(R(66, 21, 5), "Siehe, ich mache alles neu"),
    fact="Die Bibel endet, wie sie begann: mit einem Baum des Lebens und einem Strom (Offb 22,1–2; vgl. 1. Mose 2,9–10). Was im Garten verloren ging, wird in Gottes Stadt neu geschenkt.",
    prayer={"ref": R(66, 22, 20), "source": "Offenbarung 22,20 – der vorletzte Vers der Bibel"})

# rename try_ → try
for s in S:
    if "try_" in s: s["try"] = s.pop("try_")

PLAN = {
    "id": "grosse-geschichte",
    "title": "Die große Geschichte",
    "subtitle": "Der rote Faden der Bibel",
    "description": "In 44 kurzen Abschnitten von der Schöpfung bis zur neuen Schöpfung: die wichtigsten Stationen der Bibel und wie sie zusammenhängen. Danach hat jede biblische Geschichte ihren Platz.",
    "direction": "start",
    "basis": "elbbk",
    "stages": [{"id": i, "title": t} for i, t in STAGES],
    "cards": [{"id": i, "type": t, "name": n, "text": x, "refs": r} for i, t, n, x, r in CARDS],
    "sections": S,
}

out = pathlib.Path(__file__).resolve().parents[2] / "app/src/main/assets/plans/grosse-geschichte.json"
out.write_text(json.dumps(PLAN, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(S)} sections)")
