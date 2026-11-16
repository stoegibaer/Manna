#!/usr/bin/env python3
"""Source for the reading plan „Micha – Was Gott von dir will“ (generates assets/plans/micha.json).

python3 -I tools/plans/micha.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/micha.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

MI = 33

P = PlanBuilder(
    "micha", "mi", "Micha", "Was Gott von dir will",
    "Ein Prophet vom Land legt sich mit den Mächtigen in Jerusalem an: mit Landräubern, käuflichen Richtern und Propheten, "
    "die je nach Bezahlung predigen. Zwischen harten Gerichtsworten stehen einige der bekanntesten Hoffnungstexte der Bibel – "
    "Schwerter zu Pflugmessern, Bethlehem und die Frage, was Gott eigentlich vom Menschen will. 15 Abschnitte durch das ganze Buch.",
    "gerechtigkeit",
    stages=[("voelker", "Hört, ihr Völker"), ("haeupter", "Hört, ihr Häupter"), ("rechtsstreit", "Hört, was der HERR sagt")],
    cards=[
        ("micha", "person", "Micha", "Prophet aus Moreschet im Hügelland Judas. Er wirkte unter den Königen Jotam, Ahas und Hiskia, etwa 740–700 v. Chr., zur selben Zeit wie Jesaja. Sein Name ist die Kurzform von Michajahu, „Wer ist wie Jahwe?“. Er kam nicht aus der Hauptstadt und spricht vor allem gegen ihre Mächtigen. Hundert Jahre später zitierte man ihn in Jerusalem noch (Jer 26,18).", "Mi 1,1; Jer 26,18"),
        ("samaria", "ort", "Samaria", "Hauptstadt des Nordreichs Israel, von König Omri um 880 v. Chr. auf einem Hügel gebaut (1Kön 16,24). Ahab errichtete dort einen Tempel für Baal (1Kön 16,32). 722 v. Chr. eroberten die Assyrer die Stadt und verschleppten einen Teil der Bewohner (2Kön 17,5–6) – noch zu Michas Lebzeiten. Damit endete das Nordreich.", "1Kön 16,24; 2Kön 17,5–6"),
        ("assyrien", "begriff", "Assyrien", "Großmacht am Tigris mit der Hauptstadt Ninive. Im 8. Jahrhundert v. Chr. eroberte sie Damaskus und Samaria. 701 v. Chr. zog König Sanherib gegen Juda: Viele Städte fielen, Jerusalem wurde belagert, aber nicht eingenommen (2Kön 18–19). Micha nennt Assyrien auch das „Land Nimrods“ (Mi 5,5; vgl. 1Mo 10,8–11).", "2Kön 18,13; Mi 5,4–5"),
        ("lachisch", "ort", "Lachisch", "Nach Jerusalem die stärkste Festungsstadt Judas, im Hügelland südwestlich davon; Michas Heimat Moreschet lag in der Nähe. 701 v. Chr. eroberte Sanherib die Stadt (2Kön 18,14). Er ließ die Belagerung in seinem Palast in Ninive auf großen Steinreliefs darstellen. Sie sind heute im British Museum in London zu sehen.", "Mi 1,13; 2Kön 18,14"),
        ("ueberrest", "begriff", "Der Überrest", "Ein Leitwort der Propheten: Nach dem Gericht bleibt ein Rest des Volkes übrig, mit dem Gott weitergeht (Jes 10,20–22; Mi 2,12; 4,7; 5,6–7; 7,18). Jesajas Sohn hieß Schear-Jaschub, „ein Rest kehrt um“ (Jes 7,3). Paulus greift den Gedanken in Röm 11,5 auf.", "Mi 2,12; 5,6–7"),
        ("falsche-propheten", "begriff", "Falsche Propheten", "Propheten, die im Namen Gottes reden, ohne von ihm gesandt zu sein. Micha beschreibt sie als Leute, deren Botschaft davon abhängt, wer ihnen etwas gibt (Mi 3,5.11). Sie rufen Frieden, wo keiner ist (vgl. Jer 6,14). Nach 5Mo 18,21–22 erkennt man einen falschen Propheten daran, dass sein Wort nicht eintrifft.", "Mi 2,11; 3,5–11"),
        ("hiskia", "person", "Hiskia", "König von Juda gegen Ende des 8. Jahrhunderts v. Chr., Sohn des Ahas. Er entfernte die Höhenheiligtümer (2Kön 18,4) und suchte in der Belagerung durch Sanherib Hilfe bei Gott (2Kön 19). Nach Jer 26,19 fürchtete er den HERRN, als Micha das Ende Jerusalems ankündigte, und das Unheil kam damals nicht.", "2Kön 18–20; Jer 26,19"),
        ("zion", "ort", "Zion", "Ursprünglich die Burg der Jebusiter, die David eroberte (2Sam 5,7), später Name für den Tempelberg und für ganz Jerusalem. „Tochter Zion“ ist die Stadt, als Frau vorgestellt. In den Psalmen ist Zion der Ort, an dem Gott wohnt (Ps 46; 48). Im Hebräerbrief ist der Berg Zion auch ein Bild für Gottes Stadt, zu der Christen schon gekommen sind (Hebr 12,22).", "Mi 3,12; 4,1–8"),
        ("ende-der-tage", "begriff", "Am Ende der Tage", "Hebräisch beacharit hajamim, „am Ende“ oder „in der Folge der Tage“: eine Zukunft, in der Gott sein Ziel erreicht. Dispensationalisten erwarten die wörtliche Erfüllung im Tausendjährigen Reich nach der Wiederkunft Jesu. Amillenialisten sehen den Anfang schon in Jesus und der weltweiten Gemeinde (Apg 2,17; Hebr 1,2) und die Vollendung in der neuen Schöpfung.", "Mi 4,1; Jes 2,2"),
        ("bethlehem", "ort", "Bethlehem-Ephrata", "Kleine Stadt etwa 8 km südlich von Jerusalem, auch Ephrata genannt (1Mo 35,19; Rut 4,11). Heimat von Boas und Rut und von David, der dort zum König gesalbt wurde (1Sam 16). Nach Matthäus und Lukas wurde Jesus dort geboren; Matthäus zitiert dazu Mi 5,1.", "Mi 5,1; Mt 2,1–6"),
        ("rechtsstreit", "begriff", "Rechtsstreit (riv)", "Ein Prozess, in dem Gott als Kläger gegen sein Volk auftritt, oft mit Himmel, Erde oder Bergen als Zeugen (5Mo 32,1; Jes 1,2; Hos 4,1). Grundlage ist der Bund vom Sinai. Gottes Frage aus Mi 6,3 kehrt in den Improperien wieder, den Klageversen der Karfreitagsliturgie (lateinisch Popule meus).", "Mi 6,1–5"),
        ("chesed", "begriff", "Güte (chesed)", "Eines der reichsten Wörter des Alten Testaments: Güte, Treue und Liebe, die zu einer Beziehung stehen. Übersetzungen sagen Gnade, Güte, Barmherzigkeit oder Bundestreue. In Mi 6,8 soll der Mensch sie lieben, in Mi 7,18 hat Gott Gefallen an ihr. Hos 6,6 stellt sie über das Opfer; Jesus zitiert den Vers (Mt 9,13).", "Mi 6,8; 7,18.20"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Hört, ihr Völker (Kap. 1–2) ─────────────────────────
sec("voelker", [R(MI, 1, 1, 7)], "Gott kommt herab",
    "Micha aus Moreschet empfängt Worte über Samaria und Jerusalem. Gott tritt aus seinem Palast, unter ihm schmelzen die Berge. Der Grund ist die Schuld Israels und Judas – und ihr Ausgangspunkt sind die Hauptstädte. Samaria soll ein Steinhaufen werden.",
    place="samaria",
    focus="Achte darauf, wo die Schuld nach V. 5 ihren Ursprung hat.",
    quiz=[
        choice("Unter welchen Königen wirkt Micha?", ["Jotam, Ahas und Hiskia", "David, Salomo und Rehabeam", "Ahab, Jehu und Jerobeam", "Josia, Jojakim und Zedekia"], 1, "Lies Vers 1.",
               "V. 1: in den Tagen Jotams, Ahas' und Hiskias, der Könige von Juda – grob die zweite Hälfte des 8. Jahrhunderts v. Chr."),
        tf("Nach V. 5 geht die Schuld Judas von den Dörfern auf dem Land aus.", False, 5, "Lies Vers 5.",
           "V. 5: Die Übertretung Jakobs kommt aus Samaria, die „Höhen Judas“ aus Jerusalem – also aus den beiden Hauptstädten."),
        error("Gott kündigt an, Samaria zu einem [Bollwerk] des Feldes zu machen.", "Steinhaufen", 6,
              "V. 6: Samaria wird ein Steinhaufen im Feld, wo man Weinberge anlegt; ihre Steine werden ins Tal gestürzt."),
    ],
    explain=[
        E("Wer war Micha?", "Ein Prophet aus Moreschet, einem kleinen Ort im Hügelland südwestlich von Jerusalem (vgl. V. 14). Anders als sein Zeitgenosse Jesaja war er kein Mann aus der Hauptstadt. Sein Name bedeutet „Wer ist wie Jahwe?“."),
        E("Was heißt „Moraschtiter“?", "Einer aus Moreschet, Michas Heimatort (in V. 14 Moreschet-Gat).", "elbbk"),
        E("Was sind die „Höhen“?", "Kultstätten auf Hügeln, an denen neben oder statt des Tempels geopfert wurde, oft auch für andere Götter. In V. 5 nennt Micha überraschend Jerusalem selbst die „Höhen Judas“."),
        E("Warum ist von „Hurenlohn“ die Rede?", "Die Propheten beschreiben die Verehrung anderer Götter oft als eheliche Untreue (Hos 1–3). Gemeint sind in V. 7 wohl Gaben und Bilder für fremde Götter; ob auch Tempelprostitution mitgemeint ist, wird verschieden gesehen."),
    ],
    cards=["micha", "samaria"],
    teaser="Im nächsten Abschnitt steckt in fast jedem Ortsnamen ein Wortspiel – und der erste Satz stammt eigentlich von David.")

sec("voelker", [R(MI, 1, 8, 16)], "Klage über die Städte",
    "Micha klagt und geht entblößt umher, denn der Schlag reicht bis an das Tor Jerusalems. Er zählt Städte im Hügelland Judas auf, darunter seine Heimat, und spielt mit ihren Namen. Die Kinder werden weggeführt.",
    place="lachisch",
    quiz=[
        choice("Wie zeigt Micha seine Trauer in V. 8?", ["Er geht entblößt und nackt umher und klagt", "Er zerreißt seine Kleider und schweigt", "Er fastet vierzig Tage", "Er zieht sich in den Tempel zurück"], 8, "Lies Vers 8.",
               "V. 8: Micha will klagen und heulen, entblößt und nackt umhergehen – Zeichen der Trauer und der kommenden Gefangenschaft."),
        tf("Unter den Orten, die Micha nennt, ist auch sein eigener Heimatort.", True, 14, "Lies Vers 14.",
           "V. 14: Zion muss Moreschet-Gat, Michas Heimat, ein „Entlassungsgeschenk“ geben – die Stadt geht verloren."),
        choice("Warum soll sich die Tochter Zion kahl scheren?", ["Weil ihre Kinder weggeführt sind", "Weil ein Fest beginnt", "Weil sie ein Gelübde abgelegt hat", "Weil der König gestorben ist"], 16, "Lies Vers 16.",
               "V. 16: Sie soll sich kahl scheren um ihrer Kinder willen, denn sie sind von ihr weggeführt."),
    ],
    explain=[
        E("Welche Wortspiele stecken in den Namen?", "Im Hebräischen klingen Name und Unheil zusammen: Beth-Leaphra („Staubhausen“) – im Staub wälzen; Schaphir („Schönheit“) – Blöße; Marot („Bitterkeit“); Lachisch – rechesch, „Renner“; Aksib – achsav, „trügerisch“; Marescha – „Besitznehmer“. Deutsch lässt sich das kaum nachbilden."),
        E("Warum ausgerechnet Gat?", "V. 10 beginnt mit denselben Worten wie Davids Klage über Saul und Jonatan (2Sam 1,20). Gat war eine Stadt der Philister: Die Feinde sollen sich nicht über das Unglück freuen."),
        E("Warum ist Lachisch der „Anfang der Sünde“?", "Lachisch war eine Festungs- und Wagenstadt. Was genau Micha mit V. 13 meint, sagt er nicht; viele Ausleger denken an das Vertrauen auf Pferde und Wagen (vgl. 5,9)."),
        E("Warum sich kahl scheren?", "Haare abschneiden war ein Trauerbrauch (Jes 22,12; Am 8,10). Der Geier in V. 16 ist wohl ein Aasgeier mit kahlem Kopf."),
    ],
    cards=["assyrien", "lachisch"],
    teaser="Was Micha als Nächstes anprangert, beginnt nachts im Bett.")

sec("voelker", [R(MI, 2, 1, 5)], "Wehe den Ackerräubern",
    "Wehe denen, die nachts Böses planen und es morgens ausführen, weil sie die Macht dazu haben: Sie nehmen anderen Äcker und Häuser weg. Gott plant nun seinerseits Unheil gegen sie. Ihr Land wird verteilt, und sie werden keinen Anteil mehr haben.",
    quiz=[
        choice("Warum können sie ihre Pläne nach V. 1 ausführen?", ["Weil es in ihrer Macht steht", "Weil das Gesetz es erlaubt", "Weil der König es befiehlt", "Weil niemand es bemerkt"], 1, "Lies Vers 1.",
               "V. 1: Beim Morgenlicht führen sie es aus, weil es in der Macht ihrer Hand steht."),
        error("Sie begehren nach Äckern und rauben sie, und nach [Herden] und nehmen sie weg.", "Häusern", 2,
              "V. 2: Äcker und Häuser – das Erbteil der Familien. „Begehren“ ist dasselbe Wort wie im Gebot „Du sollst nicht begehren“ (2Mo 20,17)."),
        choice("Was wird ihnen nach V. 5 fehlen?", ["Jemand, der für sie in der Versammlung des HERRN die Messschnur wirft", "Ein Priester, der für sie opfert", "Ein König, der sie schützt", "Ein Prophet, der für sie betet"], 5, "Lies Vers 5.",
               "V. 5: Wenn das Land neu verteilt wird, bekommen sie kein Los und keinen Anteil mehr."),
    ],
    explain=[
        E("Warum ist ein Acker so wichtig?", "Das Land war das Erbteil der Familie, beim Einzug unter Josua durch das Los verteilt (Jos 13–19). Es sollte nicht für immer verkauft werden (3Mo 25,23). Wer es verlor, verlor seine Lebensgrundlage – wie Nabot seinen Weinberg (1Kön 21)."),
        E("Was ist die Messschnur?", "Mit Schnur und Los wurde Land vermessen und verteilt. V. 5 dreht das um: Wer anderen das Land genommen hat, steht bei der nächsten Verteilung ohne Anteil da."),
        E("Wer klagt in V. 4?", "Die Landräuber selbst. Man stimmt ein Spottlied über sie an, in dem sie jammern, dass ihre Felder einem anderen zugeteilt werden."),
    ],
    try_="Lies V. 1 und V. 3. Welches Wort kommt in beiden vor, und wer tut es jeweils?",
    teaser="Man will Micha den Mund verbieten. Welchen Propheten hätten die Leute lieber?")

sec("voelker", [R(MI, 2, 6, 13)], "„Weissagt nicht!“",
    "Man will Micha zum Schweigen bringen. Gott hält dagegen: Sein Volk zieht friedlichen Leuten den Mantel weg und vertreibt Frauen und Kinder aus ihren Häusern. Ein Prophet, der von Wein redet, wäre ihnen lieber. Dann plötzlich: Gott will den Überrest sammeln wie eine Herde, und ein Durchbrecher zieht vor ihnen her.",
    quiz=[
        choice("Was sagen die Gegner nach V. 6?", ["Man soll nicht weissagen", "Man soll für sie beten", "Micha soll nach Samaria gehen", "Micha soll ein Opfer bringen"], 6, "Lies Vers 6.",
               "V. 6: „Weissagt nicht“ – so reden sie gegen die Propheten."),
        tf("Nach V. 9 werden auch Frauen aus ihren Häusern vertrieben.", True, 9, "Lies Vers 9.",
           "V. 9: Die Frauen werden aus ihren Häusern vertrieben, den Kindern wird Gottes „Schmuck“ für immer genommen."),
        choice("Welcher Prophet würde nach V. 11 zu diesem Volk passen?", ["Einer, der von Wein und starkem Getränk weissagt", "Einer, der zur Umkehr ruft", "Einer aus Jerusalem", "Einer, der Wunder tut"], 11, "Lies Vers 11.",
               "V. 11: Ein Lügner, der Wein und starkes Getränk verspricht, wäre der passende Prophet für dieses Volk."),
    ],
    explain=[
        E("Wer redet in V. 6–7?", "Die Verse sind im Hebräischen sehr knapp; es wechseln Worte der Gegner und Antworten Gottes oder Michas. Übersetzungen setzen die Anführungszeichen deshalb verschieden."),
        E("Passen V. 12–13 hierher?", "Die meisten Ausleger lesen sie als plötzliche Verheißung, wie sie bei Micha öfter auf ein Gerichtswort folgt. Andere meinen, Micha zitiere hier die bequeme Botschaft der Propheten aus V. 11. Der Text markiert es nicht."),
        E("Wer ist der „Durchbrecher“?", "Das hebräische Wort hängt mit dem Namen Perez zusammen (1Mo 38,29), einem Vorfahren Davids. Einige jüdische Ausleger haben deshalb an den Messias gedacht; christliche Leser an Christus, der seiner Herde vorangeht (Joh 10,4)."),
        E("Was sind die „Schafe von Bozra“?", "Bozra war eine Stadt in Edom. Das Wort kann auch „Pferch“ bedeuten; viele Übersetzungen sagen deshalb „wie Schafe im Pferch“.", "elbbk"),
    ],
    cards=["ueberrest"],
    teaser="Für die Führer des Volkes findet Micha ein Bild aus der Küche.")

# ───────────────────────── 2 · Hört, ihr Häupter (Kap. 3–5) ─────────────────────────
sec("haeupter", [R(MI, 3, 1, 8)], "Wie Fleisch im Kessel",
    "Micha spricht die Führer an: Sie müssten das Recht kennen, behandeln das Volk aber wie Fleisch im Kochtopf. Die Propheten rufen Frieden, solange man sie füttert. Ihnen wird es Nacht werden. Micha dagegen ist von Gottes Geist erfüllt, mit Recht und Stärke.",
    place="jerusalem",
    focus="Achte auf V. 8. Worin unterscheidet sich Micha von den Propheten in V. 5–7?",
    quiz=[
        choice("Was müssten die Häupter nach V. 1 eigentlich kennen?", ["Das Recht", "Die Zukunft", "Die Kriegskunst", "Die Opfergesetze"], 1, "Lies Vers 1.",
               "V. 1: Ist es nicht an euch, das Recht zu kennen?"),
        tf("Die Propheten in V. 5 rufen „Frieden“, wenn man ihnen etwas zu essen gibt.", True, 5, "Lies Vers 5.",
           "V. 5: Wer ihnen etwas zu beißen gibt, dem verkünden sie Frieden; wer nichts gibt, gegen den rufen sie Krieg aus."),
        who("Ich hingegen, ich bin mit Kraft erfüllt durch den Geist des HERRN", R(MI, 3, 8), ["Micha", "Einer der Seher", "Ein Fürst des Hauses Israel", "Ein Priester in Jerusalem"],
            "V. 8: Micha stellt sich selbst den Propheten aus V. 5–7 gegenüber."),
    ],
    explain=[
        E("Warum so drastische Bilder?", "V. 2–3 beschreiben die Führer wie Metzger und Köche: Haut abziehen, Knochen zerbrechen, Fleisch in den Kessel. Micha spricht nicht von Menschenfresserei, sondern davon, wie sie mit den Menschen umgehen, die ihnen anvertraut sind."),
        E("Was sind Seher und Wahrsager?", "„Seher“ ist ein älteres Wort für Prophet (1Sam 9,9). Wahrsagerei war in Israel verboten (5Mo 18,10). Micha nennt beide in einem Atemzug (V. 7)."),
        E("Was heißt „den Bart verhüllen“?", "Ein Zeichen von Scham und Trauer (vgl. 3Mo 13,45). Die Propheten haben keine Antwort Gottes mehr und schämen sich."),
    ],
    cards=["falsche-propheten"],
    teaser="Ein Satz aus dem nächsten Abschnitt rettete hundert Jahre später einem anderen Propheten das Leben.")

sec("haeupter", [R(MI, 3, 9, 12)], "Zion wird gepflügt",
    "Führer, Priester und Propheten arbeiten für Geld und verlassen sich darauf, dass Gott in ihrer Mitte ist. Darum, sagt Micha, wird Zion wie ein Acker gepflügt, Jerusalem zum Trümmerhaufen und der Tempelberg zum bewaldeten Hügel.",
    place="jerusalem",
    quiz=[
        order("Wofür arbeiten die drei Gruppen in V. 11? Bring sie in die Reihenfolge des Verses.",
              ["Die Häupter richten um Geschenke", "Die Priester lehren um Lohn", "Die Propheten wahrsagen um Geld"],
              "V. 11: Richter, Priester und Propheten – alle drei arbeiten gegen Bezahlung.", "Lies Vers 11."),
        choice("Worauf verlassen sie sich nach V. 11?", ["Dass der HERR in ihrer Mitte ist und kein Unglück kommt", "Auf die Mauern Jerusalems", "Auf ein Bündnis mit Ägypten", "Auf ihren Reichtum"], 11, "Lies Vers 11.",
               "V. 11: Sie stützen sich auf den HERRN und sagen, er sei in ihrer Mitte, kein Unglück werde kommen."),
        error("Zion wird als [Weinberg] gepflügt werden, und Jerusalem wird zu Trümmerhaufen.", "Acker", 12,
              "V. 12: Zion wird wie ein Acker gepflügt, der Tempelberg wird zu einer Waldhöhe."),
    ],
    explain=[
        E("Ist der Satz der Führer nicht richtig?", "Er klingt wie ein Psalm: Gott ist in der Mitte seiner Stadt (Ps 46,6). Micha bestreitet in V. 11 nicht, dass Gott in Zion wohnt, und antwortet mit V. 12."),
        E("Ist das eingetroffen?", "Zu Michas Zeit wurde Jerusalem nicht zerstört. Nach Jer 26,18–19 fürchtete König Hiskia den HERRN, und Gott ließ sich das Unheil gereuen. Zerstört wurden Stadt und Tempel erst 587 v. Chr. durch die Babylonier."),
    ],
    cards=["hiskia", "zion"],
    fact="Etwa hundert Jahre nach Micha sollte Jeremia für eine ähnliche Botschaft sterben. Älteste erinnerten an Michas Wort und zitierten V. 12 wörtlich, mit Namen und Herkunft des Propheten – Jeremia blieb am Leben (Jer 26,16–24).",
    try_="Lies Jer 26,16–19. Was machten die Ältesten aus Michas Wort?",
    teaser="Direkt nach dem härtesten Satz des Buches kommt einer der bekanntesten Friedenstexte der Welt. Man findet ihn fast wortgleich bei einem anderen Propheten.")

sec("haeupter", [R(MI, 4, 1, 5)], "Schwerter zu Pflugmessern",
    "Am Ende der Tage wird der Berg des HERRN höher sein als alle Berge. Völker kommen, um von Gott zu lernen; er schlichtet ihre Streitigkeiten, und sie schmieden ihre Waffen zu Ackergeräten um. Jeder sitzt ungestört unter seinem Weinstock und Feigenbaum.",
    place="jerusalem",
    focus="Achte auf den Berg: Was sagte 3,12 über ihn, und was sagt 4,1?",
    quiz=[
        choice("Warum ziehen die Völker nach V. 2 zum Berg des HERRN?", ["Um von seinen Wegen zu lernen", "Um Jerusalem zu erobern", "Um Handel zu treiben", "Um Tribut zu zahlen"], 2, "Lies Vers 2.",
               "V. 2: Er soll sie über seine Wege belehren, und sie wollen auf seinen Pfaden gehen."),
        error("Sie werden ihre Schwerter zu Pflugmessern schmieden und ihre [Schilde] zu Winzermessern.", "Speere", 3,
              "V. 3: Schwerter werden zu Pflugmessern, Speere zu Winzermessern, und niemand lernt mehr den Krieg."),
        tf("In V. 5 heißt es, dass die Völker vorerst noch im Namen ihrer eigenen Götter leben.", True, 5, "Lies Vers 5.",
           "V. 5: Alle Völker wandeln im Namen ihres Gottes; „wir“ aber im Namen des HERRN."),
    ],
    explain=[
        E("Warum steht das fast genauso bei Jesaja?", "Jes 2,2–4 ist beinahe wortgleich; Micha und Jesaja wirkten zur selben Zeit in Juda. Ob einer vom anderen übernommen hat oder beide ein älteres Wort aufgreifen, weiß man nicht. Nur Micha hat V. 4 mit Weinstock und Feigenbaum."),
        E("Wie verstehen Christen diese Zukunft?", "Dispensationalisten und andere Prämillenialisten lesen V. 1–4 wörtlich: Nach seiner Wiederkunft regiert Jesus tausend Jahre von Jerusalem aus, und die Völker kommen dorthin (vgl. Offb 20). Amillenialisten – die Mehrheit in katholischer, orthodoxer, lutherischer und reformierter Tradition – sehen die Erfüllung schon begonnen: Seit Pfingsten geht das Wort von Jerusalem zu den Völkern (Lk 24,47; Apg 1,8), und die Gemeinde ist zum Berg Zion gekommen (Hebr 12,22); vollendet wird der Frieden in der neuen Schöpfung (Offb 21,1–4). Postmillenialisten erwarten, dass sich dieser Frieden durch das Evangelium immer weiter ausbreitet, bevor Jesus wiederkommt."),
        E("Wie lasen Juden und die frühe Kirche den Text?", "In der jüdischen Tradition beschreibt er die Zeit des Messias; dass noch Kriege geführt werden, gilt als Zeichen, dass sie noch aussteht. Justin der Märtyrer schrieb im 2. Jahrhundert, die Stelle (in der Fassung von Jes 2) erfülle sich schon, wenn frühere Krieger Christen werden und nicht mehr kämpfen (1. Apologie 39)."),
        E("Warum Weinstock und Feigenbaum?", "Ein Bild für Frieden und eigenen Besitz, das schon für die Zeit Salomos gebraucht wird (1Kön 5,5; vgl. Sach 3,10). Vergleiche damit 2,2, wo man den Leuten Äcker und Häuser nimmt."),
    ],
    cards=["ende-der-tage"],
    fact="Eine Bronzefigur eines Mannes, der ein Schwert zur Pflugschar umschmiedet, steht seit 1959 vor dem UN-Hauptquartier in New York – ein Geschenk der Sowjetunion. Ein Bild dieser Figur mit den Worten „Schwerter zu Pflugscharen“ wurde in den 1980er-Jahren zum Zeichen der kirchlichen Friedensbewegung in der DDR, das der Staat verbot.",
    try_="Lies Joel 4,10. Was ist dort andersherum als in V. 3?",
    teaser="Ein Turm aus der Geschichte Jakobs taucht auf – und eine Stadt, die zu Michas Zeit für Juda noch kaum eine Rolle spielte.")

sec("haeupter", [R(MI, 4, 6, 14)], "Tochter Zion in Wehen",
    "Gott will das Hinkende und Vertriebene sammeln und selbst König auf dem Zion sein; die frühere Herrschaft kehrt zum Herdenturm zurück. Jetzt aber liegt die Tochter Zion in Wehen: Sie muss hinaus bis nach Babel und wird dort erlöst. Viele Völker ziehen gegen sie, doch Gott hat sie gesammelt wie Garben auf der Tenne.",
    place="jerusalem",
    quiz=[
        choice("Wohin muss die Tochter Zion nach V. 10 ziehen?", ["Bis nach Babel", "Bis nach Ägypten", "Bis nach Ninive", "Bis nach Damaskus"], 10, "Lies Vers 10.",
               "V. 10: Sie muss aus der Stadt hinaus, auf dem Feld wohnen und bis nach Babel kommen."),
        tf("Nach V. 10 wird sie gerade dort, in der Fremde, errettet.", True, 10, "Lies Vers 10.",
           "V. 10: Dort wirst du errettet werden, dort wird der HERR dich erlösen."),
        choice("Was wissen die Nationen nach V. 12 nicht?", ["Die Gedanken und den Ratschluss des HERRN", "Den Weg nach Jerusalem", "Die Zahl der Verteidiger", "Den Namen des Königs"], 12, "Lies Vers 12.",
               "V. 12: Sie kennen Gottes Gedanken nicht – er hat sie gesammelt wie Garben zum Dreschen."),
    ],
    explain=[
        E("Was ist der Herdenturm?", "Hebräisch Migdal Eder. In 1Mo 35,21 schlägt Jakob dort sein Zelt auf, kurz nachdem Rahel bei Bethlehem gestorben ist. Hier ist es ein Name für Zion. Eine jüdische Überlieferung (Targum zu 1Mo 35,21) verbindet den Ort mit dem Kommen des Messias."),
        E("Warum Babel?", "Zu Michas Zeit war Assyrien die Großmacht; Babel stand meist unter ihr. Auch Jesaja kündigte Hiskia an, dass Nachkommen nach Babel weggeführt würden (2Kön 20,16–18). Das Exil begann über hundert Jahre später, 597 und 587 v. Chr."),
        E("Was bedeutet V. 13?", "Ein Bild vom Dreschen: Rinder trampelten das Getreide auf der Tenne aus. „Verbannen“ heißt, die Beute Gott zu weihen, statt sie selbst zu behalten.", "elbbk"),
        E("Warum ist die Zählung hier anders?", "In englischen Bibeln ist 4,14 schon 5,1, deshalb ist dort Bethlehem 5,2. Christliche Ausleger haben bei dem geschlagenen Richter oft an Mt 27,30 gedacht."),
    ],
    teaser="Der nächste Abschnitt beginnt mit dem kleinsten Ort, den Micha nennt – und Jahrhunderte später schlagen Gelehrte in Jerusalem genau diesen Vers auf.")

sec("haeupter", [R(MI, 5, 1, 5)], "Du, Bethlehem",
    "Aus dem kleinen Bethlehem-Ephrata soll ein Herrscher über Israel kommen, dessen Ursprünge in uralter Zeit liegen. Bis eine Gebärende geboren hat, gibt Gott sein Volk preis; dann weidet dieser Herrscher seine Herde in Gottes Kraft. Er wird Friede sein, auch wenn Assyrien kommt.",
    place="bethlehem",
    quiz=[
        choice("Wie beschreibt Micha Bethlehem-Ephrata?", ["Zu klein, um unter den Tausenden von Juda zu zählen", "Als größte Stadt Judas", "Als Stadt der Priester", "Als Festung gegen Assyrien"], 1, "Lies Vers 1.",
               "V. 1: Bethlehem ist zu klein, um unter den Tausenden (den Sippen) Judas zu sein – und doch kommt von dort der Herrscher."),
        tf("Nach V. 1 liegen die Ursprünge des Herrschers in uralter Zeit.", True, 1, "Lies Vers 1.",
           "V. 1: Seine Ausgänge sind von der Urzeit, von den Tagen der Ewigkeit her."),
        choice("Was wird über diesen Herrscher in V. 4 gesagt?", ["Er wird Friede sein", "Er wird ein Priester sein", "Er wird den Tempel neu bauen", "Er wird Babel zerstören"], 4, "Lies Vers 4.",
               "V. 4: Und dieser wird Friede sein."),
    ],
    explain=[
        E("Was ist Ephrata?", "Ein alter Name für Bethlehem oder seine Sippe (1Mo 35,19; Rut 4,11). Davids Vater Isai war ein Ephratiter aus Bethlehem (1Sam 17,12). Der Zusatz unterscheidet die Stadt auch von einem Bethlehem in Galiläa (Jos 19,15)."),
        E("Wie lesen Juden und Christen den Vers?", "Nach Mt 2,4–6 nennen die Schriftgelehrten in Jerusalem diesen Vers als Geburtsort des Messias, vgl. Joh 7,42. Auch die aramäische Übersetzung (Targum) spricht hier ausdrücklich vom Messias. Christen sehen in den „Ausgängen von der Urzeit“ oft den ewigen Sohn (Joh 1,1); jüdische Ausleger meist das alte Königshaus Davids."),
        E("Wer ist die Gebärende in V. 2?", "Viele Christen denken an Maria, auch mit Blick auf Michas Zeitgenossen Jesaja (Jes 7,14). Andere Ausleger denken an Zion, die in 4,9–10 wie eine Gebärende in Wehen liegt."),
        E("„Sieben Hirten und acht“?", "Ein Zahlenspruch wie in Spr 30,18 oder Am 1,3: eine Zahl und noch eine darüber, gemeint ist „genug und mehr als genug“. Das „Land Nimrods“ ist Assyrien (1Mo 10,8–11)."),
    ],
    cards=["bethlehem"],
    fact="Matthäus zitiert den Vers etwas anders: Bei ihm ist Bethlehem „keineswegs die geringste“ unter den Fürsten Judas (Mt 2,6).",
    try_="Lies Mt 2,3–6 und vergleiche es mit V. 1. Was ist gleich, was anders?",
    teaser="Der Überrest Israels bekommt zwei Bilder, die kaum unterschiedlicher sein könnten.")

sec("haeupter", [R(MI, 5, 6, 14)], "Tau und Löwe",
    "Der Überrest Jakobs wird unter den Völkern wie Tau sein und wie ein Löwe. An jenem Tag will Gott aus der Mitte seines Volkes Pferde, Wagen, Festungen, Zauberei und Götzenbilder entfernen. An den Völkern, die nicht gehört haben, übt er Vergeltung.",
    focus="Achte in V. 9–13 darauf, wem Gott hier etwas wegnimmt.",
    quiz=[
        choice("Womit vergleicht Micha den Überrest in V. 6?", ["Mit Tau und Regenschauern vom HERRN", "Mit einem Baum am Wasser", "Mit den Sternen am Himmel", "Mit dem Sand am Meer"], 6, "Lies Vers 6.",
               "V. 6: Wie Tau vom HERRN, wie Regen auf das Kraut, der nicht auf Menschen wartet."),
        tf("Was Gott in V. 9–13 ausrotten will, gehört den feindlichen Völkern.", False, 9, "Lies Vers 9–13.",
           "V. 9–13: Immer wieder „aus deiner Mitte“ – es geht um Pferde, Festungen, Zauberei und Bilder in Israel selbst."),
        order("In welcher Reihenfolge nennt Gott, was er wegnehmen will?", ["Pferde und Wagen", "Städte und Festungen", "Wahrsagerei und Zauberer", "Bilder und Bildsäulen"],
              "V. 9–12: zuerst das Militär, dann die Festungen, dann Zauberei, zuletzt die Götzenbilder (V. 13 nennt noch die Ascherim).", "Lies Vers 9–12."),
    ],
    explain=[
        E("Tau und Löwe – wie passt das?", "Tau kommt von Gott und hängt von keinem Menschen ab (V. 6); der Löwe ist übermächtig (V. 7). Ausleger lesen die beiden Bilder als Segen und als Gericht für die Völker. Der Text stellt sie ohne Erklärung nebeneinander."),
        E("Warum Pferde und Wagen?", "Sie waren die stärkste Waffe der Zeit. Schon das Gesetz verbot dem König, viele Pferde anzuschaffen (5Mo 17,16); vgl. Ps 20,8 und Jes 31,1."),
        E("Was sind Bildsäulen und Ascherim?", "Bildsäulen (Mazzeben) waren aufgerichtete Kultsteine. Ascherim waren hölzerne Pfähle oder heilige Bäume für die Göttin Aschera (5Mo 16,21–22).", "elbbk"),
    ],
    teaser="Gott verklagt sein Volk – und ruft keine Menschen als Zeugen auf.")

# ───────────────────────── 3 · Hört, was der HERR sagt (Kap. 6–7) ─────────────────────────
sec("rechtsstreit", [R(MI, 6, 1, 8)], "Was fordert der HERR?",
    "Gott führt einen Rechtsstreit mit seinem Volk, die Berge sind Zeugen. Er fragt, womit er es ermüdet hat, und erinnert an den Auszug aus Ägypten, an Mose, Aaron und Mirjam, an Balak und Bileam. Jemand fragt, mit welchem Opfer er vor Gott treten soll. Die Antwort: Recht üben, Güte lieben und demütig mit Gott gehen.",
    quiz=[
        choice("Wen ruft Gott in V. 1–2 als Zeugen?", ["Die Berge und die Grundfesten der Erde", "Die Ältesten Israels", "Die Priester im Tempel", "Die Völker ringsum"], 2, "Lies Vers 1–2.",
               "V. 2: Hört, ihr Berge, den Rechtsstreit des HERRN, und ihr Grundfesten der Erde."),
        order("Welche Opfer erwägt der Fragende? Bring sie in die Reihenfolge, in der er sie nennt.", ["Brandopfer und einjährige Kälber", "Tausende Widder und Ströme von Öl", "Der eigene Erstgeborene"],
              "V. 6–7: Die Angebote steigern sich bis zum eigenen Kind.", "Lies Vers 6–7."),
        error("Gott verlangt nach V. 8: Recht üben, [Opfer] lieben und demütig mit Gott gehen.", "Güte", 8,
              "V. 8: Recht üben, Güte lieben und demütig wandeln mit deinem Gott."),
    ],
    explain=[
        E("Was ist ein Rechtsstreit?", "Hebräisch riv: ein Gerichtsverfahren. Die Propheten benutzen diese Form öfter, mit Himmel, Erde oder Bergen als Zeugen (5Mo 32,1; Jes 1,2). Hier fragt der Kläger aber zuerst, was er dem Angeklagten getan hat (V. 3)."),
        E("Warum Balak, Bileam, Sittim und Gilgal?", "Balak, König von Moab, ließ Bileam holen, um Israel zu verfluchen, doch Bileam segnete (4Mo 22–24). Sittim war das letzte Lager östlich des Jordan (Jos 3,1), Gilgal das erste im Land (Jos 4,19) – dazwischen liegt der Weg durch den Jordan."),
        E("Was meinen „Güte“ und „demütig“?", "„Güte“ ist chesed: treue Liebe, die zu einer Beziehung steht. „Demütig wandeln“ ist eine seltene Wendung; sie kann auch „behutsam“ oder „aufmerksam gehen“ heißen. „O Mensch“ ist im Hebräischen adam – das Wort für den Menschen überhaupt."),
        E("Lehnt Micha Opfer ab?", "Ausleger lesen das verschieden. Viele, jüdisch wie christlich, verstehen: Opfer ohne Recht und Güte sind wertlos, nicht das Opfer an sich (vgl. 1Sam 15,22; Ps 51,18–21; Hos 6,6, von Jesus in Mt 9,13 zitiert). Das Opfer des Erstgeborenen in V. 7 war kein bloßes Gedankenspiel: König Ahas ließ seinen Sohn „durchs Feuer gehen“ (2Kön 16,3)."),
    ],
    cards=["rechtsstreit", "chesed"],
    fact="Der Talmud erzählt, dass Mose 613 Gebote erhielt. David fasste sie in elf zusammen (Ps 15), Jesaja in sechs, Micha in den drei aus V. 8 (Makkot 23b–24a).",
    memory_verse=MV(R(MI, 6, 8), "Recht zu üben und Güte zu lieben und demütig zu wandeln mit deinem Gott"),
    teaser="Im nächsten Abschnitt geht es um Waagen und Gewichtssteine – und um zwei Könige, die in Juda niemand zum Vorbild haben sollte.")

sec("rechtsstreit", [R(MI, 6, 9, 16)], "Falsche Gewichte",
    "Gottes Stimme ruft der Stadt zu. Im Haus des Gottlosen gibt es zu kleine Maße und falsche Gewichte, die Reichen sind gewalttätig, alle lügen. Deshalb wird man essen und nicht satt werden, säen und nicht ernten. Juda folgt den Satzungen Omris und Ahabs.",
    place="jerusalem",
    quiz=[
        choice("Womit wird nach V. 10–11 betrogen?", ["Mit einem zu kleinen Epha und falschen Gewichtssteinen", "Mit verdorbenem Getreide", "Mit gefälschten Münzen", "Mit gestohlenen Schafen"], 11, "Lies Vers 10–11.",
               "V. 10–11: das knappe Epha, die Waage der Gottlosigkeit und der Beutel mit betrügerischen Gewichtssteinen."),
        tf("Nach V. 15 werden sie säen, aber nicht ernten.", True, 15, "Lies Vers 15.",
           "V. 15: säen ohne Ernte, Oliven keltern ohne Öl, Most ohne Wein."),
        choice("Wessen Satzungen befolgt man nach V. 16?", ["Die Satzungen Omris und des Hauses Ahabs", "Die Gebote Moses", "Die Gesetze Assyriens", "Die Weisungen der Priester"], 16, "Lies Vers 16.",
               "V. 16: Man hält die Satzungen Omris und tut wie das Haus Ahabs."),
    ],
    explain=[
        E("Was ist ein Epha?", "Ein Hohlmaß für Getreide, etwa 20 bis 40 Liter (die Angaben schwanken). Wer mit kleinem Maß verkauft und schweren Gewichten das Silber abwiegt, betrügt doppelt. Das Gesetz verbot zweierlei Maß (5Mo 25,13–15; vgl. Am 8,5)."),
        E("Wer waren Omri und Ahab?", "Könige des Nordreichs im 9. Jahrhundert v. Chr. Omri baute Samaria (1Kön 16,24); Ahab und Isebel förderten den Baalskult und ließen Nabot wegen seines Weinbergs töten (1Kön 21). Dass Juda ihnen folgt, ist ein scharfer Vorwurf."),
        E("Was heißt V. 9?", "Der hebräische Text ist schwer zu verstehen; die Übersetzungen gehen weit auseinander, etwa „es ist weise, deinen Namen zu fürchten“. Die „Zuchtrute“ ist die Strafe, die Gott ankündigt.", "elbbk"),
    ],
    try_="Lies 5Mo 28,38–40 und vergleiche es mit V. 14–15.",
    teaser="Micha vergleicht sich mit jemandem, der nach der Ernte durch den Weinberg geht.")

sec("rechtsstreit", [R(MI, 7, 1, 7)], "Ich aber will ausschauen",
    "Micha klagt: Wie nach der Weinlese keine Traube mehr hängt, findet er keinen Rechtschaffenen mehr. Fürsten und Richter sind käuflich, niemandem ist zu trauen, nicht einmal in der Familie. Doch er will nach Gott ausschauen und auf ihn warten.",
    focus="Achte auf den Anfang von V. 7. Erinnert er dich an eine Stelle in Kapitel 3?",
    quiz=[
        choice("Womit vergleicht Micha seine Lage in V. 1?", ["Mit der Nachlese nach der Weinernte, wenn keine Traube mehr übrig ist", "Mit einem Feld voller Unkraut", "Mit einem ausgetrockneten Brunnen", "Mit einer Stadt ohne Mauer"], 1, "Lies Vers 1.",
               "V. 1: wie bei der Nachlese der Weinernte – keine Traube, keine Frühfeige."),
        tf("Nach V. 6 ist selbst in der eigenen Familie kein Verlass mehr.", True, 6, "Lies Vers 6.",
           "V. 6: Sohn gegen Vater, Tochter gegen Mutter; die Feinde sind die eigenen Hausgenossen."),
        choice("Was tut der Richter nach V. 3?", ["Er richtet gegen Bezahlung", "Er verurteilt den Fürsten", "Er flieht aus der Stadt", "Er schweigt zu allem"], 3, "Lies Vers 3.",
               "V. 3: Der Fürst fordert, und der Richter richtet gegen Entgelt."),
    ],
    explain=[
        E("Was ist die Nachlese?", "Nach der Ernte durften Arme die übrig gebliebenen Trauben und Ähren sammeln (3Mo 19,10; Rut 2). Micha findet nicht einmal mehr das."),
        E("Wer sind die „Wächter“ in V. 4?", "Wohl die Propheten, die wie Wächter auf der Mauer vor Gefahr warnen (Hes 3,17). Der Tag, vor dem sie gewarnt haben, ist gekommen."),
        E("Wo kommt V. 6 im Neuen Testament vor?", "Jesus greift den Vers auf, als er seine Jünger aussendet und ihnen sagt, dass sein Weg auch Familien spalten kann (Mt 10,35–36; Lk 12,53)."),
    ],
    prayer={"ref": R(MI, 7, 7), "source": "Micha 7,7"},
    teaser="Jetzt spricht eine Stadt – und zwar zu ihrer Feindin.")

sec("rechtsstreit", [R(MI, 7, 8, 13)], "Bin ich gefallen, so stehe ich auf",
    "Zion spricht zu ihrer Feindin: Wenn ich falle, stehe ich wieder auf, der HERR ist mein Licht. Sie trägt Gottes Zorn, weil sie gesündigt hat, bis er ihr Recht verschafft. Die Feindin, die gespottet hat, wird beschämt. Ein Tag kommt, an dem Mauern gebaut werden und Menschen von weit her kommen.",
    place="jerusalem",
    quiz=[
        choice("Was sagt Zion in V. 8 über die Zeit in der Finsternis?", ["Der HERR ist mein Licht", "Ich werde nicht mehr aufstehen", "Meine Feindin hat gesiegt", "Ich will nach Ägypten fliehen"], 8, "Lies Vers 8.",
               "V. 8: Bin ich gefallen, stehe ich wieder auf; sitze ich in Finsternis, ist der HERR mein Licht."),
        tf("Zion sagt in V. 9, sie habe gegen den HERRN gesündigt.", True, 9, "Lies Vers 9.",
           "V. 9: Sie will Gottes Grimm tragen, denn sie hat gegen ihn gesündigt."),
        choice("Was hatte die Feindin nach V. 10 gefragt?", ["Wo ist der HERR, dein Gott?", "Warum betest du nicht?", "Wer ist dein König?", "Wann kommt dein Retter?"], 10, "Lies Vers 10.",
               "V. 10: Die Feindin hatte gespottet: Wo ist der HERR, dein Gott?"),
    ],
    explain=[
        E("Wer ist die Feindin?", "Der Text nennt sie nicht. Die weibliche Form deutet auf eine Stadt oder ein Volk; Ausleger denken an Ninive, Babel oder Edom (vgl. Obd 12)."),
        E("Wie passt V. 9 zum Rechtsstreit?", "In 6,1–2 führte Gott einen Rechtsstreit gegen sein Volk. In V. 9 steht dasselbe Wort: Jetzt erwartet Zion, dass Gott ihren Rechtsstreit führt – für sie."),
        E("Was ist die „Schranke“ in V. 11?", "Das hebräische Wort kann „Grenze“ oder „Verordnung“ heißen. Manche Übersetzungen lesen, dass die Grenze weit wird, andere, dass eine Frist fern ist.", "elbbk"),
    ],
    teaser="Das Buch endet mit einer Frage, die schon im Namen des Propheten steckt.")

sec("rechtsstreit", [R(MI, 7, 14, 20)], "Wer ist ein Gott wie du?",
    "Ein Gebet bittet Gott, sein Volk zu weiden wie in alter Zeit. Gott verspricht Wunder wie beim Auszug aus Ägypten; die Völker kommen zitternd zu ihm. Am Schluss: Wer ist ein Gott wie du, der Schuld vergibt? Er wirft die Sünden in die Tiefe des Meeres und hält Abraham und Jakob die Treue.",
    quiz=[
        choice("An welche Zeit erinnert Gott in V. 15?", ["An den Auszug aus Ägypten", "An die Zeit Davids", "An die Sintflut", "An den Bau des Tempels"], 15, "Lies Vers 15.",
               "V. 15: Wie in den Tagen, als du aus Ägypten zogst, will ich Wunder sehen lassen."),
        tf("Nach V. 18 behält Gott seinen Zorn für immer.", False, 18, "Lies Vers 18.",
           "V. 18: Er behält seinen Zorn nicht auf immer, denn er hat Gefallen an Güte."),
        choice("Wohin wirft Gott nach V. 19 die Sünden?", ["In die Tiefen des Meeres", "Hinter seinen Rücken", "In die Wüste", "Ins Feuer"], 19, "Lies Vers 19.",
               "V. 19: Du wirst alle ihre Sünden in die Tiefen des Meeres werfen. (Hinter den Rücken wirft Gott sie in Jes 38,17.)"),
    ],
    explain=[
        E("Wer spricht hier?", "V. 14 ist ein Gebet an Gott (in der Elberfelder in Anführungszeichen). In V. 15 antwortet Gott, ab V. 16 sprechen wieder der Prophet und das Volk."),
        E("Was sind Basan und Gilead?", "Fruchtbares Weideland östlich des Jordan. Zu Michas Zeit hatten die Assyrer es dem Nordreich weggenommen (2Kön 15,29)."),
        E("Wie wird der Text im Judentum gelesen?", "V. 18–20 werden in vielen Synagogen am Versöhnungstag (Jom Kippur) im Anschluss an das Buch Jona gelesen. Zum Neujahrsfest gehen viele Juden an ein Gewässer und sprechen beim Taschlich-Brauch („du wirst werfen“, aus V. 19) diese Verse."),
    ],
    fact="Die Frage aus V. 18 steckt im Namen des Propheten: Micha ist die Kurzform von Michajahu, „Wer ist wie Jahwe?“.",
    memory_verse=MV(R(MI, 7, 18), "Wer ist ein Gott wie du, der die Ungerechtigkeit vergibt"),
    try_="Lies 2Mo 15,11 und dann V. 18. Welche Frage stellen beide?")

P.write()
