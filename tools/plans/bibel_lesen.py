#!/usr/bin/env python3
"""Source for the reading plan „Wie liest man die Bibel?“ (generates assets/plans/bibel-lesen.json).

python3 -I tools/plans/bibel_lesen.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/bibel-lesen.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

LK, JER, KOE2, NEH, TIM2, PETR2, PS, DTN, SPR, KOR1, APG, MT, JAK = 42, 24, 12, 16, 55, 61, 19, 5, 20, 46, 44, 40, 59

P = PlanBuilder(
    "bibel-lesen", "bl", "Wie liest man die Bibel?", "Entstehung, Gattungen, Auslegung",
    "Wer hat die Bibel geschrieben, wie ist sie zu uns gekommen – und warum liest man einen Psalm anders als einen Brief? "
    "19 Abschnitte, in denen die Bibel selbst zeigt, wie sie entsteht und wie Menschen sie lesen. Dazu, wie verschiedene Kirchen das verstehen.",
    "glauben",
    stages=[("entstehung", "Wie ein biblisches Buch entsteht"), ("selbst", "Was die Bibel über sich sagt"),
            ("gattungen", "Ein Psalm ist kein Brief"), ("lesen", "Gemeinsam lesen")],
    cards=[
        ("lukas", "person", "Lukas", "Arzt und Reisebegleiter des Paulus (Kol 4,14). Die Kirche schreibt ihm seit dem 2. Jahrhundert das Lukasevangelium und die Apostelgeschichte zu; beide sind an Theophilus gerichtet. Er war wohl kein Augenzeuge des Lebens Jesu; nach Lk 1,2 stützt er sich auf die, die es von Anfang an waren.", "Lk 1,1–4; Apg 1,1; Kol 4,14"),
        ("baruk", "person", "Baruk", "Sohn Nerijas, Schreiber und Vertrauter des Propheten Jeremia. Er schrieb Jeremias Worte nach Diktat auf, las sie öffentlich vor und musste sich danach verstecken. Später ging er mit Jeremia nach Ägypten. Nach ihm ist das deuterokanonische Buch Baruch benannt.", "Jer 36; 43,6; 45"),
        ("schriftrolle", "begriff", "Schriftrolle", "Das „Buch“ der Bibelzeit: Blätter aus Papyrus oder Tierhaut, aneinandergenäht, in Spalten beschrieben und aufgerollt. Die große Jesaja-Rolle aus Qumran ist über 7 Meter lang. Das gebundene Buch (Kodex) setzte sich erst in den ersten Jahrhunderten nach Christus durch – Christen benutzten es besonders früh.", "Jer 36,2.23; Lk 4,17"),
        ("josia", "person", "Josia", "König von Juda (etwa 640–609 v. Chr.), mit acht Jahren auf den Thron gekommen. Nach dem Fund des Gesetzbuches erneuerte er den Gottesdienst und ließ die Götzenbilder im Land entfernen. Er fiel bei Megiddo im Kampf gegen Pharao Necho. Jeremia begann unter ihm als Prophet.", "2Kön 22–23; Jer 1,2"),
        ("esra", "person", "Esra", "Priester und Schriftgelehrter. Er kam im 5. Jahrhundert v. Chr. aus Babylon nach Jerusalem, um das Volk im Gesetz zu unterweisen. Die jüdische Überlieferung sieht in ihm eine Art zweiten Mose, der die Tora neu ins Leben des Volkes brachte.", "Esr 7; Neh 8"),
        ("inspiration", "begriff", "Inspiration", "Von lateinisch inspirare, „einhauchen“, nach 2Tim 3,16 (griechisch theopneustos, „gottgehaucht“). Christen aller Konfessionen bekennen, dass Gott durch die Schrift spricht. Wie das geschieht – Wort für Wort, durch die Persönlichkeit der Verfasser oder im ganzen Weg der Überlieferung – und worauf sich die Irrtumslosigkeit bezieht, beschreiben sie unterschiedlich.", "2Tim 3,16; 2Petr 1,21"),
        ("tanach", "begriff", "Tanach", "Jüdischer Name der hebräischen Bibel, aus den Anfangsbuchstaben ihrer drei Teile: Tora (Weisung, die fünf Bücher Mose), Nevi’im (Propheten, dazu gehören auch Josua bis Könige) und Ketuvim (Schriften, beginnend mit den Psalmen). Dieselben Bücher wie das evangelische Alte Testament, aber als 24 gezählt und anders geordnet.", "Lk 24,44"),
        ("kanon", "begriff", "Kanon", "Griechisch „Richtschnur“: die Liste der Bücher, die als Heilige Schrift gelten. Die 27 Bücher des Neuen Testaments nennt als Erster Athanasius im Jahr 367 genau in dieser Zusammenstellung; vorher waren einige (z. B. Hebräer, Offenbarung) umstritten. Christen beschreiben das meist nicht als Festlegen, sondern als Erkennen, welche Bücher sich als Schrift erwiesen hatten.", "2Petr 3,16"),
        ("spaetschriften", "begriff", "Spätschriften", "Bücher wie Tobit, Judit, Weisheit, Jesus Sirach und die Makkabäerbücher. Sie stehen in der Septuaginta, nicht in der hebräischen Bibel. Für die katholische und die orthodoxe Kirche gehören sie zum Alten Testament („deuterokanonisch“). Luther übersetzte sie als „Apokryphen“: nützlich und gut zu lesen, aber der Schrift nicht gleich. Die meisten Freikirchen lassen sie weg.", ""),
        ("parallelismus", "begriff", "Parallelismus", "Hebräische Poesie reimt keine Klänge, sondern Gedanken: Die zweite Zeile wiederholt, steigert oder kontrastiert die erste – etwa in Ps 119,105: Leuchte und Licht, Fuß und Pfad. Deshalb lässt sich ein Psalm in andere Sprachen übersetzen, ohne seine Form ganz zu verlieren.", "Ps 18; Ps 119,105"),
        ("prophet", "begriff", "Prophet", "Hebräisch nabi, wohl „Berufener“ oder „Sprecher“. Propheten richten Gottes Wort an ihre eigene Zeit: Anklage, Mahnung, Trost und Ankündigung. Vorhersagen sind ein Teil davon, oft an die Reaktion der Hörer gebunden. Die hebräische Bibel zählt auch die Geschichtsbücher Josua bis Könige zu den „Propheten“.", "Jer 18,1–10"),
        ("septuaginta", "begriff", "Septuaginta", "Die griechische Übersetzung des Alten Testaments, ab dem 3. Jahrhundert v. Chr. in Alexandria entstanden. Der Name („siebzig“) stammt von der Legende der 72 Übersetzer. Die Apostel zitieren das AT meist nach ihr. Augustinus hielt auch die Übersetzer für vom Geist geführt; die orthodoxe Kirche liest ihr Altes Testament bis heute nach der Septuaginta.", "Apg 8,32–33"),
        ("handschriften", "begriff", "Handschriften", "Von keinem biblischen Buch ist die Urschrift erhalten, aber eine Fülle von Abschriften, allein über 5.000 griechische des Neuen Testaments. Die große Jesaja-Rolle aus Qumran (um 125 v. Chr.) ist rund 1.000 Jahre älter als die vorher bekannten hebräischen Handschriften und stimmt weitgehend mit ihnen überein.", "Apg 8,37"),
        ("schrift-tradition", "begriff", "Schrift und Tradition", "Wer legt die Bibel verbindlich aus? Evangelische Kirchen und Freikirchen: „Allein die Schrift“ ist oberster Maßstab, Tradition wird an ihr geprüft. Katholische Kirche: Schrift und Überlieferung gehören zusammen, das Lehramt legt sie verbindlich aus. Orthodoxe Kirche: Die Schrift ist das Herzstück der Überlieferung, die in Konzilien, Kirchenvätern und Gottesdienst lebt.", "Apg 17,11; 2Thess 2,15"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Wie ein biblisches Buch entsteht ─────────────────────────
sec("entstehung", [R(LK, 1, 1, 4)], "Der Reihe nach",
    "Lukas schreibt an Theophilus: Viele haben schon über Jesus berichtet. Er selbst ist allem von Anfang an genau nachgegangen und schreibt es der Reihe nach auf.",
    bridge="Dieser Plan beginnt nicht mit Theorie, sondern mit Stellen, an denen die Bibel selbst zeigt, wie sie entsteht und wie Menschen sie lesen. Den Anfang machen vier Verse, die Lukas seinem Evangelium voranstellt.",
    focus="Achte darauf, was Lukas über seine Quellen sagt.",
    quiz=[
        choice("Woher hat Lukas sein Wissen?", ["Von Augenzeugen und Dienern des Wortes", "Aus einem Traum", "Aus den Archiven des Tempels", "Von Jesus selbst"], 2, "Lies Vers 2.",
               "V. 2–3: von denen, die von Anfang an Augenzeugen waren – und er ist allem genau nachgegangen."),
        tf("Lukas sagt, er sei der Erste, der einen Bericht über Jesus schreibt.", False, 1, "Lies Vers 1.",
           "V. 1: Viele haben es schon unternommen. Lukas kennt also frühere Berichte."),
        choice("Wozu schreibt Lukas?", ["Damit Theophilus die Zuverlässigkeit dessen erkennt, worin er unterrichtet wurde", "Damit Theophilus zum ersten Mal von Jesus hört", "Damit die früheren Berichte ersetzt werden", "Damit der Text im Gottesdienst gelesen wird"], 4, "Lies Vers 4.",
               "V. 4: Theophilus ist schon unterrichtet worden. Lukas will, dass er erkennt, wie zuverlässig das ist."),
    ],
    explain=[
        E("Wer war Theophilus?", "Das weiß man nicht. Der Name bedeutet „Gottesfreund“. Die Anrede „vortrefflichster“ benutzt Lukas sonst für hohe römische Beamte (Apg 23,26; 26,25). Vielleicht war Theophilus ein Förderer, der die Abschrift des Buches bezahlte."),
        E("Was heißt „der Reihe nach“?", "Griechisch kathexēs, „geordnet, im Zusammenhang“. Das muss nicht streng zeitlich heißen: Lukas ordnet manche Ereignisse anders als Markus oder Matthäus."),
    ],
    cards=["lukas"],
    fact="Lukas hat auch die Apostelgeschichte geschrieben. Zusammen machen seine beiden Bücher mehr als ein Viertel des Neuen Testaments aus – mehr als die Briefe des Paulus.",
    teaser="Ein König hört einem Text zu – und schneidet ihn Stück für Stück ab.")

sec("entstehung", [R(JER, 36, 1, 8)], "Die erste Rolle",
    "Gott beauftragt Jeremia, alle Worte, die er bisher empfangen hat, auf eine Rolle zu schreiben. Jeremia diktiert, sein Schreiber Baruk schreibt und liest die Rolle im Tempel vor.",
    bridge="Jeremia ist Prophet in Jerusalem, kurz bevor die Babylonier die Stadt erobern. Er hat schon über zwanzig Jahre lang öffentlich gesprochen – bisher nur mündlich.",
    place="jerusalem",
    quiz=[
        choice("Wer schreibt die Worte auf?", ["Baruk", "Jeremia selbst", "Ein Schreiber des Königs", "Ein Priester des Tempels"], 4, "Lies Vers 4.",
               "V. 4: Jeremia diktiert, Baruk schreibt aus seinem Mund."),
        tf("Jeremia liest die Rolle selbst im Tempel vor.", False, 5, "Lies Vers 5–6.",
           "V. 5–6: Jeremia ist verhindert und darf nicht in den Tempel. Baruk liest an seiner Stelle."),
        choice("Welche Hoffnung steht hinter dem Aufschreiben?", ["Dass das Volk umkehrt und Gott vergeben kann", "Dass der König Jeremia freilässt", "Dass die Worte für spätere Generationen erhalten bleiben", "Dass Babel davon erfährt"], 3, "Lies Vers 3.",
               "V. 3 (und V. 7): vielleicht hören sie und kehren um, damit Gott vergibt."),
    ],
    explain=[
        E("Wann war das?", "Im 4. Jahr Jojakims, also 605/604 v. Chr. – das Jahr, in dem Nebukadnezar von Babel die Ägypter bei Karkemisch besiegte. Jeremia war seit dem 13. Jahr Josias Prophet (Jer 1,2), etwa seit 627 v. Chr."),
        E("Warum darf Jeremia nicht in den Tempel?", "Der Text sagt nur, dass er verhindert ist. Kurz vorher hatte er im Tempel die Zerstörung des Tempels angekündigt und war nur knapp dem Tod entgangen (Jer 26). Vielleicht hatte man ihm den Zutritt verboten."),
    ],
    cards=["baruk", "schriftrolle"],
    fact="In den 1970er-Jahren tauchte auf dem Antikenmarkt ein Tonsiegel mit der Aufschrift „Berechjahu, Sohn des Nerijahu, der Schreiber“ auf – möglicherweise Baruks Siegel. Ob es echt ist, ist heute allerdings umstritten.",
    teaser="Was macht ein König mit einem Text, der ihm nicht gefällt?")

sec("entstehung", [R(JER, 36, 21, 28), R(JER, 36, 32)], "Die zweite Rolle",
    "König Jojakim lässt sich die Rolle vorlesen, schneidet sie Stück für Stück ab und verbrennt sie. Gott lässt Jeremia alles noch einmal aufschreiben – und es kommen weitere Worte hinzu.",
    bridge="Die Hofbeamten haben die Rolle gehört und sind erschrocken. Sie raten Baruk und Jeremia, sich zu verstecken, und berichten dem König (Jer 36,9–20).",
    place="jerusalem",
    quiz=[
        order("Bring die Ereignisse in die richtige Reihenfolge.",
              ["Jehudi liest dem König vor", "Der König zerschneidet die Rolle und verbrennt sie", "Der König will Baruk und Jeremia festnehmen lassen", "Gott beauftragt Jeremia mit einer neuen Rolle"],
              "V. 21–28: Vorlesen, Verbrennen, Haftbefehl – und dann der Auftrag zur neuen Rolle."),
        tf("Einige Berater baten den König, die Rolle nicht zu verbrennen.", True, 25, "Lies Vers 25.",
           "V. 25: Elnathan, Delaja und Gemarja – aber er hört nicht auf sie."),
        choice("Was ist an der zweiten Rolle anders?", ["Es kommen noch viele Worte gleichen Inhalts hinzu", "Sie ist kürzer als die erste", "Sie wird im Tempel versteckt", "Jeremia schreibt sie selbst"], 32, "Lies Vers 32.",
               "V. 32: Baruk schreibt alles noch einmal – und viele ähnliche Worte werden hinzugefügt."),
    ],
    explain=[
        E("Warum betont der Text, dass sie nicht erschrecken?", "Kleider zerreißen war ein Zeichen von Entsetzen, Trauer oder Buße. V. 24 hält fest, dass genau das beim König und seinen Leuten ausbleibt."),
        E("Was sagt V. 32 über das Buch Jeremia?", "Es ist nicht in einem Zug entstanden: Es gab mindestens zwei Fassungen der Rolle, die zweite war länger. Die Septuaginta überliefert Jeremia sogar in einer kürzeren Fassung mit anderer Reihenfolge. In Qumran fand man hebräische Handschriften beider Formen."),
        E("Wie verstehen Gläubige so ein Wachsen?", "Viele Christen sehen auch das Ergänzen, Sammeln und Abschreiben als Teil von Gottes Wirken: Er war nicht nur beim ersten Diktat dabei, sondern auf dem ganzen Weg des Textes. Andere legen den Ton auf die endgültige Gestalt, die die Gemeinde als Schrift angenommen hat. Beide Sichtweisen rechnen mit Gottes Führung."),
    ],
    cards=[],
    teaser="Ein Buch, das jahrzehntelang niemand gelesen hat, taucht bei Bauarbeiten wieder auf.")

sec("entstehung", [R(KOE2, 22, 8, 13)], "Das gefundene Buch",
    "Bei Bauarbeiten am Tempel findet der Hohepriester Hilkija das Buch des Gesetzes. Als König Josia es vorgelesen bekommt, zerreißt er seine Kleider und lässt Gott befragen.",
    bridge="Knapp 20 Jahre vor Jeremias Rolle: Josia, der Vater Jojakims, lässt den verfallenen Tempel ausbessern (2Kön 22,3–7).",
    place="jerusalem",
    quiz=[
        who("Ich habe das Buch des Gesetzes im Haus des HERRN gefunden.", R(KOE2, 22, 8), ["Hilkija", "Schaphan", "Josia", "Jeremia"],
            "V. 8: Der Hohepriester Hilkija gibt das Buch dem Schreiber Schaphan."),
        choice("Wie reagiert Josia, als er das Buch hört?", ["Er zerreißt seine Kleider", "Er lässt es verbrennen", "Er lässt es ins Archiv bringen", "Er zweifelt an seiner Echtheit"], 11, "Lies Vers 11.",
               "V. 11: Er zerreißt seine Kleider – genau das, was sein Sohn Jojakim später nicht tut (Jer 36,24)."),
        tf("Josia meint, Gottes Zorn komme daher, dass die Väter nicht nach diesem Buch gehandelt haben.", True, 13, "Lies Vers 13.",
           "V. 13: Die Väter haben nicht auf die Worte dieses Buches gehört."),
    ],
    explain=[
        E("Was war das für ein Buch?", "Der Text nennt es „Buch des Gesetzes“. Schon Kirchenväter wie Hieronymus vermuteten, dass es das 5. Buch Mose oder ein Teil davon war, weil Josias Reformen in Kapitel 23 dessen Geboten entsprechen. Sicher wissen kann man es nicht."),
        E("Wie kann ein Gesetzbuch verloren gehen?", "Die Bibel erzählt es nicht. Unter Josias Großvater Manasse wurden jahrzehntelang fremde Götter verehrt, sogar im Tempel (2Kön 21,1–9)."),
    ],
    cards=["josia"],
    teaser="Ein ganzes Volk steht einen halben Tag lang und hört zu – und dann weinen alle.")

sec("entstehung", [R(NEH, 8, 1, 12)], "Lesen und erklären",
    "Das ganze Volk versammelt sich, und Esra liest vom Morgen bis zum Mittag aus dem Gesetz vor. Die Leviten erklären den Sinn. Das Volk weint – doch Nehemia und Esra sagen: Heute ist ein Festtag.",
    bridge="Über 170 Jahre später: Jerusalem wurde zerstört, das Volk lebte im Exil in Babylon. Nach der Rückkehr sind die Stadtmauern gerade wieder aufgebaut (Neh 6,15).",
    place="jerusalem",
    quiz=[
        choice("Was tun die Leviten?", ["Sie lesen deutlich vor und geben den Sinn an", "Sie singen Psalmen", "Sie bewachen das Wassertor", "Sie schreiben das Gesetz ab"], 8, "Lies Vers 7–8.",
               "V. 8: Sie lesen deutlich und erklären, so dass man das Gelesene versteht."),
        tf("Nehemia und Esra fordern das Volk auf, zu fasten und zu trauern.", False, 10, "Lies Vers 9–10.",
           "V. 9–10: Im Gegenteil – sie sollen essen, trinken und denen etwas schicken, die nichts haben."),
        choice("Warum feiert das Volk am Ende?", ["Weil es die Worte verstanden hat", "Weil die Mauer fertig ist", "Weil der König es befohlen hat", "Weil die Ernte gut war"], 12, "Lies Vers 12.",
               "V. 12: Sie feiern, denn sie hatten die Worte verstanden, die man ihnen mitgeteilt hatte."),
    ],
    explain=[
        E("Was heißt „gaben den Sinn an“?", "Das hebräische Wort ist nicht ganz eindeutig: deutlich, abschnittweise vorlesen oder erklären. Die jüdische Tradition (Talmud, Megilla 3a) sieht hier den Anfang der Übersetzung ins Aramäische – viele Rückkehrer verstanden Aramäisch besser als Hebräisch."),
        E("Wer waren die Leviten?", "Nachkommen des Stammes Levi, zuständig für den Dienst am Tempel. Sie hatten auch die Aufgabe, das Volk im Gesetz zu unterweisen (5Mo 33,10; 2Chr 17,7–9)."),
    ],
    cards=["esra"],
    fact="Bis heute wird in vielen Synagogen die Torarolle nach der Lesung hochgehoben und der stehenden Gemeinde gezeigt – ganz ähnlich wie in V. 5.",
    teaser="Ein einziges griechisches Wort, das im ganzen Neuen Testament nur einmal vorkommt.")

# ───────────────────────── 2 · Was die Bibel über sich sagt ─────────────────────────
sec("selbst", [R(TIM2, 3, 14, 17)], "Von Gott eingegeben",
    "Paulus erinnert Timotheus an die heiligen Schriften, die er von Kind auf kennt: Alle Schrift ist von Gott eingegeben und nützlich zur Lehre, zur Überführung, zur Zurechtweisung und zur Erziehung.",
    bridge="Neue Etappe. Paulus schreibt aus der Haft in Rom an seinen jungen Mitarbeiter Timotheus – nach der Überlieferung sein letzter Brief.",
    quiz=[
        choice("Seit wann kennt Timotheus die heiligen Schriften?", ["Von Kind auf", "Seit er Paulus kennt", "Seit seiner Taufe", "Seit seiner Zeit in Jerusalem"], 15, "Lies Vers 15.",
               "V. 15: von Kind auf. Nach 2Tim 1,5 hatten seine Mutter Eunike und seine Großmutter Lois denselben Glauben."),
        choice("Wozu können die Schriften laut V. 15 weise machen?", ["Zur Rettung durch den Glauben an Christus Jesus", "Zur Erkenntnis der Zukunft", "Zum Erfolg im Leben", "Zum Streitgespräch mit Gelehrten"], 15, "Lies Vers 15.",
               "V. 15: weise zur Rettung (Seligkeit) durch den Glauben, der in Christus Jesus ist."),
    ],
    explain=[
        E("Was heißt „von Gott eingegeben“?", "Griechisch theopneustos, wörtlich „gottgehaucht“ – das Wort kommt im Neuen Testament nur hier vor. Mit „Schrift“ meint Paulus zunächst die heiligen Schriften, die Timotheus von Kind auf kennt, also das Alte Testament. Christen haben das später auch auf das Neue Testament bezogen."),
        E("Wie verstehen evangelikale Christen Inspiration?", "Die Chicago-Erklärung (1978), wichtig für viele Freikirchen: Gott hat die Verfasser so geleitet, dass die Urschriften in allem, was sie behaupten, ohne Irrtum sind – auch in Geschichte und Natur, recht verstanden nach ihrer Gattung. Andere Evangelikale sprechen lieber von Unfehlbarkeit in Fragen des Glaubens und Lebens. Die Lausanner Verpflichtung (1974) verbindet beides: ohne Irrtum in allem, was sie bekräftigt, und einzige unfehlbare Richtschnur für Glauben und Leben."),
        E("Wie verstehen katholische und orthodoxe Christen Inspiration?", "Das Zweite Vatikanische Konzil (Dei Verbum 11, 1965): Gott ist Urheber der Schrift, und die Menschen sind echte Verfasser, die ihre eigenen Fähigkeiten gebrauchten. Die Schrift lehrt sicher, treu und ohne Irrtum die Wahrheit, die Gott um unseres Heiles willen aufgezeichnet haben wollte. Orthodoxe Christen sehen den Geist, der die Schrift eingab, auch darin am Werk, wie die Kirche sie bewahrt, sammelt und im Gottesdienst liest."),
        E("Gibt es eine Sicht, die den ganzen Weg der Bibel einschließt?", "Ja, in mehreren Traditionen: Die Botschaft, die Gott vermitteln will, ist verlässlich und ohne Irrtum – nicht unbedingt das Weltbild der Zeit, in dem sie gesagt ist. Und Gott hat nicht nur die ersten Worte gegeben, sondern auch Sammeln, Abschreiben und Übersetzen begleitet. Bausteine dafür sind Dei Verbum 11–12, Calvins Gedanke der „Anpassung“ (Gott redet in der Sprache der Menschen), das Westminster-Bekenntnis (1647, 1,8: Gottes Fürsorge hat den Text durch die Zeiten bewahrt) und Augustinus, der auch die Übersetzer der Septuaginta für vom Geist geführt hielt."),
    ],
    cards=["inspiration"],
    teaser="Petrus gibt zu, dass ihm Paulus manchmal zu kompliziert ist.")

sec("selbst", [R(PETR2, 1, 16, 21), R(PETR2, 3, 15, 16)], "Keine Fabeln",
    "Petrus betont: Wir sind keinen erfundenen Geschichten gefolgt, wir waren Augenzeugen. Prophetie kam nicht aus menschlichem Willen. Und: In den Briefen des Paulus ist manches schwer zu verstehen.",
    quiz=[
        choice("Welches Erlebnis nennt Petrus als Augenzeuge?", ["Die Stimme vom Himmel auf dem heiligen Berg", "Die Speisung der Fünftausend", "Die Kreuzigung", "Das Pfingstfest"], 17, "Lies Vers 17–18.",
               "V. 17–18: die Stimme, die Jesus seinen geliebten Sohn nannte – auf dem heiligen Berg."),
        choice("Womit vergleicht Petrus das prophetische Wort?", ["Mit einer Lampe an einem dunklen Ort", "Mit einem zweischneidigen Schwert", "Mit Brot für die Seele", "Mit einem Spiegel"], 19, "Lies Vers 19.",
               "V. 19: wie eine Lampe, die an einem dunklen Ort leuchtet, bis der Tag anbricht."),
        tf("Petrus schreibt, dass die Briefe des Paulus leicht zu verstehen seien.", False, None, "Lies 3,16.",
           "3,16: Einiges darin ist schwer zu verstehen, und manche verdrehen es."),
    ],
    explain=[
        E("Welcher heilige Berg?", "Der Berg der Verklärung Jesu (Mk 9,2–8). Die Überlieferung nennt den Berg Tabor in Galiläa; manche Ausleger denken an den Hermon."),
        E("„Keine Weissagung ist von eigener Auslegung“?", "Zwei Lesarten: (1) Prophetie stammt nicht aus der eigenen Deutung des Propheten – so begründet es V. 21. (2) Kein Leser soll die Schrift eigenmächtig auslegen. Die katholische Tradition hat die Stelle oft auf die Auslegung in der Kirche bezogen, evangelische Ausleger betonen meist die erste Lesart."),
        E("„Wie auch die übrigen Schriften“", "3,16 stellt die Briefe des Paulus neben „die übrigen Schriften“. Das ist eine der frühesten Stellen, an der christliche Texte neben das Alte Testament gestellt werden."),
    ],
    cards=["kanon"],
    teaser="Jesus nennt drei Teile der Schrift – eine Einteilung, die bis heute in jeder jüdischen Bibel steht.")

sec("selbst", [R(LK, 24, 25, 27), R(LK, 24, 44, 47)], "Mose, Propheten, Psalmen",
    "Der Auferstandene erklärt zwei Jüngern auf dem Weg nach Emmaus, was in allen Schriften über ihn steht. Später öffnet er allen Jüngern das Verständnis für die Schriften.",
    bridge="Am Ostertag sind zwei Jünger auf dem Weg nach Emmaus. Jesus geht mit, aber sie erkennen ihn nicht (Lk 24,13–24). Am Abend erscheint er allen Jüngern in Jerusalem.",
    place="emmaus",
    quiz=[
        choice("Womit beginnt Jesus seine Erklärung?", ["Mit Mose und allen Propheten", "Mit den Psalmen", "Mit seinen eigenen Gleichnissen", "Mit den Worten Johannes des Täufers"], 27, "Lies Vers 27.",
               "V. 27: von Mose und allen Propheten anfangend, in allen Schriften."),
        choice("Welche drei Teile der Schrift nennt Jesus in V. 44?", ["Gesetz Moses, Propheten und Psalmen", "Gesetz, Geschichte und Weisheit", "Mose, Könige und Propheten", "Tora, Talmud und Psalmen"], 44, "Lies Vers 44.",
               "V. 44: das Gesetz Moses, die Propheten und die Psalmen."),
    ],
    explain=[
        E("Warum diese drei Teile?", "Die hebräische Bibel hat drei Teile: Tora, Propheten und Schriften. Die Psalmen sind das erste und größte Buch der Schriften – vielleicht steht das Wort hier für den ganzen dritten Teil."),
        E("Wie lesen Christen das Alte Testament von Jesus her?", "Die Kirchenväter fanden Christus in vielen Vorbildern (z. B. Passahlamm, Isaak). Die Reformatoren betonten den Wortsinn und fragten mit Luther, „was Christum treibet“. Dispensationalisten unterscheiden genau, was Israel und was der Gemeinde gilt. Jüdische Leser lesen dieselben Texte ohne Bezug auf Jesus."),
    ],
    cards=["tanach", "spaetschriften"],
    teaser="Ein Gebet, das alle Buchstaben des hebräischen Alphabets durchgeht – achtmal jeden.")

sec("selbst", [R(PS, 119, 97, 105)], "Süßer als Honig",
    "Der Beter beschreibt, was Gottes Weisung für ihn ist: Nachsinnen den ganzen Tag, Quelle von Einsicht, süßer als Honig, eine Leuchte für den Weg.",
    quiz=[
        error("Der Beter sinnt den ganzen [Abend] über Gottes Gesetz nach.", "Tag", 97,
              "V. 97: Es ist sein Sinnen den ganzen Tag."),
        tf("Der Beter sagt, er sei verständiger als alle seine Lehrer.", True, 99, "Lies Vers 99.",
           "V. 99 – und V. 100: mehr Einsicht als die Alten."),
        choice("Womit vergleicht er Gottes Worte in V. 103?", ["Mit Honig", "Mit Gold", "Mit frischem Wasser", "Mit Brot"], 103, "Lies Vers 103.",
               "V. 103: süßer als Honig für den Mund."),
    ],
    explain=[
        E("Was ist das Besondere an Psalm 119?", "Er ist der längste Psalm (176 Verse) und ein Alphabet-Gedicht: 22 Strophen zu je 8 Versen, und alle Verse einer Strophe beginnen mit demselben hebräischen Buchstaben. V. 97–104 ist die Strophe „Mem“, V. 105 beginnt „Nun“. In fast jedem Vers steht ein Wort für Gottes Wort: Gesetz, Gebote, Zeugnisse, Vorschriften."),
        E("Welches „Gesetz“ meint der Beter?", "Hebräisch Tora, „Weisung“ – mehr als Paragrafen: Gottes Anleitung zum Leben, damals vor allem die fünf Bücher Mose."),
    ],
    cards=["parallelismus"],
    fact="Die Öllampen der Bibelzeit waren kleine Tonschalen mit einem Docht. Ihr Licht reichte für wenige Schritte.",
    memory_verse=MV(R(PS, 119, 105), "Dein Wort ist Leuchte meinem Fuß und Licht für meinen Pfad."),
    prayer={"ref": R(PS, 119, 18), "source": "Psalm 119,18"},
    teaser="Gott reitet auf einem Cherub, und aus seiner Nase steigt Rauch. Wie liest man so etwas?")

# ───────────────────────── 3 · Ein Psalm ist kein Brief ─────────────────────────
sec("gattungen", [R(PS, 18, 7, 17)], "Rauch aus seiner Nase",
    "David beschreibt seine Rettung als gewaltigen Auftritt Gottes: Die Erde bebt, Feuer und Gewitter, Gott fährt auf einem Cherub herab und zieht ihn aus großen Wassern.",
    bridge="Neue Etappe: Die Bibel enthält Erzählungen, Gesetze, Lieder, Sprichwörter, Prophetie, Gleichnisse und Briefe. Jede Art von Text liest sich anders. Psalm 18 ist laut Überschrift ein Lied Davids nach seiner Rettung vor Saul und allen Feinden.",
    focus="Achte darauf, worum der Beter in V. 7 bittet – und was am Ende geschieht.",
    quiz=[
        choice("Wovon erzählt das Lied, wenn man V. 7 und V. 17–18 nebeneinanderlegt?", ["Gott rettet den Beter vor seinen Feinden", "Ein Erdbeben zerstört Jerusalem", "Gott erschafft die Welt", "Ein Unwetter vernichtet die Ernte"], 18, "Lies Vers 7 und 17–18.",
               "V. 7: Er schreit in der Not zu Gott. V. 17–18: Gott zieht ihn heraus und rettet ihn vor seinen Feinden."),
        tf("Der Beter sagt, seine Feinde seien stärker gewesen als er.", True, 18, "Lies Vers 18.",
           "V. 18: Sie waren mächtiger als ich."),
    ],
    explain=[
        E("Ist das wörtlich gemeint?", "Psalm 18 ist Poesie. Die Bilder – Rauch, Feuer, Beben, Dunkel – kennt man auch vom Sinai (2Mo 19,16–18). Ausleger fast aller Traditionen lesen sie als Ausdruck dafür, wie David seine Rettung erlebt hat, nicht als Bericht über ein bestimmtes Gewitter."),
        E("Was ist ein Cherub?", "Ein Himmelswesen, Mehrzahl Cherubim. Cherubim bewachen den Weg zum Baum des Lebens (1Mo 3,24), stehen als Figuren auf der Bundeslade (2Mo 25,18–22) und tragen in Hesekiels Vision Gottes Thron (Hes 10)."),
        E("Wie gehen Christen mit Naturbildern in der Bibel um?", "Calvin sprach von „Anpassung“: Gott redet in der Sprache und Vorstellungswelt der Menschen, wie eine Amme mit einem kleinen Kind. Galilei zitierte 1615 Kardinal Baronius: Der Heilige Geist wolle lehren, wie man in den Himmel kommt, nicht wie der Himmel sich bewegt. Die Chicago-Erklärung betont dagegen, dass auch Aussagen über Natur und Geschichte irrtumslos sind, wenn man sie nach ihrer Gattung liest. Wo genau ein Bild ein Bild ist – etwa bei 1. Mose 1–3 –, beantworten Christen unterschiedlich."),
    ],
    fact="Psalm 18 steht fast wortgleich noch einmal in 2. Samuel 22 – mit vielen kleinen Unterschieden. Schon die Bibel selbst überliefert also manche Texte in zwei Fassungen.",
    try_="Öffne in „Frei lesen“ Psalm 18 und 2. Samuel 22 und vergleiche die Verse 8–16. Wie viele Unterschiede findest du?",
    teaser="Ein Gesetz über Vogelnester – und eins über Geländer auf dem Dach.")

sec("gattungen", [R(DTN, 22, 1, 8)], "Ein Geländer ums Dach",
    "Eine Reihe kurzer Gebote: verlaufene Tiere des Nachbarn zurückbringen, beim Aufrichten helfen, die Vogelmutter fliegen lassen, ein Geländer ums Dach bauen.",
    bridge="Das 5. Buch Mose gibt sich als Rede Moses an Israel, kurz bevor das Volk in das versprochene Land zieht.",
    focus="Achte darauf, welche Gründe der Text selbst für die Gebote nennt.",
    quiz=[
        choice("Was soll man tun, wenn der Besitzer eines verlaufenen Rindes weit weg wohnt?", ["Das Tier aufnehmen, bis er es sucht", "Es nach sieben Tagen behalten", "Es zum Priester bringen", "Es laufen lassen"], 2, "Lies Vers 2.",
               "V. 2: ins eigene Haus aufnehmen, bis der Besitzer es sucht, und dann zurückgeben."),
        choice("Welchen Grund nennt V. 8 für das Geländer?", ["Damit keine Blutschuld aufs Haus kommt, wenn jemand herunterfällt", "Damit das Haus schöner aussieht", "Damit niemand aufs Dach steigt", "Damit man dort ungestört beten kann"], 8, "Lies Vers 8.",
               "V. 8: Wer kein Geländer baut, ist mitschuldig, wenn jemand abstürzt."),
        tf("Bei dem Vogelnest erlaubt das Gebot, die Jungen zu nehmen.", True, 7, "Lies Vers 6–7.",
           "V. 7: Die Mutter soll man fliegen lassen, die Jungen darf man nehmen."),
    ],
    explain=[
        E("Warum ein Geländer auf dem Dach?", "Häuser hatten Flachdächer, die man benutzte: zum Trocknen von Flachs (Jos 2,6), zum Schlafen in heißen Nächten, zum Beten (Apg 10,9)."),
        E("Wie lesen Christen diese Gebote heute?", "Reformierte Tradition (schon Thomas von Aquin): Das Gesetz enthält Moralgebote, die bleiben, und Kult- und Rechtsvorschriften für Israel, deren Grundsatz weiter zählt. Lutherische Tradition: Das Gesetz zeigt, was Gott will, und treibt zu Christus. Dispensationalisten: Das Gesetz des Mose galt Israel, die Gemeinde lebt unter dem „Gesetz Christi“. Im Judentum gelten die Gebote weiter und werden ausgelegt."),
        E("Und V. 5 – Kleidung?", "Was genau gemeint war, ist unsicher. Manche denken an Täuschung, andere an Bräuche fremder Kulte, wieder andere an die Unterscheidung der Geschlechter überhaupt. Wie man das heute anwendet, sehen Christen unterschiedlich."),
    ],
    fact="Die jüdische Tradition zählt in den fünf Büchern Mose 613 Gebote (Talmud, Makkot 23b).",
    teaser="Zwei Sprichwörter direkt hintereinander – und sie sagen das Gegenteil.")

sec("gattungen", [R(SPR, 26, 1, 12)], "Antworte dem Toren",
    "Eine Reihe von Sprüchen über den Toren. V. 4 rät: Antworte ihm nicht. V. 5 rät: Antworte ihm.",
    bridge="Das Buch der Sprüche sammelt Lebensweisheit, vieles davon wird König Salomo zugeschrieben. Kapitel 26 gehört zu einer Sammlung, die die Männer Hiskias abgeschrieben haben (Spr 25,1).",
    quiz=[
        choice("Welchen Grund nennt V. 4, dem Toren nicht zu antworten?", ["Damit du ihm nicht gleich wirst", "Weil er sowieso nicht zuhört", "Weil Gott ihn richten wird", "Damit kein Streit entsteht"], 4, "Lies Vers 4.",
               "V. 4: damit nicht auch du ihm gleich wirst."),
        choice("Und welchen Grund nennt V. 5, ihm doch zu antworten?", ["Damit er sich nicht selbst für weise hält", "Damit er umkehrt", "Damit andere daraus lernen", "Damit du recht behältst"], 5, "Lies Vers 5.",
               "V. 5: damit er nicht weise ist in seinen eigenen Augen."),
        choice("Für wen gibt es laut V. 12 noch weniger Hoffnung als für einen Toren?", ["Für den, der sich selbst für weise hält", "Für den Faulen", "Für den Spötter", "Für den, der flucht"], 12, "Lies Vers 12.",
               "V. 12: für den, der in seinen eigenen Augen weise ist."),
    ],
    explain=[
        E("Ein Widerspruch?", "Die Sammler haben die beiden Sprüche bewusst nebeneinandergestellt. Die Rabbinen diskutierten das (Talmud, Schabbat 30b) und lösten es so: Der eine gelte für Fragen der Tora, der andere für alltägliche Dinge. Viele christliche Ausleger sagen: Die Sprüche nennen zwei Gefahren, und welche gerade größer ist, muss man selbst erkennen."),
        E("Sind Sprichwörter Versprechen?", "Sprüche beschreiben, wie das Leben in der Regel läuft. Fast alle Ausleger lesen sie nicht als Garantien. Hiob und Prediger erzählen von Fällen, in denen es anders kommt."),
        E("Was ist ein „Tor“?", "Kein Mensch mit wenig Verstand, sondern jemand, der Weisung und Gott nicht ernst nimmt (vgl. Ps 14,1)."),
    ],
    teaser="Ein Töpfer verpatzt ein Gefäß – und Gott sagt: Seht her.")

sec("gattungen", [R(JER, 18, 1, 10)], "Beim Töpfer",
    "Jeremia sieht einem Töpfer zu, der aus einem missratenen Gefäß ein neues formt. Gott sagt: Kündige ich einem Volk Unheil an und es kehrt um, dann reut mich das Unheil – und umgekehrt.",
    place="jerusalem",
    quiz=[
        choice("Was macht der Töpfer mit dem missratenen Gefäß?", ["Er macht ein anderes daraus", "Er wirft es weg", "Er verkauft es billig", "Er zerschlägt es vor dem Volk"], 4, "Lies Vers 4.",
               "V. 4: Er macht wiederum ein anderes Gefäß daraus, wie er es für gut hält. (Ein Gefäß zerschlagen wird Jeremia erst im nächsten Kapitel.)"),
        tf("Laut V. 7–8 kann ein angekündigtes Unheil ausbleiben, wenn ein Volk umkehrt.", True, 8, "Lies Vers 7–8.",
           "V. 8: Dann lässt Gott sich das Übel gereuen."),
        choice("Was gilt laut V. 9–10 für eine angekündigte gute Zukunft?", ["Auch sie kann sich ändern, wenn das Volk Böses tut", "Sie tritt in jedem Fall ein", "Sie gilt nur für Israel", "Sie wird verdoppelt, wenn das Volk gehorcht"], 10, "Lies Vers 9–10.",
               "V. 10: Tut das Volk Böses, lässt Gott sich auch das Gute gereuen."),
    ],
    explain=[
        E("Was ist Prophetie?", "Propheten waren vor allem Sprecher Gottes an ihre eigene Zeit: Anklage, Mahnung, Trost, Ankündigung. Vorhersagen gibt es, aber oft an die Reaktion der Hörer gebunden. Jona kündigt Ninive den Untergang an, Ninive kehrt um, und das Gericht bleibt aus (Jona 3,4–10)."),
        E("Ändert Gott seine Meinung?", "Die Bibel sagt beides: Gott bereut nicht wie ein Mensch (4Mo 23,19; 1Sam 15,29), und Gott ließ es sich gereuen (1Sam 15,11; Jer 18,8). Augustinus, Thomas von Aquin und Calvin: Gott ist unveränderlich, die Sprache beschreibt sein Handeln so, wie Menschen es erleben. Arminianische und manche neuere Ausleger betonen stärker, dass Gott wirklich auf Menschen antwortet."),
    ],
    cards=["prophet"],
    teaser="Eine Geschichte, in der Gott mit einem ungerechten Richter verglichen wird. Oder doch nicht?")

sec("gattungen", [R(LK, 18, 1, 8)], "Der ungerechte Richter",
    "Eine Witwe bedrängt einen Richter, der weder Gott noch Menschen fürchtet, bis er ihr Recht verschafft. Jesus fragt: Sollte Gott seinen Auserwählten nicht Recht verschaffen?",
    bridge="Jesus ist mit seinen Jüngern auf dem Weg nach Jerusalem. Kurz vorher hat er über das Kommen des Menschensohns gesprochen (Lk 17,20–37).",
    quiz=[
        tf("Lukas sagt schon vor dem Gleichnis, worum es darin geht.", True, 1, "Lies Vers 1.",
           "V. 1: dass man allezeit beten und nicht müde werden soll."),
        choice("Warum hilft der Richter der Witwe schließlich?", ["Weil sie ihm Mühe macht und sonst immer wiederkommt", "Weil er Gott fürchtet", "Weil sie ihn bezahlt", "Weil das Gesetz es verlangt"], 5, "Lies Vers 4–5.",
               "V. 4–5: Er fürchtet weder Gott noch Menschen – er will nur seine Ruhe."),
        choice("Welche Frage stellt Jesus am Ende?", ["Ob der Menschensohn bei seinem Kommen Glauben finden wird", "Ob die Witwe recht hatte", "Wer von beiden gerecht war", "Wie lange man beten soll"], 8, "Lies Vers 8.",
               "V. 8: Wird der Sohn des Menschen, wenn er kommt, den Glauben finden auf der Erde?"),
    ],
    explain=[
        E("Ist Gott wie dieser Richter?", "Viele Ausleger sehen hier einen Schluss vom Geringeren zum Größeren, eine bekannte rabbinische Denkfigur: Wenn schon ein ungerechter Richter am Ende hilft, wie viel mehr Gott. Dann zeigt das Gleichnis keinen Vergleich, sondern einen Kontrast."),
        E("Warum gerade eine Witwe?", "Witwen hatten oft keinen Schutz und kein Einkommen. Das Alte Testament fordert immer wieder Recht für Witwen und Waisen (2Mo 22,21; Jes 1,17)."),
        E("Was ist ein Gleichnis?", "Eine kurze Bildgeschichte aus dem Alltag, die etwas über Gott und sein Reich zeigt. Seit dem 19. Jahrhundert betonen viele Ausleger: Ein Gleichnis hat meist eine Hauptpointe – nicht jedes Detail bedeutet etwas. Die Kirchenväter deuteten Gleichnisse oft Zug um Zug als Allegorie."),
    ],
    fact="Dieses Gleichnis steht nur bei Lukas – wie auch der barmherzige Samariter und der verlorene Sohn.",
    teaser="Ein Satz, der in manchen Bibeln in Anführungszeichen steht, obwohl der Urtext keine hat.")

sec("gattungen", [R(KOR1, 1, 10, 17), R(KOR1, 7, 1)], "Die andere Hälfte des Gesprächs",
    "Paulus hat von Leuten der Chloe gehört, dass es in Korinth Streit gibt: Jeder beruft sich auf einen anderen Lehrer. In Kapitel 7 antwortet er auf einen Brief, den die Korinther ihm geschrieben haben.",
    bridge="Paulus hatte die Gemeinde in Korinth um 50 n. Chr. gegründet (Apg 18). Einige Jahre später schreibt er ihr aus Ephesus (1Kor 16,8).",
    place="korinth",
    quiz=[
        choice("Woher weiß Paulus vom Streit?", ["Von den Leuten der Chloe", "Aus einem Brief der Gemeinde", "Von Petrus", "Von Timotheus"], 11, "Lies Vers 11.",
               "1,11: durch die Hausgenossen der Chloe."),
        choice("Worauf antwortet Paulus in 7,1?", ["Auf einen Brief der Korinther", "Auf den Bericht der Leute der Chloe", "Auf eine Frage aus Jerusalem", "Auf ein Gespräch mit Apollos"], None, "Lies 7,1.",
               "7,1: worüber ihr mir geschrieben habt."),
        tf("Paulus schreibt, er habe in Korinth viele getauft.", False, 14, "Lies Vers 14–16.",
           "1,14–16: nur Krispus, Gajus und das Haus des Stephanas – sonst weiß er von niemandem."),
    ],
    explain=[
        E("Wer sagt den zweiten Satz in 7,1?", "Im Griechischen gab es keine Anführungszeichen. Viele neuere Ausleger und einige Übersetzungen lesen ihn als Zitat aus dem Brief der Korinther, auf das Paulus dann antwortet. Andere lesen ihn als Paulus’ eigene Aussage. Ähnlich ist es bei 1Kor 6,12."),
        E("Paulus, Apollos, Kephas?", "Kephas ist der aramäische Name des Petrus („Fels“). Apollos war ein gebildeter Jude aus Alexandria, der nach Paulus in Korinth lehrte (Apg 18,24–28)."),
    ],
    fact="21 der 27 Bücher des Neuen Testaments sind Briefe. Auch die Offenbarung beginnt mit sieben Briefen.",
    teaser="Ein hoher Beamter aus Afrika liest im Wagen laut einen Propheten – und versteht ihn nicht.")

# ───────────────────────── 4 · Gemeinsam lesen ─────────────────────────
sec("lesen", [R(APG, 8, 26, 39)], "Verstehst du, was du liest?",
    "Philippus trifft auf dem Weg nach Gaza einen äthiopischen Hofbeamten, der Jesaja liest. Auf dessen Frage erklärt er ihm von dieser Stelle aus das Evangelium von Jesus. Der Äthiopier lässt sich taufen.",
    bridge="Neue Etappe. Nach dem Tod des Stephanus sind viele Christen aus Jerusalem geflohen. Philippus hat in Samaria gepredigt (Apg 8,4–8).",
    place="gaza",
    quiz=[
        choice("Was antwortet der Äthiopier auf die Frage, ob er versteht?", ["Wie könnte ich, wenn mich niemand anleitet?", "Ja, ganz und gar", "Nur den Anfang", "Das will ich in Jerusalem fragen"], 31, "Lies Vers 31.",
               "V. 31: Er braucht jemanden, der ihn anleitet – und bittet Philippus zu sich auf den Wagen."),
        choice("Welche Frage stellt er zu der Jesaja-Stelle?", ["Ob der Prophet von sich selbst oder von einem anderen spricht", "Wann sie sich erfüllen wird", "Wer sie aufgeschrieben hat", "Warum Gott so etwas zulässt"], 34, "Lies Vers 34.",
               "V. 34: Von wem sagt der Prophet das – von sich selbst oder von einem anderen?"),
        who("Siehe, da ist Wasser; was hindert mich, getauft zu werden?", R(APG, 8, 36), ["Der Äthiopier", "Philippus", "Der Engel", "Die Königin Kandake"],
            "V. 36: Der Äthiopier fragt selbst."),
    ],
    explain=[
        E("Warum fehlt Vers 37?", "Vers 37 steht nicht in den ältesten griechischen Handschriften. Spätere Handschriften enthalten ein kurzes Glaubensbekenntnis des Äthiopiers vor der Taufe. Die Elberfelder 2019 lässt ihn im Text weg; die Verszählung behält die Lücke.", translation="elbbk"),
        E("Welche Jesaja-Stelle liest er?", "Jesaja 53,7–8, zitiert nach der Septuaginta, der griechischen Übersetzung. Sie weicht an dieser Stelle etwas vom hebräischen Text ab. Die ersten Christen benutzten meist diese Übersetzung."),
        E("Wer war die Kandake?", "Kandake ist kein Name, sondern ein Titel der Königin (oder Königinmutter) von Meroë im heutigen Sudan. „Äthiopien“ meinte damals das Land südlich von Ägypten."),
    ],
    cards=["septuaginta", "handschriften"],
    teaser="Eine Stadt, deren Bewohner jeden Tag selbst nachprüfen, was Paulus ihnen erzählt.")

sec("lesen", [R(APG, 17, 1, 4), R(APG, 17, 10, 12)], "Täglich nachgeprüft",
    "In Thessalonich redet Paulus an drei Sabbaten aus den Schriften. In Beröa hören die Leute bereitwillig zu – und prüfen täglich in den Schriften nach, ob es sich so verhält.",
    bridge="Paulus und Silas reisen durch Makedonien in Nordgriechenland. Zwischen den beiden Teilen dieses Abschnitts gibt es in Thessalonich einen Aufruhr, und die beiden müssen nachts weiterziehen (Apg 17,5–9).",
    place="beroea",
    quiz=[
        estimate("An wie vielen Sabbaten redet Paulus in Thessalonich mit den Leuten in der Synagoge?", 1, 10, 3, "Sabbate", "V. 2: an drei Sabbaten, aus den Schriften.", 2, "Lies Vers 2."),
        choice("Was tun die Leute in Beröa?", ["Sie untersuchen täglich die Schriften, ob es sich so verhält", "Sie fragen in Jerusalem nach", "Sie verlangen ein Zeichen", "Sie lassen Paulus einen Eid schwören"], 11, "Lies Vers 11.",
               "V. 11: Sie nehmen das Wort bereitwillig auf und prüfen täglich in den Schriften nach."),
        tf("Lukas nennt die Leute in Beröa „edler“ als die in Thessalonich.", True, 11, "Lies Vers 11.",
           "V. 11 – und begründet es mit beidem: Bereitschaft und Prüfen."),
    ],
    explain=[
        E("Welche Schriften prüfen sie?", "Das Alte Testament, meist in griechischer Übersetzung. Ein Neues Testament gab es noch nicht. Paulus’ erster Brief an die Thessalonicher entstand erst kurz danach, um 50 n. Chr."),
        E("Wer prüft, wer entscheidet?", "Evangelische Kirchen und Freikirchen berufen sich gern auf diese Stelle: Jede Lehre muss sich an der Schrift prüfen lassen. Katholische und orthodoxe Christen betonen, dass die Schrift in der Gemeinschaft der Kirche gelesen wird, mit ihrer Überlieferung. Strittig ist vor allem, wer im Streitfall entscheidet."),
    ],
    cards=["schrift-tradition"],
    teaser="Hungrige Jünger, ein Kornfeld und ein Vorwurf. Jesus antwortet mit einer Gegenfrage.")

sec("lesen", [R(MT, 12, 1, 8)], "Habt ihr nicht gelesen?",
    "Die Jünger pflücken am Sabbat Ähren. Die Pharisäer werfen ihnen vor, das Gebot zu brechen. Jesus antwortet mit David, mit den Priestern im Tempel und mit einem Prophetenwort.",
    bridge="Jesus zieht mit seinen Jüngern durch Galiläa. Die Auseinandersetzung mit den Pharisäern wird schärfer.",
    quiz=[
        tf("Die Pharisäer werfen den Jüngern Diebstahl vor.", False, 2, "Lies Vers 2.",
           "V. 2: Es geht nicht um Diebstahl, sondern darum, dass es am Sabbat nicht erlaubt sei."),
        order("In welcher Reihenfolge antwortet Jesus?",
              ["David und die Schaubrote", "Die Priester am Sabbat im Tempel", "Mehr als der Tempel ist hier", "Barmherzigkeit statt Opfer", "Herr des Sabbats"],
              "V. 3–8: zwei Beispiele aus der Schrift, dann ein Wort über sich, ein Prophetenwort und wieder ein Wort über sich."),
        choice("Mit welcher Frage beginnt Jesus seine Antwort?", ["Habt ihr nicht gelesen …?", "Wer von euch ist ohne Sünde?", "Was steht im Gesetz?", "Warum versucht ihr mich?"], 3, "Lies Vers 3.",
               "V. 3: Habt ihr nicht gelesen, was David tat? Und V. 5 noch einmal."),
    ],
    explain=[
        E("Was waren die Schaubrote?", "Zwölf Brote, die im Heiligtum vor Gott lagen und jeden Sabbat erneuert wurden. Essen durften sie nur die Priester (3Mo 24,5–9). Die Geschichte von David steht in 1Sam 21,1–7."),
        E("Woher stammt das Wort in V. 7?", "Aus Hosea 6,6. Jesus zitiert es bei Matthäus zweimal (auch Mt 9,13)."),
        E("Gilt der Sabbat für Christen?", "Die meisten Kirchen feiern den Sonntag als Tag der Auferstehung. Siebenten-Tags-Adventisten und einige andere halten den Samstag. Reformierte und puritanische Tradition verstehen den Sonntag als „christlichen Sabbat“, andere Traditionen sehen das Sabbatgebot in Christus erfüllt."),
    ],
    fact="Ähren abzupflücken, wenn man an einem fremden Feld vorbeiging, war ausdrücklich erlaubt (5Mo 23,26). Der Streit ging nur um den Sabbat.",
    teaser="Ein Mann schaut in den Spiegel, geht weg – und hat vergessen, wie er aussieht.")

sec("lesen", [R(JAK, 1, 19, 25)], "Der Spiegel",
    "Jakobus mahnt: schnell zum Hören, langsam zum Reden. Wer das Wort nur hört, gleicht einem, der sich im Spiegel betrachtet und sofort vergisst, wie er aussieht.",
    bridge="Der Jakobusbrief ist an Christen „in der Zerstreuung“ gerichtet. Die Überlieferung schreibt ihn Jakobus zu, dem Bruder Jesu und Leiter der Gemeinde in Jerusalem.",
    quiz=[
        choice("Wozu soll jeder schnell sein – und wozu langsam?", ["Schnell zum Hören, langsam zum Reden und zum Zorn", "Schnell zum Reden, langsam zum Urteilen", "Schnell zum Vergeben, langsam zum Strafen", "Schnell zum Beten, langsam zum Handeln"], 19, "Lies Vers 19.",
               "V. 19: schnell zum Hören, langsam zum Reden, langsam zum Zorn."),
        choice("Womit vergleicht Jakobus jemanden, der nur hört?", ["Mit einem, der in den Spiegel schaut und gleich vergisst, wie er aussieht", "Mit einem Haus auf Sand", "Mit einem Baum ohne Frucht", "Mit einem schlafenden Knecht"], 23, "Lies Vers 23–24.",
               "V. 23–24: Er betrachtet sich, geht weg und vergisst sofort, wie er beschaffen war."),
    ],
    explain=[
        E("Hören und Tun – ein Gegensatz zu Paulus?", "Luther nannte den Jakobusbrief 1522 im Vergleich zu anderen Büchern eine „stroherne Epistel“, weil er ihn schwer mit Paulus’ Lehre von der Rechtfertigung vereinbaren konnte. Viele Ausleger, auch evangelische, sehen keinen Widerspruch: Paulus und Jakobus reden von verschiedenen Fragen. Mehr dazu im Plan „Gerecht vor Gott“."),
        E("„Gesetz der Freiheit“?", "Jakobus benutzt den Ausdruck auch in 2,12. Ausleger beziehen ihn auf die Gebote, wie Jesus sie ausgelegt hat, oder auf das Evangelium insgesamt."),
    ],
    try_="Nimm einen Text, den du gut kennst, und stell ihm die Fragen aus diesem Plan: Wer schreibt? An wen? Was für eine Art Text ist das? Und was steht wirklich da?")

P.write()
