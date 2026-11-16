#!/usr/bin/env python3
"""Source for the reading plan „Markus“ (generates assets/plans/markus.json).

python3 -I tools/plans/markus.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/markus.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

MK = 41

def M(c, f, t=None): return R(MK, c, f, t)

P = PlanBuilder(
    "markus", "mk", "Markus", "Jesus kennenlernen",
    "Das kürzeste und schnellste Evangelium: Jesus heilt, streitet, erzählt, geht nach Jerusalem, stirbt – und das Grab ist leer. "
    "In 80 kurzen Abschnitten durch das ganze Markus-Evangelium, mit der Frage, die es von Anfang an stellt: Wer ist dieser?",
    "jesus",
    stages=[("anfang", "Der Anfang"), ("streit", "Streit um Jesus"), ("gleichnisse", "Gleichnisse und Machttaten"),
            ("brot", "Brot für viele"), ("wer", "Wer bin ich?"), ("weg", "Auf dem Weg nach Jerusalem"),
            ("jerusalem", "In Jerusalem"), ("nacht", "Die letzte Nacht"), ("kreuz", "Kreuz und Auferstehung")],
    cards=[
        ("johannes-taeufer", "person", "Johannes der Täufer", "Prophet in der Wüste am Jordan, in Kamelhaar gekleidet. Er ruft zur Umkehr und tauft. Markus sieht in ihm den Wegbereiter, den Jesaja und Maleachi angekündigt hatten. König Herodes Antipas lässt ihn hinrichten.", "Mk 1,1–8; 6,14–29"),
        ("synagoge", "begriff", "Synagoge", "Griechisch „Versammlung“: das jüdische Gemeindehaus zum Beten, Lesen und Auslegen der Schrift am Sabbat. Jeder erwachsene Mann konnte dort aus der Schrift vorlesen und sprechen – so auch Jesus.", "Mk 1,21; 6,2"),
        ("schriftgelehrte", "begriff", "Schriftgelehrte", "Ausgebildete Ausleger des jüdischen Gesetzes, oft als Lehrer und Richter tätig. Viele gehörten zu den Pharisäern. Sie hatten großes Ansehen; Jesus lehrt anders als sie – „mit Vollmacht“.", "Mk 1,22; 12,38–40"),
        ("pharisaeer", "begriff", "Pharisäer", "Eine fromme Laienbewegung, die das Gesetz Gottes im Alltag genau halten wollte, auch mit vielen überlieferten Regeln. Sie glaubten an die Auferstehung. Jesus stand ihnen in vielem nahe – und stritt gerade deshalb heftig mit ihnen.", "Mk 2,16; 7,1–13"),
        ("sabbat", "begriff", "Sabbat", "Der siebte Tag der Woche (Freitagabend bis Samstagabend), an dem nach den Zehn Geboten nicht gearbeitet wird. Was genau als Arbeit galt, war umstritten. Jesus: Der Sabbat ist für den Menschen da (Mk 2,27).", "2Mo 20,8–11; Mk 2,27"),
        ("die-zwoelf", "begriff", "Die Zwölf", "Der engste Jüngerkreis: Simon Petrus, Jakobus, Johannes, Andreas, Philippus, Bartholomäus, Matthäus, Thomas, Jakobus (Sohn des Alphäus), Thaddäus, Simon Kananäus, Judas Iskariot. Zwölf wie die zwölf Stämme Israels – ein Zeichen für das erneuerte Gottesvolk.", "Mk 3,13–19"),
        ("gleichnis", "begriff", "Gleichnis", "Eine Bildgeschichte aus dem Alltag – Saat, Lampe, Weinberg –, die etwas über Gott und sein Reich zeigt. Gleichnisse erklären nicht alles, sie laden ein, selbst weiterzudenken – und fordern heraus.", "Mk 4,1–34"),
        ("dekapolis", "ort", "Dekapolis", "„Zehn Städte“: ein Bund griechisch geprägter Städte östlich des Sees Genezareth und des Jordan. Hier lebten vor allem Nichtjuden – deshalb gab es dort auch Schweineherden.", "Mk 5,20; 7,31"),
        ("herodes-antipas", "person", "Herodes Antipas", "Sohn Herodes des Großen, von 4 v. Chr. bis 39 n. Chr. Landesfürst von Galiläa – Markus nennt ihn „König“. Er heiratete Herodias, die Frau seines Halbbruders, und ließ Johannes den Täufer enthaupten.", "Mk 6,14–29"),
        ("menschensohn", "begriff", "Menschensohn", "Jesus’ liebste Selbstbezeichnung. Sie kann schlicht „Mensch“ bedeuten, erinnert aber an Daniel 7,13, wo einer „wie ein Menschensohn“ mit den Wolken des Himmels kommt und ewige Herrschaft erhält. Bei Markus verbindet Jesus damit Leiden, Tod und Auferstehung.", "Mk 8,31; 14,62; Dan 7,13"),
        ("rein-unrein", "begriff", "Rein und unrein", "Begriffe aus den Gesetzen des Alten Testaments: Wer „unrein“ war – etwa durch Krankheit, Blut oder Kontakt mit Toten –, durfte eine Zeit lang nicht am Gottesdienst teilnehmen. Gemeint ist kein moralisches Urteil, sondern kultische Ordnung.", "3Mo 11–15; Mk 7,1–23"),
        ("tempel", "ort", "Der Tempel", "Das Zentrum des jüdischen Glaubens in Jerusalem, von Herodes dem Großen prachtvoll ausgebaut. Hier wurden Opfer dargebracht; Pilger kamen zu den großen Festen. 70 n. Chr. zerstörten ihn die Römer – nur Mauerreste wie die Westmauer blieben.", "Mk 11,15–17; 13,1–2"),
        ("sadduzaeer", "begriff", "Sadduzäer", "Eine Gruppe aus der priesterlichen Oberschicht in Jerusalem. Sie erkannten vor allem die fünf Bücher Mose an und glaubten nicht an eine Auferstehung der Toten.", "Mk 12,18"),
        ("hoher-rat", "begriff", "Hoher Rat (Synedrium)", "Das oberste jüdische Gremium in Jerusalem mit 71 Mitgliedern unter Vorsitz des Hohenpriesters: Priester, Älteste und Schriftgelehrte. Unter römischer Herrschaft durfte es wohl keine Todesurteile vollstrecken.", "Mk 14,53–64; 15,1"),
        ("pilatus", "person", "Pontius Pilatus", "Römischer Statthalter von Judäa (26–36 n. Chr.), bekannt für sein hartes Vorgehen. 1961 wurde in Caesarea ein Stein mit seinem Namen gefunden. Er verurteilte Jesus zum Tod am Kreuz.", "Mk 15,1–15"),
        ("maria-magdalena", "person", "Maria Magdalena", "Aus Magdala am See Genezareth. Sie folgte Jesus schon in Galiläa, stand beim Kreuz, sah das Begräbnis und war unter den ersten Zeuginnen des leeren Grabes. Die alte Kirche nannte sie „Apostelin der Apostel“.", "Mk 15,40.47; 16,1–9"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Der Anfang ─────────────────────────
sec("anfang", [M(1, 1, 8)], "Johannes der Täufer",
    "Markus beginnt ohne Geburtsgeschichte: Johannes tauft in der Wüste, ruft zur Umkehr und kündigt einen an, der stärker ist als er.",
    bridge="Markus ist das kürzeste und wahrscheinlich älteste Evangelium, geschrieben um 70 n. Chr. Es ist kurz, schnell und voller Bewegung – das Wort „sogleich“ kommt über 40-mal vor.",
    place="jordan",
    focus="Achte darauf, wie Markus Jesus gleich im ersten Satz nennt.",
    quiz=[
        choice("Was aß Johannes?", ["Heuschrecken und wilden Honig", "Brot und Fisch", "Nur Wasser und Kräuter", "Was die Leute ihm brachten"], 6, "Vers 6.",
               "V. 6: Heuschrecken und wilder Honig – und Kleidung aus Kamelhaar. Er lebt wie der Prophet Elia (vgl. 2. Kön 1,8)."),
        choice("Was sagt Johannes über den, der nach ihm kommt?", ["Er ist stärker und wird mit Heiligem Geist taufen", "Er wird ein großer König in Rom", "Er wird ihn, Johannes, taufen", "Er kommt erst in hundert Jahren"], 8, "Lies Vers 7–8.",
               "V. 7–8: Johannes hält sich nicht einmal für würdig, ihm die Sandalen aufzubinden – eine Arbeit für Sklaven."),
    ],
    explain=[
        E("Was heißt „Evangelium“?", "Griechisch „gute Nachricht“. Im Römischen Reich nannte man so z. B. die Nachricht von der Geburt oder dem Sieg eines Kaisers. Markus beansprucht das Wort für Jesus (V. 1)."),
        E("Warum in der Wüste?", "In der Wüste hatte Gott Israel nach der Befreiung aus Ägypten geführt. Die Propheten kündigten an, dass dort wieder ein Neuanfang beginnt (Jes 40,3, zitiert in V. 3)."),
        E("Was bedeutet „Buße“?", "Umkehr, eine neue Richtung im Leben. Die Taufe im Jordan war ein sichtbares Zeichen dafür: Man ließ das Alte hinter sich."),
    ],
    cards=["johannes-taeufer"],
    teaser="Jesus kommt aus einem unbedeutenden Dorf – und der Himmel reißt auf.")

sec("anfang", [M(1, 9, 13)], "Taufe und Versuchung",
    "Jesus aus Nazareth lässt sich von Johannes taufen. Der Himmel öffnet sich, der Geist kommt wie eine Taube, und eine Stimme sagt: Du bist mein geliebter Sohn. Dann treibt ihn der Geist in die Wüste.",
    place="jordan",
    quiz=[
        choice("Was sagt die Stimme aus dem Himmel?", ["Du bist mein geliebter Sohn", "Folgt ihm nach", "Dies ist der König der Juden", "Kehrt um"], 11, "Vers 11.",
               "V. 11: Bevor Jesus irgendetwas getan hat, hört er, dass er geliebt ist."),
        estimate("Wie viele Tage ist Jesus in der Wüste?", 1, 100, 40, "Tage", "V. 13: 40 Tage – wie Israels 40 Jahre in der Wüste und Moses 40 Tage am Sinai.", 13, "Vers 13.", tol=2),
    ],
    explain=[
        E("Warum lässt Jesus sich taufen?", "Johannes taufte zur Vergebung der Sünden. Christen glauben, dass Jesus ohne Sünde war. Schon die frühe Kirche verstand seine Taufe so: Er stellt sich ganz an die Seite der Menschen, die Umkehr brauchen."),
        E("Wilde Tiere und Engel?", "Markus erzählt die Versuchung in zwei Versen. Die Tiere erinnern an die Gefahr der Wüste, die Engel an Gottes Fürsorge – vielleicht auch an den Frieden des Paradieses (vgl. Jes 11,6–9)."),
    ],
    fact="Bei der Taufe kommen Vater (Stimme), Sohn und Geist (Taube) zusammen vor. Die Alte Kirche hat diese Stelle oft als frühen Hinweis auf die Dreieinigkeit gelesen.",
    teaser="Vier Fischer lassen alles stehen – für einen Satz, den Jesus zu ihnen sagt.")

sec("anfang", [M(1, 14, 20)], "Die ersten Jünger",
    "Jesus verkündet in Galiläa: Die Zeit ist erfüllt, das Reich Gottes ist nahe. Am See ruft er Simon, Andreas, Jakobus und Johannes – und sie folgen ihm sofort.",
    place="see-genezareth",
    quiz=[
        choice("Was tun Simon und Andreas gerade, als Jesus sie ruft?", ["Sie werfen ein Netz aus", "Sie flicken ihre Netze", "Sie verkaufen Fische", "Sie schlafen im Boot"], 16, "Vers 16.",
               "V. 16: Sie werfen ein Netz aus. Jakobus und Johannes dagegen flicken gerade ihre Netze (V. 19)."),
        tf("Die Jünger überlegen lange, bevor sie Jesus folgen.", False, 18, "Lies Vers 18 und 20.",
           "V. 18 und 20: „sogleich“ – sie lassen Netze, Boot und sogar den Vater zurück."),
    ],
    explain=[
        E("Warum folgen sie so schnell?", "Markus erzählt knapp. Johannes 1,35–42 deutet an, dass manche Jesus schon vorher kannten. Markus geht es um den Ruf selbst: Wenn Jesus ruft, entsteht etwas Neues."),
        E("Was heißt „Menschenfischer“?", "Ein Wortspiel mit ihrem Beruf. Bei den Propheten ist „fischen“ manchmal ein Bild für Gericht (Jer 16,16); bei Jesus wird es ein Bild dafür, Menschen für Gottes Reich zu gewinnen."),
    ],
    teaser="In der Synagoge schreit ein Mann auf – und weiß genau, wer Jesus ist.")

sec("anfang", [M(1, 21, 28)], "Vollmacht in Kapernaum",
    "Am Sabbat lehrt Jesus in der Synagoge von Kapernaum – mit Vollmacht, nicht wie die Schriftgelehrten. Ein Mensch mit einem unreinen Geist schreit auf; Jesus befiehlt dem Geist auszufahren.",
    place="kapernaum",
    quiz=[
        choice("Worüber staunen die Leute in der Synagoge zuerst?", ["Dass er lehrt wie einer, der Vollmacht hat", "Dass er so laut spricht", "Dass er aus Nazareth kommt", "Dass er Griechisch spricht"], 22, "Vers 22.",
               "V. 22: Er zitiert nicht nur Autoritäten wie die Schriftgelehrten – er spricht mit eigener Autorität."),
        who("Ich kenne dich, wer du bist: der Heilige Gottes", M(1, 24), ["Der Mann mit dem unreinen Geist", "Simon", "Ein Schriftgelehrter", "Die Menge"],
            "V. 24: Ausgerechnet der unreine Geist erkennt Jesus. Jesus lässt ihn schweigen."),
    ],
    explain=[
        E("Was ist ein „unreiner Geist“?", "So nennt das Neue Testament dämonische Mächte, die Menschen beherrschen. Manche Ausleger sehen darin auch Krankheiten, die man damals nicht anders erklären konnte; andere betonen die Wirklichkeit geistlicher Mächte. Der Text zeigt vor allem: Jesus ist stärker als alles, was Menschen gefangen hält."),
        E("Warum soll der Geist schweigen?", "Jesus will nicht, dass Dämonen ihn bekannt machen. Bei Markus verbietet er oft, über ihn zu reden – man nennt das das „Messiasgeheimnis“: Wer Jesus ist, versteht man erst vom Kreuz her richtig."),
    ],
    cards=["synagoge", "schriftgelehrte"],
    teaser="Ein ganzes Dorf steht vor der Tür. Und am nächsten Morgen ist Jesus verschwunden.")

sec("anfang", [M(1, 29, 39)], "Heilungen am Abend – und Gebet am Morgen",
    "Jesus heilt die Schwiegermutter des Simon. Abends bringt die ganze Stadt Kranke zu ihm. Früh am Morgen zieht er sich zum Beten zurück – und geht dann weiter in andere Orte.",
    place="kapernaum",
    focus="Achte darauf, was Jesus tut, nachdem alle ihn gefeiert haben.",
    quiz=[
        choice("Was tut Jesus früh am Morgen, als es noch dunkel ist?", ["Er geht an einen einsamen Ort und betet", "Er heilt weitere Kranke", "Er predigt am See", "Er schläft lange"], 35, "Vers 35.",
               "V. 35: Nach dem Trubel sucht Jesus die Stille mit Gott."),
        tf("Jesus bleibt in Kapernaum, weil ihn dort alle suchen.", False, 38, "Lies Vers 37–38.",
           "V. 37–38: Gerade als alle ihn suchen, zieht er weiter: Er will auch anderswo predigen."),
    ],
    explain=[
        E("Warum dient die Schwiegermutter sofort?", "Das Fieber ist ganz weg – sie ist wieder voll da. Das griechische Wort für „dienen“ (diakonein) ist dasselbe, das später für Jesus selbst und seine Jünger benutzt wird (Mk 10,45)."),
        E("Warum zieht Jesus sich zurück?", "Markus erwähnt Jesu Gebet nur an wenigen, entscheidenden Stellen (1,35; 6,46; 14,32). Selbst Jesus braucht Zeiten allein mit Gott – gerade wenn viel los ist."),
    ],
    try_="Nimm dir heute fünf Minuten an einem ruhigen Ort – ohne etwas zu leisten.",
    teaser="Ein Aussätziger kniet nieder. Seine Bitte beginnt mit „wenn“.")

sec("anfang", [M(1, 40, 45)], "Der Aussätzige",
    "Ein Aussätziger bittet: Wenn du willst, kannst du mich reinigen. Jesus ist innerlich bewegt, berührt ihn und sagt: Ich will. Der Mann wird rein – und erzählt es überall herum.",
    quiz=[
        choice("Was tut Jesus, bevor er den Mann heilt?", ["Er streckt die Hand aus und berührt ihn", "Er schickt ihn zuerst zum Priester", "Er befiehlt ihm, sich zu waschen", "Er betet eine Stunde lang"], 41, "Vers 41.",
               "V. 41: Er berührt ihn – einen, den niemand berühren durfte."),
        tf("Der Geheilte hält sich an Jesu Bitte, niemandem etwas zu sagen.", False, 45, "Lies Vers 45.",
           "V. 45: Er erzählt es überall – mit der Folge, dass Jesus nicht mehr offen in die Städte gehen kann."),
    ],
    explain=[
        E("Was war Aussatz?", "Das Wort meint verschiedene Hautkrankheiten. Betroffene galten als unrein und mussten außerhalb der Gemeinschaft leben (3. Mose 13,45–46). Die Berührung durch Jesus war deshalb unerhört."),
        E("Warum soll er zum Priester?", "Nur ein Priester konnte offiziell feststellen, dass jemand wieder rein war – dann durfte er zurück in die Gemeinschaft (3. Mose 14). Jesus will, dass der Mann auch sozial wieder dazugehört."),
    ],
    cards=["rein-unrein"],
    fact="Das Wort, das Markus für „innerlich bewegt“ benutzt, meint wörtlich: Es geht einem an die Eingeweide. In manchen alten Handschriften steht stattdessen „zornig“ – vielleicht über die Krankheit selbst.",
    teaser="Vier Freunde finden keinen Weg hinein. Also machen sie sich einen – durchs Dach.")

# ───────────────────────── 2 · Streit um Jesus ─────────────────────────
sec("streit", [M(2, 1, 12)], "Durchs Dach",
    "Vier Männer decken ein Dach ab, um einen Gelähmten zu Jesus herunterzulassen. Jesus sagt ihm zuerst: Deine Sünden sind vergeben. Die Schriftgelehrten sind empört – da heilt Jesus ihn auch.",
    place="kapernaum",
    quiz=[
        choice("Was sagt Jesus zuerst zu dem Gelähmten?", ["Deine Sünden sind vergeben", "Steh auf und geh", "Dein Glaube hat dich gerettet", "Was willst du?"], 5, "Vers 5.",
               "V. 5: Zuerst die Vergebung, dann die Heilung. Jesus sieht mehr als das, wofür man ihn gebracht hat."),
        tf("Jesus lobt den Glauben der Freunde, die den Mann bringen.", True, 5, "Lies Vers 5 genau.",
           "V. 5: Als Jesus „ihren“ Glauben sah – den der vier Träger."),
    ],
    explain=[
        E("Warum regen sich die Schriftgelehrten auf?", "Sünden vergeben kann nur Gott (V. 7). Wenn Jesus das tut, beansprucht er etwas, das allein Gott zusteht. Für sie ist das Gotteslästerung – oder es stimmt."),
        E("Was ist ein Ruhebett?", "Eine einfache Matte oder Trage, auf der man lag. Häuser hatten flache Dächer aus Balken, Zweigen und Lehm, die man öffnen konnte.", "elbbk"),
    ],
    try_="Gibt es jemanden, den du heute – im übertragenen Sinn – zu Jesus „tragen“ kannst? Ein Gebet für ihn reicht.",
    teaser="Jesus lädt sich zu jemandem ein, den alle anderen meiden.")

sec("streit", [M(2, 13, 17)], "Levi und die Sünder",
    "Jesus ruft den Zöllner Levi in seine Nachfolge und isst danach mit vielen Zöllnern und Sündern. Den Kritikern sagt er: Nicht die Gesunden brauchen den Arzt, sondern die Kranken.",
    place="kapernaum",
    quiz=[
        choice("Wo sitzt Levi, als Jesus ihn ruft?", ["Am Zollhaus", "In der Synagoge", "Im Boot", "Am Brunnen"], 14, "Vers 14.",
               "V. 14: Am Zollhaus – bei der Arbeit, die ihn bei vielen verhasst machte."),
        error("Jesus sagt: Die Starken bedürfen nicht eines Arztes, sondern die [Reichen].", "Kranken", 17,
              "V. 17: Jesus versteht sich als Arzt – gekommen für die, die es nötig haben."),
    ],
    explain=[
        E("Warum waren Zöllner verhasst?", "Sie trieben Zölle für Herodes Antipas bzw. Rom ein und behielten oft mehr als vorgeschrieben. Man sah sie als Kollaborateure und Betrüger."),
        E("Was bedeutet das gemeinsame Essen?", "Im Orient bedeutete Tischgemeinschaft Zugehörigkeit und Annahme. Mit Sündern zu essen hieß: Ich gehöre zu euch. Genau das empört die Frommen."),
    ],
    cards=["pharisaeer"],
    fact="Levi wird im Matthäusevangelium „Matthäus“ genannt (Mt 9,9). Nach alter Tradition ist es derselbe Mann.",
    teaser="Warum fasten die einen und die anderen nicht? Jesus antwortet mit einer Hochzeit.")

sec("streit", [M(2, 18, 22)], "Fasten und neuer Wein",
    "Man fragt Jesus, warum seine Jünger nicht fasten. Er antwortet: Solange der Bräutigam da ist, fastet man nicht. Und: Neuer Wein gehört in neue Schläuche.",
    quiz=[
        choice("Womit vergleicht Jesus die Zeit mit ihm?", ["Mit einer Hochzeit", "Mit einer Ernte", "Mit einem Krieg", "Mit einer Wüstenwanderung"], 19, "Vers 19.",
               "V. 19: Jesus ist der Bräutigam – solange er da ist, ist Festzeit."),
        tf("Jesus sagt, dass seine Jünger niemals fasten werden.", False, 20, "Lies Vers 20.",
           "V. 20: Es kommen Tage, an denen der Bräutigam weggenommen wird – dann werden sie fasten. Ein erster leiser Hinweis auf seinen Tod."),
    ],
    explain=[
        E("Was ist mit den Schläuchen gemeint?", "Wein wurde in Schläuchen aus Tierhaut aufbewahrt. Junger Wein gärt noch und dehnt sich aus – alte, spröde Schläuche platzen. Das Neue, das mit Jesus kommt, passt nicht einfach in alte Formen."),
        E("Fasten Christen heute?", "Ja, in unterschiedlicher Form: Orthodoxe Christen haben viele feste Fastenzeiten, Katholiken und viele Evangelische vor allem die Passionszeit vor Ostern. In Freikirchen ist Fasten meist freiwillig und persönlich."),
    ],
    teaser="Hungrige Jünger pflücken Ähren – und das ausgerechnet am Sabbat.")

sec("streit", [M(2, 23, 28)], "Herr über den Sabbat",
    "Die Jünger pflücken am Sabbat Ähren. Die Pharisäer protestieren. Jesus erinnert an David und sagt: Der Sabbat ist für den Menschen da, nicht der Mensch für den Sabbat.",
    quiz=[
        error("Jesus sagt: Der Mensch wurde um des Sabbats willen, nicht der Sabbat um des [Gesetzes] willen.", "Menschen", 27,
              "V. 27: Andersherum! Der Sabbat ist ein Geschenk für den Menschen.", "Lies Vers 27 genau."),
        choice("An welches Beispiel erinnert Jesus?", ["David, der die Schaubrote aß", "Mose am brennenden Dornbusch", "Elia in der Wüste", "Noah in der Arche"], 25, "Lies Vers 25–26.",
               "V. 25–26: David und seine Männer aßen in der Not die heiligen Brote, die eigentlich nur Priester essen durften (1. Sam 21)."),
    ],
    explain=[
        E("War Ähren pflücken verboten?", "Am Feld eines anderen Ähren mit der Hand zu pflücken, war erlaubt (5. Mose 23,26). Am Sabbat galt es manchen als Erntearbeit."),
        E("Was heißt „Herr des Sabbats“?", "Jesus beansprucht, auslegen zu dürfen, wozu Gott den Sabbat gegeben hat. Für Markus ist das ein weiterer Hinweis darauf, wer Jesus ist."),
    ],
    cards=["sabbat"],
    teaser="Jesus stellt eine Frage, auf die niemand antworten will.")

sec("streit", [M(3, 1, 6)], "Die verdorrte Hand",
    "In der Synagoge lauern sie, ob Jesus am Sabbat heilt. Er fragt: Darf man am Sabbat Gutes tun oder Böses? Sie schweigen. Jesus heilt die Hand – und die Pharisäer planen mit den Herodianern seinen Tod.",
    focus="Achte auf Jesu Gefühle in diesem Abschnitt.",
    quiz=[
        choice("Wie reagieren die Gegner auf Jesu Frage?", ["Sie schweigen", "Sie stimmen ihm zu", "Sie lachen ihn aus", "Sie zitieren Mose"], 4, "Vers 4.",
               "V. 4: Sie schweigen – obwohl die Antwort eigentlich klar ist."),
        choice("Welche Gefühle Jesu nennt Markus?", ["Zorn und Trauer über ihre Verstocktheit", "Angst und Unsicherheit", "Freude und Stolz", "Gleichgültigkeit"], 5, "Vers 5.",
               "V. 5: Er blickt sie zornig an und ist zugleich traurig. Markus zeigt Jesus mit echten Gefühlen."),
    ],
    explain=[
        E("Wer sind die Herodianer?", "Anhänger des Herodes Antipas. Normalerweise hatten sie mit den frommen Pharisäern wenig gemeinsam. Dass sie sich verbünden, zeigt, wie bedrohlich Jesus für beide ist."),
        E("Warum schon jetzt Mordpläne?", "Schon im 3. Kapitel steht das Kreuz am Horizont. Markus erzählt die ganze Geschichte auf das Ende in Jerusalem zu."),
    ],
    teaser="Auf einem Berg wählt Jesus zwölf Männer – darunter einen, der ihn verraten wird.")

sec("streit", [M(3, 7, 19)], "Die Zwölf",
    "Menschen aus dem ganzen Land strömen zu Jesus. Auf einem Berg bestimmt er zwölf, damit sie bei ihm sind und er sie aussenden kann: von Simon Petrus bis Judas Iskariot.",
    place="see-genezareth",
    quiz=[
        choice("Wozu bestimmt Jesus die Zwölf zuerst?", ["Damit sie bei ihm sind", "Damit sie Geld sammeln", "Damit sie die Menge zurückhalten", "Damit sie ein Reich gründen"], 14, "Vers 14.",
               "V. 14: Zuerst „bei ihm sein“, dann ausgesandt werden. Beziehung kommt vor Auftrag."),
        choice("Welchen Beinamen gibt Jesus Jakobus und Johannes?", ["Söhne des Donners", "Fischer der Menschen", "Felsen", "Söhne des Lichts"], 17, "Vers 17.",
               "V. 17: Boanerges, Söhne des Donners – vielleicht wegen ihres Temperaments (vgl. Lk 9,54)."),
    ],
    explain=[
        E("Warum gerade zwölf?", "Israel bestand aus zwölf Stämmen. Mit zwölf Jüngern zeigt Jesus: Hier beginnt Gottes Volk neu."),
        E("Warum nimmt Jesus Judas auf?", "Markus nennt ihn schon jetzt den, der Jesus später ausliefert (V. 19). Warum Jesus ihn trotzdem wählt, sagt der Text nicht. Die Zwölf sind keine perfekten Menschen – das zeigt Markus immer wieder."),
    ],
    cards=["die-zwoelf"],
    teaser="Seine eigene Familie glaubt, er habe den Verstand verloren.")

sec("streit", [M(3, 20, 30)], "„Er ist von Sinnen“",
    "Jesu Familie will ihn zurückholen: Er ist außer sich. Schriftgelehrte aus Jerusalem behaupten, er treibe Dämonen mit dem Obersten der Dämonen aus. Jesus antwortet: Ein in sich gespaltenes Reich kann nicht bestehen.",
    quiz=[
        choice("Was behaupten die Schriftgelehrten aus Jerusalem?", ["Er treibt Dämonen durch den Obersten der Dämonen aus", "Er ist ein Prophet wie Elia", "Er ist ein Zauberer aus Ägypten", "Er ist der Messias"], 22, "Vers 22.",
               "V. 22: Sie können die Macht Jesu nicht leugnen – also erklären sie sie für teuflisch."),
        tf("Jesu Angehörige wollen ihn holen, weil sie ihn für verrückt halten.", True, 21, "Lies Vers 21.",
           "V. 21: Selbst die eigene Familie versteht ihn nicht."),
    ],
    explain=[
        E("Was ist die „Lästerung gegen den Heiligen Geist“?", "Gemeint ist im Zusammenhang: Gottes Wirken bewusst als Werk des Bösen zu erklären (V. 30). Viele Ausleger betonen: Wer Angst hat, diese Sünde begangen zu haben, hat sie gerade nicht begangen – denn die Angst zeigt, dass er Gott nicht verachtet."),
        E("Wer ist der „Starke“?", "Satan. Jesus ist der Stärkere, der ihn bindet und ihm seine „Beute“ – die gefangenen Menschen – abnimmt (V. 27)."),
    ],
    teaser="Draußen stehen seine Mutter und seine Brüder. Jesu Antwort ist überraschend.")

sec("streit", [M(3, 31, 35)], "Jesu wahre Familie",
    "Mutter und Brüder Jesu stehen draußen und lassen ihn rufen. Jesus blickt auf die Menschen um sich und sagt: Wer Gottes Willen tut, ist mein Bruder, meine Schwester und meine Mutter.",
    quiz=[
        choice("Wen nennt Jesus seine Familie?", ["Alle, die den Willen Gottes tun", "Nur seine leibliche Familie", "Nur die Zwölf", "Alle Bewohner Nazareths"], 35, "Vers 35.",
               "V. 35: Wer Gottes Willen tut – eine Familie, zu der jeder gehören kann."),
        tf("Jesus nennt auch Frauen ausdrücklich als Teil seiner Familie.", True, 35, "Lies Vers 35 genau.",
           "V. 35: Bruder, Schwester und Mutter – Frauen gehören ausdrücklich dazu."),
    ],
    explain=[
        E("Lehnt Jesus seine Familie ab?", "Nein. Er weitet den Begriff Familie. Später gehört seine Mutter zu den Jüngern (Apg 1,14), sein Bruder Jakobus wird ein Leiter der Gemeinde in Jerusalem."),
        E("Wie verstehen die Kirchen „Brüder Jesu“?", "Evangelische und freikirchliche Christen sehen darin meist leibliche jüngere Geschwister. Die orthodoxe Tradition versteht sie oft als Kinder Josefs aus einer früheren Ehe, die katholische als Cousins oder nahe Verwandte – passend zur Lehre, dass Maria Jungfrau blieb. Das griechische Wort kann alle drei Bedeutungen tragen."),
    ],
    memory_verse=MV(M(3, 35), "derselbe ist mein Bruder und meine Schwester und meine Mutter"),
    teaser="Ein Bauer sät verschwenderisch – auch dahin, wo nichts wachsen kann.")

# ───────────────────────── 3 · Gleichnisse und Machttaten ─────────────────────────
sec("gleichnisse", [M(4, 1, 9)], "Der Sämann",
    "Vom Boot aus erzählt Jesus: Ein Sämann sät. Manches fällt auf den Weg, auf Felsen, unter Dornen – und manches auf gute Erde und bringt dreißig-, sechzig- und hundertfach Frucht.",
    place="see-genezareth",
    quiz=[
        order("Wohin fällt die Saat? Bring es in die Reihenfolge der Geschichte.", ["Auf den Weg", "Auf felsigen Boden", "Unter die Dornen", "Auf gute Erde"], "V. 4–8."),
        choice("Was passiert mit der Saat auf dem Weg?", ["Vögel fressen sie auf", "Die Sonne verbrennt sie", "Dornen ersticken sie", "Sie wird zertreten"], 4, "Vers 4.",
               "V. 4: Die Vögel holen sie, bevor sie überhaupt keimen kann."),
    ],
    explain=[
        E("Warum sät der Bauer so verschwenderisch?", "In Palästina wurde oft zuerst gesät und danach gepflügt. Der Bauer streut großzügig, auch auf Stellen, die erst später umgegraben werden. Manche sehen darin ein Bild für Gottes großzügiges Wort, das allen gilt."),
        E("Ist hundertfach realistisch?", "Eine gute Ernte brachte vielleicht das Zehnfache. Hundertfach ist eine übertriebene, wunderbare Ernte – ein Bild für Gottes Reich, das am Ende alles übertrifft."),
    ],
    cards=["gleichnis"],
    teaser="Die Jünger verstehen das Gleichnis nicht – und Jesus sagt etwas Rätselhaftes über Gleichnisse überhaupt.")

sec("gleichnisse", [M(4, 10, 20)], "Die Deutung",
    "Allein mit den Jüngern erklärt Jesus: Der Same ist das Wort. Bei manchen nimmt Satan es sofort weg, bei anderen hat es keine Wurzel oder wird von Sorgen und Reichtum erstickt. Bei manchen bringt es Frucht.",
    focus="Achte darauf, was die Dornen bedeuten.",
    quiz=[
        choice("Was ist der Same?", ["Das Wort", "Der Glaube", "Das Geld", "Die Jünger"], 14, "Vers 14.", "V. 14: Der Sämann sät das Wort."),
        choice("Was erstickt das Wort bei denen unter den Dornen?", ["Sorgen, Reichtum und Begierden", "Verfolgung", "Der Satan", "Zweifel an Gott"], 19, "Vers 19.",
               "V. 19: Die Sorgen des Lebens, der trügerische Reichtum und die Gier nach anderen Dingen."),
    ],
    explain=[
        E("Warum sollen manche nicht verstehen (V. 12)?", "Ein schwieriger Vers, ein Zitat aus Jesaja 6,9–10. Viele Ausleger verstehen es so: Gleichnisse öffnen sich denen, die sich darauf einlassen und nachfragen – wer nur von außen zuschaut, sieht nur eine Geschichte. Gerade die Jünger fragen nach (V. 10)."),
        E("Welcher Boden bin ich?", "Eine naheliegende Frage – aber das Gleichnis lädt nicht zur Selbstverurteilung ein. Die meisten Menschen erleben alle vier Böden in verschiedenen Zeiten ihres Lebens."),
    ],
    try_="Was ist heute deine größte „Dorne“ – eine Sorge, die dir den Kopf füllt? Benenne sie einfach einmal vor Gott.",
    teaser="Eine Lampe, ein Maß und ein Bauer, der schläft, während die Saat wächst.")

sec("gleichnisse", [M(4, 21, 29)], "Licht und wachsende Saat",
    "Eine Lampe stellt man nicht unter den Scheffel, sondern auf den Leuchter. Und Gottes Reich wächst wie Saat: Der Bauer schläft und steht auf, und sie wächst – er weiß selbst nicht wie.",
    quiz=[
        tf("Im Gleichnis von der wachsenden Saat weiß der Bauer genau, wie die Saat wächst.", False, 27, "Lies Vers 27.",
           "V. 27: Er weiß selbst nicht wie. Die Erde bringt von selbst Frucht."),
        order("Wie wächst die Saat? Bring es in die Reihenfolge.", ["Gras", "Ähre", "Voller Weizen in der Ähre"], "V. 28: Erst Halm, dann Ähre, dann das volle Korn – Schritt für Schritt.", "Vers 28."),
    ],
    explain=[
        E("Was ist ein Scheffel?", "Ein Hohlmaß für Getreide, etwa ein großer Eimer. Eine Lampe darunter zu stellen, würde sie ersticken.", "elbbk"),
        E("Was sagt die wachsende Saat?", "Gottes Reich wächst nicht durch menschlichen Druck. Wir dürfen säen und schlafen – Gott lässt wachsen. Für Menschen, die sich unter Leistungsdruck setzen, ein befreiender Gedanke."),
    ],
    fact="Das griechische Wort für „von selbst“ in V. 28 ist „automatē“ – daher kommt unser Wort „automatisch“.",
    teaser="Das kleinste aller Samenkörner – du kennst es schon von deinem Startbildschirm.")

sec("gleichnisse", [M(4, 30, 34)], "Das Senfkorn",
    "Gottes Reich ist wie ein Senfkorn: kleiner als alle Samen – doch gesät, wird es größer als alle Gartenpflanzen, und die Vögel finden in seinem Schatten Platz.",
    focus="Achte darauf, wer am Ende im Schatten der Pflanze wohnt.",
    quiz=[
        choice("Was wird aus dem Senfkorn?", ["Größer als alle Kräuter, mit großen Zweigen", "Ein riesiger Zedernbaum", "Ein Weinstock", "Ein Feld voller Weizen"], 32, "Vers 32.",
               "V. 32: Aus dem Winzigsten wird etwas Großes, das anderen Schutz bietet."),
        tf("Jesus erklärt seinen Jüngern die Gleichnisse besonders.", True, 34, "Lies Vers 34.",
           "V. 34: Den Jüngern erklärt er alles – wer nachfragt, bekommt Antwort."),
    ],
    explain=[
        E("Ist das Senfkorn wirklich das kleinste?", "Botanisch gibt es kleinere Samen. Jesus spricht in der Sprache seiner Zuhörer: Für sie war das Senfkorn sprichwörtlich das Kleinste. Die Senfpflanze am See Genezareth kann über zwei Meter hoch werden."),
        E("Warum gerade die Vögel?", "Im Alten Testament ist ein großer Baum, in dem Vögel nisten, ein Bild für ein Reich, das vielen Völkern Schutz gibt (Hes 17,23; Dan 4,9). Gottes Reich wird ein Ort für alle."),
    ],
    memory_verse=MV(M(4, 31), "Wie ein Senfkorn, das, wenn es auf die Erde gesät wird, kleiner ist als alle Samen"),
    fact="Darum wächst in dieser App ein Senfkorn: Jeder kleine Abschnitt, den du liest, lässt es ein Stück wachsen.",
    teaser="Abends auf dem See: Sturm, Wasser im Boot – und Jesus schläft.")

sec("gleichnisse", [M(4, 35, 41)], "Sturm auf dem See",
    "Auf der Überfahrt bricht ein heftiger Sturm los, das Boot läuft voll. Jesus schläft. Die Jünger wecken ihn: Ist es dir egal, dass wir umkommen? Er gebietet dem Wind – und es wird ganz still.",
    place="see-genezareth",
    quiz=[
        who("Lehrer, liegt dir nichts daran, dass wir umkommen", M(4, 38), ["Die Jünger", "Die Menge am Ufer", "Jesus", "Die Schiffer"],
            "V. 38: Ein ehrlicher, fast vorwurfsvoller Hilferuf – und Jesus antwortet darauf."),
        choice("Was fragt Jesus die Jünger nach der Stille?", ["Warum seid ihr so furchtsam? Habt ihr keinen Glauben?", "Wer hat das Boot gesteuert?", "Warum habt ihr mich geweckt?", "Seht ihr nun, wer ich bin?"], 40, "Vers 40.",
               "V. 40: Er fragt nach ihrem Vertrauen – nicht nach ihrer Seglerkunst."),
    ],
    explain=[
        E("Warum schläft Jesus?", "Markus zeigt Jesus ganz menschlich: erschöpft nach einem langen Tag. Sein Schlaf mitten im Sturm wird aber auch zum Bild seines Vertrauens auf Gott (vgl. Ps 4,9)."),
        E("Warum ist die Frage in V. 41 so wichtig?", "Im Alten Testament gebietet nur Gott dem Meer (Ps 107,29; Hiob 38,8–11). Die Jünger fragen: Wer ist denn dieser? Das ist die Grundfrage des ganzen Markusevangeliums."),
    ],
    prayer={"ref": M(4, 38), "source": "Markus 4,38 – ein ehrlicher Hilferuf, den man auch beten darf"},
    teaser="Am anderen Ufer wartet ein Mann, den niemand mehr bändigen kann.")

sec("gleichnisse", [M(5, 1, 13)], "Legion",
    "Im Land der Gadarener lebt ein besessener Mann in den Grabhöhlen, stark und selbstzerstörerisch. Die Geister in ihm nennen sich Legion. Jesus treibt sie aus – sie fahren in eine Schweineherde, die sich in den See stürzt.",
    place="gadarener",
    quiz=[
        who("Legion ist mein Name, denn wir sind viele", M(5, 9), ["Der unreine Geist im Mann", "Ein römischer Soldat", "Ein Schweinehirt", "Jesus"],
            "V. 9: Eine Legion war eine römische Heereseinheit mit Tausenden Soldaten – ein Bild für eine überwältigende Macht."),
        estimate("Wie viele Schweine waren in der Herde?", 100, 5000, 2000, "Schweine", "V. 13: etwa 2.000.", 13, "Vers 13.", tol=200),
    ],
    explain=[
        E("Warum gibt es hier Schweine?", "Das Gebiet östlich des Sees war überwiegend nichtjüdisch (Dekapolis). Für Juden galten Schweine als unrein. Jesus geht hier in fremdes Land."),
        E("Ist das nicht grausam gegenüber den Tieren?", "Die Frage stellen viele. Der Text deutet nicht. Manche Ausleger sehen darin, dass ein Mensch Jesus mehr wert ist als eine ganze Herde; andere, dass das Zerstörerische hier sichtbar endet – im See, der für Chaos steht."),
    ],
    teaser="Die Leute der Gegend sehen den Geheilten – und bitten Jesus, zu gehen.")

sec("gleichnisse", [M(5, 14, 20)], "Geh nach Hause und erzähl",
    "Die Leute finden den Mann bekleidet und vernünftig – und fürchten sich. Sie bitten Jesus zu gehen. Der Geheilte will mit, doch Jesus schickt ihn nach Hause: Erzähl, was der Herr an dir getan hat.",
    place="gadarener",
    quiz=[
        choice("Wie reagieren die Bewohner auf die Heilung?", ["Sie fürchten sich und bitten Jesus zu gehen", "Sie feiern ein Fest", "Sie bringen alle ihre Kranken", "Sie wollen Jesus zum König machen"], 17, "Lies Vers 15–17.",
               "V. 15–17: Furcht statt Freude – vielleicht auch wegen des wirtschaftlichen Verlusts."),
        tf("Jesus erlaubt dem Geheilten, mit ihm zu gehen.", False, 19, "Lies Vers 19.",
           "V. 19: Er schickt ihn zu seiner Familie. Sein Auftrag ist zu Hause – und er verkündet in der ganzen Dekapolis."),
    ],
    explain=[
        E("Warum darf er hier erzählen?", "Sonst verbietet Jesus oft, von ihm zu reden. Hier im nichtjüdischen Gebiet bestand nicht die Gefahr, dass man ihn als politischen Messias missverstand. Der Mann wird zu einem der ersten Boten unter Nichtjuden."),
    ],
    cards=["dekapolis"],
    try_="Erzähl heute einer Person von etwas Gutem, das du erlebt hast – es muss nichts Großes sein.",
    teaser="Ein angesehener Mann bittet für seine sterbende Tochter. Und dann wird Jesus aufgehalten.")

sec("gleichnisse", [M(5, 21, 34)], "Die Frau im Gedränge",
    "Jaïrus bittet Jesus, seine sterbende Tochter zu heilen. Unterwegs berührt eine Frau, die seit zwölf Jahren an Blutungen leidet, heimlich sein Gewand – und ist geheilt. Jesus bleibt stehen und sucht sie: Tochter, dein Glaube hat dich gerettet.",
    focus="Achte darauf, wie Jesus die Frau am Ende nennt.",
    quiz=[
        estimate("Wie viele Jahre litt die Frau schon?", 1, 40, 12, "Jahre", "V. 25: zwölf Jahre – genau so alt wie die Tochter des Jaïrus (V. 42).", 25, "Vers 25."),
        choice("Wie nennt Jesus die Frau?", ["Tochter", "Schwester", "Sünderin", "Fremde"], 34, "Vers 34.",
               "V. 34: „Tochter“ – eine Ausgestoßene wird in die Familie aufgenommen."),
    ],
    explain=[
        E("Warum berührt sie ihn heimlich?", "Mit ihren Blutungen galt sie als unrein; wer sie berührte, wurde es auch (3. Mose 15,25–27). Sie durfte eigentlich nicht in die Menge. Jesus holt sie aus der Heimlichkeit – nicht um sie bloßzustellen, sondern um sie öffentlich als geheilt und angenommen zu erklären."),
        E("Warum sucht Jesus sie, obwohl es eilt?", "Ein sterbendes Kind wartet – und Jesus bleibt stehen. Markus verschachtelt die beiden Geschichten bewusst: Für Jesus ist keiner unwichtiger als der andere."),
    ],
    teaser="Boten kommen: Zu spät, das Mädchen ist tot. Jesus hört es – und geht trotzdem weiter.")

sec("gleichnisse", [M(5, 35, 43)], "„Talita kum“",
    "Die Tochter des Jaïrus ist gestorben. Jesus sagt: Fürchte dich nicht, glaube nur. Im Haus nimmt er das Mädchen bei der Hand: Talita kum – Mädchen, steh auf! Sie steht auf und geht umher.",
    focus="Achte auf den kleinen, praktischen Auftrag ganz am Ende.",
    quiz=[
        choice("Was bedeutet „Talitha kumi“?", ["Mädchen, ich sage dir, steh auf!", "Friede sei mit dir!", "Kind, deine Sünden sind vergeben", "Wach auf und iss!"], 41, "Vers 41.",
               "V. 41: Markus überliefert Jesu Worte auf Aramäisch, seiner Muttersprache."),
        tf("Jesus lässt alle Trauernden mit ins Zimmer.", False, 40, "Lies Vers 40.",
           "V. 40: Er schickt die Spötter hinaus und nimmt nur die Eltern und drei Jünger mit."),
        choice("Was sollen die Eltern dem Mädchen geben?", ["Etwas zu essen", "Ein neues Kleid", "Ein Opfer für den Tempel", "Einen neuen Namen"], 43, "Vers 43.",
               "V. 43: Etwas zu essen – ganz praktische Fürsorge nach dem Wunder."),
    ],
    explain=[
        E("„Nicht gestorben, sondern es schläft“?", "Die Leute wissen, dass das Kind tot ist – deshalb lachen sie. Jesus spricht vom Tod als einem Schlaf, aus dem er wecken kann. Das frühe Christentum hat dieses Bild für den Tod der Glaubenden übernommen (1. Thess 4,13–14)."),
        E("Warum aramäisch?", "Aramäisch war die Alltagssprache Jesu. Dass Markus, der griechisch schreibt, die Worte original überliefert, zeigt, wie wertvoll die Erinnerung daran war."),
    ],
    teaser="In seiner Heimatstadt kennen ihn alle. Genau das wird zum Problem.")

# ───────────────────────── 4 · Brot für viele ─────────────────────────
sec("brot", [M(6, 1, 6)], "Nazareth",
    "In seiner Vaterstadt staunen die Leute über Jesu Weisheit – und nehmen Anstoß: Ist das nicht der Zimmermann, Marias Sohn? Jesus kann dort kaum Wunder tun und wundert sich über ihren Unglauben.",
    place="nazareth",
    quiz=[
        choice("Welchen Beruf hatte Jesus laut den Leuten in Nazareth?", ["Zimmermann", "Fischer", "Hirte", "Schriftgelehrter"], 3, "Vers 3.",
               "V. 3: Zimmermann bzw. Bauhandwerker – sie kennen ihn als einen von ihnen."),
        tf("In Nazareth heilt Jesus niemanden.", False, 5, "Lies Vers 5 genau.",
           "V. 5: Er legt einigen Kranken die Hände auf und heilt sie – aber große Wunder geschehen nicht."),
    ],
    explain=[
        E("Was heißt „Zimmermann“?", "Das griechische Wort „tekton“ meint einen Bauhandwerker, der mit Holz und Stein arbeitet. Nahe Nazareth wurde damals die Stadt Sepphoris neu gebaut – vielleicht arbeitete Jesus dort."),
        E("Warum konnte Jesus dort nichts tun?", "Markus sagt ehrlich, dass Jesus „nicht konnte“. Seine Wunder sind keine Zaubershow; sie geschehen in einer Beziehung des Vertrauens."),
    ],
    teaser="Die Zwölf werden ausgesandt – mit erstaunlich wenig Gepäck.")

sec("brot", [M(6, 7, 13)], "Die Aussendung",
    "Jesus sendet die Zwölf zu zweit aus. Sie sollen nichts mitnehmen außer einem Stab – kein Brot, keine Tasche, kein Geld. Sie predigen Umkehr, treiben Dämonen aus und heilen Kranke.",
    quiz=[
        choice("Was dürfen die Zwölf mitnehmen?", ["Nur einen Stab (und Sandalen)", "Brot für drei Tage", "Eine Tasche mit Geld", "Zwei Gewänder"], 8, "Lies Vers 8–9.",
               "V. 8–9: Nur Stab und Sandalen. Sie sollen sich auf Gott und die Gastfreundschaft anderer verlassen."),
        tf("Jesus schickt die Zwölf einzeln los.", False, 7, "Vers 7.", "V. 7: zu zweit – niemand ist allein unterwegs."),
    ],
    explain=[
        E("Was heißt „Staub abschütteln“?", "Fromme Juden schüttelten den Staub ab, wenn sie aus heidnischem Gebiet zurückkamen. Hier ist es ein Zeichen: Wir lassen euch die Verantwortung für eure Ablehnung – ohne Gewalt oder Rache."),
        E("Warum mit Öl salben?", "Öl war ein bekanntes Heilmittel und zugleich ein Zeichen für Gottes Zuwendung. Daraus entstand in vielen Kirchen die Krankensalbung (vgl. Jak 5,14)."),
    ],
    teaser="König Herodes hört von Jesus – und bekommt ein schlechtes Gewissen.")

sec("brot", [M(6, 14, 20)], "Herodes und Johannes",
    "Herodes hält Jesus für den auferstandenen Johannes. Rückblende: Herodes hatte Johannes eingesperrt, weil dieser seine Ehe mit Herodias kritisierte. Er fürchtete Johannes – und hörte ihm trotzdem gern zu.",
    quiz=[
        choice("Warum ließ Herodes Johannes gefangen nehmen?", ["Weil Johannes seine Ehe mit Herodias kritisierte", "Weil Johannes zum Aufstand aufrief", "Weil Johannes keine Steuern zahlte", "Weil Johannes ein Römer war"], 18, "Lies Vers 17–18.",
               "V. 17–18: Herodias war die Frau seines Bruders Philippus. Johannes sagte ihm offen: Das ist dir nicht erlaubt."),
        tf("Herodes hörte Johannes gern zu.", True, 20, "Lies Vers 20.",
           "V. 20: Er wusste, dass Johannes gerecht war – und war zugleich ratlos. Ein innerlich zerrissener Mann."),
    ],
    explain=[
        E("Wer hielt Jesus für wen?", "Manche hielten Jesus für Elia, andere für einen Propheten, Herodes für den auferstandenen Johannes (V. 14–16). Die Frage „Wer ist dieser?“ zieht sich durch das ganze Buch – und wird in Kapitel 8 beantwortet."),
    ],
    cards=["herodes-antipas"],
    teaser="Ein Fest, ein Tanz, ein unbedachter Schwur.")

sec("brot", [M(6, 21, 29)], "Der Tod des Täufers",
    "An seinem Geburtstag verspricht Herodes der tanzenden Tochter der Herodias jeden Wunsch. Auf Drängen ihrer Mutter verlangt sie den Kopf des Johannes. Herodes ist betrübt – und gibt nach.",
    quiz=[
        choice("Bis zu welcher Grenze verspricht Herodes dem Mädchen ihren Wunsch?", ["Bis zur Hälfte seines Reiches", "Bis zu hundert Silberstücken", "Bis zu einem Palast", "Ohne jede Grenze"], 23, "Vers 23.",
               "V. 23: bis zur Hälfte seines Reiches – ein großspuriger Schwur vor Gästen."),
        choice("Warum gibt Herodes nach, obwohl er betrübt ist?", ["Wegen seines Schwurs und der Gäste", "Weil er Johannes hasste", "Weil Rom es befahl", "Weil Johannes geflohen war"], 26, "Vers 26.",
               "V. 26: Aus Angst, vor den Gästen sein Gesicht zu verlieren. Menschenfurcht siegt über das Gewissen."),
    ],
    explain=[
        E("Warum steht diese Geschichte hier?", "Markus erzählt sie zwischen Aussendung und Rückkehr der Jünger. Das ist ein Hinweis: Wer Gottes Botschaft ausrichtet, kann wie Johannes Widerstand erfahren – und Jesu eigenes Schicksal kündigt sich an."),
    ],
    fact="Der jüdische Historiker Flavius Josephus berichtet ebenfalls von der Hinrichtung Johannes des Täufers durch Herodes Antipas – in der Festung Machärus östlich des Toten Meeres.",
    teaser="Die Jünger sind erschöpft. Jesus sagt etwas, das du vielleicht heute selbst hören musst.")

sec("brot", [M(6, 30, 34)], "Ruht ein wenig aus",
    "Die Apostel kommen zurück und erzählen. Jesus sagt: Kommt an einen ruhigen Ort und ruht ein wenig aus. Doch die Menge läuft voraus. Jesus sieht sie und hat Mitleid, denn sie sind wie Schafe ohne Hirten.",
    focus="Achte darauf, was Jesus seinen müden Jüngern zuerst anbietet.",
    quiz=[
        choice("Was sagt Jesus zu den heimgekehrten Aposteln?", ["Kommt an einen öden Ort und ruht ein wenig aus", "Geht sofort wieder los", "Erzählt es niemandem", "Fastet drei Tage"], 31, "Vers 31.",
               "V. 31: Ausruhen ist kein Luxus – Jesus selbst lädt dazu ein."),
        choice("Womit vergleicht Jesus die Menschenmenge?", ["Mit Schafen, die keinen Hirten haben", "Mit Weizen vor der Ernte", "Mit Kindern auf dem Markt", "Mit Fischen im Netz"], 34, "Vers 34.",
               "V. 34: Ohne Hirte – orientierungslos. Das erinnert an Hesekiel 34, wo Gott selbst sein Volk weiden will."),
    ],
    explain=[
        E("Warum steht hier „Apostel“?", "Das Wort heißt „Gesandte“. Markus benutzt es nur hier – genau nach ihrer ersten Sendung."),
    ],
    memory_verse=MV(M(6, 31), "Kommt ihr selbst her an einen öden Ort besonders und ruht ein wenig aus"),
    try_="Plan dir heute bewusst eine kleine Pause ein – ohne schlechtes Gewissen. Jesus hat es seinen Jüngern verordnet.",
    teaser="Fünftausend hungrige Menschen. Fünf Brote. Und Jesus sagt: Gebt ihr ihnen zu essen.")

sec("brot", [M(6, 35, 44)], "Brot für Fünftausend",
    "Es wird spät, die Menge ist hungrig. Jesus sagt: Gebt ihr ihnen zu essen. Fünf Brote und zwei Fische – er segnet, bricht und lässt verteilen. Alle werden satt, und zwölf Körbe bleiben übrig.",
    quiz=[
        order("Was tut Jesus mit den Broten? In der Reihenfolge von Vers 41:", ["Er blickt zum Himmel", "Er segnet", "Er bricht die Brote", "Er gibt sie den Jüngern"], "V. 41 – dieselben Schritte wie später beim letzten Mahl (14,22).", "Vers 41."),
        estimate("Wie viele Körbe mit Resten sammeln sie ein?", 1, 20, 12, "Körbe", "V. 43: zwölf – so viele wie die Stämme Israels und die Jünger.", 43, "Vers 43."),
    ],
    explain=[
        E("Warum lagern sie in Gruppen zu 100 und 50?", "Das erinnert an Israels Ordnung in der Wüste (2. Mose 18,21). Auch das „grüne Gras“ (V. 39) erinnert an Psalm 23: Der gute Hirte lässt lagern auf grüner Weide."),
        E("Wie viele Menschen waren es wirklich?", "Markus zählt 5.000 Männer (V. 44). Frauen und Kinder wurden damals oft nicht mitgezählt – es waren also wohl noch mehr."),
    ],
    fact="Die Speisung ist das einzige Wunder Jesu (außer der Auferstehung), das in allen vier Evangelien erzählt wird.",
    teaser="Mitten in der Nacht, mitten auf dem See: Jemand kommt übers Wasser.")

sec("brot", [M(6, 45, 56)], "Auf dem Wasser",
    "Jesus schickt die Jünger voraus und betet auf dem Berg. Sie kämpfen gegen den Wind. Gegen Morgen kommt er auf dem See zu ihnen. Sie halten ihn für ein Gespenst. Er sagt: Seid getrost, ich bin es; fürchtet euch nicht!",
    place="see-genezareth",
    quiz=[
        who("Seid guten Mutes, ich bin es; fürchtet euch nicht", M(6, 50), ["Jesus", "Petrus", "Ein Engel", "Ein Fischer am Ufer"],
            "V. 50: „Ich bin es“ – im Griechischen dieselben Worte, mit denen Gott sich in 2. Mose 3,14 vorstellt."),
        tf("Bei Markus geht Petrus Jesus auf dem Wasser entgegen.", False, None, "Kommt Petrus in diesem Abschnitt überhaupt vor?",
           "Das erzählt nur Matthäus (Mt 14,28–31). Markus erzählt knapper und betont das Unverständnis der Jünger (V. 52)."),
    ],
    explain=[
        E("Was ist die „vierte Nachtwache“?", "Die Römer teilten die Nacht in vier Wachen. Die vierte war zwischen etwa 3 und 6 Uhr morgens – die Jünger hatten also die ganze Nacht gekämpft."),
        E("Warum „wollte er vorübergehen“?", "Ein seltsamer Satz (V. 48). Er erinnert an Gotteserscheinungen im Alten Testament: Gott „ging vorüber“ an Mose und Elia (2. Mose 33,22; 1. Kön 19,11). Jesus zeigt sich hier mit göttlicher Würde."),
    ],
    teaser="Ungewaschene Hände lösen einen Grundsatzstreit aus.")

sec("brot", [M(7, 1, 13)], "Überlieferung oder Gebot?",
    "Pharisäer kritisieren, dass Jesu Jünger mit ungewaschenen Händen essen. Jesus antwortet mit Jesaja: Dieses Volk ehrt mich mit den Lippen, aber ihr Herz ist fern. Menschliche Überlieferungen dürfen Gottes Gebot nicht aushebeln.",
    quiz=[
        choice("Worüber beschweren sich die Pharisäer?", ["Die Jünger essen mit ungewaschenen Händen", "Die Jünger fasten nicht", "Die Jünger arbeiten am Sabbat", "Die Jünger essen Schweinefleisch"], 5, "Vers 5.",
               "V. 5: Es geht um rituelles Händewaschen nach der Überlieferung der Ältesten."),
        choice("Welches Beispiel nennt Jesus für ausgehebeltes Gebot?", ["Eltern nicht zu versorgen, weil man es „Korban“ nennt", "Am Sabbat zu arbeiten", "Den Tempel zu meiden", "Fremde nicht zu grüßen"], 11, "Lies Vers 10–12.",
               "V. 10–12: Mit einem frommen Gelübde sollte man sich vor der Pflicht drücken können, für die Eltern zu sorgen."),
    ],
    explain=[
        E("Was ist „Korban“?", "Hebräisch „Opfergabe“. Wer etwas als Korban erklärte, weihte es Gott – und konnte es angeblich den Eltern verweigern. Jesus sagt: So wird das Gebot, die Eltern zu ehren, ausgehebelt."),
        E("War Händewaschen schlecht?", "Nein. Es ging nicht um Hygiene, sondern um rituelle Reinheit. Jesus kritisiert, wenn Regeln wichtiger werden als Gottes eigentlicher Wille."),
    ],
    teaser="Jesus erklärt, was einen Menschen wirklich unrein macht – und die Antwort ist unbequem.")

sec("brot", [M(7, 14, 23)], "Was wirklich unrein macht",
    "Jesus erklärt: Nichts, was von außen in den Menschen hineingeht, macht ihn unrein – sondern was aus seinem Herzen herauskommt: böse Gedanken, Habgier, Neid, Hochmut und vieles mehr.",
    quiz=[
        choice("Woher kommt laut Jesus das, was den Menschen unrein macht?", ["Von innen, aus dem Herzen", "Aus unreinem Essen", "Von fremden Menschen", "Aus dem Tempel"], 21, "Vers 21.",
               "V. 21: Aus dem Herzen. Jesus verlagert die Frage nach Reinheit vom Teller ins Innere."),
        tf("Markus folgert: Damit erklärte Jesus alle Speisen für rein.", True, 19, "Lies Vers 19 genau.",
           "V. 19: Markus fügt diesen Kommentar ein – für die frühe Kirche aus Juden und Nichtjuden eine wichtige Frage."),
    ],
    explain=[
        E("Was bedeutet das für Speisegebote?", "Für die frühen Christen war das eine große Frage: Müssen Nichtjuden jüdische Speisegesetze halten? Die Kirche hat das verneint (vgl. Apg 10; 15). Jüdische Gläubige halten sie bis heute als Teil ihres Bundes mit Gott."),
    ],
    teaser="Eine ausländische Frau lässt sich nicht abwimmeln – und Jesus gibt ihr recht.")

sec("brot", [M(7, 24, 30)], "Die syrophönizische Frau",
    "Im Gebiet von Tyrus bittet eine nichtjüdische Frau um Hilfe für ihre Tochter. Jesus antwortet hart: Erst die Kinder, nicht den Hunden das Brot. Sie kontert: Auch die Hunde essen die Krümel unter dem Tisch. Jesus heilt ihre Tochter.",
    place="tyrus",
    quiz=[
        who("Ja, Herr; denn es essen ja auch die Hündchen unter dem Tisch von den Brotkrumen der Kinder", M(7, 28),
            ["Die syrophönizische Frau", "Ein Jünger", "Die Tochter", "Ein Pharisäer"],
            "V. 28: Eine schlagfertige, demütige und zugleich mutige Antwort."),
        choice("Warum heilt Jesus die Tochter?", ["Wegen der Antwort der Frau", "Weil die Jünger ihn drängen", "Weil sie viel Geld bietet", "Weil sie Jüdin wird"], 29, "Vers 29.",
               "V. 29: Wegen ihrer Antwort – ihr Vertrauen überzeugt ihn."),
    ],
    explain=[
        E("Warum spricht Jesus so hart?", "Eine schwierige Stelle. „Kinder“ meint Israel, zu dem Jesus zuerst gesandt ist; „Hunde“ war ein gängiges abwertendes Wort für Nichtjuden. Manche Ausleger meinen, Jesus prüfe die Frau; andere, er lasse sich von ihr bewegen. Auf jeden Fall endet die Geschichte damit, dass auch Nichtjuden Anteil an Gottes Brot bekommen."),
    ],
    fact="Die Frau ist die einzige Person im Markusevangelium, die mit Jesus diskutiert und dabei recht bekommt.",
    teaser="Jesus legt einem Tauben die Finger in die Ohren, seufzt und sagt ein einziges aramäisches Wort.")

sec("brot", [M(7, 31, 37)], "„Effata“",
    "In der Dekapolis bringt man einen Tauben mit einer Sprachstörung zu Jesus. Er nimmt ihn beiseite, berührt Ohren und Zunge, seufzt und sagt: Effata – öffne dich! Der Mann hört und spricht klar.",
    place="dekapolis",
    quiz=[
        choice("Was bedeutet „Ephata“?", ["Werde aufgetan!", "Steh auf!", "Sei rein!", "Geh in Frieden!"], 34, "Vers 34.", "V. 34: Öffne dich!"),
        tf("Jesus heilt den Mann vor der ganzen Menge.", False, 33, "Lies Vers 33.",
           "V. 33: Er nimmt ihn beiseite – eine persönliche, behutsame Heilung."),
    ],
    explain=[
        E("Warum diese Gesten?", "Finger in die Ohren, Speichel auf die Zunge: Jesus „spricht“ mit dem Mann in einer Sprache, die er versteht – durch Berührung. Speichel galt damals auch als Heilmittel."),
        E("Was bedeutet der Ausruf in V. 37?", "Dass er alles gut gemacht hat, erinnert an die Schöpfung (1. Mose 1,31), „Taube hören, Stumme reden“ an Jesaja 35,5–6: Gottes neue Welt bricht an."),
    ],
    fact="In manchen Kirchen berührt der Pfarrer bei der Taufe Ohren und Mund des Täuflings und spricht „Effata“ – nach dieser Geschichte.",
    teaser="Schon wieder eine hungrige Menge in der Wüste. Und die Jünger fragen, als wäre nichts gewesen.")

# ───────────────────────── 5 · Wer bin ich? ─────────────────────────
sec("wer", [M(8, 1, 10)], "Brot für Viertausend",
    "Wieder ist eine große Menge seit drei Tagen bei Jesus und hat nichts zu essen. Mit sieben Broten und ein paar Fischen werden etwa 4.000 Menschen satt; sieben Körbe bleiben übrig.",
    quiz=[
        estimate("Wie viele Brote haben die Jünger diesmal?", 1, 12, 7, "Brote", "V. 5: sieben Brote – und am Ende sieben Körbe voll Reste.", 5, "Vers 5."),
        choice("Was fragen die Jünger, obwohl sie die erste Speisung erlebt haben?", ["Woher soll man hier in der Einöde Brot nehmen?", "Sollen wir Geld sammeln?", "Dürfen wir zuerst essen?", "Warum hast du so lange gewartet?"], 4, "Vers 4.",
               "V. 4: Als hätten sie nichts erlebt. Markus zeigt ehrlich, wie langsam die Jünger verstehen."),
    ],
    explain=[
        E("Ist das nicht dieselbe Geschichte zweimal?", "Manche Ausleger vermuten zwei Fassungen desselben Ereignisses. Markus erzählt sie bewusst als zwei Ereignisse (vgl. 8,19–20): einmal wohl am jüdischen Westufer, einmal im nichtjüdischen Gebiet. Brot für beide."),
    ],
    teaser="Die Jünger haben nur ein Brot im Boot – und verstehen Jesu Warnung völlig falsch.")

sec("wer", [M(8, 11, 21)], "Sauerteig und harte Herzen",
    "Pharisäer verlangen ein Zeichen; Jesus verweigert es. Im Boot warnt er vor dem Sauerteig der Pharisäer und des Herodes. Die Jünger denken nur an das fehlende Brot. Jesus fragt: Versteht ihr immer noch nicht?",
    quiz=[
        choice("Wovor warnt Jesus die Jünger?", ["Vor dem Sauerteig der Pharisäer und des Herodes", "Vor dem Sturm auf dem See", "Vor den Römern", "Vor zu viel Essen"], 15, "Vers 15.",
               "V. 15: Sauerteig durchdringt alles – ein Bild für eine Haltung, die sich ausbreitet."),
        tf("Die Jünger verstehen die Warnung sofort richtig.", False, 16, "Lies Vers 16.",
           "V. 16: Sie denken, es gehe um vergessenes Brot."),
    ],
    explain=[
        E("Was ist der „Sauerteig“?", "Sauerteig lässt den ganzen Teig gären. Gemeint ist wohl eine Grundhaltung: bei den Pharisäern die Forderung nach Beweisen, bei Herodes Machtstreben. Beides macht blind für Gott."),
        E("Warum fragt Jesus nach den Körben?", "Zwölf und sieben Körbe übrig (V. 19–20) – es war immer mehr als genug. Wer das erlebt hat, muss sich um ein fehlendes Brot keine Sorgen machen."),
    ],
    teaser="Ein Blinder sieht zunächst nur halb. Jesus legt ein zweites Mal die Hände auf.")

sec("wer", [M(8, 22, 26)], "Der Blinde von Bethsaida",
    "In Bethsaida führt Jesus einen Blinden aus dem Dorf, legt ihm die Hände auf und fragt: Siehst du etwas? Der Mann sieht Menschen wie umhergehende Bäume. Erst nach einer zweiten Berührung sieht er alles klar.",
    place="bethsaida",
    focus="Achte darauf, dass diese Heilung in zwei Schritten geschieht.",
    quiz=[
        error("Der Mann sagt: Ich sehe die Menschen, denn ich gewahre solche, die wie [Schatten] umherwandeln.", "Bäume", 24,
              "V. 24: Wie Bäume – er sieht, aber noch verschwommen."),
        choice("Wie oft legt Jesus dem Blinden die Hände auf?", ["Zweimal", "Einmal", "Dreimal", "Gar nicht"], 25, "Lies Vers 23–25.",
               "V. 23 und 25: In zwei Schritten – die einzige Heilung dieser Art in den Evangelien."),
    ],
    explain=[
        E("Warum in zwei Schritten?", "Viele Ausleger sehen darin ein Bild für die Jünger: Sie haben „halb gesehen“, wer Jesus ist, aber noch verschwommen. Im nächsten Abschnitt erkennt Petrus Jesus als Christus – und versteht doch noch nicht alles."),
    ],
    teaser="Auf dem Weg fragt Jesus: Für wen haltet ihr mich? Die Antwort ist die Mitte des Buches.")

sec("wer", [M(8, 27, 33)], "„Du bist der Christus“",
    "Bei Cäsarea Philippi fragt Jesus: Für wen halten mich die Leute – und ihr? Petrus antwortet: Du bist der Christus. Dann kündigt Jesus erstmals offen sein Leiden an. Petrus widerspricht – und Jesus weist ihn scharf zurück.",
    place="caesarea-philippi",
    focus="Achte darauf, wie schnell Petrus vom besten zum schlechtesten Moment wechselt.",
    quiz=[
        who("Du bist der Christus", M(8, 29), ["Petrus", "Johannes", "Ein Dämon", "Die Leute"],
            "V. 29: Das zentrale Bekenntnis – genau in der Mitte des Markusevangeliums."),
        order("Was kündigt Jesus an? In der Reihenfolge von Vers 31:", ["Vieles leiden", "Verworfen werden", "Getötet werden", "Nach drei Tagen auferstehen"], "V. 31.", "Vers 31."),
        choice("Warum nennt Jesus Petrus „Satan“?", ["Weil er ihn vom Weg des Leidens abbringen will", "Weil er gelogen hat", "Weil er Jesus verraten wird", "Weil er zu laut war"], 33, "Vers 33.",
               "V. 33: Petrus denkt wie Menschen denken: Ein Messias leidet nicht. Das ist dieselbe Versuchung wie in der Wüste – den leichteren Weg zu gehen."),
    ],
    explain=[
        E("Was heißt „Christus“?", "Griechisch für „Messias“, der Gesalbte – der erwartete König. Viele erwarteten einen politischen Befreier von Rom. Deshalb soll niemand es weitersagen (V. 30): Jesus ist ein anderer Messias."),
        E("Ist Petrus jetzt „der Satan“?", "Nein – „Satan“ heißt „Widersacher“. Jesus weist den Gedanken zurück, nicht die Person. Petrus bleibt Jünger."),
    ],
    cards=["menschensohn"],
    teaser="Jesus sagt, was es kostet, ihm nachzufolgen – und was man dabei gewinnt.")

sec("wer", [M(8, 34, 38), M(9, 1)], "Nachfolge",
    "Jesus ruft alle: Wer mir folgen will, verleugne sich selbst, nehme sein Kreuz und folge mir. Wer sein Leben retten will, verliert es; wer es um seinetwillen verliert, gewinnt es. Was nützt die ganze Welt, wenn man seine Seele verliert?",
    quiz=[
        choice("Was nützt es laut Jesus, die ganze Welt zu gewinnen?", ["Nichts, wenn man dabei seine Seele verliert", "Viel, wenn man es teilt", "Es ist ein Zeichen von Gottes Segen", "Es macht einen zum König"], 36, "Vers 36.",
               "V. 36: Das Wichtigste lässt sich nicht kaufen."),
        tf("Jesus richtet diese Worte nur an die Zwölf.", False, 34, "Lies Vers 34.",
           "V. 34: Er ruft die Menge samt den Jüngern – die Einladung gilt allen."),
    ],
    explain=[
        E("Was heißt „sein Kreuz aufnehmen“?", "Verurteilte mussten den Querbalken ihres Kreuzes selbst zum Hinrichtungsort tragen. Jesus meint: bereit sein, für ihn auch Nachteile, Ablehnung, sogar den Tod in Kauf zu nehmen. Es meint nicht, jedes Unglück als gottgewollt hinzunehmen."),
        E("Was bedeutet 9,1?", "Ein schwieriger Vers. Viele verstehen ihn als Hinweis auf die Verklärung, die direkt danach folgt: Drei Jünger sehen dort Gottes Herrlichkeit schon jetzt. Andere beziehen ihn auf Auferstehung und Pfingsten."),
    ],
    memory_verse=MV(M(8, 36), "was wird es einem Menschen nützen, wenn er die ganze Welt gewönne und seine Seele einbüßte"),
    teaser="Auf einem hohen Berg sehen drei Jünger Jesus so, wie sie ihn nie gesehen haben.")

sec("wer", [M(9, 2, 13)], "Die Verklärung",
    "Auf einem hohen Berg wird Jesus vor Petrus, Jakobus und Johannes verwandelt; seine Kleider strahlen. Mose und Elia erscheinen. Aus einer Wolke spricht eine Stimme: Das ist mein geliebter Sohn, auf ihn sollt ihr hören.",
    quiz=[
        choice("Wer erscheint bei Jesus auf dem Berg?", ["Mose und Elia", "Abraham und David", "Johannes der Täufer und Jesaja", "Zwei Engel"], 4, "Vers 4.",
               "V. 4: Mose steht für das Gesetz, Elia für die Propheten – beide bestätigen Jesus."),
        choice("Was schlägt Petrus vor?", ["Drei Hütten zu bauen", "Sofort hinabzusteigen", "Den anderen Jüngern Bescheid zu geben", "Gemeinsam zu beten"], 5, "Vers 5.",
               "V. 5: Er möchte den Moment festhalten – aber er weiß nicht, was er sagt (V. 6)."),
    ],
    explain=[
        E("Was ist eine „Verklärung“?", "Jesus wird „umgestaltet“ (griechisch metamorphoō): Für einen Moment sehen die Jünger seine göttliche Herrlichkeit. Die Ostkirche feiert dieses Ereignis als eines der großen Feste."),
        E("Was hat Elia mit Johannes zu tun?", "Nach Maleachi 3,23 sollte Elia vor dem großen Tag Gottes wiederkommen. Jesus sagt: Elia ist schon gekommen (V. 13) – gemeint ist Johannes der Täufer."),
    ],
    fact="Die Stimme bei der Verklärung wiederholt fast die Worte bei der Taufe (1,11) – mit einem Zusatz an die Jünger: „Ihn hört.“",
    teaser="Unten im Tal ist das Chaos groß: Die Jünger haben versagt, und ein Vater ist verzweifelt.")

sec("wer", [M(9, 14, 20)], "Die Jünger können nicht",
    "Unten am Berg streiten Schriftgelehrte mit den Jüngern. Ein Vater hat seinen Sohn mit einem stummen Geist gebracht – die Jünger konnten nicht helfen. Jesus ruft: Bringt ihn zu mir! Der Junge bricht vor ihm zusammen.",
    quiz=[
        choice("Was ist das Problem, als Jesus vom Berg kommt?", ["Die Jünger konnten den Jungen nicht heilen", "Die Menge will Jesus steinigen", "Die Jünger sind eingeschlafen", "Es gibt nichts zu essen"], 18, "Vers 18.",
               "V. 18: Die Jünger haben es versucht – und es hat nicht geklappt."),
        tf("Jesus ist von der Lage frustriert.", True, 19, "Lies Vers 19.",
           "V. 19: Er fragt, wie lange er sie noch ertragen soll. Auch Jesu Ungeduld verschweigt Markus nicht."),
    ],
    explain=[
        E("Welche Krankheit hatte der Junge?", "Die Beschreibung (Krämpfe, Schaum, Zähneknirschen) erinnert an Epilepsie. Matthäus nennt ihn „mondsüchtig“. Der Text spricht von einem Geist. Für Markus wichtig: Das Leiden ist schlimm, alt und hat menschliche Hilfe überfordert."),
    ],
    teaser="Der Vater sagt den vielleicht ehrlichsten Satz des Neuen Testaments.")

sec("wer", [M(9, 21, 29)], "Hilf meinem Unglauben",
    "Der Vater erzählt: Seit der Kindheit. Wenn du etwas kannst, hilf uns! Jesus: Alles ist möglich dem, der glaubt. Der Vater schreit: Ich glaube; hilf meinem Unglauben! Jesus heilt den Jungen.",
    focus="Achte auf den Satz des Vaters in Vers 24.",
    quiz=[
        who("Ich glaube; hilf meinem Unglauben", M(9, 24), ["Der Vater des Jungen", "Petrus", "Der Junge", "Ein Schriftgelehrter"],
            "V. 24: Glaube und Zweifel in einem Satz – und Jesus hilft trotzdem."),
        tf("Jesus wartet mit der Heilung, bis der Vater keine Zweifel mehr hat.", False, 25, "Lies Vers 24–25.",
           "V. 24–25: Der Vater gesteht seinen Unglauben – und Jesus heilt sofort. Ein schwacher Glaube reicht."),
    ],
    explain=[
        E("Was ist mit „Gebet und Fasten“?", "V. 29: Diese Art kann nur durch Gebet ausfahren. „Und Fasten“ fehlt in vielen alten Handschriften – deshalb steht es in manchen Bibeln in Klammern. Gemeint ist: Nicht Technik, sondern die Verbindung zu Gott ist entscheidend."),
    ],
    memory_verse=MV(M(9, 24), "Ich glaube; hilf meinem Unglauben!"),
    prayer={"ref": M(9, 24), "source": "Markus 9,24 – das Gebet des Vaters"},
    teaser="Jesus kündigt sein Leiden an. Die Jünger reden auf dem Weg über etwas ganz anderes.")

sec("wer", [M(9, 30, 37)], "Wer ist der Größte?",
    "Jesus kündigt zum zweiten Mal Tod und Auferstehung an. Die Jünger verstehen es nicht – und streiten unterwegs, wer der Größte ist. Jesus stellt ein Kind in ihre Mitte: Wer der Erste sein will, sei der Letzte und Diener aller.",
    place="kapernaum",
    quiz=[
        choice("Worüber haben die Jünger unterwegs gesprochen?", ["Wer von ihnen der Größte ist", "Über Jesu Leiden", "Über das Essen", "Über die Römer"], 34, "Vers 34.",
               "V. 34: Während Jesus vom Leiden spricht, geht es ihnen um Rang – deshalb schweigen sie verlegen."),
        error("Jesus sagt: Wenn jemand der erste sein will, so soll er der letzte von allen und aller [Herr] sein.", "Diener", 35,
              "V. 35: Diener aller – Größe auf den Kopf gestellt."),
    ],
    explain=[
        E("Warum ein Kind?", "Kinder hatten damals keine Rechte und keinen Status. Wer ein Kind aufnimmt, bekommt nichts zurück. Genau so, sagt Jesus, nimmt man ihn und Gott auf (V. 37)."),
    ],
    try_="Achte heute auf eine Person, die leicht übersehen wird – und schenk ihr Aufmerksamkeit.",
    teaser="Jemand treibt in Jesu Namen Dämonen aus – ohne zu den Jüngern zu gehören. Darf er das?")

sec("wer", [M(9, 38, 50)], "Salz und Frieden",
    "Johannes will einen fremden Exorzisten stoppen. Jesus: Wer nicht gegen uns ist, ist für uns. Dann mahnt er drastisch: Lieber Hand, Fuß oder Auge verlieren, als andere oder sich selbst zu Fall zu bringen. Habt Salz in euch und haltet Frieden untereinander.",
    quiz=[
        choice("Was sagt Jesus über den Mann, der nicht zu den Jüngern gehört?", ["Wer nicht gegen uns ist, ist für uns", "Er soll sofort aufhören", "Er muss sich erst taufen lassen", "Er ist ein falscher Prophet"], 40, "Vers 40.",
               "V. 40: Jesus ist großzügiger als seine Jünger."),
        tf("Ein Becher Wasser in Jesu Namen bleibt nicht unbelohnt.", True, 41, "Lies Vers 41.",
           "V. 41: Selbst die kleinste Hilfe ist vor Gott nicht vergessen."),
    ],
    explain=[
        E("Soll man sich wirklich die Hand abhauen?", "Nein, das ist bewusste Übertreibung – ein orientalisches Stilmittel. Gemeint ist: Nimm ernst, was dich oder andere von Gott wegbringt, und trenne dich davon, auch wenn es weh tut."),
        E("Was bedeutet „Salz“?", "Salz würzt und konserviert. Jesu Jünger sollen etwas Wertvolles in sich tragen – und es zeigt sich darin, dass sie Frieden halten (V. 50)."),
    ],
    memory_verse=MV(M(9, 50), "Habt Salz in euch selbst, und seid in Frieden untereinander."),
    teaser="Auf dem Weg nach Süden stellen Pharisäer eine Fangfrage über die Ehe.")

# ───────────────────────── 6 · Auf dem Weg nach Jerusalem ─────────────────────────
sec("weg", [M(10, 1, 12)], "Was Gott verbunden hat",
    "Pharisäer fragen: Darf ein Mann seine Frau entlassen? Mose habe es erlaubt. Jesus: Wegen eurer Herzenshärte. Von Anfang an schuf Gott Mann und Frau – was Gott verbunden hat, soll der Mensch nicht trennen.",
    quiz=[
        choice("Warum hat Mose laut Jesus den Scheidebrief erlaubt?", ["Wegen der Hartherzigkeit der Menschen", "Weil Gott es so wollte", "Weil die Ehe unwichtig war", "Wegen des Krieges"], 5, "Vers 5.",
               "V. 5: Ein Zugeständnis an die Wirklichkeit, nicht Gottes ursprüngliche Absicht."),
        choice("Auf welchen Text greift Jesus zurück?", ["Auf den Anfang der Schöpfung", "Auf die Zehn Gebote", "Auf die Psalmen Davids", "Auf das Buch Jona"], 6, "Lies Vers 6–8.",
               "V. 6–8: 1. Mose 1,27 und 2,24 – Gottes ursprüngliche Absicht."),
    ],
    explain=[
        E("Wie gehen die Kirchen mit Scheidung um?", "Die katholische Kirche hält eine gültig geschlossene sakramentale Ehe für unauflöslich; eine Wiederheirat ist kirchlich nur nach einer Annullierung möglich. Orthodoxe Kirchen erlauben in Ausnahmen eine zweite Ehe als Zugeständnis. Evangelische und viele Freikirchen sehen die Ehe als lebenslang gedacht, ermöglichen aber Scheidung und Wiederheirat als Weg in zerbrochenen Situationen. Allen ist wichtig: Gott meint die Ehe auf Dauer – und Gottes Gnade gilt auch nach dem Scheitern."),
        E("Warum fragen sie das?", "Die Frage war unter jüdischen Lehrern umstritten: Manche erlaubten Scheidung aus fast jedem Grund, andere nur bei Ehebruch. Außerdem war Herodes Antipas geschieden und wieder verheiratet – die Frage war politisch heikel (vgl. 6,17–18)."),
    ],
    teaser="Die Jünger wollen Kinder fernhalten. Jesus wird darüber richtig ärgerlich.")

sec("weg", [M(10, 13, 16)], "Lasst die Kinder zu mir kommen",
    "Leute bringen Kinder zu Jesus, die Jünger wollen sie abweisen. Jesus wird unwillig: Lasst die Kinder zu mir kommen, ihnen gehört das Reich Gottes. Er nimmt sie in die Arme und segnet sie.",
    quiz=[
        choice("Wie reagiert Jesus auf die Jünger?", ["Er wird unwillig", "Er lobt sie", "Er schweigt", "Er schickt die Kinder weg"], 14, "Vers 14.",
               "V. 14: Er ist empört – eines der wenigen Male, dass Markus Jesu Ärger über die Jünger erwähnt."),
        tf("Jesus segnet die Kinder nur mit Worten aus der Ferne.", False, 16, "Lies Vers 16.",
           "V. 16: Er nimmt sie in die Arme, legt die Hände auf und segnet sie."),
    ],
    explain=[
        E("Was heißt, das Reich „wie ein Kind“ aufnehmen?", "Kinder können sich nichts verdienen – sie empfangen. So, sagt Jesus, empfängt man Gottes Reich: als Geschenk, nicht als Leistung."),
        E("Hat das etwas mit der Kindertaufe zu tun?", "Kirchen, die Säuglinge taufen, berufen sich oft auch auf diesen Text: Kinder gehören schon jetzt zu Gottes Reich. Kirchen mit Glaubenstaufe segnen Kinder stattdessen in einem Gottesdienst – ebenfalls mit Bezug auf diese Stelle."),
    ],
    teaser="Ein Mann hat alle Gebote gehalten. Jesus sieht ihn an, liebt ihn – und sagt ihm, was fehlt.")

sec("weg", [M(10, 17, 27)], "Der reiche Mann",
    "Ein Mann fragt: Was muss ich tun, um das ewige Leben zu erben? Er hat alle Gebote gehalten. Jesus sieht ihn an und liebt ihn: Eins fehlt dir – verkauf alles, gib es den Armen und folge mir. Traurig geht er weg.",
    focus="Achte darauf, was Jesus fühlt, bevor er die schwere Forderung ausspricht.",
    quiz=[
        choice("Was tut Jesus, bevor er sagt, was dem Mann fehlt?", ["Er sieht ihn an und liebt ihn", "Er tadelt ihn", "Er fragt die Jünger", "Er prüft sein Vermögen"], 21, "Vers 21.",
               "V. 21: Die Forderung kommt aus Liebe, nicht aus Härte."),
        choice("Was sagt Jesus über das Kamel?", ["Es geht leichter durch ein Nadelöhr, als ein Reicher ins Reich Gottes", "Es trägt die Lasten der Armen", "Es ist ein Bild für Geduld", "Es gehört dem Tempel"], 25, "Vers 25.",
               "V. 25: Ein unmögliches Bild – und Jesus fügt hinzu: Bei Gott ist alles möglich (V. 27)."),
    ],
    explain=[
        E("Gab es ein „Nadelöhr-Tor“ in Jerusalem?", "Diese oft erzählte Erklärung ist nicht belegt. Jesus benutzt ein absichtlich absurdes Bild: Aus eigener Kraft schafft es keiner – nur Gott macht es möglich (V. 27)."),
        E("Müssen alle Christen ihren Besitz verkaufen?", "Jesus sagt das zu diesem Mann, dessen Besitz ihn festhielt. Mönchsorden haben es wörtlich genommen; die meisten Christen verstehen es als Frage an sich selbst: Was hält mich davon ab, Jesus ganz zu folgen?"),
    ],
    teaser="Petrus sagt: Wir haben alles verlassen. Was haben wir davon?")

sec("weg", [M(10, 28, 31)], "Hundertfach",
    "Petrus: Wir haben alles verlassen und sind dir gefolgt. Jesus verspricht: Niemand verlässt etwas um meinetwillen, der es nicht hundertfach zurückbekommt – mit Verfolgungen – und in der kommenden Welt ewiges Leben.",
    quiz=[
        tf("Jesus verspricht seinen Nachfolgern ein Leben ohne Schwierigkeiten.", False, 30, "Lies Vers 30 genau.",
           "V. 30: hundertfach – „mit Verfolgungen“. Ehrlich, nicht naiv."),
        error("Jesus sagt: Viele Erste werden [Erste] und Letzte Letzte sein.", "Letzte", 31,
              "V. 31: Viele Erste werden Letzte und Letzte Erste sein – Gottes Maßstäbe sind andere."),
    ],
    explain=[
        E("Wie bekommt man „hundertfach Häuser und Brüder“?", "Viele verstehen es so: In der Gemeinschaft der Jünger findet man eine neue, große Familie – offene Häuser, Geschwister, Mütter. Die frühen Gemeinden haben das erlebt (Apg 2,44–46)."),
    ],
    teaser="Jesus geht voran nach Jerusalem. Die Jünger folgen – und haben Angst.")

sec("weg", [M(10, 32, 34)], "Die dritte Ankündigung",
    "Auf dem Weg hinauf nach Jerusalem geht Jesus voran; die Jünger erschrecken und fürchten sich. Zum dritten Mal kündigt er an: Ich werde ausgeliefert, verspottet, gegeißelt, getötet – und nach drei Tagen auferstehen.",
    quiz=[
        tf("Jesus geht den Jüngern auf dem Weg nach Jerusalem voraus.", True, 32, "Lies Vers 32.",
           "V. 32: Er geht vorne – entschlossen, obwohl er weiß, was kommt."),
        order("Was wird dem Menschensohn widerfahren? In der Reihenfolge des Textes:", ["Er wird den Hohenpriestern überliefert", "Er wird zum Tod verurteilt", "Er wird verspottet und gegeißelt", "Er wird nach drei Tagen auferstehen"], "V. 33–34.", "Lies Vers 33–34."),
    ],
    explain=[
        E("Warum dreimal?", "Markus erzählt drei Leidensankündigungen (8,31; 9,31; 10,33–34). Jedes Mal reagieren die Jünger mit Unverständnis – und jedes Mal folgt eine Lehre über Dienen und Nachfolge."),
    ],
    teaser="Zwei Jünger wollen die besten Plätze. Die anderen sind empört.")

sec("weg", [M(10, 35, 45)], "Dienen statt herrschen",
    "Jakobus und Johannes wollen rechts und links von Jesus sitzen. Die anderen ärgern sich. Jesus: Bei euch soll es nicht so sein wie bei den Mächtigen. Wer groß sein will, soll dienen – denn der Menschensohn ist gekommen, um zu dienen.",
    quiz=[
        who("Wir können es", M(10, 39), ["Jakobus und Johannes", "Petrus und Andreas", "Die Zehn", "Jesus"],
            "V. 39: Sie überschätzen sich – und doch werden sie später tatsächlich für Jesus leiden."),
        choice("Wofür ist der Menschensohn gekommen?", ["Um zu dienen und sein Leben zu geben", "Um zu herrschen", "Um Rom zu stürzen", "Um den Tempel neu zu bauen"], 45, "Vers 45.",
               "V. 45: einer der wichtigsten Verse des Markusevangeliums."),
    ],
    explain=[
        E("Was ist der „Kelch“?", "Im Alten Testament ein Bild für das Schicksal, oft für Gottes Gericht (Jes 51,17). Jesus meint sein Leiden – in Gethsemane bittet er, dieser Kelch möge an ihm vorübergehen (14,36)."),
    ],
    memory_verse=MV(M(10, 45), "nicht gekommen, um bedient zu werden, sondern um zu dienen"),
    teaser="Ein blinder Bettler schreit – und je mehr man ihn zum Schweigen bringt, desto lauter wird er.")

sec("weg", [M(10, 46, 52)], "Bartimäus",
    "Bei Jericho schreit der blinde Bettler Bartimäus: Sohn Davids, erbarme dich meiner! Viele wollen ihn zum Schweigen bringen; er schreit lauter. Jesus ruft ihn: Was willst du? – Dass ich sehen kann. Er wird sehend und folgt Jesus nach.",
    place="jericho",
    focus="Achte darauf, was Bartimäus mit seinem Mantel macht.",
    quiz=[
        who("Sohn Davids, Jesus, erbarme dich meiner", M(10, 47), ["Bartimäus", "Ein Jünger", "Die Menge", "Ein Pharisäer"],
            "V. 47: Er nennt Jesus „Sohn Davids“ – den Messias-Titel. Der Blinde sieht, wer Jesus ist."),
        choice("Was tut Bartimäus, als Jesus ihn ruft?", ["Er wirft seinen Mantel ab und springt auf", "Er bleibt sitzen und wartet", "Er läuft weg", "Er bittet um Geld"], 50, "Vers 50.",
               "V. 50: Der Mantel war vielleicht sein einziger Besitz und Schutz – er lässt ihn zurück."),
    ],
    explain=[
        E("Warum fragt Jesus „Was willst du?“", "Es ist offensichtlich, was ein Blinder will. Doch Jesus nimmt ihn als Person ernst und lässt ihn seinen Wunsch selbst aussprechen. Dieselbe Frage hatte er kurz vorher Jakobus und Johannes gestellt (10,36) – mit ganz anderer Antwort."),
        E("Warum steht diese Geschichte hier?", "Sie schließt den Weg nach Jerusalem ab, der mit der Heilung eines Blinden begann (8,22–26). Bartimäus ist am Ende das Vorbild: Er sieht und folgt Jesus „auf dem Weg“ – nach Jerusalem."),
    ],
    prayer={"text": "Herr Jesus Christus, Sohn Gottes, erbarme dich meiner.", "source": "Das „Jesusgebet“ der Ostkirche, das auf den Ruf des Bartimäus zurückgeht"},
    teaser="Jesus reitet in Jerusalem ein – nicht auf einem Pferd.")

# ───────────────────────── 7 · In Jerusalem ─────────────────────────
sec("jerusalem", [M(11, 1, 11)], "Der Einzug",
    "Jesus lässt ein junges Fohlen holen, auf dem noch niemand saß, und reitet nach Jerusalem. Menschen legen Kleider und Zweige auf den Weg und rufen: Hosanna! Gepriesen sei, der im Namen des Herrn kommt!",
    place="jerusalem",
    quiz=[
        choice("Was sollen die Jünger sagen, wenn jemand fragt, warum sie das Fohlen losbinden?", ["Der Herr braucht es", "Wir zahlen später", "Jesus ist König", "Es gehört uns"], 3, "Vers 3.",
               "V. 3: Der Herr braucht es – und alles geht so, wie Jesus es gesagt hat."),
        choice("Was rufen die Menschen?", ["Hosanna! Gepriesen sei, der im Namen des Herrn kommt!", "Kreuzige ihn!", "Heil dem Kaiser!", "Der Herr ist auferstanden!"], 9, "Vers 9.",
               "V. 9: Worte aus Psalm 118,25–26, einem Festpsalm."),
    ],
    explain=[
        E("Warum auf einem Fohlen?", "Der Prophet Sacharja hatte angekündigt: Dein König kommt zu dir, sanftmütig, auf einem Esel (Sach 9,9). Ein Kriegsherr ritt auf einem Pferd – Jesus kommt als Friedenskönig."),
        E("Was heißt „Hosanna“?", "Hebräisch „Hilf doch!“ oder „Rette doch!“ – ursprünglich ein Gebetsruf, später ein Jubelruf."),
    ],
    cards=["tempel"],
    fact="Der Palmsonntag, eine Woche vor Ostern, erinnert an diesen Einzug. Die „Palmzweige“ stammen allerdings aus Johannes 12,13 – Markus spricht nur von „Zweigen“.",
    teaser="Ein Baum ohne Früchte und ein Tempel voller Händler – zwei Geschichten, die zusammengehören.")

sec("jerusalem", [M(11, 12, 19)], "Feigenbaum und Tempel",
    "Jesus findet an einem Feigenbaum keine Früchte und verflucht ihn. Im Tempel stößt er die Tische der Geldwechsler um: Mein Haus soll ein Bethaus für alle Völker sein – ihr habt eine Räuberhöhle daraus gemacht.",
    place="jerusalem",
    quiz=[
        tf("Laut Markus war gerade keine Zeit für Feigen.", True, 13, "Lies Vers 13 genau.",
           "V. 13: Ein seltsames Detail – es zeigt: Es geht um ein Zeichen, nicht um Jesu Hunger."),
        error("Jesus sagt: Mein Haus wird ein Bethaus genannt werden für alle [Priester].", "Nationen", 17,
              "V. 17: für alle Nationen (Jes 56,7). Der Handel fand wohl im Vorhof der Nichtjuden statt – ihr Gebetsort wurde zum Markt."),
    ],
    explain=[
        E("Warum verflucht Jesus einen Baum?", "Markus verschachtelt die Feigenbaum-Geschichte mit der Tempelreinigung. Der Baum hat Blätter, aber keine Frucht – wie ein Tempelbetrieb, der prächtig aussieht, aber nicht bringt, wofür er da ist. Es ist eine Zeichenhandlung wie bei den Propheten."),
        E("Warum gab es Händler im Tempel?", "Pilger brauchten Opfertiere und mussten Geld in die Tempelwährung umtauschen. Das war legal – aber Jesus kritisiert, dass das Haus des Gebets zum Geschäft geworden ist."),
    ],
    teaser="Der Feigenbaum ist verdorrt. Jesus redet über Berge, die ins Meer fallen – und übers Vergeben.")

sec("jerusalem", [M(11, 20, 26)], "Glaube und Vergebung",
    "Am nächsten Morgen ist der Feigenbaum verdorrt. Jesus sagt: Habt Glauben an Gott! Wer glaubt, kann Berge versetzen. Und wenn ihr betet, vergebt – damit auch euer Vater euch vergibt.",
    quiz=[
        choice("Was gehört laut Jesus zum Beten dazu?", ["Vergeben, wenn man etwas gegen jemanden hat", "Lange Worte", "Ein Opfer im Tempel", "Fasten"], 25, "Vers 25.",
               "V. 25: Gebet und Vergebung gehören zusammen."),
        tf("Jesus sagt, ein Berg könne ins Meer geworfen werden.", True, 23, "Lies Vers 23.",
           "V. 23: ein bewusst starkes Bild – manche denken dabei an den Tempelberg, vor dem Jesus gerade steht."),
    ],
    explain=[
        E("Bekomme ich alles, worum ich bete?", "Jesus ermutigt zu vertrauensvollem Gebet (V. 24). Er selbst betet in Gethsemane um etwas, das nicht geschieht – und fügt hinzu: Nicht was ich will, sondern was du willst (14,36). Vertrauen heißt nicht, Gott zu steuern."),
        E("Warum fehlt Vers 26 manchmal?", "Er steht nicht in den ältesten Handschriften und ist vermutlich aus Matthäus 6,15 übernommen. Manche Bibeln setzen ihn deshalb in Klammern oder lassen ihn weg."),
    ],
    try_="Gibt es jemanden, dem du etwas nachträgst? Du musst heute nichts lösen – bring den Namen nur einmal vor Gott.",
    teaser="Die Mächtigen fragen nach Jesu Vollmacht. Er antwortet mit einer Gegenfrage, die sie in die Falle lockt.")

sec("jerusalem", [M(11, 27, 33)], "Mit welchem Recht?",
    "Hohepriester, Schriftgelehrte und Älteste fragen: Mit welchem Recht tust du das? Jesus fragt zurück: War die Taufe des Johannes vom Himmel oder von Menschen? Sie trauen sich keine Antwort – also antwortet auch Jesus nicht.",
    place="jerusalem",
    quiz=[
        choice("Was antworten die Gegner auf Jesu Gegenfrage?", ["Wir wissen es nicht", "Vom Himmel", "Von Menschen", "Sie schweigen und gehen"], 33, "Vers 33.",
               "V. 33: Jede ehrliche Antwort hätte ihnen geschadet – also weichen sie aus."),
        tf("Die Gegner fürchten das Volk, das Johannes für einen Propheten hält.", True, 32, "Lies Vers 32.",
           "V. 32: Sie denken taktisch, nicht ehrlich."),
    ],
    explain=[
        E("Warum diese Gegenfrage?", "Wer Johannes als Gottes Propheten anerkennt, müsste auch auf ihn hören – und Johannes hatte auf Jesus hingewiesen. Die Frage nach Johannes beantwortet also die Frage nach Jesu Vollmacht."),
    ],
    cards=["hoher-rat"],
    teaser="Jesus erzählt von Weingärtnern, die sogar den Sohn des Besitzers töten. Die Zuhörer merken, wer gemeint ist.")

sec("jerusalem", [M(12, 1, 12)], "Die Weingärtner",
    "Ein Mann verpachtet seinen Weinberg. Die Pächter schlagen und töten seine Knechte, schließlich auch seinen geliebten Sohn. Jesus zitiert: Der Stein, den die Bauleute verworfen haben, ist zum Eckstein geworden.",
    place="jerusalem",
    quiz=[
        choice("Wen schickt der Besitzer zuletzt?", ["Seinen geliebten Sohn", "Einen Soldaten", "Seinen besten Knecht", "Niemanden mehr"], 6, "Vers 6.",
               "V. 6: den geliebten Sohn – wie die Stimme bei Taufe und Verklärung Jesus nennt."),
        tf("Die Gegner merken, dass das Gleichnis gegen sie gerichtet ist.", True, 12, "Lies Vers 12.",
           "V. 12: Sie verstehen genau – und wollen ihn festnehmen."),
    ],
    explain=[
        E("Wer ist wer im Gleichnis?", "Der Weinberg erinnert an Jesaja 5, wo Israel Gottes Weinberg ist. Die Pächter stehen für die religiöse Führung, die Knechte für die Propheten, der Sohn für Jesus. Wichtig: Gemeint ist nicht „die Juden“ insgesamt – Jesus und seine Jünger waren selbst Juden."),
        E("Was ist ein „Eckstein“?", "Der wichtigste Stein eines Gebäudes, an dem sich alles ausrichtet (Ps 118,22). Der Verworfene wird zum Fundament – ein Hinweis auf Kreuz und Auferstehung."),
    ],
    teaser="Eine Fangfrage über Steuern – egal wie Jesus antwortet, er scheint zu verlieren.")

sec("jerusalem", [M(12, 13, 17)], "Kaiser und Gott",
    "Pharisäer und Herodianer fragen listig: Darf man dem Kaiser Steuern zahlen? Jesus lässt sich einen Denar zeigen: Wessen Bild ist das? Des Kaisers. Also gebt dem Kaiser, was des Kaisers ist, und Gott, was Gottes ist.",
    place="jerusalem",
    quiz=[
        choice("Was lässt sich Jesus bringen?", ["Einen Denar", "Eine Schriftrolle", "Ein Schwert", "Einen Steuerbescheid"], 15, "Vers 15.",
               "V. 15: Eine römische Silbermünze mit dem Bild des Kaisers."),
        who("So gebt dem Kaiser, was des Kaisers ist, und Gott, was Gottes ist", M(12, 17), ["Jesus", "Ein Pharisäer", "Ein Herodianer", "Pilatus"],
            "V. 17: Eine Antwort, die beide Seiten sprachlos macht."),
    ],
    explain=[
        E("Warum war die Frage eine Falle?", "Sagt Jesus „Ja“, verliert er das Volk, das die römischen Steuern hasste. Sagt er „Nein“, können ihn die Herodianer bei den Römern als Aufrührer anzeigen."),
        E("Was gehört Gott?", "Auf der Münze ist das Bild des Kaisers. Der Mensch aber trägt Gottes Bild (1. Mose 1,27). Viele verstehen Jesu Antwort deshalb so: Gib dem Staat sein Geld – aber dich selbst gib Gott."),
    ],
    teaser="Die Sadduzäer erfinden eine absurde Geschichte, um die Auferstehung lächerlich zu machen.")

sec("jerusalem", [M(12, 18, 27)], "Die Frage nach der Auferstehung",
    "Die Sadduzäer, die nicht an die Auferstehung glauben, erzählen von einer Frau, die nacheinander sieben Brüder heiratete: Wessen Frau ist sie in der Auferstehung? Jesus: Ihr irrt. Gott ist nicht ein Gott der Toten, sondern der Lebenden.",
    place="jerusalem",
    quiz=[
        estimate("Wie viele Brüder heiraten in der Geschichte nacheinander dieselbe Frau?", 1, 12, 7, "Brüder", "V. 20–22: sieben – eine bewusst übertriebene Geschichte.", 20, "Lies Vers 20."),
        choice("Was sagt Jesus über die Auferstandenen?", ["Sie heiraten nicht, sondern sind wie Engel", "Sie leben wie vorher", "Sie werden zu Sternen", "Sie schlafen bis zum Ende der Welt"], 25, "Vers 25.",
               "V. 25: Das neue Leben ist kein bloßes Weiter-so des alten."),
    ],
    explain=[
        E("Warum zitiert Jesus den Dornbusch?", "Die Sadduzäer erkannten vor allem die fünf Bücher Mose an. Jesus antwortet aus genau diesen Büchern: Gott nennt sich der Gott Abrahams, Isaaks und Jakobs (2. Mose 3,6) – lange nach deren Tod. Also leben sie für Gott."),
    ],
    cards=["sadduzaeer"],
    memory_verse=MV(M(12, 27), "Er ist nicht der Gott der Toten, sondern der Lebendigen."),
    teaser="Endlich eine ehrliche Frage: Welches Gebot ist das wichtigste?")

sec("jerusalem", [M(12, 28, 34)], "Das höchste Gebot",
    "Ein Schriftgelehrter fragt ehrlich nach dem ersten Gebot. Jesus: Höre, Israel – liebe Gott mit allem, was du hast. Und das zweite: Liebe deinen Nächsten wie dich selbst. Der Schriftgelehrte stimmt zu – und Jesus sagt: Du bist nicht fern vom Reich Gottes.",
    place="jerusalem",
    focus="Achte darauf, wie Jesus diesem Schriftgelehrten begegnet.",
    quiz=[
        choice("Welches ist laut Jesus das zweite Gebot?", ["Du sollst deinen Nächsten lieben wie dich selbst", "Du sollst nicht töten", "Ehre Vater und Mutter", "Halte den Sabbat"], 31, "Vers 31.",
               "V. 31: aus 3. Mose 19,18. Gottesliebe und Nächstenliebe gehören zusammen."),
        tf("Jesus lobt den Schriftgelehrten.", True, 34, "Lies Vers 34.",
           "V. 34: Er sei nicht fern vom Reich Gottes. Nicht alle Schriftgelehrten sind Gegner."),
    ],
    explain=[
        E("Woher stammen die beiden Gebote?", "Das erste ist das Schma Israel aus 5. Mose 6,4–5, das fromme Juden täglich beten. Das zweite stammt aus 3. Mose 19,18. Jesus verbindet beide zu einer Einheit."),
    ],
    memory_verse=MV(M(12, 31), "Du sollst deinen Nächsten lieben wie dich selbst"),
    try_="Was wäre heute eine kleine, konkrete Art, deinen Nächsten zu lieben? Mach es.",
    teaser="Jetzt stellt Jesus eine Frage, die niemand beantworten kann – und warnt vor frommer Show.")

sec("jerusalem", [M(12, 35, 40)], "Davids Sohn und die Schriftgelehrten",
    "Jesus fragt: Wie kann der Christus Davids Sohn sein, wenn David ihn „Herr“ nennt? Dann warnt er vor Schriftgelehrten, die Ehre lieben, lange Gebete zur Schau stellen und dabei Witwen ausnehmen.",
    place="jerusalem",
    quiz=[
        choice("Wovor warnt Jesus bei manchen Schriftgelehrten?", ["Ehrsucht und Ausbeutung von Witwen", "Zu viel Fasten", "Zu wenig Wissen", "Freundschaft mit Römern"], 40, "Lies Vers 38–40.",
               "V. 38–40: Fromme Fassade, aber Rücksichtslosigkeit gegenüber den Schwächsten."),
        tf("Die Menge hört Jesus gern zu.", True, 37, "Lies Vers 37.", "V. 37: Die große Menge hört ihn gern."),
    ],
    explain=[
        E("Was will Jesus mit Psalm 110 zeigen?", "Der Messias ist mehr als ein Nachkomme Davids – David selbst nennt ihn „Herr“. Jesus deutet an, dass der Messias zugleich Davids Sohn und Davids Herr ist. Psalm 110 ist der im Neuen Testament am häufigsten zitierte Psalm."),
    ],
    teaser="Viele Reiche geben viel. Eine arme Witwe gibt fast nichts – und Jesus sagt: Sie hat mehr gegeben als alle.")

sec("jerusalem", [M(12, 41, 44)], "Die arme Witwe",
    "Jesus beobachtet, wie Menschen in den Opferkasten des Tempels einlegen. Viele Reiche geben viel. Eine arme Witwe legt zwei kleine Münzen hinein. Jesus: Sie hat mehr gegeben als alle – alles, was sie zum Leben hatte.",
    place="jerusalem",
    quiz=[
        estimate("Wie viele Münzen legt die Witwe ein?", 1, 10, 2, "Münzen", "V. 42: zwei Scherflein – die kleinste Münze, die es gab.", 42, "Vers 42."),
        choice("Warum hat sie laut Jesus mehr gegeben als alle?", ["Sie gab alles, was sie zum Leben hatte", "Ihre Münzen waren aus Gold", "Sie gab heimlich", "Sie gab zuerst"], 44, "Vers 44.",
               "V. 44: Die anderen gaben vom Überfluss, sie aus ihrem Mangel."),
    ],
    explain=[
        E("Lobt Jesus sie – oder klagt er an?", "Die meisten lesen es als Lob ihrer Hingabe. Manche Ausleger verbinden es mit dem Vers davor (12,40): Ein System, das Witwen ihr Letztes nimmt, wird kritisiert. Beides schließt sich nicht aus."),
        E("Was ist ein „Scherflein“?", "Die kleinste Kupfermünze (griechisch Lepton). Markus rechnet für römische Leser um.", "elbbk"),
    ],
    teaser="Ein Jünger bestaunt die gewaltigen Steine des Tempels. Jesus sagt: Kein Stein wird auf dem anderen bleiben.")

sec("jerusalem", [M(13, 1, 13)], "Anfänge der Wehen",
    "Jesus kündigt die Zerstörung des Tempels an. Auf dem Ölberg fragen ihn vier Jünger: Wann? Jesus warnt: Lasst euch nicht verführen. Kriege, Erdbeben, Hungersnöte sind erst der Anfang. Ihr werdet verfolgt – wer bis ans Ende durchhält, wird gerettet.",
    place="oelberg",
    quiz=[
        choice("Womit beginnt Jesus seine Antwort?", ["Seht zu, dass euch niemand verführe", "Es wird morgen geschehen", "Betet für den Kaiser", "Verlasst sofort die Stadt"], 5, "Vers 5.",
               "V. 5: Seine erste Sorge ist nicht der Zeitplan, sondern dass die Jünger nicht in die Irre gehen."),
        tf("Laut Jesus sind Kriege und Erdbeben schon das Ende.", False, 7, "Lies Vers 7–8.",
           "V. 7–8: Noch nicht das Ende – erst die Anfänge der Wehen."),
    ],
    explain=[
        E("Ist das geschehen?", "Im Jahr 70 n. Chr. zerstörten römische Truppen Jerusalem und den Tempel – nur Teile der Umfassungsmauer blieben stehen, etwa die Westmauer („Klagemauer“)."),
        E("Wie lesen Christen Markus 13?", "Die Rede verbindet die nahe Zerstörung Jerusalems mit dem fernen Ende der Welt. Manche beziehen fast alles auf das Jahr 70, andere vieles auf die Zukunft; viele sehen beide Ebenen ineinander verwoben. Allen gemeinsam: Jesus will Mut machen zum Durchhalten, nicht Angst."),
    ],
    teaser="Jesus spricht von einem „Gräuel der Verwüstung“ – und gibt sehr praktische Ratschläge zur Flucht.")

sec("jerusalem", [M(13, 14, 23)], "Flieht auf die Berge",
    "Wenn der „Gräuel der Verwüstung“ steht, wo er nicht hingehört, sollen die Menschen in Judäa sofort fliehen. Es kommt große Not. Falsche Messiasse werden auftreten. Jesus: Ich habe euch alles vorhergesagt.",
    quiz=[
        choice("Wozu rät Jesus, wenn der Gräuel der Verwüstung erscheint?", ["Sofort auf die Berge zu fliehen", "Im Tempel zu bleiben", "Zu kämpfen", "Abzuwarten"], 14, "Vers 14.",
               "V. 14–16: Nicht zögern, nichts holen – sofort fliehen."),
        tf("Jesus warnt vor falschen Christussen, die Zeichen tun.", True, 22, "Lies Vers 22.",
           "V. 22: Wunder allein beweisen nichts."),
    ],
    explain=[
        E("Was ist der „Gräuel der Verwüstung“?", "Ein Ausdruck aus Daniel (9,27; 11,31). Er erinnerte an 167 v. Chr., als ein syrischer König im Tempel einen heidnischen Altar errichtete. Jesus kündigt eine ähnliche Entweihung an. Nach alter Überlieferung flohen die Christen vor der Zerstörung 70 n. Chr. nach Pella östlich des Jordan."),
    ],
    teaser="Sonne und Mond verdunkeln sich – und dann kommt der Menschensohn in den Wolken.")

sec("jerusalem", [M(13, 24, 31)], "Das Kommen des Menschensohns",
    "Nach der Not werden Sonne und Mond dunkel. Dann kommt der Menschensohn in den Wolken und sammelt seine Auserwählten. Lernt vom Feigenbaum. Himmel und Erde werden vergehen, meine Worte aber nicht.",
    quiz=[
        choice("Was lehrt der Feigenbaum?", ["Wenn er austreibt, ist der Sommer nahe", "Dass Gott keine Frucht findet", "Dass man geduldig sein muss", "Dass alles vergeht"], 28, "Vers 28.",
               "V. 28–29: An den Zeichen erkennt man, dass etwas nahe ist."),
        error("Jesus sagt: Der Himmel und die Erde werden vergehen, meine [Wunder] aber sollen nicht vergehen.", "Worte", 31,
              "V. 31: Seine Worte bleiben, auch wenn alles andere vergeht."),
    ],
    explain=[
        E("Was bedeutet „Dieses Geschlecht wird nicht vergehen“?", "V. 30 ist schwierig. Viele beziehen ihn auf die Zerstörung Jerusalems, die noch zu Lebzeiten der Zuhörer geschah. Andere übersetzen „Geschlecht“ als „Menschenart“ oder „Volk“. Einfache Antworten gibt es hier nicht."),
    ],
    memory_verse=MV(M(13, 31), "Der Himmel und die Erde werden vergehen, meine Worte aber sollen nicht vergehen."),
    teaser="Wann ist es soweit? Jesus gibt eine überraschend demütige Antwort.")

sec("jerusalem", [M(13, 32, 37)], "Wacht!",
    "Den Tag und die Stunde kennt niemand – nicht die Engel, nicht einmal der Sohn, nur der Vater. Darum: Seid wachsam, wie Knechte, deren Herr jederzeit heimkommen kann. Was ich euch sage, sage ich allen: Wacht!",
    quiz=[
        choice("Wer kennt den Tag und die Stunde?", ["Nur der Vater", "Die Engel", "Der Sohn", "Die Propheten"], 32, "Vers 32.",
               "V. 32: Nicht einmal der Sohn. Wer heute Termine für das Weltende berechnet, weiß mehr als Jesus selbst beanspruchte."),
        tf("Jesus richtet den Aufruf zum Wachen nur an die vier Jünger.", False, 37, "Lies Vers 37.",
           "V. 37: „Was ich euch sage, sage ich allen“ – also auch dir."),
    ],
    explain=[
        E("Was heißt „wachen“?", "Nicht ängstlich auf Zeichen starren, sondern treu die eigene Aufgabe erfüllen (V. 34) – wie Knechte, die ihr Werk tun, solange der Herr weg ist."),
    ],
    teaser="Zwei Tage vor dem Passa salbt eine Frau Jesus mit einem Vermögen – und erntet Empörung.")

# ───────────────────────── 8 · Die letzte Nacht ─────────────────────────
sec("nacht", [M(14, 1, 11)], "Die Salbung in Bethanien",
    "Die Hohenpriester planen Jesu Tod. In Bethanien gießt eine Frau kostbares Nardenöl über Jesu Kopf. Einige sind empört über die Verschwendung. Jesus: Sie hat mich im Voraus für mein Begräbnis gesalbt. Judas geht zu den Hohenpriestern.",
    place="betanien",
    focus="Achte auf den Gegensatz zwischen der Frau und Judas.",
    quiz=[
        estimate("Für wie viele Denare hätte man das Öl verkaufen können?", 50, 1000, 300, "Denare", "V. 5: mehr als 300 Denare – fast ein Jahreslohn eines Arbeiters.", 5, "Vers 5.", tol=20),
        choice("Was verspricht Jesus der Frau?", ["Man wird überall in der Welt von ihrer Tat erzählen", "Sie wird reich belohnt", "Sie wird eine Jüngerin unter den Zwölf", "Ihre Sünden sind vergeben"], 9, "Vers 9.",
               "V. 9: ein Versprechen, das sich erfüllt – du liest gerade davon."),
    ],
    explain=[
        E("Warum ist die Salbung so bedeutend?", "„Christus“ heißt „der Gesalbte“. Ausgerechnet eine namenlose Frau salbt Jesus – nicht zum König, sondern zum Begräbnis. Sie versteht, was die Jünger nicht verstehen wollen."),
        E("„Die Armen habt ihr allezeit bei euch“?", "Jesus spielt nicht Hilfe für Arme gegen Liebe zu ihm aus. Er zitiert 5. Mose 15,11, wo es weitergeht: Darum öffne deine Hand für den Armen. Jetzt aber ist ein einmaliger Moment."),
    ],
    teaser="Die Jünger sollen einem Mann mit einem Wasserkrug folgen. Beim Essen sagt Jesus: Einer von euch wird mich verraten.")

sec("nacht", [M(14, 12, 21)], "Das Passa",
    "Jesus schickt zwei Jünger in die Stadt: Folgt einem Mann mit einem Wasserkrug. Sie bereiten das Passa in einem großen Obersaal. Beim Essen sagt Jesus: Einer von euch wird mich verraten. Betroffen fragen sie: Doch nicht ich?",
    place="jerusalem",
    quiz=[
        choice("Woran sollen die Jünger den Weg erkennen?", ["An einem Mann, der einen Wasserkrug trägt", "An einem Stern", "An einem weißen Esel", "An einem Engel"], 13, "Vers 13.",
               "V. 13: Wasser tragen war meist Frauenarbeit – ein Mann mit Krug fiel auf."),
        who("Doch nicht ich", M(14, 19), ["Die Jünger, einer nach dem anderen", "Judas allein", "Petrus allein", "Der Hausherr"],
            "V. 19: Keiner zeigt auf den anderen – jeder fragt nach sich selbst."),
    ],
    explain=[
        E("Was ist das Passa?", "Das Fest der Befreiung aus Ägypten. Man aß ein Lamm, ungesäuertes Brot und bittere Kräuter und erzählte die Geschichte des Auszugs (2. Mose 12)."),
        E("Warum diese geheime Vorbereitung?", "Jesus wusste, dass man ihn suchte. Der Ort sollte vielleicht bis zuletzt verborgen bleiben, damit das Mahl ungestört stattfinden konnte."),
    ],
    teaser="Jesus nimmt Brot und Kelch – und gibt ihnen eine neue Bedeutung, die Christen bis heute feiern.")

sec("nacht", [M(14, 22, 26)], "Das Abendmahl",
    "Während des Essens nimmt Jesus Brot, segnet, bricht es: Nehmt, das ist mein Leib. Dann den Kelch: Das ist mein Blut des Bundes, vergossen für viele. Nach einem Lobgesang gehen sie hinaus zum Ölberg.",
    place="jerusalem",
    quiz=[
        tf("Alle Jünger trinken aus dem Kelch.", True, 23, "Lies Vers 23.", "V. 23: Sie tranken alle daraus – auch Judas und Petrus."),
        choice("Was tun sie, bevor sie zum Ölberg gehen?", ["Sie singen einen Lobgesang", "Sie waschen sich die Füße", "Sie beten im Tempel", "Sie schlafen"], 26, "Vers 26.",
               "V. 26: Zum Passa wurden die Hallel-Psalmen gesungen (Ps 113–118)."),
    ],
    explain=[
        E("Wie verstehen das die Kirchen?", "Katholiken: Brot und Wein werden wirklich Leib und Blut Christi (Wandlung). Orthodoxe: wirkliche Gegenwart Christi als Geheimnis. Lutheraner: Christus ist in, mit und unter Brot und Wein gegenwärtig. Reformierte: geistliche Gegenwart. Viele Freikirchen: ein Gedächtnismahl der Erinnerung und Gemeinschaft. Alle feiern es, weil Jesus es so gestiftet hat."),
        E("Warum „Bund“?", "Am Sinai wurde der Bund mit Blut besiegelt (2. Mose 24,8). Jesus deutet seinen Tod als Besiegelung eines Bundes zwischen Gott und den Menschen."),
    ],
    teaser="Petrus schwört: Selbst wenn alle dich verlassen – ich nicht.")

sec("nacht", [M(14, 27, 31)], "„Ich nicht!“",
    "Auf dem Weg sagt Jesus: Ihr werdet alle Anstoß nehmen. Aber nach meiner Auferstehung gehe ich euch voraus nach Galiläa. Petrus: Ich nicht! Jesus: Noch heute Nacht, bevor der Hahn zweimal kräht, wirst du mich dreimal verleugnen.",
    quiz=[
        choice("Was verspricht Jesus nach seiner Auferstehung?", ["Er wird ihnen nach Galiläa vorausgehen", "Er wird im Tempel erscheinen", "Er wird Rom besiegen", "Er wird sofort in den Himmel fahren"], 28, "Vers 28.",
               "V. 28: Schon vor dem Versagen der Jünger steht die Zusage eines Neuanfangs."),
        tf("Nur Petrus behauptet, Jesus niemals zu verleugnen.", False, 31, "Lies Vers 31 bis zum Ende.",
           "V. 31: Alle anderen sagen dasselbe."),
    ],
    explain=[
        E("Was ist mit dem Hirten gemeint?", "Jesus zitiert Sacharja 13,7: Ich werde den Hirten schlagen, und die Schafe werden zerstreut. Er sieht sein Schicksal in der Schrift vorgezeichnet."),
    ],
    teaser="In einem Garten betet Jesus in Todesangst. Seine Freunde schlafen.")

sec("nacht", [M(14, 32, 42)], "Gethsemane",
    "Im Garten Gethsemane ist Jesus zu Tode betrübt. Er betet: Abba, Vater, alles ist dir möglich, nimm diesen Kelch von mir – doch nicht was ich will, sondern was du willst. Dreimal findet er die Jünger schlafend.",
    place="oelberg",
    focus="Achte darauf, wie ehrlich Jesus mit seinem Vater spricht.",
    quiz=[
        estimate("Wie oft kommt Jesus zurück und findet die Jünger schlafend?", 1, 7, 3, "Mal", "V. 37–41: dreimal.", 41, "Lies Vers 37–41."),
        error("Jesus sagt: Der Geist zwar ist willig, das Fleisch aber [stark].", "schwach", 38,
              "V. 38: Der Geist ist willig, das Fleisch schwach – Jesus kennt die Grenzen seiner Freunde."),
    ],
    explain=[
        E("Was heißt „Abba“?", "Aramäisch für „Vater“ – das Wort, mit dem Kinder ihren Vater ansprachen. Jesus betet in seiner tiefsten Angst so vertraut."),
        E("Hatte Jesus wirklich Angst?", "Markus beschönigt nichts: Jesus ist erschüttert und geängstigt (V. 33–34). Für Christen ist das tröstlich: Jesus kennt Angst von innen – und betet trotzdem."),
    ],
    memory_verse=MV(M(14, 36), "Doch nicht, was ich will, sondern was du willst!"),
    prayer={"ref": M(14, 36), "source": "Markus 14,36 – Jesu Gebet in Gethsemane"},
    teaser="Judas kommt mit einer bewaffneten Menge – und begrüßt Jesus mit einem Kuss.")

sec("nacht", [M(14, 43, 52)], "Die Verhaftung",
    "Judas kommt mit einer bewaffneten Menge und küsst Jesus als Erkennungszeichen. Jesus wird festgenommen. Einer schlägt mit dem Schwert zu. Alle Jünger fliehen – ein junger Mann sogar nackt.",
    place="oelberg",
    quiz=[
        choice("Welches Zeichen hat Judas vereinbart?", ["Einen Kuss", "Einen Handschlag", "Einen Zuruf", "Eine Fackel"], 44, "Vers 44.",
               "V. 44–45: Ein Zeichen der Freundschaft wird zum Zeichen des Verrats."),
        tf("Am Ende bleiben die Jünger bei Jesus.", False, 50, "Lies Vers 50.", "V. 50: Es verließen ihn alle und flohen."),
    ],
    explain=[
        E("Wer ist der junge Mann?", "Nur Markus erzählt von ihm (V. 51–52). Eine alte Vermutung lautet: Markus selbst. Sicher ist das nicht. Das Bild ist stark: Selbst wer zuletzt noch folgt, lässt alles zurück und flieht."),
        E("Warum mit Schwertern und Stöcken?", "Jesus fragt selbst: Bin ich ein Räuber (V. 48)? Er hatte offen im Tempel gelehrt. Die nächtliche Verhaftung zeigt die Angst seiner Gegner vor dem Volk."),
    ],
    teaser="Vor dem Hohen Rat schweigt Jesus lange. Dann sagt er zwei Worte, die alles entscheiden.")

sec("nacht", [M(14, 53, 65)], "Vor dem Hohen Rat",
    "Nachts wird Jesus vor dem Hohen Rat verhört. Falsche Zeugen widersprechen sich. Der Hohepriester fragt: Bist du der Christus? Jesus: Ich bin es. Sie verurteilen ihn wegen Gotteslästerung, bespucken und schlagen ihn.",
    place="jerusalem",
    quiz=[
        who("Ich bin es", M(14, 62), ["Jesus", "Petrus", "Ein Zeuge", "Der Hohepriester"],
            "V. 62: Das Messiasgeheimnis ist zu Ende. Jetzt, wo es ihn das Leben kostet, sagt Jesus offen, wer er ist."),
        tf("Die falschen Zeugen stimmen in ihren Aussagen überein.", False, 56, "Lies Vers 56 und 59.",
           "V. 56 und 59: Ihre Aussagen passen nicht zusammen – nach jüdischem Recht hätte das nicht gereicht."),
    ],
    explain=[
        E("Warum zerreißt der Hohepriester sein Gewand?", "Ein Zeichen äußersten Entsetzens über eine Gotteslästerung. Für ihn ist Jesu Anspruch, zur Rechten Gottes zu sitzen (Dan 7,13; Ps 110,1), Lästerung – oder Wahrheit."),
    ],
    teaser="Unten im Hof wärmt sich Petrus am Feuer. Eine Magd erkennt ihn.")

sec("nacht", [M(14, 66, 72)], "Petrus verleugnet",
    "Im Hof erkennt eine Magd Petrus: Du warst auch mit Jesus. Petrus leugnet – dreimal, zuletzt mit Fluch und Schwur. Da kräht der Hahn zum zweiten Mal. Petrus erinnert sich an Jesu Wort und weint.",
    place="jerusalem",
    quiz=[
        choice("Woran erkennen die Umstehenden zuletzt, dass Petrus zu Jesus gehört?", ["Er ist ein Galiläer", "An seinem Schwert", "An seiner Kleidung", "Ein Jünger zeigt auf ihn"], 70, "Vers 70.",
               "V. 70: Seine galiläische Herkunft (Matthäus ergänzt: seine Aussprache)."),
        order("Bring die Ereignisse in die richtige Reihenfolge.", ["Eine Magd spricht Petrus an", "Der Hahn kräht zum ersten Mal", "Petrus schwört: Ich kenne diesen Menschen nicht", "Der Hahn kräht zum zweiten Mal", "Petrus weint"], "V. 66–72."),
    ],
    explain=[
        E("Warum erzählt das Evangelium davon?", "Petrus war später der wichtigste Leiter der Gemeinde. Dass sein Versagen erzählt wird, zeigt Ehrlichkeit – und Hoffnung: Auch nach tiefem Versagen gibt es einen Neuanfang (vgl. 16,7)."),
    ],
    fact="Nach alter Überlieferung (Papias, um 120 n. Chr.) schrieb Markus auf, was Petrus über Jesus predigte. Dann hätte Petrus diese peinliche Geschichte selbst erzählt.",
    teaser="Am Morgen steht Jesus vor Pilatus. Die Menge darf wählen: Jesus oder einen Mörder.")

# ───────────────────────── 9 · Kreuz und Auferstehung ─────────────────────────
sec("kreuz", [M(15, 1, 15)], "Pilatus und Barabbas",
    "Am Morgen wird Jesus Pilatus übergeben: Bist du der König der Juden? – Du sagst es. Zum Fest darf das Volk einen Gefangenen freibitten. Aufgehetzt fordert die Menge Barabbas – und für Jesus: Kreuzige ihn! Pilatus gibt nach.",
    place="jerusalem",
    quiz=[
        choice("Warum hatten die Hohenpriester Jesus laut Pilatus ausgeliefert?", ["Aus Neid", "Wegen Steuerhinterziehung", "Weil er Rom angegriffen hatte", "Wegen eines Mordes"], 10, "Vers 10.",
               "V. 10: Pilatus durchschaut die Motive – und handelt trotzdem nicht gerecht."),
        tf("Pilatus findet ein Verbrechen, das Jesus begangen hat.", False, 14, "Lies Vers 14.",
           "V. 14: Pilatus fragt, was Jesus denn Böses getan habe – und gibt der Menge doch nach, um sie zufriedenzustellen (V. 15)."),
    ],
    explain=[
        E("Wer war Barabbas?", "Ein Aufrührer, der bei einem Aufstand einen Mord begangen hatte (V. 7). Sein Name bedeutet „Sohn des Vaters“. Der Schuldige kommt frei, der Unschuldige stirbt an seiner Stelle – Christen haben darin ein Bild für Jesu Tod für andere gesehen."),
        E("Wer ist schuld an Jesu Tod?", "Die Evangelien nennen die Hohenpriester, Pilatus und die aufgehetzte Menge. Christen haben diese Texte über Jahrhunderte missbraucht, um „die Juden“ insgesamt zu beschuldigen – mit schrecklichen Folgen. Die Kirchen haben das inzwischen klar als Unrecht benannt (z. B. das Zweite Vatikanische Konzil 1965). Theologisch sagen Christen: Jesus starb für die Schuld aller Menschen."),
    ],
    cards=["pilatus"],
    teaser="Soldaten setzen Jesus eine Krone auf – aus Dornen.")

sec("kreuz", [M(15, 16, 20)], "Die Verspottung",
    "Die Soldaten führen Jesus ins Prätorium, legen ihm einen Purpurmantel um, setzen ihm eine Dornenkrone auf und grüßen ihn spöttisch: Sei gegrüßt, König der Juden! Sie schlagen ihn, spucken ihn an und führen ihn hinaus zur Kreuzigung.",
    place="jerusalem",
    quiz=[
        choice("Was setzen die Soldaten Jesus auf?", ["Eine Dornenkrone", "Einen Lorbeerkranz", "Einen Helm", "Eine goldene Krone"], 17, "Vers 17.",
               "V. 17: Eine Dornenkrone – ein Spott auf seine Königswürde."),
        tf("Die Soldaten verspotten Jesus als König der Juden.", True, 18, "Lies Vers 18.",
           "V. 18: Ohne es zu wissen, sprechen sie aus, was Markus seinen Lesern sagen will: Jesus ist wirklich König – ein gekreuzigter König."),
    ],
    explain=[
        E("Was ist das Prätorium?", "Der Amtssitz des römischen Statthalters in Jerusalem, wohl im ehemaligen Palast des Herodes. Dort war eine ganze Abteilung Soldaten versammelt (V. 16)."),
    ],
    teaser="Ein Mann vom Land wird gezwungen, das Kreuz zu tragen. Markus kennt sogar die Namen seiner Söhne.")

sec("kreuz", [M(15, 21, 32)], "Die Kreuzigung",
    "Simon von Kyrene muss das Kreuz tragen. Auf Golgatha wird Jesus gekreuzigt, zwischen zwei Verbrechern. Über ihm steht: Der König der Juden. Vorübergehende, Hohepriester und sogar die Mitgekreuzigten verspotten ihn: Andere hat er gerettet, sich selbst kann er nicht retten.",
    place="jerusalem",
    quiz=[
        choice("Wer muss Jesu Kreuz tragen?", ["Simon von Kyrene", "Simon Petrus", "Joseph von Arimathäa", "Ein Soldat"], 21, "Vers 21.",
               "V. 21: ein Mann, der zufällig vom Feld kommt. Seine Söhne Alexander und Rufus waren den ersten Lesern offenbar bekannt."),
        who("Andere hat er gerettet, sich selbst kann er nicht retten", M(15, 31), ["Die Hohenpriester und Schriftgelehrten", "Pilatus", "Der Hauptmann", "Simon von Kyrene"],
            "V. 31: Ein Spott, der unfreiwillig wahr ist: Gerade weil er andere retten will, rettet er sich nicht selbst."),
    ],
    explain=[
        E("Was heißt „Golgatha“?", "Aramäisch „Schädel(stätte)“ – vielleicht wegen der Form des Hügels oder weil dort Hinrichtungen stattfanden. Die Grabeskirche in Jerusalem steht nach alter Überlieferung über diesem Ort."),
        E("Warum verteilen sie seine Kleider?", "Die Kleider eines Hingerichteten gehörten den Soldaten. Markus erinnert damit an Psalm 22,19 – denselben Psalm, den Jesus gleich betet."),
    ],
    teaser="Mittags wird es dunkel. Jesus schreit einen Psalm.")

sec("kreuz", [M(15, 33, 41)], "Der Tod",
    "Von Mittag bis drei Uhr ist es finster. Jesus schreit: Eloi, Eloi, lama sabachthani – mein Gott, warum hast du mich verlassen? und stirbt. Der Tempelvorhang zerreißt. Der römische Hauptmann bekennt: Wahrhaftig, dieser Mensch war Gottes Sohn. Frauen sehen von fern zu.",
    place="jerusalem",
    quiz=[
        choice("Wie verstehen manche Umstehende Jesu Ruf?", ["Er ruft Elia", "Er ruft seine Mutter", "Er verflucht die Römer", "Er betet für seine Feinde"], 35, "Vers 35.",
               "V. 35: „Eloi“ klang wie „Elia“ – ein Missverständnis."),
        choice("Wer schaut beim Kreuz von fern zu?", ["Frauen, darunter Maria Magdalena", "Die Zwölf", "Petrus und Johannes", "Pilatus"], 40, "Vers 40.",
               "V. 40–41: Die Frauen, die ihm seit Galiläa gefolgt sind – die Männer sind geflohen."),
    ],
    explain=[
        E("Was bedeutet der zerrissene Vorhang?", "Der Vorhang trennte das Allerheiligste, wo Gott gegenwärtig gedacht wurde. Er zerreißt „von oben nach unten“ – wie von Gott selbst. Viele verstehen das so: Durch Jesu Tod ist der Weg zu Gott offen (vgl. Hebr 10,19–20)."),
        E("Warum gerade ein Römer?", "Am Anfang nennt Markus Jesus „Sohn Gottes“ (1,1). Kein Jünger spricht das im Evangelium aus – erst ein heidnischer Offizier, unter dem Kreuz. Das ist der Höhepunkt des Buches."),
    ],
    cards=["maria-magdalena"],
    prayer={"text": "Wenn ich einmal soll scheiden, so scheide nicht von mir; wenn ich den Tod soll leiden, so tritt du dann herfür.", "source": "Paul Gerhardt, „O Haupt voll Blut und Wunden“ (1656)"},
    teaser="Ein Ratsherr fasst Mut und bittet Pilatus um den Leichnam.")

sec("kreuz", [M(15, 42, 47)], "Das Begräbnis",
    "Am Abend vor dem Sabbat bittet Joseph von Arimathäa, ein angesehener Ratsherr, Pilatus mutig um Jesu Leichnam. Er wickelt ihn in Leinen, legt ihn in ein Felsengrab und rollt einen Stein vor den Eingang. Zwei Marias sehen zu.",
    place="jerusalem",
    quiz=[
        choice("Wer bittet Pilatus um den Leichnam?", ["Joseph von Arimathäa", "Petrus", "Nikodemus", "Maria Magdalena"], 43, "Vers 43.",
               "V. 43: ein Ratsherr, der das Reich Gottes erwartete – er wagt, was die Jünger nicht wagen."),
        tf("Pilatus wundert sich, dass Jesus schon tot ist.", True, 44, "Lies Vers 44.",
           "V. 44: Gekreuzigte starben oft erst nach Tagen. Pilatus lässt sich den Tod vom Hauptmann bestätigen."),
    ],
    explain=[
        E("Warum die Eile?", "Mit Sonnenuntergang begann der Sabbat, an dem nicht gearbeitet werden durfte. Außerdem schrieb das Gesetz vor, Gehängte vor der Nacht zu begraben (5. Mose 21,23)."),
        E("Warum betont Markus, wer zusah?", "Die Frauen wissen genau, wo das Grab ist (V. 47). Am Ostermorgen gehen sie also nicht aus Versehen zum falschen Grab."),
    ],
    teaser="Früh am Sonntag fragen sich drei Frauen: Wer wälzt uns den Stein weg?")

sec("kreuz", [M(16, 1, 8)], "Das leere Grab",
    "Früh am ersten Wochentag kommen drei Frauen mit Salben zum Grab. Der große Stein ist weggerollt. Ein junger Mann in weißem Gewand sagt: Er ist auferstanden, er ist nicht hier. Sagt seinen Jüngern und Petrus: Er geht euch voraus nach Galiläa. Zitternd fliehen sie.",
    place="jerusalem",
    focus="Achte darauf, wer in der Botschaft des Engels extra genannt wird.",
    quiz=[
        who("Wer wird uns den Stein von der Tür der Gruft wälzen", M(16, 3), ["Die drei Frauen", "Die Jünger", "Die Wachen", "Joseph von Arimathäa"],
            "V. 3: Sie machen sich Sorgen über etwas, das Gott längst gelöst hat."),
        choice("Wer wird in der Botschaft ausdrücklich namentlich genannt?", ["Petrus", "Johannes", "Judas", "Pilatus"], 7, "Vers 7.",
               "V. 7: Neben den Jüngern wird Petrus extra genannt – ausgerechnet der, der ihn verleugnet hat. Ein stilles Zeichen der Vergebung."),
        tf("Die Frauen erzählen sofort allen, was sie gesehen haben.", False, 8, "Lies Vers 8.",
           "V. 8: Sie fliehen und sagen niemandem etwas, denn sie fürchten sich. So endet der älteste Text des Markusevangeliums."),
    ],
    explain=[
        E("Warum endet Markus so abrupt?", "Die ältesten Handschriften enden mit V. 8: Furcht und Schweigen. Manche meinen, der ursprüngliche Schluss sei verloren gegangen. Andere sehen darin Absicht: Das Ende bleibt offen – und die Leser sollen weitertragen, was die Frauen erst nicht wagten. Dass wir die Geschichte kennen, zeigt: Die Frauen haben später doch erzählt."),
        E("Wer ist der junge Mann?", "Markus nennt ihn nicht „Engel“, beschreibt ihn aber so: weißes Gewand, himmlische Botschaft. Matthäus spricht von einem Engel (Mt 28,2), Lukas von zwei Männern (Lk 24,4)."),
    ],
    memory_verse=MV(M(16, 6), "Er ist auferstanden, er ist nicht hier."),
    teaser="Später wurde dem Evangelium ein längerer Schluss angefügt – mit einem großen Auftrag.")

sec("kreuz", [M(16, 9, 20)], "Der längere Schluss",
    "Der Auferstandene erscheint Maria Magdalena, dann zwei Jüngern unterwegs, schließlich den Elf. Er tadelt ihren Unglauben und sendet sie: Geht in die ganze Welt und verkündet das Evangelium allen Geschöpfen. Dann wird er in den Himmel aufgenommen.",
    focus="Achte darauf, wie oft hier vom Unglauben der Jünger die Rede ist.",
    quiz=[
        choice("Wem erscheint der Auferstandene zuerst?", ["Maria Magdalena", "Petrus", "Den Elf", "Seiner Mutter"], 9, "Vers 9.",
               "V. 9: Maria Magdalena, aus der er sieben Dämonen ausgetrieben hatte."),
        choice("Was ist der Auftrag an die Jünger?", ["In die ganze Welt gehen und das Evangelium verkünden", "In Jerusalem auf ihn warten", "Einen Tempel bauen", "Nach Galiläa zurückkehren und fischen"], 15, "Vers 15.",
               "V. 15: der „Missionsbefehl“ in der Fassung des Markusschlusses."),
    ],
    explain=[
        E("Gehört dieser Schluss zur Bibel?", "Die Verse 9–20 fehlen in den ältesten Handschriften und unterscheiden sich im Stil vom Rest. Sie wurden wohl im 2. Jahrhundert angefügt und fassen Ostergeschichten aus den anderen Evangelien zusammen. Die Kirchen haben sie trotzdem als Teil der Bibel anerkannt; viele Bibeln setzen sie in Klammern oder kennzeichnen sie. Katholisch gelten sie als kanonisch (Konzil von Trient), und auch für die meisten anderen Kirchen gehören sie zur Heiligen Schrift."),
        E("Sollen Christen Schlangen anfassen?", "V. 18 wird von fast allen Kirchen nicht als Aufforderung verstanden, sondern als Zusage von Gottes Schutz bei der Verkündigung (vgl. Apg 28,3–6). Gott auf die Probe zu stellen, lehnt Jesus selbst ab (Mt 4,7)."),
    ],
    fact="Es gibt sogar noch einen „kürzeren Schluss“ des Markusevangeliums – zwei Sätze, die in wenigen alten Handschriften nach Vers 8 stehen.",
)

P.write()
