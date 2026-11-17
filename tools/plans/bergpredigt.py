#!/usr/bin/env python3
"""Source for the reading plan „Die Bergpredigt – Ich aber sage euch“ (generates assets/plans/bergpredigt.json).

python3 -I tools/plans/bergpredigt.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/bergpredigt.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

MT, PS = 40, 19

P = PlanBuilder(
    "bergpredigt", "bp", "Die Bergpredigt", "Ich aber sage euch",
    "Drei Kapitel, die man zitiert, ohne sie ganz zu kennen: Seligpreisungen, andere Wange, Vaterunser, Haus auf dem Felsen. "
    "15 Abschnitte durch Matthäus 5–7, Vers für Vers – und dazu die Frage, die Christen seit 2000 Jahren verschieden beantworten: "
    "Für wen und wie ist das gemeint?",
    "jesus",
    stages=[("berg", "Auf dem Berg"), ("antithesen", "Ich aber sage euch"), ("vater", "Vor dem Vater"), ("wege", "Zwei Wege")],
    cards=[
        ("bergpredigt", "begriff", "Bergpredigt und Feldrede", "Matthäus 5–7 ist die erste von fünf großen Reden Jesu im Matthäusevangelium; jede endet mit einer ähnlichen Schlussformel (7,28; 11,1; 13,53; 19,1; 26,1). Lukas hat eine kürzere Parallele, die Feldrede (Lk 6,17–49): auf einem ebenen Platz, mit vier Seligpreisungen und vier Weherufen. Manche sehen darin dieselbe Rede, andere ähnliche Reden bei verschiedenen Gelegenheiten.", "Mt 5–7; Lk 6,17–49"),
        ("berg", "ort", "Der Berg", "Matthäus nennt keinen Namen. Seit byzantinischer Zeit wird ein Hügel am Nordwestufer des Sees Genezareth, nahe Kapernaum und Tabgha, als Ort verehrt; die heutige Kirche dort wurde 1938 gebaut. Viele Ausleger achten auf die Parallele: Mose empfängt das Gesetz auf dem Berg Sinai, Jesus lehrt auf einem Berg über das Gesetz.", "Mt 5,1; 2Mo 19,20"),
        ("glueckselig", "begriff", "Glückselig", "Griechisch makarios, hebräisch aschre, wie in Ps 1,1. Kein Gefühl („glücklich“), sondern ein Zuspruch: Dieser Mensch ist gut dran, ihm wird etwas zuteil. Luther übersetzte „selig“, andere „glücklich“ oder „wohl denen“. Die Seligpreisungen nennen meist zuerst eine Lage und dann, was Gott daran ändert.", "Mt 5,3–12; Ps 1,1"),
        ("reich", "begriff", "Das Reich der Himmel", "Matthäus sagt über 30-mal „Reich der Himmel“, wo Markus und Lukas „Reich Gottes“ sagen; gemeint ist dasselbe. Viele erklären das mit dem jüdischen Brauch, den Gottesnamen zu umschreiben. Gemeint ist kein Ort im Jenseits, sondern Gottes Königsherrschaft, die mit Jesus anbricht und noch kommen soll.", "Mt 4,17; 5,3; 6,10.33"),
        ("gesetz", "begriff", "Das Gesetz und die Propheten", "So nannte man im Judentum die heiligen Schriften: die Tora (die fünf Bücher Mose) und die Propheten, wozu auch Josua bis Könige gehörten. Tora heißt eigentlich „Weisung“. Die Bergpredigt nennt das Paar am Anfang (5,17) und am Ende (7,12) – wie eine Klammer um den Hauptteil.", "Mt 5,17; 7,12; 22,40"),
        ("pharisaeer", "person", "Schriftgelehrte und Pharisäer", "Schriftgelehrte waren Ausleger der Tora, oft zugleich Lehrer und Richter. Die Pharisäer waren eine Laienbewegung, die das Gesetz im Alltag genau halten wollte, auch mit überlieferten Auslegungen. Im Volk waren sie angesehen. Nach der Zerstörung des Tempels 70 n. Chr. ging das rabbinische Judentum vor allem aus ihnen hervor.", "Mt 5,20; 23,2–3"),
        ("antithesen", "begriff", "„Ich aber sage euch“", "Sechsmal stellt Jesus in Mt 5,21–48 ein überliefertes Wort neben sein eigenes. Man nennt diese Stellen die Antithesen. Ausleger fragen: Verschärft Jesus das Gesetz, legt er seinen ursprünglichen Sinn aus, oder setzt er sich darüber? Auffällig ist, dass er ohne Berufung auf eine andere Autorität spricht (vgl. 7,29).", "Mt 5,21–48"),
        ("gehenna", "ort", "Gehenna", "Das Wort, das die Elberfelder mit „Hölle“ übersetzt, ist der Name eines Tals südlich von Jerusalem: Ge-Hinnom. Dort wurden unter den Königen Ahas und Manasse Kinder geopfert (2Kön 23,10; Jer 7,31). Später wurde es zum Bild für Gottes endgültiges Gericht. Dass dort eine brennende Müllhalde lag, wird erst im Mittelalter erwähnt und ist unsicher.", "Mt 5,22.29; Jer 7,31–32"),
        ("heuchler", "begriff", "Heuchler", "Griechisch hypokrites bezeichnete den Schauspieler im Theater, der hinter einer Maske eine Rolle spielt. In der Bergpredigt sind es Menschen, die Frömmigkeit vor Publikum aufführen (6,2.5.16). Im Neuen Testament steht das Wort fast nur in den Evangelien, am häufigsten bei Matthäus.", "Mt 6,2.5.16; 7,5"),
        ("vaterunser", "begriff", "Das Vaterunser", "Bei Matthäus steht es mitten in der Bergpredigt, bei Lukas kürzer auf die Bitte eines Jüngers hin (Lk 11,1–4). Die Didache, eine Kirchenordnung um 100 n. Chr., bringt es fast wie Matthäus und rät, es dreimal täglich zu beten. Der Schluss „Denn dein ist das Reich …“ fehlt in den ältesten Handschriften von Matthäus; die Didache hat eine kürzere Form davon.", "Mt 6,9–13; Lk 11,2–4"),
        ("mammon", "begriff", "Mammon", "Ein aramäisches Wort für Besitz und Vermögen, in jüdischen Texten der Zeit auch ohne negativen Klang gebraucht. Herkunft unsicher; manche leiten es von einer Wurzel ab, die „worauf man sich verlässt“ bedeutet. In 6,24 steht es wie ein Herr, dem man dient, Gott gegenüber.", "Mt 6,24; Lk 16,9.13"),
        ("zoellner", "person", "Zöllner", "Einheimische, die Zölle und Abgaben für die Römer oder für Herodes Antipas eintrieben, oft mit eigenem Aufschlag. Sie galten als Betrüger und Kollaborateure. Matthäus, nach der Überlieferung der Verfasser dieses Evangeliums, war selbst einer (9,9; 10,3).", "Mt 5,46; 9,9–11; 10,3"),
        ("lesarten", "begriff", "Wie man die Bergpredigt liest", "Katholisch früher: Gebote für alle, „Räte“ für Ordensleute; heute ein Ruf an alle (2. Vatikanum). Orthodox: ein Weg der Verwandlung in Gottes Bild. Lutherisch: Sie zeigt, wie sehr man Gnade braucht, und gilt dem Christen als Person, nicht dem Amt. Täuferisch: wörtlich in der Gemeinde zu leben. Dispensationalistisch (Scofield): vor allem Ordnung des kommenden Reiches.", "Mt 5–7"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Auf dem Berg ─────────────────────────
sec("berg", [R(MT, 5, 1, 6)], "Glückselig die Armen",
    "Jesus sieht die Menschenmengen, steigt auf einen Berg und setzt sich; seine Jünger kommen zu ihm. Er beginnt mit vier Seligpreisungen: die Armen im Geist, die Trauernden, die Sanftmütigen und die, die nach Gerechtigkeit hungern und dürsten.",
    place="berg-seligpreisungen",
    focus="Achte darauf, wie jede Seligpreisung gebaut ist: Wer wird glückselig genannt, und was wird ihm zugesagt?",
    quiz=[
        choice("Was tut Jesus nach V. 1, bevor er zu lehren beginnt?", ["Er setzt sich", "Er stellt sich auf einen Felsen", "Er betet die ganze Nacht", "Er schickt die Menge weg"], 1, "Lies Vers 1.",
               "V. 1: Er steigt auf den Berg und setzt sich. Im Judentum der Zeit lehrten Lehrer im Sitzen."),
        choice("Was wird den Sanftmütigen zugesagt?", ["Sie werden das Land erben", "Sie werden getröstet werden", "Sie werden gesättigt werden", "Ihrer ist das Reich der Himmel"], 5, "Lies Vers 5.",
               "V. 5: Sie werden das Land erben. Getröstet werden die Trauernden (V. 4), gesättigt die Hungernden (V. 6)."),
        tf("Die erste Seligpreisung und die über die Verfolgten (V. 10) haben dieselbe Zusage.", True, 10, "Vergleiche Vers 3 und Vers 10.",
           "V. 3 und 10: Beide Male heißt es, ihnen gehöre das Reich der Himmel. Viele Ausleger sehen darin eine Klammer um die acht Seligpreisungen."),
    ],
    explain=[
        E("Was heißt „arm im Geist“?", "Lukas sagt einfach „ihr Armen“ (Lk 6,20). Matthäus' Ausdruck wird verschieden verstanden: Menschen, die vor Gott nichts vorzuweisen haben und das wissen; die Demütigen; oder die wirklich Armen, die ganz auf Gott angewiesen sind. In den Psalmen und bei Jesaja sind die „Armen“ oft beides zugleich (z. B. Jes 61,1)."),
        E("Was meint „sanftmütig“?", "Griechisch praus: nicht schwach, sondern nicht gewaltsam, nicht auf Durchsetzung aus. Matthäus nennt auch Jesus so (11,29; 21,5). V. 5 greift fast wörtlich Ps 37,11 auf, wo die Sanftmütigen das Land besitzen werden."),
        E("Wer sind die Trauernden?", "Der Text sagt nicht, worüber sie trauern. Manche denken an Trauer über eigene Schuld, andere an Leid und Verlust, wieder andere an die Trauer über den Zustand der Welt. Jes 61,2–3 spricht vom Trösten der Trauernden Zions."),
    ],
    cards=["bergpredigt", "berg", "glueckselig", "reich"],
    memory_verse=MV(R(MT, 5, 3), "Glückselig die Armen im Geist, denn ihrer ist das Reich der Himmel."),
    teaser="Die nächsten Seligpreisungen gelten Menschen, die etwas tun. Und dann wechselt Jesus plötzlich die Anrede.")

sec("berg", [R(MT, 5, 7, 12)], "Glückselig die Friedensstifter",
    "Vier weitere Seligpreisungen: die Barmherzigen, die reinen Herzens, die Friedensstifter und die um der Gerechtigkeit willen Verfolgten. Dann spricht Jesus seine Zuhörer direkt an: Glückselig seid ihr, wenn man euch um seinetwillen schmäht und verfolgt. Sie sollen sich freuen, denn so ging es schon den Propheten.",
    quiz=[
        choice("Was wird denen zugesagt, die reinen Herzens sind?", ["Sie werden Gott schauen", "Sie werden Söhne Gottes heißen", "Ihnen wird Barmherzigkeit widerfahren", "Sie werden das Land erben"], 8, "Lies Vers 8.",
               "V. 8: Sie werden Gott schauen. Söhne Gottes heißen die Friedensstifter (V. 9)."),
        error("Ab V. 11 sagt Jesus: Glückselig seid ihr, wenn man euch um der [Gerechtigkeit] willen schmäht und verfolgt.", "meinetwillen", 11,
              "V. 11: um meinetwillen, also um Jesu willen. In V. 10 heißt es noch „um Gerechtigkeit willen“ – in V. 11 verbindet Jesus die Verfolgung mit sich selbst."),
        choice("Womit begründet Jesus in V. 12, dass die Verfolgten sich freuen sollen?", ["Ihr Lohn ist groß in den Himmeln, und die Propheten wurden auch so verfolgt", "Die Verfolger werden bald bestraft", "Verfolgung macht sie stärker", "Die Verfolgung dauert nur kurz"], 12, "Lies Vers 12.",
               "V. 12: Zwei Gründe – großer Lohn in den Himmeln, und die Propheten vor ihnen erlebten dasselbe."),
    ],
    explain=[
        E("Was heißt „reinen Herzens“?", "Das Herz ist in der Bibel nicht nur das Gefühl, sondern die Mitte des Menschen: Denken, Wollen, Entscheiden. „Reines Herz“ steht in Ps 24,3–4 bei der Frage, wer auf den Berg des HERRN steigen darf. Viele verstehen es als ungeteilt, ohne Doppelspiel."),
        E("Friedensstifter oder Friedfertige?", "Griechisch eirenopoioi, wörtlich „Friedensmacher“. Gemeint sind wohl nicht nur Menschen, die selbst friedlich sind, sondern solche, die Frieden herstellen, wo Streit ist. Luther übersetzte „die Friedfertigen“."),
        E("Wie viele Seligpreisungen sind es?", "Je nach Zählung acht (V. 3–10, jeweils in der dritten Person) oder neun, wenn man V. 11–12 mitzählt. V. 11 wechselt zum „ihr“ und ist länger als die anderen."),
    ],
    fact="Lukas stellt seinen vier Seligpreisungen vier Weherufe gegenüber (Lk 6,24–26): Wehe euch Reichen, euch Satten, euch Lachenden. Matthäus hat an dieser Stelle keine Weherufe – dafür eine ganze Reihe in Kap. 23.",
    memory_verse=MV(R(MT, 5, 8), "Glückselig die reinen Herzens sind, denn sie werden Gott schauen."),
    teaser="Salz, das nicht mehr salzt – im Griechischen steht dafür ein Wort, aus dem unser „Moron“ kommt.")

sec("berg", [R(MT, 5, 13, 20)], "Salz, Licht und das Gesetz",
    "Jesus sagt seinen Jüngern zu, sie seien das Salz der Erde und das Licht der Welt; eine Lampe stellt man nicht unter einen Scheffel. Dann erklärt er, er sei nicht gekommen, Gesetz und Propheten aufzulösen, sondern zu erfüllen. Nichts davon vergeht, und die Gerechtigkeit der Jünger soll die der Schriftgelehrten und Pharisäer übertreffen.",
    focus="Achte auf V. 17. Was Jesus hier über das Gesetz sagt, ist der Schlüssel für alles, was ab V. 21 kommt.",
    quiz=[
        tf("Jesus fordert in V. 13–14 seine Jünger auf, Salz und Licht zu werden.", False, 14, "Lies Vers 13 und 14 genau.",
           "V. 13–14: Jesus sagt ihr seid – nicht ihr sollt werden. Er spricht es ihnen zu. Erst in V. 16 folgt eine Aufforderung: das Licht leuchten lassen."),
        choice("Warum sollen nach V. 16 die Menschen die guten Werke sehen?", ["Damit sie den Vater in den Himmeln verherrlichen", "Damit die Jünger Lohn bekommen", "Damit die Pharisäer beschämt werden", "Damit sich die Menschen bekehren müssen"], 16, "Lies Vers 16.",
               "V. 16: Damit sie den Vater verherrlichen. Die Ehre geht nicht an die Jünger, sondern an Gott."),
        choice("Was sagt Jesus über das Gesetz in V. 17?", ["Er ist gekommen, es zu erfüllen, nicht aufzulösen", "Er ist gekommen, es durch ein neues Gesetz zu ersetzen", "Es gilt nur noch bis zu seinem Tod", "Nur die Zehn Gebote bleiben gültig"], 17, "Lies Vers 17.",
               "V. 17: nicht auflösen, sondern erfüllen. Was „erfüllen“ genau heißt, wird verschieden verstanden – siehe „Versteh ich nicht“."),
    ],
    explain=[
        E("Wie kann Salz kraftlos werden?", "Reines Kochsalz verliert seinen Geschmack nicht. Im Altertum war Salz aber oft mit anderen Stoffen vermischt, etwa am Toten Meer gewonnen; wurde das Salz ausgewaschen, blieb ein fader Rest. Salz würzte und machte haltbar; manche denken auch an das Salz bei den Opfern (3Mo 2,13)."),
        E("Was ist ein Scheffel?", "Ein Hohlmaß für Getreide, etwa 9 Liter, als Gefäß in jedem Haus vorhanden. Eine Öllampe darunter würde nicht leuchten und bald ausgehen.", "elbbk"),
        E("Was heißt „erfüllen“?", "Mehrere Lesarten, die sich oft verbinden: Jesus tut, was das Gesetz verlangt; er legt seinen eigentlichen Sinn aus (wie in den folgenden Versen); oder er ist selbst das Ziel, auf das Gesetz und Propheten hinzeigen (vgl. die vielen „damit erfüllt würde“ bei Matthäus). Wie die Gebote dann für Christen gelten, beantworten die Kirchen unterschiedlich."),
        E("Jota und Strichlein?", "Jota ist der kleinste griechische Buchstabe, er steht für das hebräische Jod, den kleinsten Buchstaben des hebräischen Alphabets. Das „Strichlein“ ist wohl ein winziger Haken, der ähnliche hebräische Buchstaben unterscheidet."),
    ],
    cards=["gesetz", "pharisaeer"],
    fact="Das griechische Wort für „kraftlos werden“ in V. 13 (moraino) heißt sonst „töricht werden“ (so in Röm 1,22). Davon kommt auch das englische „moron“.",
    memory_verse=MV(R(MT, 5, 14), "Ihr seid das Licht der Welt"),
    prayer={"ref": R(PS, 119, 18), "source": "Psalm 119,18"},
    teaser="Jesus zitiert jetzt die Zehn Gebote – und sagt dann etwas, das den Gang zum Altar unterbricht.")

# ───────────────────────── 2 · Ich aber sage euch ─────────────────────────
sec("antithesen", [R(MT, 5, 21, 26)], "Zorn und Versöhnung",
    "Das Gebot gegen das Töten – Jesus sagt: Schon wer seinem Bruder zürnt oder ihn beschimpft, verfällt dem Gericht. Wer am Altar steht und merkt, dass sein Bruder etwas gegen ihn hat, soll erst hingehen und sich versöhnen. Und mit einem Gegner soll man sich einigen, solange man noch auf dem Weg zum Richter ist.",
    quiz=[
        order("In welcher Reihenfolge steigert sich V. 22?", ["Zürnen – dem Gericht verfallen", "Dummkopf sagen – dem Synedrium verfallen", "Du Narr sagen – der Hölle des Feuers verfallen"],
              "V. 22: drei Stufen, vom örtlichen Gericht über den Hohen Rat bis zur Gehenna.", "Lies Vers 22."),
        choice("Was soll man nach V. 23–24 tun, wenn einem am Altar einfällt, dass der Bruder etwas gegen einen hat?", ["Die Gabe liegen lassen, sich versöhnen, dann wiederkommen", "Die Gabe schnell darbringen und danach hingehen", "Für den Bruder ein zweites Opfer bringen", "Warten, bis der Bruder zu einem kommt"], 24, "Lies Vers 24.",
               "V. 24: Die Gabe bleibt vor dem Altar liegen. Erst die Versöhnung, dann das Opfer."),
        tf("In V. 23 geht es darum, dass man selbst etwas gegen den Bruder hat.", False, 23, "Lies Vers 23 genau.",
           "V. 23: Umgekehrt – der Bruder hat etwas gegen dich. Der Schritt zur Versöhnung liegt trotzdem bei dem, der am Altar steht."),
    ],
    explain=[
        E("Was ist das Synedrium?", "Der Hohe Rat in Jerusalem, das oberste jüdische Gericht mit 71 Mitgliedern unter dem Hohepriester. Vor ihm stand später auch Jesus (26,59)."),
        E("Warum steht „ohne Grund“ in Klammern?", "Das Wort fehlt in einigen der ältesten Handschriften, darunter im Codex Vaticanus, und kam wohl später hinzu. Die Elberfelder zeigt solche unsicheren Stellen mit eckigen Klammern. Viele neuere Übersetzungen lassen es weg.", "elbbk"),
        E("Was heißt „Dummkopf“?", "Im Griechischen steht hier ein aramäisches Schimpfwort: raka, wohl „Hohlkopf“. Das zweite, „Narr“ (moros), war ein schwereres Wort, das jemandem Verstand und oft auch Gottesfurcht absprach.", "elbbk"),
        E("Welchen Altar meint Jesus?", "Den Brandopferaltar im Tempel in Jerusalem, wo Opfergaben dargebracht wurden. Die Hörer in Galiläa hätten dafür mehrere Tage reisen müssen – das Hingehen zum Bruder war also kein kleiner Umweg."),
    ],
    cards=["antithesen", "gehenna"],
    memory_verse=MV(R(MT, 5, 24), "geh zuvor hin, versöhne dich mit deinem Bruder"),
    try_="Lies V. 21 und dann 2. Mose 20,13. Was hat Jesus zu dem Gebot hinzugefügt, und was zitiert er wörtlich?",
    teaser="Im nächsten Abschnitt stehen die drastischsten Bilder der ganzen Bergpredigt. Ob sie wörtlich gemeint sind, war schon früh eine Frage.")

sec("antithesen", [R(MT, 5, 27, 32)], "Begehren und Scheidung",
    "Das Gebot gegen den Ehebruch – Jesus sagt: Wer eine Frau begehrlich ansieht, hat im Herzen schon die Ehe gebrochen. Wenn das rechte Auge oder die rechte Hand zur Sünde verführt, soll man sie lieber weggeben als ganz verloren zu gehen. Dann das Wort über den Scheidebrief: Wer seine Frau entlässt, außer wegen Hurerei, macht, dass sie Ehebruch begeht.",
    quiz=[
        choice("Wo beginnt nach V. 28 der Ehebruch?", ["Im Herzen", "Bei der ersten Berührung", "Beim Verlassen der Ehefrau", "Bei der Hochzeit mit einer anderen"], 28, "Lies Vers 28.",
               "V. 28: Er hat schon im Herzen Ehebruch begangen."),
        who("Wer seine Frau entlassen wird, gebe ihr einen Scheidebrief.", R(MT, 5, 31), ["Ein überliefertes Wort, das Jesus zitiert", "Jesus selbst als neue Regel", "Die Pharisäer in einem Streitgespräch", "Mose auf dem Berg Sinai, wörtlich zitiert"],
            "V. 31: Mit „es ist gesagt“ führt Jesus eine überlieferte Regel an, die auf 5Mo 24,1 zurückgeht – und stellt in V. 32 sein Wort daneben.", "Achte auf die Einleitung von Vers 31."),
        choice("Welche Ausnahme nennt Jesus in V. 32?", ["Hurerei", "Kinderlosigkeit", "Streit in der Ehe", "Verschiedener Glaube"], 32, "Lies Vers 32.",
               "V. 32: außer auf Grund von Hurerei (griechisch porneia). Was dieses Wort hier genau meint, ist umstritten."),
    ],
    explain=[
        E("Ist das mit Auge und Hand wörtlich gemeint?", "Fast alle Ausleger, schon in der alten Kirche, verstehen es als drastische Bildsprache: Nichts ist es wert, dafür das Ganze zu verlieren. Als der Theologe Origenes sich im 3. Jahrhundert nach einer ähnlichen Stelle (19,12) selbst verstümmelt haben soll, wurde das später scharf kritisiert."),
        E("Was war damals umstritten?", "5Mo 24,1 erlaubt die Scheidung, wenn der Mann an der Frau etwas „Schändliches“ findet. Die Schule Schammais verstand darunter nur sexuelle Untreue, die Schule Hillels fast jeden Grund. Nur der Mann konnte sich scheiden; der Scheidebrief gab der Frau immerhin die Freiheit, wieder zu heiraten."),
        E("Wie verstehen das verschiedene Kirchen?", "Katholisch: Eine gültige sakramentale Ehe ist unauflöslich; porneia wird oft als von Anfang an ungültige Verbindung verstanden, daher die Möglichkeit der Annullierung. Orthodox: Ehe ist auf Dauer angelegt, aber die Kirche kann nach einem Scheitern aus Barmherzigkeit eine zweite Ehe segnen. Evangelisch: Seit der Reformation ist Scheidung bei Ehebruch und Verlassenwerden (1Kor 7,15) anerkannt. In Freikirchen reicht das Spektrum von strenger bis offener Praxis."),
    ],
    prayer={"ref": R(PS, 139, 23, 24), "source": "Psalm 139,23–24"},
    teaser="Ein Eid ist nicht verboten, steht im Gesetz. Jesus sagt etwas anderes – und dann folgt die andere Wange.")

sec("antithesen", [R(MT, 5, 33, 42)], "Ja, nein, und die zweite Meile",
    "Über den Eid sagt Jesus: Schwört überhaupt nicht, weder beim Himmel noch bei der Erde, noch bei Jerusalem oder beim eigenen Kopf; ein einfaches Ja oder Nein soll gelten. Auf „Auge um Auge“ antwortet er: dem Bösen nicht widerstehen, die andere Wange hinhalten, auch den Mantel lassen, die zweite Meile gehen und dem geben, der bittet.",
    quiz=[
        choice("Warum soll man nach V. 36 nicht beim eigenen Haupt schwören?", ["Man kann kein einziges Haar weiß oder schwarz machen", "Der Kopf ist Gottes Thron", "Das Haupt gehört dem König", "Weil man dann seinen Kopf verlieren kann"], 36, "Lies Vers 36.",
               "V. 36: Man hat nicht einmal über ein Haar Macht. Man kann also nichts verpfänden, was einem wirklich gehört."),
        order("In welcher Reihenfolge stehen die Beispiele in V. 39–42?", ["Die andere Wange", "Den Mantel lassen", "Zwei Meilen gehen", "Dem Bittenden geben"],
              "V. 39–42: Schlag, Gericht, Zwangsdienst, Bitte um Geld – vier Lagen, in denen jemand etwas von dir will.", "Lies Vers 39–42."),
        tf("„Auge um Auge“ steht so im Alten Testament.", True, 38, "Jesus beginnt mit: Ihr habt gehört, dass gesagt ist.",
           "Ja: 2Mo 21,24; 3Mo 24,20; 5Mo 19,21. Dort ist es eine Regel für Richter, die die Strafe begrenzt – nicht mehr als den Schaden."),
    ],
    explain=[
        E("Was hat es mit der Meile auf sich?", "Römische Soldaten durften Einheimische zwingen, ihr Gepäck ein Stück zu tragen. Das griechische Wort für „zwingen“ in V. 41 steht auch in 27,32, als Simon von Kyrene das Kreuz Jesu tragen muss. Eine römische Meile war knapp 1,5 Kilometer."),
        E("Warum gerade die rechte Wange?", "Wer mit der rechten Hand die rechte Wange trifft, schlägt mit dem Handrücken – das war im Altertum eher eine Demütigung als ein Angriff. Manche Ausleger leiten daraus ab, dass es um Beleidigung geht; andere halten das für überdeutet."),
        E("Leibrock und Mantel?", "Der Leibrock war das Untergewand, der Mantel das Obergewand, nachts auch die Decke. Nach 2Mo 22,25–26 durfte man den Mantel eines Armen nicht über Nacht als Pfand behalten. Wer beides hergibt, steht fast nackt da."),
        E("Wie leben verschiedene Kirchen diese Verse?", "Täufer, Mennoniten und Quäker lehnen Eid und Waffendienst ab (Schleitheimer Artikel 1527). Katholische, lutherische und reformierte Lehre erlauben den Eid vor Gericht und die Gewalt des Staates zum Schutz anderer; die Verse gelten dort dem persönlichen Verhalten. In Deutschland kann man statt eines Eides eine Bekräftigung ohne Schwur abgeben."),
    ],
    fact="Tolstoi las diese Verse wörtlich und schrieb darüber das Buch „Das Reich Gottes ist in euch“ (1894). Gandhi las es als junger Anwalt in Südafrika und nannte es später einen der wichtigsten Einflüsse auf sein Denken.",
    memory_verse=MV(R(MT, 5, 37), "Es sei aber eure Rede: Ja, ja; nein, nein"),
    teaser="„Hasse deinen Feind“ – steht das wirklich im Alten Testament?")

sec("antithesen", [R(MT, 5, 43, 48)], "Liebt eure Feinde",
    "„Liebe deinen Nächsten und hasse deinen Feind“ – Jesus sagt: Liebt eure Feinde und betet für die, die euch verfolgen. So werdet ihr Söhne eures Vaters, der seine Sonne über Böse und Gute aufgehen lässt. Wer nur die liebt, die ihn lieben, tut nichts Besonderes. Am Ende steht: Ihr sollt vollkommen sein, wie euer Vater vollkommen ist.",
    focus="Achte darauf, womit Jesus die Feindesliebe begründet – es ist kein Argument über die Feinde.",
    quiz=[
        choice("Womit begründet Jesus in V. 45 die Feindesliebe?", ["Gott lässt Sonne und Regen über Gute und Böse kommen", "Feinde werden durch Liebe zu Freunden", "Die Feinde wissen nicht, was sie tun", "Wer Feinde liebt, wird von ihnen verschont"], 45, "Lies Vers 45.",
               "V. 45: Er verweist auf Gottes eigenes Handeln – Sonne und Regen für alle. So handeln heißt, Söhne dieses Vaters zu sein."),
        choice("Wen nennt Jesus als Beispiel für Leute, die nur die lieben, die sie lieben?", ["Die Zöllner und die Nationen", "Die Pharisäer und Schriftgelehrten", "Die Römer und Herodes", "Die Priester und Leviten"], 46, "Lies Vers 46–47.",
               "V. 46–47: Zöllner und die von den Nationen (Nichtjuden) tun dasselbe – das ist nichts Besonderes."),
        tf("Das Gebot, den Feind zu hassen, steht so im Alten Testament.", False, 43, "Denk an 3. Mose 19,18.",
           "3Mo 19,18 gebietet die Nächstenliebe. Ein Gebot zum Feindeshass gibt es im Alten Testament nicht; Jesus zitiert hier wohl eine verbreitete Auslegung."),
    ],
    explain=[
        E("Woher kommt dann „hasse deinen Feind“?", "Manche denken an eine gängige Folgerung: Wenn der Nächste der eigene Volksgenosse ist, ist der Feind ausgenommen. In den Schriftrollen von Qumran wird tatsächlich dazu aufgerufen, die „Söhne der Finsternis“ zu hassen (Gemeinderegel 1QS 1,10). Spr 25,21 dagegen gebietet, dem hungrigen Feind Brot zu geben."),
        E("Was heißt „vollkommen“?", "Griechisch teleios: ganz, ungeteilt, ans Ziel gekommen – nicht fehlerlos im modernen Sinn. Im Zusammenhang geht es um eine Liebe, die niemanden ausnimmt, wie Gottes Liebe. Lukas hat an der Parallelstelle „barmherzig“ (Lk 6,36)."),
        E("Warum stehen Teile von V. 44 in Klammern?", "Die eingeklammerten Worte fehlen in den ältesten Handschriften und stammen wohl aus der Parallele Lk 6,27–28, wo sie fest stehen.", "elbbk"),
        E("Wie verstehen Kirchen das „vollkommen“?", "Orthodox und katholisch: ein Ruf zu wachsender Heiligkeit, an dem Gottes Gnade mitwirkt. Lutherisch: Das Wort zeigt den Maßstab, an dem jeder scheitert, und treibt zu Christus. Wesleyanisch und methodistisch: Eine „christliche Vollkommenheit“ in der Liebe ist in diesem Leben erreichbar."),
    ],
    cards=["zoellner", "lesarten"],
    memory_verse=MV(R(MT, 5, 44), "Ich aber sage euch: Liebt eure Feinde"),
    teaser="Drei fromme Übungen, dreimal derselbe Satz über Lohn. Und ein Vater, der etwas weiß, bevor man etwas sagt.")

# ───────────────────────── 3 · Vor dem Vater ─────────────────────────
sec("vater", [R(MT, 6, 1, 8)], "Im Verborgenen",
    "Jesus warnt davor, Gutes zu tun, um gesehen zu werden. Beim Almosengeben soll man nicht vor sich herposaunen lassen, sondern so, dass die linke Hand nicht weiß, was die rechte tut. Beten soll man in der Kammer bei geschlossener Tür und ohne viele Worte, denn der Vater weiß schon, was man braucht.",
    quiz=[
        choice("Was haben die Heuchler nach V. 2 und 5?", ["Ihren Lohn schon dahin", "Gar keinen Lohn mehr", "Einen großen Lohn im Himmel", "Den Zorn Gottes"], 2, "Lies Vers 2.",
               "V. 2 und 5: Sie haben ihren Lohn dahin – sie wollten gesehen werden, und sie wurden gesehen. Mehr kommt nicht."),
        error("Die Heuchler beten gern in den Synagogen und an den Straßenecken, damit [Gott] sie sieht.", "die Menschen", 5,
              "V. 5: damit sie von den Menschen gesehen werden. Das Publikum ist das Problem, nicht der Ort."),
        choice("Warum muss man nach V. 8 nicht plappern?", ["Der Vater weiß, was ihr braucht, bevor ihr bittet", "Gott hört nur kurze Gebete", "Lange Gebete sind nur für Priester", "Gott hat ohnehin schon alles festgelegt"], 8, "Lies Vers 8.",
               "V. 8: Der Vater weiß, was ihr bedürft, ehe ihr ihn bittet."),
    ],
    explain=[
        E("Was sind Almosen?", "Gaben an Arme. Im Judentum gehörten sie mit Gebet und Fasten zu den drei großen frommen Werken (vgl. Tobit 12,8) – genau diese drei behandelt Jesus hier."),
        E("Wurde wirklich posaunt?", "Belege dafür gibt es nicht. Manche denken an die trompetenförmigen Opferkästen im Tempel, andere an eine bildhafte Redensart wie unser „etwas an die große Glocke hängen“."),
        E("Was ist die „Kammer“?", "Griechisch tameion, ein Vorratsraum im Inneren des Hauses, oft der einzige Raum mit einer Tür, die man schließen konnte. Jesus selbst betete auch öffentlich und mit anderen; hier geht es um das Gebet für Zuschauer."),
        E("Was meint „plappern“?", "Das seltene griechische Wort meint wohl das Wiederholen von Formeln und Götternamen, wie es in heidnischen Gebeten üblich war, damit der Gott sicher hört. Jesus stellt dem nicht das Schweigen gegenüber, sondern ein kurzes Gebet – das folgt im nächsten Abschnitt."),
    ],
    cards=["heuchler"],
    memory_verse=MV(R(MT, 6, 8), "denn euer Vater weiß, was ihr bedürft, ehe ihr ihn bittet."),
    try_="Lies V. 2, 5 und 16 nebeneinander. Welcher Satz kommt in allen drei Versen fast gleich vor?",
    teaser="Das bekannteste Gebet der Welt hat einen Nachsatz, den kaum jemand mitspricht.")

sec("vater", [R(MT, 6, 9, 18)], "Unser Vater",
    "Jesus gibt ein Gebet vor: Unser Vater in den Himmeln – dein Name werde geheiligt, dein Reich komme, dein Wille geschehe; gib uns unser Brot, vergib uns, wie wir vergeben, führe uns nicht in Versuchung und rette uns vom Bösen. Danach betont er das Vergeben noch einmal. Wer fastet, soll sich salben und das Gesicht waschen, damit es nur der Vater sieht.",
    focus="Achte darauf, wie das Gebet aufgebaut ist: Worum geht es in der ersten Hälfte, worum in der zweiten?",
    quiz=[
        order("In welcher Reihenfolge stehen die Bitten?", ["Dein Name werde geheiligt", "Dein Reich komme", "Unser nötiges Brot gib uns heute", "Vergib uns unsere Schuld", "Errette uns von dem Bösen"],
              "V. 9–13: Zuerst drei Bitten um Gottes Sache (Name, Reich, Wille), dann die Bitten für uns (Brot, Vergebung, Bewahrung).", "Lies Vers 9–13."),
        choice("Welche Bitte greift Jesus in V. 14–15 noch einmal auf?", ["Die Bitte um Vergebung", "Die Bitte um Brot", "Die Bitte um Gottes Reich", "Die Bitte um Bewahrung vor Versuchung"], 14, "Lies Vers 14–15.",
               "V. 14–15: Nur die Bitte um Vergebung bekommt einen Nachsatz – das Vergeben untereinander und das Vergeben Gottes hängen zusammen."),
        tf("Wer fastet, soll nach V. 17 sein Haupt salben und sein Gesicht waschen.", True, 17, "Lies Vers 17.",
           "V. 17: Wie an einem gewöhnlichen Tag aussehen – im Gegensatz zu den Heuchlern, die düster dreinschauen (V. 16)."),
    ],
    explain=[
        E("Was heißt „nötiges Brot“?", "Das griechische Wort epiousios gibt es fast nur hier und in der Parallele bei Lukas. Mögliche Bedeutungen: das Brot, das man heute braucht; das Brot für den kommenden Tag; oder, wie Hieronymus übersetzte, „überwesentliches“ Brot, was viele mit dem Abendmahl verbanden. Deshalb übersetzen Bibeln es verschieden."),
        E("Wo ist „Denn dein ist das Reich“?", "Der bekannte Schluss fehlt in den ältesten Handschriften von Matthäus. Er stammt wohl aus dem gottesdienstlichen Gebrauch; eine kürzere Form steht schon in der Didache um 100 n. Chr. Evangelische und Orthodoxe beten ihn mit, in der katholischen Messe folgt er nach einem eingeschobenen Gebet.", "elbbk"),
        E("Führt Gott in Versuchung?", "Jak 1,13 sagt, Gott versuche niemanden. Das griechische Wort peirasmos heißt auch „Prüfung“ oder „Bedrängnis“. Viele verstehen die Bitte so: Lass uns nicht in eine Lage kommen, in der wir untergehen. Die italienischen Bischöfe änderten 2018 ihre Übersetzung in „überlass uns nicht der Versuchung“; die deutschen Bischöfe behielten die vertraute."),
        E("Wann fastete man?", "Fromme Juden fasteten freiwillig zweimal pro Woche (vgl. Lk 18,12), nach späteren Quellen montags und donnerstags. Die Didache rät den Christen, mittwochs und freitags zu fasten – ausdrücklich, um sich von den „Heuchlern“ zu unterscheiden."),
    ],
    cards=["vaterunser"],
    fact="Bei Lukas beginnt das Gebet nur mit „Vater“ und hat fünf Bitten (Lk 11,2–4). Bei Matthäus sind es sieben, wenn man die Bitte um Gottes Willen und die um Rettung vor dem Bösen als eigene Bitten zählt – so zählte schon Augustinus.",
    memory_verse=MV(R(MT, 6, 10), "dein Reich komme; dein Wille geschehe, wie im Himmel, so auch auf der Erde."),
    try_="Bete das Vaterunser heute einmal sehr langsam und halte nach jeder Bitte kurz an.",
    teaser="Motten, Rost und Diebe – und dann ein Satz über das Auge, der im Hebräischen etwas ganz anderes bedeutet, als man denkt.")

sec("vater", [R(MT, 6, 19, 24)], "Wo dein Herz ist",
    "Jesus rät, keine Schätze auf der Erde zu sammeln, wo Motte, Rost und Diebe sie zerstören, sondern im Himmel – denn wo der Schatz ist, ist auch das Herz. Das Auge ist die Lampe des Leibes: Ist es einfältig, ist der ganze Leib hell. Niemand kann zwei Herren dienen, Gott und dem Mammon.",
    quiz=[
        choice("Was folgt nach V. 21 dem Schatz?", ["Das Herz", "Die Augen", "Die Sorgen", "Der Lohn"], 21, "Lies Vers 21.",
               "V. 21: Wo dein Schatz ist, da wird auch dein Herz sein."),
        error("Niemand kann zwei Herren dienen; ihr könnt nicht Gott dienen und dem [Kaiser].", "Mammon", 24,
              "V. 24: Gott und dem Mammon – das aramäische Wort für Besitz, hier wie ein zweiter Herr dargestellt."),
        tf("Nach V. 22–23 hängt es am Auge, ob der ganze Leib hell oder finster ist.", True, 22, "Lies Vers 22–23.",
           "V. 22–23: Das Auge ist die Lampe des Leibes. Was es bedeutet, ist im Zusammenhang mit Besitz zu lesen – siehe „Versteh ich nicht“."),
    ],
    explain=[
        E("Was ist ein „einfältiges“ Auge?", "Griechisch haplous: einfach, ungeteilt, aber auch großzügig. Das „böse Auge“ ist im Hebräischen eine Redewendung für Neid und Geiz (z. B. 5Mo 15,9; Spr 28,22). Weil V. 19–24 von Besitz handeln, lesen viele den Satz so: Wer großzügig blickt, ist ganz hell."),
        E("Schätze im Himmel?", "Der Ausdruck war im Judentum geläufig für gute Taten, besonders Gaben an Arme, die bei Gott „aufbewahrt“ sind. In 19,21 sagt Jesus zu einem reichen jungen Mann, er solle seinen Besitz den Armen geben, dann habe er einen Schatz im Himmel."),
        E("Rost oder Fraß?", "Das griechische Wort brosis heißt wörtlich „Fressen“. Manche Übersetzungen haben „Rost“, andere „Wurm“ oder „Fraß“. Gemeint ist alles, was Vorräte und Stoffe zerstört.", "elbbk"),
    ],
    cards=["mammon"],
    memory_verse=MV(R(MT, 6, 21), "denn wo dein Schatz ist, da wird auch dein Herz sein."),
    try_="Lies V. 19–24 als Ganzes und frag dich: Wie hängen Schatz, Auge und die zwei Herren zusammen?",
    teaser="Vögel, Wildblumen und die Frage, ob man mit Sorgen größer werden kann.")

sec("vater", [R(MT, 6, 25, 34)], "Sorgt euch nicht",
    "Jesus sagt: Sorgt euch nicht um Essen, Trinken und Kleidung. Die Vögel säen nicht und werden ernährt, die Lilien arbeiten nicht und sind schöner gekleidet als Salomo. Wer kann durch Sorgen sein Leben verlängern? Der Vater weiß, was ihr braucht. Sucht zuerst sein Reich und seine Gerechtigkeit; morgen sorgt für sich selbst.",
    quiz=[
        choice("Mit wem vergleicht Jesus in V. 29 die Lilien?", ["Mit Salomo in seiner Herrlichkeit", "Mit dem Hohepriester im Tempel", "Mit dem Kaiser in Rom", "Mit den Engeln im Himmel"], 29, "Lies Vers 29.",
               "V. 29: Nicht einmal Salomo in all seiner Herrlichkeit war so gekleidet. Von Salomos Reichtum erzählt 1Kön 10."),
        order("In welcher Reihenfolge kommen die Bilder vor?", ["Die Vögel des Himmels", "Eine Elle zur Größe", "Die Lilien des Feldes", "Das Gras im Ofen"],
              "V. 26, 27, 28 und 30: Vögel, Elle, Lilien, Gras – Tiere und Pflanzen, die nicht vorsorgen und doch versorgt sind.", "Lies Vers 26–30."),
        choice("Was sollen die Hörer nach V. 33 zuerst suchen?", ["Gottes Reich und seine Gerechtigkeit", "Eine sichere Arbeit", "Den Frieden mit allen Menschen", "Die Vergebung ihrer Sünden"], 33, "Lies Vers 33.",
               "V. 33: zuerst das Reich Gottes und seine Gerechtigkeit – und dies alles wird hinzugefügt."),
    ],
    explain=[
        E("Größe oder Lebenszeit?", "Das griechische Wort helikia heißt beides: Körpergröße und Lebensalter. Die Elle (etwa 45 cm) passt eher zur Größe, der Zusammenhang eher zur Lebenszeit. Deshalb übersetzen manche Bibeln „sein Leben um eine Spanne verlängern“."),
        E("Welche Blumen sind die Lilien?", "Unklar. Das Wort meint wohl allgemein die bunten Wildblumen Galiläas, etwa Anemonen, die im Frühjahr ganze Hänge rot färben."),
        E("Warum Gras im Ofen?", "Holz war knapp; getrocknetes Gras und Dornen wurden als Brennstoff für Backöfen verwendet. Heute blüht es, morgen ist es Heizmaterial."),
        E("Wer sind „die Nationen“?", "So übersetzt die Elberfelder das griechische ethne, die nichtjüdischen Völker, die den Gott Israels nicht kannten. Andere Bibeln schreiben „die Heiden“.", "elbbk"),
    ],
    memory_verse=MV(R(MT, 6, 33), "Trachtet aber zuerst nach dem Reich Gottes und nach seiner Gerechtigkeit"),
    prayer={"ref": R(PS, 31, 15, 16), "source": "Psalm 31,15–16"},
    teaser="Splitter und Balken – und danach ein Satz über Hunde und Schweine, den schon die frühe Kirche auf etwas Bestimmtes bezog.")

# ───────────────────────── 4 · Zwei Wege ─────────────────────────
sec("wege", [R(MT, 7, 1, 6)], "Splitter und Balken",
    "Richtet nicht, damit ihr nicht gerichtet werdet; mit dem Maß, mit dem ihr messt, wird euch gemessen. Wer den Splitter im Auge seines Bruders sieht, soll zuerst den Balken aus dem eigenen ziehen – dann sieht er klar, um dem Bruder zu helfen. Und: Das Heilige nicht den Hunden geben, die Perlen nicht vor die Schweine werfen.",
    quiz=[
        who("Erlaube, ich will den Splitter aus deinem Auge ziehen", R(MT, 7, 4), ["Einer, der selbst einen Balken im Auge hat", "Ein Arzt in Kapernaum", "Ein Pharisäer zu Jesus", "Ein Bruder, der helfen will und klar sieht"],
            "V. 4: Das sagt der mit dem Balken im eigenen Auge – Jesus nennt ihn in V. 5 Heuchler.", "Lies Vers 4–5."),
        tf("Nach V. 5 soll man sich nie um den Splitter im Auge des Bruders kümmern.", False, 5, "Lies Vers 5 bis zum Ende.",
           "V. 5: Zuerst den Balken aus dem eigenen Auge – dann sieht man klar, um den Splitter herauszuziehen. Die Hilfe ist nicht verboten, aber die Reihenfolge ist klar."),
        choice("Womit wird man nach V. 2 gemessen?", ["Mit dem Maß, mit dem man selbst misst", "Mit dem Gesetz des Mose", "Mit dem Maß der Engel", "Mit einem gnädigeren Maß"], 2, "Lies Vers 2.",
               "V. 2: Mit dem Maß, mit dem ihr messt, wird euch gemessen werden."),
    ],
    explain=[
        E("Ist jedes Urteilen verboten?", "Der Abschnitt selbst verlangt Unterscheidung: In V. 6 und V. 15–20 muss man sehr wohl beurteilen. Viele verstehen „richten“ hier als Verurteilen und Abschreiben eines Menschen, nicht als jedes Urteil über Richtig und Falsch."),
        E("Was meint V. 6?", "Der Vers ist rätselhaft. Hunde und Schweine galten als unrein. Die Didache (9,5) bezieht ihn auf das Abendmahl: Nur Getaufte sollen davon essen. Andere sehen darin den Rat, Wertvolles nicht Menschen aufzudrängen, die es nur verachten."),
    ],
    fact="Splitter und Balken sind Holzwörter: karphos ist ein Spänchen, dokos ein Dachbalken. Matthäus nennt Jesus den Sohn des Zimmermanns (13,55), Markus ihn selbst einen Zimmermann (Mk 6,3).",
    memory_verse=MV(R(MT, 7, 1), "Richtet nicht, damit ihr nicht gerichtet werdet"),
    teaser="Ein Sohn bittet um Brot. Welcher Vater gibt ihm einen Stein?")

sec("wege", [R(MT, 7, 7, 12)], "Bittet, sucht, klopft an",
    "Bittet, sucht, klopft an – wer bittet, empfängt; wer sucht, findet; wem anklopft, dem wird geöffnet. Kein Vater gibt seinem Kind einen Stein statt Brot. Wenn schon Menschen, die böse sind, ihren Kindern Gutes geben, wie viel mehr der Vater in den Himmeln. Dann die Goldene Regel: Was ihr wollt, dass andere euch tun, das tut ihnen – das ist das Gesetz und die Propheten.",
    quiz=[
        order("In welcher Reihenfolge stehen die drei Aufforderungen in V. 7?", ["Bittet", "Sucht", "Klopft an"],
              "V. 7: bitten, suchen, anklopfen – und in V. 8 wiederholt in derselben Reihenfolge.", "Lies Vers 7."),
        choice("Was gibt nach V. 10 kein Vater seinem Kind, das um einen Fisch bittet?", ["Eine Schlange", "Einen Skorpion", "Einen Stein", "Ein Brot"], 10, "Lies Vers 9–10.",
               "V. 10: eine Schlange statt eines Fisches. Der Stein statt Brot steht in V. 9. Lukas hat dazu ein Ei und einen Skorpion (Lk 11,12)."),
        choice("Was ist nach V. 12 die Goldene Regel?", ["Das Gesetz und die Propheten", "Ein neues Gebot, das das Gesetz ablöst", "Eine Regel nur für die Jünger", "Die Zusammenfassung der Seligpreisungen"], 12, "Lies Vers 12 bis zum Ende.",
               "V. 12: Dies ist das Gesetz und die Propheten. Damit schließt sich die Klammer, die in 5,17 begann."),
    ],
    explain=[
        E("Gab es die Goldene Regel schon vorher?", "In verneinter Form ja: Tobit 4,15 rät, niemandem zu tun, was man selbst hasst. Von Rabbi Hillel, einem älteren Zeitgenossen Jesu, wird erzählt, er habe so die ganze Tora zusammengefasst; der Rest sei Auslegung. Jesus formuliert positiv: nicht nur unterlassen, sondern tun."),
        E("„Die ihr böse seid“?", "Jesus spricht beiläufig und ohne Vorwurf aus, dass seine Hörer nicht gut sind wie Gott – und trotzdem ihren Kindern Gutes geben. Das Argument geht vom Kleineren zum Größeren: Wenn schon ihr, wie viel mehr Gott."),
        E("Bekommt man alles, worum man bittet?", "Der Text verspricht, dass der Vater Gutes gibt (V. 11); bei Lukas heißt es, er gebe den Heiligen Geist (Lk 11,13). Wie das mit unerhörten Gebeten zusammengeht, haben Christen immer wieder gefragt – auch Jesus selbst betete in Gethsemane um etwas, das nicht geschah (26,39)."),
    ],
    memory_verse=MV(R(MT, 7, 7), "Bittet, und es wird euch gegeben werden; sucht, und ihr werdet finden"),
    prayer={"ref": R(PS, 27, 7, 8), "source": "Psalm 27,7–8"},
    teaser="Zwei Tore, zwei Wege – und Wölfe, die aussehen wie Schafe.")

sec("wege", [R(MT, 7, 13, 20)], "Enge Pforte, gute Früchte",
    "Jesus spricht von zwei Pforten: Die weite und der breite Weg führen ins Verderben, und viele gehen dort; die enge und der schmale Weg führen zum Leben, und wenige finden ihn. Dann warnt er vor falschen Propheten in Schafskleidern. Man erkennt sie an ihren Früchten, wie man einen Baum an seinen Früchten erkennt.",
    quiz=[
        choice("Woran erkennt man nach V. 16 die falschen Propheten?", ["An ihren Früchten", "An ihren Worten", "An ihren Wundern", "An ihrer Kleidung"], 16, "Lies Vers 16 und 20.",
               "V. 16 und 20: An ihren Früchten werdet ihr sie erkennen – der Satz rahmt den Abschnitt ein."),
        tf("Nach V. 13–14 führt der breite Weg zum Leben.", False, 14, "Lies Vers 13–14.",
           "V. 13–14: Der breite Weg führt ins Verderben, der schmale zum Leben."),
        error("Die falschen Propheten kommen in [Wolfspelzen], innen aber sind sie reißende Wölfe.", "Schafskleidern", 15,
              "V. 15: in Schafskleidern. Von außen sehen sie aus wie die Herde."),
    ],
    explain=[
        E("Woher kommt das Bild der zwei Wege?", "Es ist alt: 5Mo 30,15 stellt Leben und Tod vor das Volk, Ps 1 den Weg der Gerechten und der Gottlosen, Jer 21,8 den Weg des Lebens und des Todes. Die Didache beginnt gleich mit dem Satz, es gebe zwei Wege, einen des Lebens und einen des Todes."),
        E("Was sind die Früchte?", "Im Zusammenhang wohl das Tun, das zu den Worten passt – oder nicht passt (vgl. V. 21). Manche denken auch an die Lehre, also das, was durch einen Propheten in anderen wächst. Galater 5,22 zählt die Frucht des Geistes auf."),
    ],
    fact="Der Ausdruck „Wolf im Schafspelz“ geht auf diesen Vers zurück. Er ist so verbreitet, dass viele nicht mehr wissen, dass er aus der Bibel stammt.",
    memory_verse=MV(R(MT, 7, 20), "Deshalb, an ihren Früchten werdet ihr sie erkennen."),
    teaser="Manche werden am Ende Wunder vorzeigen können – und trotzdem einen erschreckenden Satz hören.")

sec("wege", [R(MT, 7, 21, 29)], "Fels oder Sand",
    "Nicht jeder, der „Herr, Herr“ sagt, kommt ins Reich der Himmel, sondern wer den Willen des Vaters tut. Manche werden auf Weissagungen und Wunder verweisen und hören: Ich habe euch nie gekannt. Wer Jesu Worte hört und tut, baut auf Felsen; wer sie hört und nicht tut, auf Sand. Die Menge staunt, denn er lehrt wie einer mit Vollmacht.",
    place="berg-seligpreisungen",
    focus="Achte darauf, was die beiden Hausbauer gemeinsam haben – und was sie unterscheidet.",
    quiz=[
        choice("Worauf verweisen die Leute in V. 22?", ["Auf Weissagen, Dämonen austreiben und Wunder in seinem Namen", "Auf ihre Opfer und Gebete", "Auf ihre Herkunft von Abraham", "Auf ihre Almosen und ihr Fasten"], 22, "Lies Vers 22.",
               "V. 22: Sie haben in seinem Namen geweissagt, Dämonen ausgetrieben und viele Wunder getan. Trotzdem sagt er, er habe sie nie gekannt (V. 23)."),
        choice("Was unterscheidet nach V. 24 und 26 die beiden Hausbauer?", ["Der eine tut die Worte, der andere nicht", "Der eine hört die Worte, der andere nicht", "Der eine baut schneller", "Der eine hat mehr Geld"], 26, "Lies Vers 24 und 26.",
               "V. 24 und 26: Beide hören die Worte. Der Unterschied ist das Tun – und das zeigt sich erst im Sturm."),
        tf("Nach V. 28–29 lehrte Jesus wie die Schriftgelehrten.", False, 29, "Lies Vers 29.",
           "V. 29: Er lehrte wie einer, der Vollmacht hat, und nicht wie die Schriftgelehrten."),
    ],
    explain=[
        E("Was heißt hier „Gewalt“?", "Griechisch exousia: Vollmacht, Autorität. Die Schriftgelehrten beriefen sich auf frühere Lehrer; Jesus sagte „Ich aber sage euch“. Neuere Übersetzungen schreiben „Vollmacht“.", "elbbk"),
        E("Rechtfertigung aus Glauben und dieser Text?", "Die Frage, wie das Tun zum Glauben steht, beschäftigt die Kirchen seit der Reformation. Evangelische betonen: Gerettet wird man aus Gnade durch Glauben, das Tun ist Frucht. Katholische Lehre betont das Mitwirken mit der Gnade. Die Gemeinsame Erklärung zur Rechtfertigungslehre (1999) hält fest, dass beide Seiten Gnade und gute Werke zusammen sehen, wenn auch verschieden betont."),
        E("Wie kommt ein Haus auf Sand?", "In Palästina führen Trockentäler (Wadis) den größten Teil des Jahres kein Wasser; ihr Boden ist eben und bequem zum Bauen. Nach einem Wolkenbruch werden sie in kurzer Zeit zu reißenden Flüssen."),
    ],
    fact="Bonhoeffer schrieb 1937 sein Buch „Nachfolge“ vor allem über die Bergpredigt. Darin prägte er den Begriff der „billigen Gnade“: Gnade, die nichts kostet und nichts verändert.",
    memory_verse=MV(R(MT, 7, 24), "Jeder nun, der irgend diese meine Worte hört und sie tut"),
    try_="Lies heute noch einmal Mt 5,1–2 und dann 7,28–29. Wer hört am Anfang zu, und wer staunt am Ende?")

P.write()
