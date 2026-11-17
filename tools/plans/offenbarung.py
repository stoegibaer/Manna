#!/usr/bin/env python3
"""Source for the reading plan „Offenbarung – Das Lamm auf dem Thron“ (generates assets/plans/offenbarung.json).

python3 -I tools/plans/offenbarung.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/offenbarung.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

OFFB, DAN, PS = 66, 27, 19

P = PlanBuilder(
    "offenbarung", "of", "Offenbarung", "Das Lamm auf dem Thron",
    "Ein Brief an sieben kleine Gemeinden in der heutigen Türkei – voller Bilder von Thronen, Tieren, Reitern und einer Stadt aus Gold. "
    "Kein Buch der Bibel wird so verschieden gelesen. 32 Abschnitte durch die zentralen Kapitel, mit Daniel 7 als Hintergrund, "
    "und bei den umstrittenen Stellen die Sichtweisen, mit denen Christen dieses Buch verstehen.",
    "glauben",
    stages=[("briefe", "Ein Brief an sieben Gemeinden"), ("thron", "Der Thron und das Lamm"), ("siegel", "Siegel, Gebete und Zeugen"),
            ("tiere", "Der Drache und die Tiere"), ("babylon", "Babylon fällt"), ("ende", "Das Ende und der Anfang")],
    cards=[
        ("johannes", "person", "Johannes", "Der Verfasser nennt sich nur Johannes, Knecht Jesu und Bruder der Gemeinden (1,1.9). Seit dem 2. Jahrhundert (Justin, Irenäus) gilt er als der Apostel Johannes. Schon im 3. Jahrhundert fragte Dionysius von Alexandria wegen des ganz anderen Griechisch, ob ein anderer Johannes schrieb. Die Frage ist bis heute offen.", "Offb 1,1.4.9; 22,8"),
        ("patmos", "ort", "Patmos", "Kleine, felsige Insel in der Ägäis, südwestlich von Ephesus vor der kleinasiatischen Küste. Die Römer verbannten dorthin unbequeme Personen. Johannes war dort „um des Wortes Gottes willen“ (1,9). Eine Höhle auf der Insel wird seit Langem als Ort seiner Visionen verehrt; das Kloster darüber ist UNESCO-Welterbe.", "Offb 1,9"),
        ("apokalypse", "begriff", "Apokalypse", "Griechisch apokalypsis, „Enthüllung“ – das erste Wort des Buches. So heißt auch eine Gattung jüdischer und christlicher Schriften (z. B. Daniel 7–12, 1. Henoch, 4. Esra): Visionen, die ein Engel deutet, Tiere als Bilder für Reiche, symbolische Zahlen. Gemeint ist nicht Weltuntergang, sondern das Aufdecken dessen, was hinter der sichtbaren Geschichte steht.", "Offb 1,1; Dan 7"),
        ("sieben-gemeinden", "ort", "Die sieben Gemeinden", "Ephesus, Smyrna, Pergamus, Thyatira, Sardes, Philadelphia und Laodizea lagen in der römischen Provinz Asia, im Westen der heutigen Türkei. In dieser Reihenfolge liegen sie an einem Rundweg, den ein Bote von Ephesus aus gehen konnte. Jede bekommt einen eigenen Brief; alle sollen alle Briefe hören (2,7).", "Offb 1,11; 2–3"),
        ("kaiserkult", "begriff", "Kaiserkult", "In der Provinz Asia wurden römische Kaiser in Tempeln verehrt, mit Opfern, Festen und Statuen. Pergamon erhielt 29 v. Chr. als erste Stadt der Provinz einen Tempel für Roma und Augustus. Wer nicht mitmachte, galt als illoyal – auch Händlerzünfte hatten ihre Götter und Mahlzeiten. Viele Ausleger sehen hier den Hintergrund für die Konflikte im Buch.", "Offb 2,13; 13,4.15"),
        ("menschensohn", "begriff", "Der Menschensohn", "Aramäisch bar enasch, „ein Mensch“. In Dan 7,13 kommt einer „wie ein Menschensohn“ mit den Wolken zum Alten an Tagen und bekommt ewige Herrschaft. In den Evangelien ist „Menschensohn“ die häufigste Selbstbezeichnung Jesu (z. B. Mk 14,62). Offb 1,13 greift das Bild auf.", "Dan 7,13–14; Mk 14,62; Offb 1,13"),
        ("lamm", "begriff", "Das Lamm", "Die häufigste Bezeichnung für Christus in der Offenbarung, fast 30-mal. Im Hintergrund stehen das Passahlamm (2Mo 12), das Lamm in Jes 53,7 und das Wort des Täufers (Joh 1,29). Das Lamm steht „wie geschlachtet“ (5,6) – es trägt die Todeswunde und lebt.", "Offb 5,6; 7,17; 21,22"),
        ("vier-lesarten", "begriff", "Vier Arten, die Offenbarung zu lesen", "Präteristisch: Das meiste erfüllte sich im 1. Jahrhundert (Rom, Jerusalem). Historisch: Das Buch zeichnet die Kirchengeschichte bis zum Ende – so lasen viele Reformatoren. Futuristisch: Ab Kap. 4 geht es um die Endzeit – so lesen Dispensationalisten. Idealistisch: Es zeigt zeitlose Muster des Kampfes zwischen Gott und dem Bösen. Viele Ausleger verbinden mehrere.", "Offb 1,19; 4,1"),
        ("zahlen", "begriff", "Zahlen in der Offenbarung", "Sieben steht für Vollständigkeit (sieben Gemeinden, Siegel, Posaunen, Schalen), zwölf für das Gottesvolk (Stämme, Apostel). 3½ Jahre = 42 Monate = 1260 Tage, nach Dan 7,25 „eine Zeit und Zeiten und eine halbe Zeit“: eine begrenzte Zeit der Bedrängnis. Ob die Zahlen auch wörtlich gemeint sind, ist eine der großen Auslegungsfragen.", "Offb 11,2–3; 12,6.14; 13,5"),
        ("daniel", "person", "Daniel", "Ein junger Judäer, der nach Babylon verschleppt wurde und am Königshof diente (Dan 1). Kap. 7–12 enthalten seine Visionen von Weltreichen und dem Reich Gottes. Die Offenbarung greift seine Bilder immer wieder auf, besonders aus Kap. 7.", "Dan 1,1–7; 7,1"),
        ("nero", "person", "Nero", "Römischer Kaiser 54–68 n. Chr. Nach dem Brand Roms 64 ließ er Christen hinrichten; nach der Überlieferung starben damals Petrus und Paulus. Nach seinem Selbstmord ging das Gerücht um, er lebe noch oder kehre zurück. Viele Ausleger, alte und neue, verbinden ihn mit dem Tier aus Offb 13 und 17; andere sehen darin höchstens ein Vorbild.", "Offb 13,3.18; 17,8–11"),
        ("babylon", "ort", "Babylon", "Die Stadt am Euphrat, die 587 v. Chr. Jerusalem zerstörte. Schon im Judentum und in 1Petr 5,13 ein Deckname für Rom. In Offb 14–18 ist „Babylon, die große“ eine Stadt auf sieben Bergen, die über die Könige herrscht. Gedeutet wird sie als Rom, als Jerusalem, als künftige Weltmacht oder als jede Macht, die sich an die Stelle Gottes setzt.", "Offb 14,8; 17,5.18; 1Petr 5,13"),
        ("entrueckung", "begriff", "Entrückung", "Nach 1Thess 4,17 werden die Lebenden bei der Wiederkunft Christi „entrückt“, ihm entgegen. Dispensationalisten (seit J. N. Darby, 19. Jh.) erwarten das sieben Jahre vor seinem sichtbaren Kommen, vor der „großen Drangsal“. Andere setzen es in die Mitte oder ans Ende der Drangsal. Die meisten Kirchen verstehen es als Teil der einen Wiederkunft.", "1Thess 4,15–17; Offb 3,10"),
        ("millennium", "begriff", "Das Tausendjährige Reich", "Nur in Offb 20,1–7 erwähnt. Prämillenialisten: Christus kommt zurück und herrscht danach 1000 Jahre auf der Erde. Amillenialisten: Die 1000 Jahre sind die Zeit der Kirche zwischen Auferstehung und Wiederkunft; Christus herrscht schon. Postmillenialisten: Das Evangelium durchdringt die Welt, danach kommt Christus. Alle drei Sichten gibt es seit Langem.", "Offb 20,1–7"),
        ("neues-jerusalem", "ort", "Das neue Jerusalem", "Die Stadt, die am Ende aus dem Himmel auf die neue Erde herabkommt (21,2). Sie ist ein Würfel wie das Allerheiligste im Tempel (1Kön 6,20), hat Tore mit den Namen der zwölf Stämme und Grundsteine mit den Namen der zwölf Apostel, und einen Tempel braucht sie nicht. Sie wird auch „die Braut, die Frau des Lammes“ genannt.", "Offb 3,12; 21,2.9–27"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Ein Brief an sieben Gemeinden ─────────────────────────
sec("briefe", [R(OFFB, 1, 1, 8)], "Was bald geschehen muss",
    "Das Buch stellt sich vor: eine Offenbarung, die Gott Jesus Christus gab und die ein Engel Johannes zeigte. Es ist zugleich ein Brief an sieben Gemeinden in der Provinz Asia, mit Gruß und Segen. Gepriesen wird Christus, der liebt, befreit hat und mit den Wolken kommen wird; Gott nennt sich das Alpha und das Omega.",
    place="patmos",
    focus="Achte darauf, wie viele verschiedene Arten von Text in diesen acht Versen stecken.",
    quiz=[
        choice("Wem gab Gott nach V. 1 die Offenbarung zuerst?", ["Jesus Christus", "Johannes", "Den sieben Gemeinden", "Einem Engel"], 1, "Lies Vers 1 genau.",
               "V. 1: Gott gab sie Jesus Christus; der zeigte sie durch seinen Engel seinem Knecht Johannes."),
        tf("Nach V. 3 gilt der Segen dem, der das Buch liest, und denen, die es hören und bewahren.", True, 3, "Lies Vers 3.",
           "V. 3: Glückselig der Vorleser und die Hörer, die bewahren, was darin steht – das Buch war zum Vorlesen in der Gemeinde gedacht."),
        choice("Wie nennt sich Gott in V. 8?", ["Das Alpha und das Omega", "Der Löwe aus Juda", "Der Morgenstern", "Der Alte an Tagen"], 8, "Lies Vers 8.",
               "V. 8: Alpha und Omega, der erste und der letzte Buchstabe des griechischen Alphabets – der ist, der war und der kommt."),
    ],
    explain=[
        E("Was für ein Buch ist das?", "Drei Gattungen in einem: Es heißt Offenbarung (apokalypsis, V. 1), nennt sich Weissagung, also Prophetie (V. 3), und beginnt wie ein Brief mit Absender, Empfängern und Gruß (V. 4). Wer es liest, liest also auch die Post einer Gemeinde im 1. Jahrhundert."),
        E("Was heißt „bald“?", "Das Buch sagt am Anfang und am Ende, dass es um etwas geht, das bald geschehen muss (1,1; 22,6). Präteristische Ausleger sehen darin einen Hinweis auf Ereignisse im 1. Jahrhundert. Futuristische verweisen auf 2Petr 3,8: Bei Gott sind tausend Jahre wie ein Tag. Andere verstehen „bald“ als „jederzeit möglich“."),
        E("Was ist eine „Versammlung“?", "So übersetzt die Elberfelder das griechische ekklesia, das andere Bibeln mit „Gemeinde“ wiedergeben. Gemeint ist die örtliche Gemeinschaft der Christen, kein Gebäude.", "elbbk"),
        E("Wer sind die sieben Geister?", "Drei Lesarten: der Heilige Geist in seiner Fülle (sieben = vollständig, vgl. die sieben Gaben des Geistes in Jes 11,2 nach der griechischen Bibel), sieben Engel vor Gottes Thron, oder beides verbunden. In 5,6 sind sie die sieben Augen des Lammes."),
    ],
    cards=["johannes", "apokalypse", "sieben-gemeinden"],
    fact="V. 3 ist die erste von genau sieben Seligpreisungen im Buch (1,3; 14,13; 16,15; 19,9; 20,6; 22,7; 22,14). Auch sonst ist die Offenbarung voller Siebenerreihen.",
    teaser="Johannes dreht sich um, um eine Stimme zu sehen. Was er dann sieht, haut ihn um – im wörtlichen Sinn.")

sec("briefe", [R(OFFB, 1, 9, 20)], "Einer wie der Sohn des Menschen",
    "Johannes ist auf der Insel Patmos, wegen des Wortes Gottes. Am Tag des Herrn hört er eine Stimme wie eine Posaune und sieht zwischen sieben goldenen Leuchtern einen wie den Sohn des Menschen: weißes Haar, Augen wie Feuer, ein Schwert aus dem Mund. Johannes fällt wie tot nieder; der Erscheinende legt die Hand auf ihn und erklärt die Sterne und Leuchter.",
    place="patmos",
    quiz=[
        choice("Was tut der Menschensohn, als Johannes wie tot zu Boden fällt?", ["Er legt seine rechte Hand auf ihn und sagt: Fürchte dich nicht", "Er befiehlt ihm aufzustehen und zu schweigen", "Er gibt ihm ein Buch zu essen", "Er schickt einen Engel, der ihn aufrichtet"], 17, "Lies Vers 17.",
               "V. 17: Er legt seine Rechte auf ihn und sagt, er solle sich nicht fürchten."),
        error("Der Menschensohn hält sieben [Leuchter] in seiner rechten Hand und steht inmitten von sieben Sternen.", "Sterne", 16,
              "V. 13.16: Er steht inmitten der Leuchter und hält die Sterne in der Rechten. V. 20 erklärt: Sterne sind Engel der Gemeinden, Leuchter die Gemeinden.", "Lies Vers 13 und 16."),
        choice("Was hat der Menschensohn nach V. 18?", ["Die Schlüssel des Todes und des Hades", "Ein goldenes Rohr zum Messen", "Eine Waage in der Hand", "Einen Bogen und eine Krone"], 18, "Lies Vers 18.",
               "V. 18: Er war tot, lebt in Ewigkeit und hat die Schlüssel des Todes und des Hades."),
    ],
    explain=[
        E("Woher stammen diese Bilder?", "Fast jedes Detail hat ein Vorbild im Alten Testament: der Menschensohn aus Dan 7,13, weißes Haar wie beim Alten an Tagen (Dan 7,9), das Gewand und die Augen aus Dan 10,5–6, die Stimme wie viele Wasser aus Hes 43,2. Johannes beschreibt Christus mit Bildern, die dort Gott oder seinem Boten gehören."),
        E("Was ist der „Tag des Herrn“?", "Die meisten Ausleger verstehen ihn als Sonntag, den Tag der Auferstehung, an dem sich die Christen versammelten; so wird der Ausdruck bald nach dem Neuen Testament gebraucht. Manche lesen ihn als den prophetischen „Tag des HERRN“, also als Versetzung in die Endzeit."),
        E("Wer sind die Engel der Gemeinden?", "Drei Lesarten: himmlische Schutzengel jeder Gemeinde, menschliche Boten oder Leiter (griechisch angelos heißt auch einfach „Bote“), oder eine Verkörperung des Wesens jeder Gemeinde."),
        E("Was ist der Hades?", "Das griechische Wort für das Totenreich, entsprechend dem hebräischen Scheol: der Ort der Toten, nicht schon die Hölle als Strafort."),
    ],
    cards=["patmos", "menschensohn"],
    memory_verse=MV(R(OFFB, 1, 17, 18), "Fürchte dich nicht! Ich bin der Erste und der Letzte und der Lebendige"),
    try_="Lies Dan 7,9 und 7,13 und leg die Verse neben Offb 1,13–14. Welche Merkmale des Alten an Tagen bekommt hier der Menschensohn?",
    teaser="Der erste Brief geht an eine Gemeinde, die fast alles richtig macht. Fast.")

sec("briefe", [R(OFFB, 2, 1, 7)], "Ephesus: die erste Liebe",
    "Der erste Brief geht an Ephesus. Die Gemeinde arbeitet hart, harrt aus, prüft falsche Apostel und wird nicht müde. Aber sie hat ihre erste Liebe verlassen. Sie soll sich erinnern und umkehren, sonst wird ihr Leuchter weggerückt. Dem, der überwindet, ist der Baum des Lebens versprochen.",
    place="ephesus",
    quiz=[
        choice("Was hält der Absender der Gemeinde in Ephesus vor?", ["Sie hat ihre erste Liebe verlassen", "Sie duldet falsche Apostel", "Sie ist müde geworden", "Sie hat seinen Namen verleugnet"], 4, "Lies Vers 4.",
               "V. 4: Sie hat ihre erste Liebe verlassen – obwohl sie falsche Apostel entlarvt (V. 2) und nicht müde wird (V. 3)."),
        order("In welcher Reihenfolge ist der Brief aufgebaut?", ["Wer spricht", "Ich kenne deine Werke", "Aber ich habe gegen dich", "Wer ein Ohr hat, höre", "Verheißung für den, der überwindet"],
              "V. 1–7: Absender, Lob, Kritik mit Aufruf zur Umkehr, Weckruf an alle Gemeinden und Verheißung."),
        tf("Dem, der überwindet, wird in V. 7 der Baum des Lebens versprochen.", True, 7, "Lies Vers 7.",
           "V. 7: vom Baum des Lebens im Paradies Gottes essen. Der Baum kommt am Ende des Buches wieder (22,2)."),
    ],
    explain=[
        E("Was war Ephesus?", "Hauptstadt der Provinz Asia mit vielleicht 200.000 Einwohnern, großem Hafen und dem Tempel der Artemis, einem der sieben Weltwunder. Paulus wirkte hier etwa drei Jahre (Apg 19–20). Heute liegt die Ruinenstadt einige Kilometer vom Meer entfernt, weil der Hafen verlandete."),
        E("Was ist mit „erste Liebe“ gemeint?", "Der Text sagt es nicht genau. Ausleger denken an die Liebe zu Christus, an die Liebe der Christen untereinander oder an beides. Dass zur Umkehr die „ersten Werke“ gehören (V. 5), lässt manche an gelebte Liebe denken."),
        E("Wer waren die Nikolaiten?", "Eine Gruppe, die nur hier und in 2,15 erwähnt wird. Kirchenväter wie Irenäus verbanden sie mit Nikolaus aus Apg 6,5, sicher ist das nicht. Aus 2,14–15 schließen viele, dass sie die Teilnahme an Götzenopfermahlen erlaubten."),
        E("Sind die sieben Gemeinden Kirchenzeitalter?", "In der dispensationalistischen Tradition (z. B. Scofield-Bibel) stehen die sieben Briefe auch für sieben Epochen der Kirchengeschichte, von Ephesus (Apostelzeit) bis Laodizea (Endzeit). Die meisten anderen Ausleger lesen sie als Briefe an wirkliche Gemeinden, deren Lage sich in jeder Zeit wiederfinden kann. Der Text selbst nennt nur die sieben Städte."),
    ],
    cards=["vier-lesarten"],
    teaser="Die nächsten zwei Gemeinden: eine ist arm und wird gleich reich genannt. Die andere wohnt dort, wo der Satan seinen Thron hat.")

sec("briefe", [R(OFFB, 2, 8, 17)], "Smyrna und Pergamus",
    "Smyrna ist arm, wird verleumdet und soll ins Gefängnis kommen; der Brief enthält kein Wort der Kritik, nur die Aufforderung, treu zu sein bis zum Tod. Pergamus wohnt, wo der Thron des Satans ist, und hat Christus auch nicht verleugnet, als Antipas ermordet wurde. Doch einige dort halten an der Lehre Bileams fest.",
    place="smyrna",
    bridge="Der Bote reist von Ephesus nordwärts: Smyrna liegt etwa 60 km entfernt an der Küste, Pergamus noch einmal gut 100 km weiter.",
    quiz=[
        tf("Der Brief an Smyrna enthält einen Tadel.", False, 9, "Lies Vers 8–11.",
           "V. 8–11: Kein Tadel. Smyrna hört Trost (V. 9), eine Vorwarnung (V. 10) und eine Verheißung."),
        choice("Wer wurde in Pergamus ermordet?", ["Antipas, der treue Zeuge", "Bileam", "Balak", "Der Engel der Gemeinde"], 13, "Lies Vers 13.",
               "V. 13: Antipas, mein treuer Zeuge – er ist nur hier erwähnt."),
        choice("Was bekommt nach V. 17 der, der überwindet?", ["Verborgenes Manna und einen weißen Stein mit einem neuen Namen", "Eine Krone aus Gold", "Einen Platz am Tor der Stadt", "Ein weißes Pferd"], 17, "Lies Vers 17.",
               "V. 17: verborgenes Manna und einen weißen Stein mit einem neuen Namen, den nur der Empfänger kennt."),
    ],
    explain=[
        E("Was ist der „Thron des Satans“?", "Pergamon war ein Zentrum der Götterverehrung: mit dem großen Zeusaltar, einem Heiligtum des Heilgottes Asklepios, dessen Zeichen die Schlange war, und dem ersten Kaisertempel der Provinz. Ausleger denken an eines davon oder an alles zusammen."),
        E("Wer war Bileam?", "Ein Seher, den der Moabiterkönig Balak anheuerte, um Israel zu verfluchen (4Mo 22–24). Nach 4Mo 31,16 riet er später, Israel zu Götzendienst und Unzucht zu verführen (4Mo 25). Hier steht er für eine Lehre, die Götzenopfer zu essen erlaubt."),
        E("Wie ist „Synagoge des Satans“ zu verstehen?", "Ein harter Ausdruck aus einem Streit innerhalb des Gottesvolkes in Smyrna und Philadelphia (2,9; 3,9). Er bezieht sich auf bestimmte Gegner, die die Christen dort anklagten, nicht auf das jüdische Volk. Nach der Schoa haben Kirchen ausdrücklich erklärt, dass solche Verse nicht gegen Juden verwendet werden dürfen."),
        E("Was bedeutet der weiße Stein?", "Das bleibt offen. Vorgeschlagen werden: ein weißer Stimmstein für einen Freispruch vor Gericht, eine Eintrittsmarke für ein Festmahl oder ein Amulett mit einem Namen. Alle passen zum Zusammenhang."),
    ],
    cards=["kaiserkult"],
    fact="Polykarp, Bischof von Smyrna, wurde um 155 dort verbrannt. Nach dem Bericht über sein Martyrium sagte er dem Statthalter, er diene Christus seit 86 Jahren und könne seinen König nicht lästern. Nach Irenäus hatte Polykarp noch den Apostel Johannes gekannt.",
    memory_verse=MV(R(OFFB, 2, 10), "Sei getreu bis zum Tod, und ich werde dir die Krone des Lebens geben."),
    teaser="Im nächsten Brief steht ein Vers, auf den eine ganze Endzeitlehre gebaut wird. Der Brief selbst handelt von einer Tür.")

sec("briefe", [R(OFFB, 3, 7, 13)], "Philadelphia: die offene Tür",
    "Der den Schlüssel Davids hat, hat Philadelphia eine Tür geöffnet, die niemand schließen kann. Die Gemeinde hat wenig Kraft, aber sie hat sein Wort bewahrt. Darum will er sie bewahren vor der Stunde der Versuchung, die über die ganze Welt kommt. Wer überwindet, wird eine Säule im Tempel Gottes.",
    place="philadelphia",
    bridge="Dazwischen stehen die Briefe an Thyatira, wo eine falsche Prophetin geduldet wird, und an Sardes, das als lebendig gilt und doch tot ist (2,18–3,6).",
    quiz=[
        choice("Was gibt der Absender Philadelphia nach V. 8?", ["Eine geöffnete Tür, die niemand schließen kann", "Eine große Kraft", "Eine Krone aus Gold", "Einen neuen Leuchter"], 8, "Lies Vers 8.",
               "V. 8: eine geöffnete Tür – und das, obwohl die Gemeinde nur eine kleine Kraft hat."),
        error("Weil du das Wort meines Ausharrens bewahrt hast, werde ich dich bewahren vor der Stunde der [Strafe].", "Versuchung", 10,
              "V. 10: vor der Stunde der Versuchung oder Prüfung, die über den ganzen Erdkreis kommt."),
        choice("Was wird aus dem, der überwindet (V. 12)?", ["Eine Säule im Tempel Gottes", "Ein Ältester auf einem Thron", "Ein Engel vor Gott", "Ein Tor in der neuen Stadt"], 12, "Lies Vers 12.",
               "V. 12: eine Säule im Tempel Gottes, die nie mehr hinausgeht, mit dem Namen Gottes und des neuen Jerusalem."),
    ],
    explain=[
        E("Was ist der „Schlüssel Davids“?", "Ein Bild aus Jes 22,22: Eljakim bekommt als Palastverwalter den Schlüssel des Hauses Davids und entscheidet, wer zum König vorgelassen wird. Hier hat Christus diese Vollmacht."),
        E("Wie wird V. 10 verstanden?", "Dispensationalisten lesen: Christus bewahrt die Gemeinde vor der Stunde, also bewahrt er sie aus ihr heraus – durch die Entrückung vor einer siebenjährigen Drangsal. Andere lesen: Er bewahrt sie in der Prüfung hindurch, wie Jesus in Joh 17,15 bittet, nicht aus der Welt genommen, sondern vor dem Bösen bewahrt zu werden. Präteristen beziehen die Stunde auf eine Verfolgungswelle im Römerreich. Das griechische tereo ek („bewahren aus“) lässt sprachlich mehr als eine Lesart zu."),
        E("Warum eine Säule?", "Philadelphia wurde im Jahr 17 n. Chr. von einem schweren Erdbeben getroffen, und Nachbeben ließen die Bewohner noch lange aus der Stadt fliehen. Eine Säule, die nie mehr hinausgehen muss, könnte darauf anspielen. Säulen trugen in Tempeln auch Inschriften zu Ehren von Personen."),
    ],
    cards=["entrueckung"],
    try_="Lies Joh 17,15 und dann noch einmal Offb 3,10. Welche Lesart von V. 10 scheint dir näher am Text – und woran machst du das fest?",
    teaser="Der letzte Brief geht an eine reiche Stadt. Und der Absender steht draußen vor der Tür.")

sec("briefe", [R(OFFB, 3, 14, 22)], "Laodizea: weder kalt noch warm",
    "Laodizea ist weder kalt noch warm, sondern lau; darum will der Absender es ausspeien. Die Gemeinde hält sich für reich und weiß nicht, dass sie arm, blind und nackt ist. Er rät ihr, Gold, weiße Kleider und Augensalbe bei ihm zu kaufen. Er steht an der Tür und klopft an.",
    place="laodizea",
    quiz=[
        who("Ich bin reich und bin reich geworden und bedarf nichts", R(OFFB, 3, 17), ["Die Gemeinde in Laodizea", "Babylon, die große Stadt", "Die Kaufleute der Erde", "Die Gemeinde in Smyrna"],
            "V. 17: So spricht Laodizea über sich selbst – der Absender sieht es ganz anders."),
        choice("Was rät der Absender in V. 18 zu kaufen?", ["Geläutertes Gold, weiße Kleider und Augensalbe", "Öl, Wein und Weizen", "Einen neuen Leuchter", "Weihrauch und Myrrhe"], 18, "Lies Vers 18.",
               "V. 18: Gold, im Feuer geläutert; weiße Kleider; Augensalbe, damit sie sehen."),
        tf("Nach V. 19 tadelt und züchtigt er die, die er liebt.", True, 19, "Lies Vers 19.",
           "V. 19: Wen er liebt, den überführt und züchtigt er – der härteste Brief enthält auch diesen Satz."),
    ],
    explain=[
        E("Warum gerade kalt, warm und lau?", "Laodizea hatte kein eigenes gutes Wasser und bekam es über eine Leitung, lauwarm und kalkhaltig. In der Nachbarstadt Hierapolis gab es heiße Heilquellen, in Kolossä kaltes, frisches Wasser. Viele Ausleger lesen „kalt oder warm“ darum nicht als „gegen oder für Christus“, sondern als „erfrischend oder heilend“ – beides ist brauchbar, Lauwarmes nicht."),
        E("Warum Gold, Kleider und Augensalbe?", "Laodizea war eine Bankenstadt, bekannt für Kleidung aus schwarzer Schafwolle und für eine Ärzteschule. Der Rat greift genau das auf, worauf die Stadt stolz war."),
        E("An welche Tür klopft er?", "V. 20 wird oft auf den einzelnen Menschen bezogen, der Christus einlässt. Im Zusammenhang steht er vor der Tür einer Gemeinde. Das gemeinsame Abendessen erinnert viele Ausleger auch an das Abendmahl."),
    ],
    fact="Laodizea wurde 60 n. Chr. von einem Erdbeben zerstört. Der römische Geschichtsschreiber Tacitus berichtet, die Stadt habe sich ohne Hilfe aus Rom aus eigenen Mitteln wieder aufgebaut (Annalen 14,27).",
    memory_verse=MV(R(OFFB, 3, 20), "Siehe, ich stehe an der Tür und klopfe an"),
    teaser="Eben stand jemand vor einer Tür. Jetzt öffnet sich eine – im Himmel.")

# ───────────────────────── 2 · Der Thron und das Lamm ─────────────────────────
sec("thron", [R(OFFB, 4, 1, 11)], "Der Thron",
    "Eine Tür im Himmel ist offen, und Johannes wird hinaufgerufen. Er sieht einen Thron und einen, der darauf sitzt, leuchtend wie Edelsteine, umgeben von einem Regenbogen. Um den Thron sitzen 24 Älteste, und vier lebendige Wesen rufen ohne Pause: Heilig, heilig, heilig. Die Ältesten werfen ihre Kronen vor dem Thron nieder.",
    focus="Achte darauf, was Johannes über den beschreibt, der auf dem Thron sitzt – und was er nicht beschreibt.",
    quiz=[
        estimate("Wie viele Älteste sitzen um den Thron?", 4, 40, 24, "Älteste", "V. 4: 24 Älteste auf 24 Thronen, in weißen Kleidern mit goldenen Kronen.", 4, "Lies Vers 4."),
        choice("Womit wird der, der auf dem Thron sitzt, beschrieben?", ["Mit Edelsteinen und einem Regenbogen", "Mit weißem Haar und Augen wie Feuer", "Mit einem Gesicht wie ein Mensch", "Mit sechs Flügeln"], 3, "Lies Vers 3.",
               "V. 3: wie Jaspis und Sardis, ringsum ein Regenbogen wie ein Smaragd. Eine Gestalt beschreibt Johannes nicht."),
        tf("Die Ältesten preisen Gott in V. 11 als den, der alle Dinge erschaffen hat.", True, 11, "Lies Vers 11.",
           "V. 11: Er ist würdig, denn er hat alles erschaffen, und durch seinen Willen ist alles."),
    ],
    explain=[
        E("Wer sind die 24 Ältesten?", "Häufige Deutungen: das ganze Gottesvolk, vertreten durch 12 Stämme und 12 Apostel (vgl. 21,12–14); himmlische Wesen, die Gott umgeben; oder ein Abbild der 24 Priesterabteilungen in 1Chr 24. Dispensationalisten sehen in ihnen oft die bereits entrückte Gemeinde."),
        E("Ist V. 1 die Entrückung?", "Dispensationalistische Ausleger lesen den Ruf „Komm hier herauf“ oft als Bild der Entrückung der Gemeinde; sie verweisen darauf, dass das Wort „Gemeinde“ von Kap. 4 bis 21 nicht mehr vorkommt. Die meisten anderen Ausleger verstehen den Vers als Ruf an Johannes selbst, wie bei anderen Propheten, die in Gottes Thronrat blicken (Jes 6; Hes 1)."),
        E("Woher kommen die vier Wesen?", "Sie verbinden Bilder aus Hes 1 (vier Gesichter: Mensch, Löwe, Stier, Adler) und Jes 6 (sechs Flügel, dreimal „heilig“). Sie werden meist als höchste Engelwesen verstanden, die die ganze Schöpfung vertreten."),
        E("Was ist ein „Sardis“?", "Ein rötlicher Edelstein, wohl Karneol. Jaspis war in der Antike oft ein heller, durchscheinender Stein.", "elbbk"),
    ],
    fact="Seit Irenäus und Hieronymus stehen die vier Wesen für die vier Evangelisten. Nach Hieronymus: Mensch für Matthäus, Löwe für Markus, Stier für Lukas, Adler für Johannes. Darum sind sie bis heute an vielen Kanzeln und in alten Evangelienbüchern zu sehen.",
    teaser="Gleich weint Johannes. Ein Ältester tröstet ihn mit einem Löwen – aber Johannes sieht etwas ganz anderes.")

sec("thron", [R(OFFB, 5, 1, 7)], "Löwe und Lamm",
    "In der Hand dessen, der auf dem Thron sitzt, liegt ein Buch mit sieben Siegeln. Niemand ist würdig, es zu öffnen, und Johannes weint. Ein Ältester sagt: Der Löwe aus Juda hat überwunden. Johannes schaut hin und sieht ein Lamm, das wie geschlachtet dasteht. Es nimmt das Buch.",
    focus="Achte auf den Unterschied zwischen dem, was Johannes hört (V. 5), und dem, was er sieht (V. 6).",
    quiz=[
        choice("Warum weint Johannes?", ["Weil niemand würdig ist, das Buch zu öffnen", "Weil er sich vor dem Thron fürchtet", "Weil die Gemeinden leiden", "Weil das Buch zerrissen ist"], 4, "Lies Vers 4.",
               "V. 4: Er weint sehr, weil niemand würdig ist, das Buch zu öffnen oder hineinzusehen."),
        order("In welcher Reihenfolge geschieht es?", ["Ein starker Engel fragt, wer würdig ist", "Johannes weint", "Ein Ältester spricht vom Löwen aus Juda", "Johannes sieht ein Lamm wie geschlachtet", "Das Lamm nimmt das Buch"],
              "V. 2–7: die Frage, das Weinen, die Ankündigung, das überraschende Bild, die Tat."),
        tf("Das Lamm in V. 6 hat sieben Hörner und sieben Augen.", True, 6, "Lies Vers 6.",
           "V. 6: sieben Hörner (Horn = Macht) und sieben Augen, die die sieben Geister Gottes sind."),
    ],
    explain=[
        E("Was ist das Buch mit sieben Siegeln?", "Eine Schriftrolle, innen und außen beschrieben und siebenfach versiegelt – wie ein römisches Testament, das erst geöffnet werden durfte, wenn alle Siegel gebrochen waren. Gedeutet wird es als Gottes Plan für die Geschichte, als Urkunde über das Erbe der Erde oder als das Buch, dessen Inhalt in den folgenden Kapiteln aufgerollt wird."),
        E("Löwe aus Juda, Wurzel Davids?", "Zwei messianische Titel: Jakob segnet Juda als jungen Löwen, von dem das Zepter nicht weicht (1Mo 49,9–10); Jes 11,1.10 spricht von einem Spross aus der Wurzel Isais, des Vaters Davids."),
        E("Warum hört Johannes das eine und sieht das andere?", "Dieses Muster kommt mehrmals im Buch vor (z. B. 7,4 und 7,9). Viele Ausleger verstehen das Gesehene als Deutung des Gehörten: Der Löwe siegt als geschlachtetes Lamm. Andere halten beides für gleichrangige Bilder derselben Person."),
    ],
    cards=["lamm"],
    teaser="Das Lamm hat das Buch genommen. Jetzt singen alle – und Johannes beginnt, die Sänger zu zählen.")

sec("thron", [R(OFFB, 5, 8, 14)], "Das neue Lied",
    "Die Wesen und die Ältesten fallen vor dem Lamm nieder, mit Harfen und Schalen voll Räucherwerk, den Gebeten der Heiligen. Sie singen ein neues Lied: Das Lamm ist würdig, denn es wurde geschlachtet und hat Menschen aus allen Völkern für Gott erkauft. Unzählige Engel stimmen ein, dann jedes Geschöpf im Himmel, auf der Erde, unter der Erde und im Meer.",
    quiz=[
        choice("Was ist das Räucherwerk in den goldenen Schalen?", ["Die Gebete der Heiligen", "Das Blut des Lammes", "Die Tränen der Märtyrer", "Die Ehre der Nationen"], 8, "Lies Vers 8.",
               "V. 8: Das Räucherwerk sind die Gebete der Heiligen."),
        error("Das Lamm hat für Gott Menschen erkauft aus [Israel] und hat sie zu Königen und Priestern gemacht.", "jedem", 9,
              "V. 9: aus jedem Stamm, jeder Sprache, jedem Volk und jeder Nation."),
        choice("Wer singt am Ende (V. 13)?", ["Jedes Geschöpf im Himmel, auf der Erde, unter der Erde und im Meer", "Nur die 24 Ältesten", "Nur die Engel", "Die sieben Gemeinden"], 13, "Lies Vers 13.",
               "V. 13: Der Kreis wird immer größer – Wesen und Älteste, dann unzählige Engel, schließlich die ganze Schöpfung."),
    ],
    explain=[
        E("Was ist neu an dem Lied?", "Im Alten Testament wird oft ein „neues Lied“ gesungen, wenn Gott neu gehandelt hat (Ps 96,1; Jes 42,10). Hier ist der Anlass ausdrücklich genannt: Das Lamm wurde geschlachtet und hat erkauft (V. 9)."),
        E("Was heißt „erkauft“?", "Das griechische Wort agorazo stammt vom Marktplatz und wurde auch für den Freikauf von Sklaven gebraucht. Wie das Blut Christi „erkauft“ – als Lösegeld, als Opfer, als Befreiung –, darüber gibt es in den Kirchen verschiedene, sich ergänzende Erklärungen."),
        E("Ist es richtig, das Lamm anzubeten?", "Der Text zeigt genau das: Dieselbe Anbetung, die in 4,11 dem Schöpfer gilt, gilt in 5,12–13 dem Lamm. In 19,10 und 22,9 dagegen wehrt ein Engel ab, als Johannes ihn anbeten will. Die Alte Kirche sah darin einen der Texte, die zur Lehre von der Gottheit Christi führten."),
    ],
    memory_verse=MV(R(OFFB, 5, 12), "Würdig ist das Lamm, das geschlachtet worden ist"),
    prayer={"text": "Dich, Gott, loben wir, dich, Herr, bekennen wir. Dich, den ewigen Vater, verehrt die ganze Erde. Dir rufen alle Engel, die Himmel und alle Mächte, dir rufen Cherubim und Seraphim mit nie endender Stimme zu: Heilig, heilig, heilig, Herr, Gott der Heerscharen.",
            "source": "Te Deum, 4. Jahrhundert (eigene Übersetzung)"},
    teaser="Das Lamm bricht das erste Siegel. Was herauskommt, ist das bekannteste Bild des ganzen Buches.")

# ───────────────────────── 3 · Siegel, Gebete und Zeugen ─────────────────────────
sec("siegel", [R(OFFB, 6, 1, 8)], "Die vier Reiter",
    "Das Lamm öffnet die ersten vier Siegel. Jedes Mal ruft eines der Wesen „Komm!“, und ein Reiter erscheint: auf einem weißen Pferd mit Bogen und Krone, auf einem roten, das den Frieden nimmt, auf einem schwarzen mit einer Waage und auf einem fahlen, dessen Name Tod ist. Sie bekommen Macht über ein Viertel der Erde.",
    quiz=[
        order("In welcher Reihenfolge erscheinen die Pferde?", ["Weiß", "Feuerrot", "Schwarz", "Fahl"], "V. 2, 4, 5 und 8.", "Lies Vers 2–8."),
        choice("Was hält der Reiter auf dem schwarzen Pferd?", ["Eine Waage", "Einen Bogen", "Ein großes Schwert", "Eine Sichel"], 5, "Lies Vers 5.",
               "V. 5: eine Waage – dazu passen die Getreidepreise in V. 6."),
        choice("Wer öffnet die Siegel?", ["Das Lamm", "Einer der Ältesten", "Ein starker Engel", "Johannes"], 1, "Lies Vers 1.",
               "V. 1: Das Lamm öffnet die Siegel. Die Reiter bekommen ihre Macht gegeben (V. 2.4.8)."),
    ],
    explain=[
        E("Was bedeuten die Preise in V. 6?", "Ein Chönix war etwa ein Liter Getreide, die Tagesration eines Mannes; ein Denar war der Tageslohn eines Arbeiters (Mt 20,2). Ein ganzer Tageslohn für das eigene Brot oder für die billigere Gerste: eine Teuerung, bei der Familien hungern. Öl und Wein bleiben verschont – deutet das auf eine begrenzte Not hin oder auf eine, die die Reichen weniger trifft? Ausleger antworten verschieden."),
        E("Wer ist der weiße Reiter?", "Manche sehen in ihm Christus oder den Siegeszug des Evangeliums, weil in 19,11 Christus auf einem weißen Pferd reitet. Andere halten ihn für einen Eroberer oder einen falschen Christus, weil er in einer Reihe mit Krieg, Hunger und Tod steht. Manche denken an die Parther, ein Reitervolk mit gefürchteten Bogenschützen an der Ostgrenze Roms."),
        E("Wann geschieht das?", "Futuristische Ausleger setzen die Siegel in eine künftige siebenjährige Drangsal. Präteristische beziehen sie auf Kriege und Hungersnöte im 1. Jahrhundert, idealistische auf Krieg, Hunger und Tod in jeder Epoche, wie Jesus sie in Mk 13,7–8 ankündigt."),
    ],
    cards=["zahlen"],
    try_="Lies Sach 1,8–10 und 6,1–5. Was haben die farbigen Pferde dort für eine Aufgabe?",
    teaser="Beim fünften Siegel kommen keine Reiter. Es kommt eine Frage, die viele Psalmen stellen.")

sec("siegel", [R(OFFB, 6, 9, 17)], "Wie lange noch?",
    "Unter dem Altar sieht Johannes die Seelen derer, die wegen des Wortes Gottes getötet wurden. Sie rufen: Bis wann richtest du nicht? Sie bekommen weiße Gewänder und sollen noch eine kleine Zeit ruhen. Beim sechsten Siegel bebt die Erde, die Sonne wird schwarz, die Sterne fallen. Könige und Sklaven verstecken sich vor dem Zorn des Lammes.",
    quiz=[
        who("Bis wann, o Herrscher, der du heilig und wahrhaftig bist, richtest und rächst du nicht unser Blut", R(OFFB, 6, 10),
            ["Die Seelen unter dem Altar", "Die 24 Ältesten", "Die Könige der Erde", "Die vier lebendigen Wesen"],
            "V. 9–10: die Seelen derer, die um des Wortes Gottes willen geschlachtet wurden."),
        choice("Was wird den Seelen gesagt?", ["Sie sollen noch eine kleine Zeit ruhen", "Ihr Blut ist schon gerächt", "Sie sollen auf die Erde zurückkehren", "Sie sollen schweigen"], 11, "Lies Vers 11.",
               "V. 11: Sie bekommen weiße Gewänder und sollen noch eine kleine Zeit ruhen, bis die Zahl ihrer Mitknechte voll ist."),
        tf("Nach V. 15 verstecken sich nur die Könige und Mächtigen.", False, 15, "Lies Vers 15.",
           "V. 15: Könige, Große, Reiche, Starke – und jeder Sklave und Freie."),
    ],
    explain=[
        E("Ist ein Rachegebet erlaubt?", "Die Märtyrer nehmen die Rache nicht selbst in die Hand, sie legen sie in Gottes Hand – wie viele Klagepsalmen (Ps 79,10; 94,1–3). Gott weist ihre Frage nicht zurück, aber er lässt sie warten. Paulus schreibt ähnlich in Röm 12,19."),
        E("Ist das schon das Ende?", "Das sechste Siegel klingt wie der Weltuntergang, aber danach geht das Buch weiter. Darum fragen Ausleger: Erzählt das Buch nacheinander, oder blickt es mehrfach auf das Ende? Die Bilder stammen aus prophetischen Gerichtsworten (Jes 13,10; 34,4; Joel 3,4), die schon dort große Umbrüche in der Geschichte beschreiben."),
        E("Was ist ein „härener Sack“?", "Grobes Tuch aus Ziegen- oder Kamelhaar, dunkel und rau, das man zur Trauer trug.", "elbbk"),
    ],
    prayer={"ref": R(PS, 94, 3), "source": "Psalm 94,3"},
    teaser="Der Abschnitt endete mit einer Frage: Wer kann bestehen? Der nächste antwortet – mit einer sehr genauen Zahl.")

sec("siegel", [R(OFFB, 7, 1, 8)], "Die 144.000",
    "Vier Engel halten die Winde fest, damit der Erde noch nichts geschieht. Ein anderer Engel mit dem Siegel des lebendigen Gottes ruft: Erst müssen die Knechte Gottes an ihren Stirnen versiegelt werden. Johannes hört die Zahl der Versiegelten: 144.000, je 12.000 aus zwölf Stämmen Israels.",
    quiz=[
        choice("Wo werden die Knechte Gottes versiegelt?", ["An ihren Stirnen", "An ihrer rechten Hand", "Auf ihren Kleidern", "An ihren Türen"], 3, "Lies Vers 3.",
               "V. 3: an den Stirnen – das Gegenbild zum Malzeichen des Tieres in 13,16."),
        tf("Johannes sieht die 144.000 in V. 4.", False, 4, "Lies Vers 4 genau.",
           "V. 4: Er hört ihre Zahl. Was er danach sieht, folgt im nächsten Abschnitt."),
        choice("Welcher Stamm fehlt in der Liste?", ["Dan", "Juda", "Levi", "Benjamin"], 5, "Lies Vers 5–8 und vergleiche mit den zwölf Söhnen Jakobs.",
               "V. 5–8: Dan fehlt, ebenso Ephraim. Dafür stehen Levi und Joseph neben Manasse in der Liste."),
    ],
    explain=[
        E("Wer sind die 144.000?", "Dispensationalisten verstehen sie als Juden, die in der Endzeit zum Glauben an Jesus kommen – unterschieden von der Gemeinde. Viele andere Ausleger, katholisch, orthodox wie evangelisch, sehen in ihnen das ganze Gottesvolk aus Juden und Heiden: 12 × 12 × 1000, die vollständige Zahl, als Heer aufgestellt wie bei der Musterung in 4Mo 1. Sie verweisen darauf, dass Johannes in V. 9 dieselbe Gruppe als unzählbare Menge sieht."),
        E("Was bedeutet das Siegel?", "In der Antike markierte ein Siegel Eigentum und Schutz. Vorbild ist Hes 9,4–6: Wer an der Stirn gezeichnet ist, wird im Gericht verschont. Die Versiegelten werden also nicht aus der Not herausgenommen, sondern in ihr als Gottes Eigentum gekennzeichnet."),
        E("Warum fehlt Dan?", "Der Text nennt keinen Grund. Irenäus vermutete im 2. Jahrhundert, aus Dan werde der Antichrist kommen. Andere verweisen darauf, dass Dan in Ri 18 als erster Stamm Götzendienst einführte. Auch im Alten Testament schwanken die Stammeslisten."),
    ],
    teaser="Johannes hat eine Zahl gehört. Jetzt dreht er sich um und sieht eine Menge, die niemand zählen kann.")

sec("siegel", [R(OFFB, 7, 9, 17)], "Die Menge, die niemand zählen konnte",
    "Johannes sieht eine riesige Menge aus allen Nationen, in weißen Gewändern und mit Palmzweigen vor dem Thron. Ein Ältester fragt, wer sie sind, und erklärt: Sie kommen aus der großen Drangsal und haben ihre Kleider im Blut des Lammes weiß gewaschen. Sie werden nicht mehr hungern noch dürsten; Gott wird jede Träne abwischen.",
    quiz=[
        choice("Woher kommen die Menschen in weißen Gewändern?", ["Aus der großen Drangsal", "Aus dem Stamm Juda", "Aus den sieben Gemeinden", "Aus dem Totenreich"], 14, "Lies Vers 14.",
               "V. 14: aus der großen Drangsal; sie haben ihre Kleider im Blut des Lammes gewaschen."),
        who("Diese, die mit weißen Gewändern bekleidet sind, wer sind sie", R(OFFB, 7, 13), ["Einer der Ältesten", "Johannes", "Ein starker Engel", "Das Lamm"],
            "V. 13: Ein Ältester stellt die Frage – und beantwortet sie, als Johannes zurückfragt."),
        choice("Wer weidet die Menge nach V. 17?", ["Das Lamm", "Die Ältesten", "Die Engel", "Der Löwe aus Juda"], 17, "Lies Vers 17.",
               "V. 17: Das Lamm wird ihr Hirte – ein Lamm, das weidet."),
    ],
    explain=[
        E("Ist das dieselbe Gruppe wie die 144.000?", "Wie bei Löwe und Lamm (5,5–6) hört Johannes das eine und sieht das andere. Viele Ausleger schließen daraus: Die gezählte Heerschar Israels und die unzählbare Menge aus allen Völkern sind dasselbe Gottesvolk. Dispensationalisten sehen zwei Gruppen: gläubige Juden und gläubige Menschen aus den Nationen während der Drangsal."),
        E("Was ist die „große Drangsal“?", "Dispensationalisten verstehen sie als eine künftige Zeit von sieben Jahren (nach Dan 9,27). Andere denken an die Verfolgungen der ersten Jahrhunderte oder an die ganze Leidenszeit der Kirche. Jesus spricht in Mt 24,21 von einer großen Bedrängnis; die Jünger bezogen ähnliche Worte auch auf die Zerstörung Jerusalems."),
        E("Warum Palmzweige?", "Palmzweige trug man beim Laubhüttenfest (3Mo 23,40) und beim Einzug Jesu in Jerusalem (Joh 12,13). Sie stehen für Sieg und Freude. Auch die Bilder von Wasser und Zelt in V. 15–17 erinnern an das Laubhüttenfest."),
    ],
    try_="Lies Jes 25,8 und Jes 49,10 und vergleiche sie mit Offb 7,16–17. Welche Worte hat Johannes aufgegriffen?",
    teaser="Das siebte Siegel wird geöffnet. Was folgt, ist das Letzte, womit man in diesem lauten Buch rechnen würde.")

sec("siegel", [R(OFFB, 8, 1, 5)], "Eine halbe Stunde Stille",
    "Als das Lamm das siebte Siegel öffnet, ist es im Himmel etwa eine halbe Stunde still. Sieben Engel bekommen sieben Posaunen. Ein anderer Engel steht am Altar und bringt viel Räucherwerk mit den Gebeten aller Heiligen vor Gott. Dann füllt er das Räucherfass mit Feuer vom Altar und wirft es auf die Erde.",
    focus="Achte darauf, was mit den Gebeten geschieht – und was danach auf die Erde fällt.",
    quiz=[
        estimate("Wie lange ist es im Himmel still?", 0, 60, 30, "Minuten", "V. 1: etwa eine halbe Stunde.", 1, "Lies Vers 1.", 5),
        choice("Was steigt mit dem Rauch des Räucherwerks vor Gott auf?", ["Die Gebete der Heiligen", "Der Lobgesang der Engel", "Das Blut der Märtyrer", "Die Namen der Versiegelten"], 4, "Lies Vers 4.",
               "V. 3–4: Das Räucherwerk steigt mit den Gebeten aller Heiligen vor Gott auf."),
        tf("Der Engel wirft das Räucherfass mit Feuer vom Altar auf die Erde.", True, 5, "Lies Vers 5.",
           "V. 5: Er füllt es mit Feuer vom Altar und wirft es auf die Erde; es folgen Donner, Blitze und ein Erdbeben."),
    ],
    explain=[
        E("Folgen Siegel, Posaunen und Schalen aufeinander?", "Zwei Grundmodelle: Viele futuristische Ausleger lesen die drei Siebenerreihen als zeitliche Abfolge; das siebte Siegel enthält dann die sieben Posaunen. Seit Victorinus von Pettau (um 300) und Augustinus lesen viele die Reihen als Wiederholung (Rekapitulation): Dreimal wird derselbe Zeitraum bis zum Ende gezeigt, jedes Mal heftiger. Sie verweisen darauf, dass jede Reihe mit Donner, Blitzen und Erdbeben endet (8,5; 11,19; 16,18)."),
        E("Warum die Stille?", "Der Text erklärt sie nicht. Manche denken an das Schweigen vor Gottes Gericht (Hab 2,20; Zef 1,7), andere an die Stille im Tempel, während das Räucheropfer dargebracht wurde, sodass die Gebete gehört werden."),
        E("Was ist ein Räucherfass?", "Eine Pfanne oder Schale, in der glühende Kohlen vom Altar getragen wurden, auf die man Weihrauch streute. Im Tempel stand der Räucheraltar vor dem Vorhang zum Allerheiligsten (2Mo 30,1–8)."),
    ],
    prayer={"ref": R(PS, 141, 2), "source": "Psalm 141,2"},
    teaser="Wir springen über die Posaunen. Johannes bekommt einen Messstab in die Hand – und dann treten zwei Zeugen auf, die an zwei bekannte Propheten erinnern.")

sec("siegel", [R(OFFB, 11, 1, 13)], "Die zwei Zeugen",
    "Johannes soll den Tempel Gottes vermessen; der äußere Hof aber ist den Nationen gegeben, die die heilige Stadt 42 Monate zertreten. Zwei Zeugen weissagen 1260 Tage, mit Vollmacht, den Regen zu verschließen und Wasser in Blut zu verwandeln. Das Tier aus dem Abgrund tötet sie, ihre Leichen liegen auf der Straße. Nach dreieinhalb Tagen stehen sie auf und steigen in den Himmel.",
    bridge="Dazwischen blasen sechs Engel ihre Posaunen: Plagen treffen Land, Meer, Wasser und Gestirne, Heuschrecken und Reiterheere ziehen heran (8,6–9,21). Ein Engel gibt Johannes ein kleines Buch zu essen (Kap. 10).",
    quiz=[
        choice("Was soll Johannes nicht vermessen?", ["Den Hof außerhalb des Tempels", "Den Altar", "Die, die im Tempel anbeten", "Den Tempel selbst"], 2, "Lies Vers 1–2.",
               "V. 2: Den äußeren Hof soll er auslassen, denn er ist den Nationen gegeben."),
        choice("An welche Propheten erinnern die Vollmachten der Zeugen in V. 6?", ["Elia und Mose", "Jesaja und Jeremia", "Daniel und Hesekiel", "Samuel und Nathan"], 6, "Lies Vers 6 und denk an 1Kön 17,1 und 2Mo 7,20.",
               "V. 6: Den Regen verschließen wie Elia (1Kön 17,1), Wasser in Blut verwandeln wie Mose (2Mo 7,20)."),
        order("In welcher Reihenfolge geschieht es?", ["Die Zeugen weissagen 1260 Tage", "Das Tier tötet sie", "Ihre Leichen liegen dreieinhalb Tage auf der Straße", "Der Geist des Lebens kommt in sie", "Sie steigen in einer Wolke in den Himmel"],
              "V. 3–12."),
    ],
    explain=[
        E("Wer sind die zwei Zeugen?", "Futuristische Ausleger erwarten zwei wirkliche Propheten in der Endzeit, oft Mose und Elia, in der Alten Kirche meist Henoch und Elia, weil beide nicht starben. Viele andere sehen in ihnen ein Bild für die bezeugende Kirche: V. 4 nennt sie zwei Leuchter, und Leuchter sind in 1,20 die Gemeinden. Zwei Zeugen braucht es nach 5Mo 19,15 für ein gültiges Zeugnis."),
        E("Welcher Tempel ist gemeint?", "Präteristen denken an den Tempel in Jerusalem vor seiner Zerstörung im Jahr 70. Dispensationalisten erwarten einen wiederaufgebauten Tempel in der Endzeit. Andere lesen den Tempel als Bild für das Gottesvolk, wie Paulus die Gemeinde Tempel nennt (1Kor 3,16): geschützt im Innersten, äußerlich bedrängt."),
        E("Welche Stadt ist Sodom und Ägypten?", "V. 8 sagt, es sei die Stadt, in der ihr Herr gekreuzigt wurde – also Jerusalem. Das Wort „geistlicherweise“ zeigt, dass der Text hier selbst bildhaft redet. Manche sehen darin zugleich jede Stadt, die Gottes Boten verwirft."),
    ],
    fact="Drei Zeitangaben in diesem Abschnitt und im nächsten meinen dieselbe Dauer: 42 Monate (11,2), 1260 Tage (11,3; 12,6) und eine Zeit, zwei Zeiten und eine halbe Zeit (12,14) – jeweils dreieinhalb Jahre, die Hälfte von sieben.",
    teaser="Gleich springen wir mehr als 600 Jahre zurück – zu einem Propheten, der in Babylon vier Tiere aus dem Meer steigen sah.")

# ───────────────────────── 4 · Der Drache und die Tiere ─────────────────────────
sec("tiere", [R(DAN, 7, 1, 14)], "Daniel: vier Tiere aus dem Meer",
    "Daniel sieht in einem Traum vier Tiere aus dem aufgewühlten Meer steigen: einen Löwen mit Adlerflügeln, einen Bären, einen Leoparden mit vier Köpfen und ein viertes, schreckliches Tier mit zehn Hörnern, aus denen ein kleines Horn mit großem Mund wächst. Dann setzt sich der Alte an Tagen auf seinen Thron. Einer wie ein Menschensohn kommt mit den Wolken und bekommt ewige Herrschaft.",
    bridge="Nach der siebten Posaune ruft der Himmel, das Reich der Welt gehöre nun Gott und seinem Christus (11,15–19). Bevor die Offenbarung ihre Tiere zeigt, lesen wir die Vision, auf die sie sich bezieht.",
    place="babylon",
    focus="Achte auf jedes Tier genau. Im übernächsten Abschnitt der Offenbarung tauchen ihre Merkmale wieder auf.",
    quiz=[
        order("In welcher Reihenfolge steigen die Tiere auf?", ["Wie ein Löwe mit Adlerflügeln", "Wie ein Bär", "Wie ein Leopard", "Ein schreckliches Tier mit zehn Hörnern"], "V. 4–7.", "Lies Vers 4–7."),
        choice("Was redet das kleine Horn?", ["Große Worte", "Weissagungen", "Lügen über Daniel", "Nichts – es schweigt"], 8, "Lies Vers 8.",
               "V. 8: Es hat Augen wie Menschenaugen und einen Mund, der große Worte redet."),
        choice("Was bekommt der, der wie ein Menschensohn mit den Wolken kommt?", ["Herrschaft, Herrlichkeit und ein Königtum, das nicht zerstört wird", "Ein versiegeltes Buch", "Einen Platz unter den Ältesten", "Die Herrschaft über das vierte Tier für eine Zeit"], 14, "Lies Vers 14.",
               "V. 14: Herrschaft, Herrlichkeit, Königtum; alle Völker dienen ihm, seine Herrschaft vergeht nicht."),
    ],
    explain=[
        E("Was bedeuten die Tiere?", "Der Engel deutet sie selbst als vier Könige oder Königreiche (V. 17.23). Die jüdische und christliche Tradition liest meist: Babylon, Medien-Persien, Griechenland, Rom; das kleine Horn wird mit einem späteren Herrscher oder dem Antichrist verbunden. Andere Ausleger zählen Babylon, Medien, Persien und Griechenland und sehen im kleinen Horn den Seleukidenkönig Antiochus IV., der 167 v. Chr. den Tempel entweihte. Beide Lesarten finden sich unter gläubigen Auslegern."),
        E("Was ist das Meer?", "Im Alten Testament steht das tobende Meer oft für Chaos und gottfeindliche Mächte (Ps 74,13; Jes 51,9–10). Dass die Tiere aus dem Meer steigen, sagt etwas über ihre Herkunft. In Offb 21,1 heißt es von der neuen Welt, dass das Meer nicht mehr ist."),
        E("Wer ist der Alte an Tagen?", "Ein Bild für Gott als den ewigen Richter: weißes Gewand, Haar wie reine Wolle, ein Thron aus Feuerflammen (V. 9). In Offb 1,14 trägt Christus dieses Merkmal."),
    ],
    cards=["daniel"],
    fact="Dan 2,4b bis 7,28 ist nicht auf Hebräisch geschrieben, sondern auf Aramäisch, der Verkehrssprache des babylonischen und persischen Reiches. Kap. 7 ist das letzte aramäische Kapitel des Buches.",
    teaser="Zurück in der Offenbarung erscheint ein Zeichen am Himmel: eine Frau, die in den Wehen schreit, und vor ihr ein Drache.")

sec("tiere", [R(OFFB, 12, 1, 9)], "Die Frau und der Drache",
    "Am Himmel erscheint eine Frau, mit der Sonne bekleidet, mit zwölf Sternen gekrönt, in Geburtswehen. Ein feuerroter Drache mit sieben Köpfen wartet, um ihr Kind zu verschlingen. Sie bringt einen Sohn zur Welt, der die Nationen weiden soll; er wird zu Gottes Thron entrückt. Die Frau flieht in die Wüste. Michael und seine Engel kämpfen mit dem Drachen und werfen ihn auf die Erde.",
    bridge="Wir sind zurück in der Offenbarung, direkt nach der siebten Posaune (11,19).",
    quiz=[
        choice("Was will der Drache mit dem Kind der Frau tun?", ["Es verschlingen, sobald es geboren ist", "Es in die Wüste tragen", "Es zum König machen", "Es vor Michael verstecken"], 4, "Lies Vers 4.",
               "V. 4: Er steht vor der Frau, um ihr Kind zu verschlingen."),
        choice("Wer kämpft im Himmel gegen den Drachen?", ["Michael und seine Engel", "Das Lamm und die Ältesten", "Die zwei Zeugen", "Die vier lebendigen Wesen"], 7, "Lies Vers 7.",
               "V. 7: Michael und seine Engel."),
        tf("V. 9 nennt den Drachen ausdrücklich die alte Schlange, den Teufel und Satan.", True, 9, "Lies Vers 9.",
           "V. 9: Der Text deutet sein Bild hier selbst – mit einem Rückgriff auf die Schlange aus 1Mo 3."),
    ],
    explain=[
        E("Wer ist die Frau?", "Drei Hauptlesarten: Israel, aus dem der Messias kommt (die zwölf Sterne erinnern an Josefs Traum, 1Mo 37,9); Maria, die Mutter Jesu – so liest die katholische und orthodoxe Tradition, die Kirche liest den Text am Fest Mariä Himmelfahrt; oder das Gottesvolk des Alten und Neuen Bundes, das in V. 17 weitere Nachkommen hat. Viele Ausleger verbinden die Lesarten."),
        E("Wer ist der Sohn?", "V. 5 zitiert Ps 2,9: Er soll die Nationen mit eiserner Rute weiden. Die meisten Ausleger aller Traditionen sehen hier Christus. Auffällig ist, dass zwischen Geburt und Entrückung nichts erzählt wird: Das ganze Leben Jesu steht in einem Satz."),
        E("Wann wurde der Drache gestürzt?", "Futuristische Ausleger setzen den Kampf in die Mitte einer künftigen Drangsal. Viele andere verbinden ihn mit Tod und Auferstehung Jesu: In Lk 10,18 sieht Jesus den Satan wie einen Blitz vom Himmel fallen, und Joh 12,31 sagt, nun werde der Fürst dieser Welt hinausgeworfen."),
    ],
    teaser="Nach dem Sturz ruft eine Stimme im Himmel, wodurch die Verklagten den Drachen besiegt haben. Die Antwort ist kein Schwert.")

sec("tiere", [R(OFFB, 12, 10, 17)], "Überwunden durch das Blut des Lammes",
    "Eine laute Stimme im Himmel ruft: Jetzt ist das Reich Gottes gekommen, denn der Verkläger ist gestürzt. Die Brüder haben ihn überwunden durch das Blut des Lammes und das Wort ihres Zeugnisses. Der Drache weiß, dass er wenig Zeit hat, und verfolgt die Frau; sie wird mit Adlerflügeln in die Wüste getragen. Dann führt er Krieg gegen ihre übrigen Nachkommen.",
    quiz=[
        choice("Was tat der Drache nach V. 10 vor Gott?", ["Er verklagte die Brüder Tag und Nacht", "Er bat um Gnade", "Er sang ein Lied", "Er forderte das Buch"], 10, "Lies Vers 10.",
               "V. 10: der Verkläger unserer Brüder, der sie Tag und Nacht vor Gott verklagte."),
        error("Sie haben ihn überwunden um des Blutes des Lammes und um des [Schwertes] ihres Zeugnisses willen.", "Wortes", 11,
              "V. 11: durch das Blut des Lammes und das Wort ihres Zeugnisses – und weil sie ihr Leben nicht über alles liebten."),
        choice("Warum hat der Teufel große Wut?", ["Weil er weiß, dass er wenig Zeit hat", "Weil die Frau ihn verklagt hat", "Weil das Kind gestorben ist", "Weil Michael ihn gefesselt hat"], 12, "Lies Vers 12.",
               "V. 12: Er weiß, dass er wenig Zeit hat."),
    ],
    explain=[
        E("Woher kommt „Verkläger“?", "Satan heißt auf Hebräisch „Ankläger, Widersacher“. In Hiob 1–2 und Sach 3,1 tritt er vor Gott als Ankläger auf. Hier verliert er seinen Platz vor Gott."),
        E("Warum Adlerflügel und Wüste?", "Bilder aus der Auszugsgeschichte: Gott trug Israel wie auf Adlerflügeln aus Ägypten (2Mo 19,4) und ernährte es 40 Jahre in der Wüste. Die Frau wird geschützt, aber nicht aus der Wüste herausgeholt."),
        E("Was ist die Zeit von V. 14?", "Eine Zeit, zwei Zeiten und eine halbe Zeit, also dreieinhalb Jahre – dieselbe Formel wie in Dan 7,25 und dieselbe Dauer wie die 1260 Tage in V. 6. Ob wörtlich oder als Bild für eine begrenzte Zeit der Bedrängnis: Darin unterscheiden sich die Lesarten."),
    ],
    prayer={"ref": R(PS, 46, 2, 3), "source": "Psalm 46,2–3"},
    teaser="Der Drache steht am Ufer. Aus dem Meer steigt ein Tier, das dir bekannt vorkommen wird, wenn du Daniel 7 noch im Kopf hast.")

sec("tiere", [R(OFFB, 13, 1, 10)], "Das Tier aus dem Meer",
    "Aus dem Meer steigt ein Tier mit zehn Hörnern und sieben Köpfen, wie ein Leopard, mit Bärenfüßen und Löwenmaul. Der Drache gibt ihm seine Macht. Einer seiner Köpfe hat eine tödliche Wunde, die geheilt ist, und die ganze Erde staunt und betet es an. Es lästert Gott 42 Monate und führt Krieg gegen die Heiligen. Hier ist das Ausharren der Heiligen gefragt.",
    focus="Achte darauf, welche Merkmale der vier Tiere aus Daniel 7 hier in einem einzigen Tier zusammenkommen.",
    quiz=[
        choice("Wer gibt dem Tier seine Macht und seinen Thron?", ["Der Drache", "Die Könige der Erde", "Das zweite Tier", "Babylon"], 2, "Lies Vers 2.",
               "V. 2: Der Drache gibt ihm seine Macht, seinen Thron und große Gewalt."),
        who("Wer ist dem Tier gleich? Und wer vermag mit ihm zu kämpfen", R(OFFB, 13, 4), ["Die Bewohner der Erde", "Die Heiligen", "Michael und seine Engel", "Daniel"],
            "V. 3–4: Die ganze Erde staunt über das Tier und betet es an."),
        tf("Nach V. 8 beten alle das Tier an, auch die, deren Namen im Buch des Lebens stehen.", False, 8, "Lies Vers 8.",
           "V. 8: Anbeten werden es die, deren Name nicht im Buch des Lebens des geschlachteten Lammes steht."),
    ],
    explain=[
        E("Wer ist das Tier?", "Präteristen sehen im Tier das Römische Reich und im geheilten Kopf Nero, von dem man nach seinem Tod erzählte, er kehre zurück. Futuristen erwarten eine künftige Person, den Antichrist, an der Spitze eines Weltreiches. Die Reformatoren lasen das Tier oft auf das Papsttum hin; heute vertritt das kaum eine Kirche mehr. Idealistische Ausleger sehen ein Muster: jede politische Macht, die Anbetung fordert."),
        E("Warum gleicht es den Tieren aus Daniel 7?", "Leopard, Bär, Löwe und zehn Hörner – das Tier vereint die vier Reiche Daniels in sich (Dan 7,4–7). Wie das kleine Horn redet es große Worte (Dan 7,8) und führt Krieg gegen die Heiligen (Dan 7,21). Die Zeit von 42 Monaten entspricht Dan 7,25."),
        E("Was heißt V. 10?", "Ein schwieriger Vers mit Varianten in den Handschriften. Die meisten Ausleger verstehen ihn mit Jer 15,2: Wer gefangen geführt wird, geht in Gefangenschaft – die Heiligen sollen nicht mit Gewalt zurückschlagen, sondern ausharren."),
    ],
    cards=["nero"],
    teaser="Das zweite Tier sieht aus wie ein Lamm. Und es hat eine Zahl, über die seit fast 2000 Jahren gerechnet wird.")

sec("tiere", [R(OFFB, 13, 11, 18)], "Das zweite Tier und die 666",
    "Ein zweites Tier steigt aus der Erde: Es hat Hörner wie ein Lamm und redet wie ein Drache. Es tut Zeichen, lässt Feuer vom Himmel fallen, lässt ein Bild des ersten Tieres machen und zum Reden bringen. Alle sollen ein Malzeichen an der rechten Hand oder der Stirn tragen; ohne es kann niemand kaufen oder verkaufen. Die Zahl des Tieres ist 666.",
    quiz=[
        choice("Wie sieht das zweite Tier aus?", ["Es hat zwei Hörner wie ein Lamm und redet wie ein Drache", "Es gleicht einem Leoparden", "Es hat sieben Köpfe", "Es hat Flügel wie ein Adler"], 11, "Lies Vers 11.",
               "V. 11: zwei Hörner wie ein Lamm – aber seine Sprache verrät es."),
        choice("Was kann man ohne das Malzeichen nicht?", ["Kaufen oder verkaufen", "Beten", "Reisen", "Heiraten"], 17, "Lies Vers 17.",
               "V. 17: Niemand kann kaufen oder verkaufen, der das Malzeichen nicht hat."),
        tf("Nach V. 18 ist die Zahl die eines Menschen.", True, 18, "Lies Vers 18.",
           "V. 18: Es ist eines Menschen Zahl – darum fordert der Vers dazu auf, sie zu berechnen."),
    ],
    explain=[
        E("Wie berechnet man eine Namenszahl?", "Im Hebräischen und Griechischen standen Buchstaben auch für Zahlen. Die Summe eines Namens nannte man Gematria. Schreibt man „Kaiser Nero“ in hebräischen Buchstaben (Neron Qesar), ergibt sich 666. Die lateinische Form ohne das letzte n ergibt 616 – und genau diese Zahl steht in einigen alten Handschriften. Futuristische Ausleger halten die Lösung für noch verborgen."),
        E("Was ist das Malzeichen?", "Das griechische charagma bezeichnete den Stempel auf Urkunden und das Bild auf Münzen, die den Kaiser zeigten. Viele Ausleger sehen darin ein Gegenbild zum Siegel Gottes an der Stirn (7,3) und zu 5Mo 6,8, wo Gottes Wort an Hand und Stirn gebunden wird: Es geht um Zugehörigkeit und um das, was das Handeln und Denken bestimmt. Futuristen erwarten zusätzlich ein wörtliches Zeichen in der Endzeit."),
        E("Wer ist das zweite Tier?", "In 16,13 und 19,20 heißt es „der falsche Prophet“. Präteristen denken an die Priesterschaft des Kaiserkults in Asia, Futuristen an einen religiösen Führer an der Seite des Antichrists, idealistische Ausleger an jede Religion, die sich in den Dienst der Macht stellt."),
    ],
    fact="Der Papyrus Oxyrhynchus 115, um 1900 in Ägypten ausgegraben und erst 2005 entziffert und veröffentlicht, ist eines der ältesten Bruchstücke von Offb 13 – und hat die Zahl 616. Schon Irenäus kannte diese Lesart um 180 und hielt sie für einen Abschreibfehler.",
    teaser="Nach den Tieren fliegen drei Engel über die Erde. Der erste hat eine Botschaft, die mit einem Wort beginnt, das eher nach guten Nachrichten klingt.")

sec("tiere", [R(OFFB, 14, 6, 13)], "Drei Engel",
    "Ein Engel fliegt mit einem ewigen Evangelium für alle Völker und ruft: Fürchtet Gott und betet den Schöpfer an. Ein zweiter ruft: Gefallen ist Babylon, die große. Ein dritter warnt: Wer das Tier anbetet, trinkt vom Wein des Zorns Gottes. Hier ist das Ausharren der Heiligen. Eine Stimme sagt: Glückselig die Toten, die im Herrn sterben.",
    bridge="Auf dem Berg Zion steht das Lamm mit den 144.000, die seinen Namen und den seines Vaters an der Stirn tragen (14,1–5).",
    quiz=[
        choice("Wem soll der erste Engel das ewige Evangelium verkünden?", ["Jeder Nation, jedem Stamm, jeder Sprache und jedem Volk", "Nur den Heiligen", "Nur Israel", "Den Königen der Erde"], 6, "Lies Vers 6.",
               "V. 6: denen, die auf der Erde wohnen, und jeder Nation, jedem Stamm, jeder Sprache und jedem Volk."),
        order("Was rufen die drei Engel, der Reihe nach?", ["Fürchtet Gott und gebt ihm Ehre", "Gefallen ist Babylon", "Wer das Tier anbetet, trinkt den Zorn Gottes"], "V. 7, 8 und 9–10."),
        choice("Warum sind die Toten, die im Herrn sterben, glückselig (V. 13)?", ["Sie ruhen von ihren Mühen, und ihre Werke folgen ihnen", "Sie werden sofort Engel", "Sie müssen nicht vor Gericht", "Sie herrschen über Babylon"], 13, "Lies Vers 13.",
               "V. 13: Sie ruhen von ihren Mühen, denn ihre Werke folgen ihnen nach."),
    ],
    explain=[
        E("Wie ist V. 10–11 zu verstehen?", "Die Bilder von Feuer, Schwefel und Rauch stammen aus dem Gericht über Sodom (1Mo 19,24.28) und über Edom (Jes 34,9–10). Ob sie eine ewige bewusste Qual beschreiben, eine endgültige Vernichtung oder in Bildern die Schwere des Gerichts, darüber sind sich Christen nicht einig. Die meisten Kirchen lehren eine ewige Trennung von Gott; manche Evangelikale vertreten die Vernichtung."),
        E("Warum „gefallen“ in der Vergangenheit?", "Der Ruf greift Jes 21,9 auf. In der Prophetie steht Künftiges oft in der Vergangenheit, so sicher ist es. Erzählt wird der Fall Babylons erst in Kap. 17–18."),
        E("Was heißt „im Herrn sterben“?", "In Christus sterben, also als jemand, der zu ihm gehört – unter den Umständen des Buches oft als Märtyrer. Der Vers ist bis heute ein häufiger Text bei christlichen Beerdigungen."),
    ],
    cards=["babylon"],
    memory_verse=MV(R(OFFB, 14, 13), "Glückselig die Toten, die im Herrn sterben, von nun an!"),
    teaser="Jetzt bekommt Babylon ein Gesicht: eine Frau in Purpur, betrunken – aber nicht von Wein.")

# ───────────────────────── 5 · Babylon fällt ─────────────────────────
sec("babylon", [R(OFFB, 17, 1, 6)], "Die Frau auf dem Tier",
    "Einer der Engel mit den Schalen führt Johannes in die Wüste, um ihm das Urteil über die große Hure zu zeigen. Er sieht eine Frau auf einem scharlachroten Tier mit sieben Köpfen und zehn Hörnern, in Purpur und Gold, mit einem goldenen Becher voller Gräuel. Auf ihrer Stirn steht: Babylon, die große. Sie ist betrunken vom Blut der Heiligen.",
    bridge="Sieben Engel gießen sieben Schalen des Zorns aus; die Könige der Erde versammeln sich an einem Ort namens Harmagedon (Kap. 15–16).",
    quiz=[
        choice("Wovon ist die Frau betrunken?", ["Vom Blut der Heiligen und der Zeugen Jesu", "Vom Wein der Könige", "Vom Rauch ihres Brandes", "Von ihrer eigenen Pracht"], 6, "Lies Vers 6.",
               "V. 6: vom Blut der Heiligen und vom Blut der Zeugen Jesu."),
        error("Auf ihrer Stirn steht der Name: Geheimnis, [Jerusalem], die große, die Mutter der Huren.", "Babylon", 5,
              "V. 5: Babylon, die große, die Mutter der Huren und der Gräuel der Erde."),
        tf("Johannes reagiert auf die Frau mit großer Verwunderung.", True, 6, "Lies Vers 6.",
           "V. 6: Er verwundert sich sehr – der Engel fragt im nächsten Vers, warum."),
    ],
    explain=[
        E("Warum „Hure“?", "Die Propheten nennen Untreue gegen Gott oft Hurerei (Hos 2; Hes 16). Auch die heidnische Stadt Ninive wird so genannt, wegen ihrer Verführung und ihres Handels (Nah 3,4). Hier steht das Bild für eine Macht, die die Könige der Erde verführt – eine Gegenfigur zur Braut des Lammes in Kap. 19 und 21."),
        E("Wie lesen die Kirchen Babylon?", "Die meisten Ausleger sehen zuerst Rom, das Christen verfolgte. Manche präteristische Ausleger denken an das abtrünnige Jerusalem. Reformatoren wie Luther deuteten Babylon auf das Papsttum; das gehört zur Geschichte der Reformationszeit und wird heute von den evangelischen Kirchen nicht mehr vertreten. Dispensationalisten erwarten ein künftiges religiöses oder wirtschaftliches System, manche eine wiederaufgebaute Stadt am Euphrat."),
        E("Was sind Purpur und Scharlach?", "Die teuersten Farbstoffe der Antike. Purpur wurde aus Meeresschnecken gewonnen und war Kaisern und hohen Beamten vorbehalten."),
    ],
    teaser="Der Engel erklärt das Geheimnis – mit sieben Bergen und sieben Königen. Seitdem rechnen Leser Kaiserlisten durch.")

sec("babylon", [R(OFFB, 17, 7, 18)], "Sieben Berge, sieben Könige",
    "Der Engel erklärt: Das Tier war, ist nicht und wird wieder aufsteigen. Die sieben Köpfe sind sieben Berge, auf denen die Frau sitzt, und zugleich sieben Könige: Fünf sind gefallen, einer ist, einer kommt noch. Die zehn Hörner sind zehn Könige, die mit dem Lamm Krieg führen, aber das Lamm besiegt sie. Am Ende wenden sie sich gegen die Hure und verbrennen sie.",
    quiz=[
        choice("Was sind die sieben Köpfe nach V. 9?", ["Sieben Berge, auf denen die Frau sitzt", "Sieben Gemeinden", "Sieben Engel", "Sieben Siegel"], 9, "Lies Vers 9.",
               "V. 9–10: sieben Berge – und zugleich sieben Könige."),
        choice("Warum besiegt das Lamm die zehn Könige?", ["Weil es Herr der Herren und König der Könige ist", "Weil sie untereinander uneins sind", "Weil Michael ihm hilft", "Weil die Frau sie verrät"], 14, "Lies Vers 14.",
               "V. 14: Das Lamm wird sie überwinden, denn es ist Herr der Herren und König der Könige."),
        tf("Nach V. 16 wenden sich das Tier und die zehn Hörner am Ende gegen die Hure.", True, 16, "Lies Vers 16.",
           "V. 16: Sie hassen die Hure, machen sie öde und nackt und verbrennen sie – das Böse zerstört sich selbst."),
    ],
    explain=[
        E("Welche sieben Berge?", "Rom war schon in der Antike als die Stadt auf sieben Hügeln bekannt; so lesen die meisten Ausleger V. 9. Die sieben Könige werden dann oft als römische Kaiser gezählt, doch je nachdem, mit wem man beginnt, kommt man auf verschiedene Kaiser. Andere verstehen „sieben“ als Zahl der Vollständigkeit: alle Weltreiche der Geschichte. Futuristen erwarten ein künftiges Reich mit zehn Königen."),
        E("Was heißt „war und ist nicht und wird kommen“?", "Eine Parodie auf Gottes Namen, der ist, der war und der kommt (1,8; 4,8). Viele Ausleger sehen darin auch eine Anspielung auf die Sage vom wiederkehrenden Nero. Das Tier ahmt Gott und das Lamm nach – auch das Lamm war tot und lebt."),
        E("Wer sind die Berufenen und Auserwählten?", "Die mit dem Lamm sind (V. 14). Sie siegen nicht durch eigene Waffen, sondern stehen an der Seite dessen, der siegt."),
    ],
    teaser="Babylon brennt. Und die Ersten, die weinen, sind nicht ihre Opfer, sondern ihre Kunden.")

sec("babylon", [R(OFFB, 18, 9, 20)], "Die Klage der Kaufleute",
    "Könige, Kaufleute und Seeleute stehen von fern, sehen den Rauch und klagen: Wehe, die große Stadt, in einer Stunde ist ihr Gericht gekommen! Die Kaufleute zählen ihre Waren auf, die niemand mehr kauft – von Gold und Seide über Zimt und Weizen bis zu Leibeigenen und Menschenseelen. Der Himmel und die Heiligen dagegen sollen sich freuen.",
    bridge="Ein Engel ruft, Babylon sei gefallen, und eine Stimme fordert Gottes Volk auf, aus ihr hinauszugehen, um nicht an ihren Sünden teilzuhaben (18,1–8).",
    focus="Achte darauf, worüber die Klagenden eigentlich trauern – und womit die Warenliste endet.",
    quiz=[
        choice("Warum weinen die Kaufleute?", ["Weil niemand mehr ihre Ware kauft", "Weil sie ihre Sünden bereuen", "Weil ihre Familien in der Stadt waren", "Weil Gott sie gestraft hat"], 11, "Lies Vers 11.",
               "V. 11: Sie trauern, weil niemand mehr ihre Ware kauft."),
        estimate("Wie lange dauert es, bis Babylons Gericht kommt?", 1, 24, 1, "Stunde(n)", "V. 10, 17 und 19: in einer Stunde – dreimal wiederholt.", 10, "Lies Vers 10."),
        choice("Womit endet die Liste der Waren in V. 13?", ["Mit Leibeigenen und Menschenseelen", "Mit Gold und Silber", "Mit Wein und Öl", "Mit Pferden und Wagen"], 13, "Lies Vers 13.",
               "V. 13: Am Ende der Luxusliste stehen Menschen – Leiber und Seelen."),
    ],
    explain=[
        E("Woher kommt diese Klage?", "Sie ist der Klage über die Handelsstadt Tyrus in Hes 26–27 nachgebildet, mit Königen, Kaufleuten, Seeleuten und einer langen Warenliste. Auch dort werden am Ende Menschen gehandelt (Hes 27,13)."),
        E("Was ist „Thynenholz“ und „Amomum“?", "Thynenholz (Thuja) war ein duftendes nordafrikanisches Edelholz, aus dem man teure Tische machte. Amomum war ein indisches Gewürz für Salben und Duftöle. Die Liste ist ein Querschnitt durch den Luxushandel Roms.", "elbbk"),
        E("Ist es richtig, sich über den Fall zu freuen?", "V. 20 fordert dazu auf, weil Gott das Urteil für die Verfolgten gesprochen hat. Die Freude gilt der Gerechtigkeit für die Opfer, deren Blut in 18,24 genannt wird – vergleichbar mit Ps 58,11 oder dem Lied am Schilfmeer (2Mo 15)."),
    ],
    try_="Lies V. 12–13 langsam und zähle, wie viele Waren genannt werden, bevor die Menschen kommen.",
    teaser="Nach dem Untergang hört Johannes ein Wort, das im ganzen Neuen Testament nur in diesem einen Kapitel vorkommt.")

sec("babylon", [R(OFFB, 19, 1, 10)], "Die Hochzeit des Lammes",
    "Eine große Menge im Himmel ruft Halleluja: Gottes Gerichte sind wahr und gerecht. Die Ältesten und Wesen stimmen ein, eine Stimme vom Thron ruft zum Lob, und die Menge antwortet wie Donner: Der Herr hat die Herrschaft angetreten, die Hochzeit des Lammes ist gekommen. Die Braut ist in reines Leinen gekleidet. Als Johannes den Engel anbeten will, wehrt dieser ab.",
    quiz=[
        estimate("Wie oft steht „Halleluja“ in V. 1–6?", 1, 10, 4, "mal", "V. 1, 3, 4 und 6: viermal.", None, "Zähl in Vers 1–6."),
        choice("Was ist die feine Leinwand der Braut nach V. 8?", ["Die gerechten Taten der Heiligen", "Das Blut des Lammes", "Die Gebete der Heiligen", "Die Herrlichkeit Gottes"], 8, "Lies Vers 8.",
               "V. 8: Die feine Leinwand sind die Gerechtigkeiten, also gerechten Taten, der Heiligen – und sie wurde ihr gegeben."),
        who("Siehe zu, tu es nicht. Ich bin dein Mitknecht", R(OFFB, 19, 10), ["Der Engel", "Das Lamm", "Einer der Ältesten", "Johannes"],
            "V. 10: Der Engel weist die Anbetung zurück – nur Gott soll angebetet werden."),
    ],
    explain=[
        E("Was heißt Halleluja?", "Hebräisch: „Lobt Jah!“, also „Lobt den HERRN“. In den Psalmen häufig (z. B. Ps 146–150), im Neuen Testament nur hier in Offb 19,1–6."),
        E("Wer ist die Braut?", "Im Alten Testament ist Israel die Braut Gottes (Jes 54,5; Hos 2,21), im Neuen die Gemeinde die Braut Christi (Eph 5,25–32; 2Kor 11,2). In 21,2.9 ist das neue Jerusalem die Braut. Die Braut ist damit das Gegenbild zur Hure Babylon."),
        E("Gegeben oder selbst gemacht?", "V. 8 sagt beides: Das Kleid wurde der Braut gegeben, und es besteht aus den gerechten Taten der Heiligen. Wie Gnade und Werke hier zusammengehören, beschreiben evangelische, katholische und orthodoxe Theologie verschieden; in der Gemeinsamen Erklärung zur Rechtfertigungslehre (1999) halten Lutheraner und Katholiken fest, dass gute Werke Frucht der Rechtfertigung sind."),
    ],
    fact="Händels berühmter Halleluja-Chor aus dem „Messias“ (1742) besteht fast ganz aus Versen der Offenbarung: 19,6, 11,15 und 19,16.",
    memory_verse=MV(R(OFFB, 19, 9), "Glückselig, die geladen sind zum Hochzeitsmahl des Lammes!"),
    teaser="Der Himmel öffnet sich, und ein Reiter auf einem weißen Pferd kommt. Achte im nächsten Abschnitt darauf, wessen Blut an seinem Gewand ist – und womit er kämpft.")

sec("babylon", [R(OFFB, 19, 11, 21)], "Der Reiter auf dem weißen Pferd",
    "Der Himmel öffnet sich, und ein Reiter auf einem weißen Pferd kommt: Treu und Wahrhaftig, mit Augen wie Feuer, in einem in Blut getauchten Gewand, sein Name ist das Wort Gottes. Aus seinem Mund kommt ein scharfes Schwert. Das Tier und die Könige der Erde ziehen gegen ihn. Das Tier und der falsche Prophet werden in den Feuersee geworfen.",
    quiz=[
        choice("Wie heißt der Reiter nach V. 13?", ["Das Wort Gottes", "Der Löwe aus Juda", "Michael", "Der Menschensohn"], 13, "Lies Vers 13.",
               "V. 13: Sein Name ist das Wort Gottes – vgl. Joh 1,1."),
        choice("Womit werden die Feinde in V. 21 getötet?", ["Mit dem Schwert, das aus seinem Mund kommt", "Mit Feuer vom Himmel", "Mit einem Erdbeben", "Mit den Schwertern seines Heeres"], 21, "Lies Vers 21.",
               "V. 21: mit dem Schwert, das aus dem Mund des Reiters hervorgeht. Sein Heer kämpft nicht."),
        tf("Das Heer, das dem Reiter folgt, trägt nach V. 14 Rüstungen und Waffen.", False, 14, "Lies Vers 14.",
           "V. 14: weiße, reine Leinwand – dieselbe Kleidung wie die Braut in V. 8."),
    ],
    explain=[
        E("Wessen Blut ist am Gewand?", "Der Text sagt es nicht. Manche verweisen auf Jes 63,1–3, wo Gott vom Treten der Kelter mit dem Blut der Feinde befleckt ist. Andere betonen, dass das Gewand schon vor der Schlacht blutig ist, und denken an das Blut des Lammes selbst."),
        E("Was bedeutet das Schwert aus dem Mund?", "Ein Bild aus Jes 11,4 und 49,2: Der Messias schlägt mit dem Stab seines Mundes. Viele Ausleger lesen es so, dass Christus durch sein Wort siegt. Futuristen erwarten zugleich eine wirkliche Schlacht bei seiner Wiederkunft, oft Harmagedon genannt (16,16)."),
        E("Ist das die Wiederkunft?", "Die meisten Ausleger aller Traditionen sehen hier die Wiederkunft Christi. Präteristische Ausleger lesen den Abschnitt teilweise als Bild für Christi Sieg über Rom in der Geschichte. Bei der Frage, was danach in Kap. 20 kommt, gehen die Sichten auseinander."),
    ],
    teaser="Jetzt kommt das Kapitel, über das Christen sich seit 1800 Jahren nicht einig werden: tausend Jahre.")

# ───────────────────────── 6 · Das Ende und der Anfang ─────────────────────────
sec("ende", [R(OFFB, 20, 1, 6)], "Die tausend Jahre",
    "Ein Engel fesselt den Drachen für 1000 Jahre und wirft ihn in den Abgrund, damit er die Nationen nicht mehr verführt. Johannes sieht Throne und die Seelen derer, die wegen ihres Zeugnisses enthauptet wurden und das Tier nicht anbeteten. Sie werden lebendig und herrschen mit Christus 1000 Jahre. Das ist die erste Auferstehung.",
    focus="Achte darauf, was der Text über die 1000 Jahre sagt – und was er nicht sagt, z. B. wo diese Herrschaft stattfindet.",
    quiz=[
        choice("Wozu wird der Drache gefesselt?", ["Damit er die Nationen nicht mehr verführt", "Damit er die Heiligen nicht mehr verklagt", "Damit die Erde neu wird", "Damit er Buße tut"], 3, "Lies Vers 3.",
               "V. 3: damit er die Nationen nicht mehr verführt, bis die 1000 Jahre vollendet sind."),
        choice("Wer herrscht mit Christus 1000 Jahre?", ["Die, die um des Zeugnisses Jesu willen enthauptet wurden und das Tier nicht anbeteten", "Alle Menschen", "Die zehn Könige", "Die Engel"], 4, "Lies Vers 4.",
               "V. 4: die Seelen der Enthaupteten, die das Tier nicht anbeteten – sie wurden lebendig."),
        tf("Über die, die an der ersten Auferstehung teilhaben, hat der zweite Tod keine Macht.", True, 6, "Lies Vers 6.",
           "V. 6: Der zweite Tod hat über sie keine Gewalt; sie sind Priester Gottes und herrschen mit Christus."),
    ],
    explain=[
        E("Prämillenialismus", "Christus kommt zurück (Kap. 19), bindet Satan und herrscht danach 1000 Jahre sichtbar auf der Erde; dann folgen das letzte Gericht und die neue Schöpfung. Diese Sicht vertraten schon Papias, Justin und Irenäus im 2. Jahrhundert. Der dispensationalistische Prämillenialismus verbindet sie seit dem 19. Jahrhundert mit einer Entrückung vor der Drangsal und einer besonderen Rolle Israels im Tausendjährigen Reich; der „historische“ Prämillenialismus kennt diese Unterscheidungen nicht."),
        E("Amillenialismus", "Die 1000 Jahre sind keine Zeit nach der Wiederkunft, sondern die Zeit der Kirche jetzt: Satan wurde durch Kreuz und Auferstehung gebunden (Mk 3,27: der Starke wird gefesselt), sodass das Evangelium zu den Nationen kann. Die Märtyrer herrschen schon jetzt mit Christus im Himmel; die erste Auferstehung ist ihr Leben bei ihm. Kap. 20 setzt dann noch einmal vor Kap. 19 ein. Diese Sicht prägte Augustinus (Vom Gottesstaat, Buch 20); ihr folgen die katholische und orthodoxe Kirche und viele lutherische und reformierte Kirchen."),
        E("Postmillenialismus", "Das Evangelium gewinnt in der Geschichte nach und nach die Welt, sodass eine lange Zeit des Friedens und der Gerechtigkeit anbricht – die 1000 Jahre. Am Ende kommt Christus wieder. Diese Sicht war bei Puritanern und in der Erweckungsbewegung des 18. und 19. Jahrhunderts verbreitet (z. B. Jonathan Edwards)."),
        E("Worin sind sich alle einig?", "Christus kommt wieder, Satan wird endgültig besiegt, die Toten werden auferweckt, Gott richtet und schafft alles neu. Die Unterschiede liegen in der Reihenfolge und darin, wie wörtlich die Bilder dieses Kapitels zu lesen sind."),
    ],
    cards=["millennium"],
    fact="Das lutherische Augsburger Bekenntnis von 1530 verwirft in Artikel 17 die Erwartung, dass vor der Auferstehung der Toten ein irdisches Reich der Frommen errichtet werde. Gerichtet war das gegen radikale Gruppen der Reformationszeit.",
    try_="Lies Mk 3,27 und Offb 20,2–3 nacheinander. Kann man beide Stellen auf dasselbe Geschehen beziehen – oder nicht?",
    teaser="Satan wird noch einmal losgelassen. Dann steht ein großer weißer Thron da, und Bücher werden aufgeschlagen.")

sec("ende", [R(OFFB, 20, 7, 15)], "Der große weiße Thron",
    "Nach den 1000 Jahren wird Satan losgelassen, verführt die Nationen, Gog und Magog, und umzingelt das Lager der Heiligen. Feuer vom Himmel verzehrt sie, und der Teufel wird in den Feuersee geworfen. Dann sieht Johannes einen großen weißen Thron. Die Toten stehen davor, Bücher werden geöffnet, und sie werden nach ihren Werken gerichtet. Tod und Hades werden in den Feuersee geworfen.",
    quiz=[
        choice("Wonach werden die Toten gerichtet?", ["Nach ihren Werken, wie es in den Büchern steht", "Nach ihrer Herkunft", "Nach dem Urteil der Ältesten", "Nach der Zahl ihrer Gebete"], 12, "Lies Vers 12.",
               "V. 12–13: nach dem, was in den Büchern geschrieben ist, nach ihren Werken."),
        tf("Nach V. 14 werden auch der Tod und der Hades in den Feuersee geworfen.", True, 14, "Lies Vers 14.",
           "V. 14: Der Tod selbst wird vernichtet – das ist der zweite Tod."),
        choice("Was entscheidet nach V. 15, ob jemand in den Feuersee geworfen wird?", ["Ob sein Name im Buch des Lebens steht", "Ob er die erste Auferstehung erlebt hat", "Wie viele Werke er hat", "Ob er im Meer gestorben ist"], 15, "Lies Vers 15.",
               "V. 15: wer nicht im Buch des Lebens geschrieben gefunden wird."),
    ],
    explain=[
        E("Bücher und das Buch des Lebens?", "V. 12 nennt beides: Bücher mit den Werken und das Buch des Lebens. Das Bild vom Buch, in dem Gott die Seinen aufschreibt, kommt schon in 2Mo 32,32 und Dan 12,1 vor. Wie Gericht nach Werken und Rettung aus Gnade zusammengehen, ist ein Thema der ganzen Bibel (vgl. Röm 2,6 und Eph 2,8–9)."),
        E("Wer sind Gog und Magog?", "In Hes 38–39 ist Gog ein Herrscher aus dem Land Magog im fernen Norden, der Israel angreift. Hier stehen die Namen für alle Nationen von den vier Ecken der Erde (V. 8). Dispensationalisten unterscheiden oft zwei Angriffe, einen bei Hesekiel und einen hier."),
        E("Warum gibt das Meer seine Toten heraus?", "V. 13 lässt das Meer seine Toten herausgeben. Wer im Meer starb, galt in der Antike als ohne Grab. Der Vers sagt: Niemand ist verloren gegangen."),
    ],
    teaser="Das erste Mal im Buch spricht der, der auf dem Thron sitzt, selbst. Er sagt nur wenige Sätze.")

sec("ende", [R(OFFB, 21, 1, 8)], "Alles neu",
    "Johannes sieht einen neuen Himmel und eine neue Erde; das Meer ist nicht mehr. Das neue Jerusalem kommt aus dem Himmel herab wie eine geschmückte Braut. Eine Stimme ruft: Gott wohnt bei den Menschen, er wischt jede Träne ab, und der Tod wird nicht mehr sein. Der auf dem Thron sagt: Ich mache alles neu, und gibt dem Durstigen umsonst vom Wasser des Lebens.",
    quiz=[
        choice("Wohin bewegt sich das neue Jerusalem?", ["Aus dem Himmel herab", "Von der Erde in den Himmel", "Aus dem Meer herauf", "Aus der Wüste nach Zion"], 2, "Lies Vers 2.",
               "V. 2: Die Stadt kommt aus dem Himmel von Gott herab – nicht die Menschen fahren auf."),
        who("Siehe, ich mache alles neu", R(OFFB, 21, 5), ["Der, der auf dem Thron saß", "Ein Engel", "Johannes", "Einer der Ältesten"],
            "V. 5: Der, der auf dem Thron sitzt, spricht – zum ersten Mal seit Kap. 1,8 direkt."),
        tf("Das Wasser des Lebens gibt es nach V. 6 umsonst.", True, 6, "Lies Vers 6.",
           "V. 6: Dem Dürstenden aus der Quelle des Wassers des Lebens umsonst – ein Echo von Jes 55,1."),
    ],
    explain=[
        E("Neu oder erneuert?", "Das griechische kainos meint eher „neu in der Art“ als „neu hergestellt“. Manche lesen darum: Die alte Welt wird nicht weggeworfen, sondern verwandelt, wie der Auferstehungsleib Jesu derselbe und doch neu war. Andere verstehen V. 1 als völlige Neuschöpfung nach der Vernichtung der alten Welt (vgl. 2Petr 3,10–13)."),
        E("Warum ist das Meer nicht mehr?", "Das Meer war für Israel Ort des Chaos (Dan 7,3; Offb 13,1) und der Trennung – Johannes war auf einer Insel verbannt. Die meisten Ausleger lesen V. 1 nicht als Aussage über Geografie, sondern über das Ende von allem, wofür das Meer stand."),
        E("Was heißt „die Hütte Gottes bei den Menschen“?", "Das griechische skene erinnert an die Stiftshütte, das Zelt, in dem Gott in der Wüste unter Israel wohnte (2Mo 25,8; 3Mo 26,11–12), und an Joh 1,14: Das Wort „zeltete“ unter uns.", "elbbk"),
    ],
    cards=["neues-jerusalem"],
    memory_verse=MV(R(OFFB, 21, 4), "Und er wird jede Träne von ihren Augen abwischen, und der Tod wird nicht mehr sein"),
    teaser="Ein Engel misst die Stadt aus. Die Maße ergeben eine Form, die im Tempel nur ein einziger Raum hatte.")

sec("ende", [R(OFFB, 21, 9, 21)], "Die Stadt aus Gold",
    "Der Engel, der Johannes die Hure gezeigt hat, zeigt ihm nun die Braut: das neue Jerusalem, leuchtend wie Jaspis. Es hat eine hohe Mauer mit zwölf Toren, auf denen die Namen der zwölf Stämme stehen, und zwölf Grundsteine mit den Namen der zwölf Apostel. Die Stadt ist so lang wie breit wie hoch, 12.000 Stadien, aus reinem Gold wie Glas; jedes Tor ist eine einzige Perle.",
    quiz=[
        choice("Was steht auf den zwölf Grundsteinen der Mauer?", ["Die Namen der zwölf Apostel", "Die Namen der zwölf Stämme", "Die Namen der sieben Gemeinden", "Die Namen der Engel"], 14, "Lies Vers 14.",
               "V. 14: die Namen der zwölf Apostel des Lammes. Die Stämme stehen auf den Toren (V. 12)."),
        tf("Länge, Breite und Höhe der Stadt sind gleich.", True, 16, "Lies Vers 16.",
           "V. 16: Die Stadt ist ein Würfel."),
        choice("Woraus ist jedes Tor?", ["Aus einer einzigen Perle", "Aus Jaspis", "Aus reinem Gold", "Aus Saphir"], 21, "Lies Vers 21.",
               "V. 21: Jedes der zwölf Tore ist aus einer Perle."),
    ],
    explain=[
        E("Warum ein Würfel?", "Das Allerheiligste im Tempel Salomos war ein Würfel von 20 Ellen, mit Gold überzogen (1Kön 6,20). Die ganze Stadt hat diese Form: Viele Ausleger lesen daraus, dass die ganze Stadt Ort der Gegenwart Gottes ist. Dispensationalisten verstehen die Stadt oft als wirklichen künftigen Wohnort, andere als Bild für das vollendete Gottesvolk – die Stadt ist ja zugleich die Braut (V. 9)."),
        E("Wie groß ist das?", "12.000 Stadien sind etwa 2200 km, ungefähr die Entfernung von Lissabon bis Berlin – in Länge, Breite und Höhe. Die Zahl ist 12 × 1000; die Mauer misst 144 Ellen, also 12 × 12. Die Zwölf ist die Zahl des Gottesvolkes."),
        E("Woher kommen die Edelsteine?", "Sie erinnern an die zwölf Steine auf der Brusttasche des Hohenpriesters, auf denen die Namen der Stämme standen (2Mo 28,17–21), und an Jes 54,11–12, wo Jerusalem auf Saphiren gegründet wird."),
    ],
    teaser="In der Stadt fehlt etwas, das in jeder antiken Stadt das wichtigste Gebäude war. Und dann fließt ein Strom.")

sec("ende", [R(OFFB, 21, 22, 27), R(OFFB, 22, 1, 5)], "Der Strom und der Baum",
    "Johannes sieht keinen Tempel in der Stadt, denn Gott und das Lamm sind ihr Tempel; sie braucht weder Sonne noch Mond. Die Nationen gehen in ihrem Licht, die Tore schließen nie. Vom Thron fließt der Strom des Lebenswassers, an seinen Ufern steht der Baum des Lebens, dessen Blätter die Nationen heilen. Kein Fluch ist mehr, und sie werden Gottes Angesicht sehen.",
    focus="Achte auf die Rückbezüge zu den ersten Kapiteln der Bibel (1Mo 1–3).",
    quiz=[
        choice("Warum gibt es keinen Tempel in der Stadt?", ["Gott und das Lamm sind ihr Tempel", "Die Nationen haben ihn zerstört", "Der Tempel ist im Himmel geblieben", "Es gibt keine Priester mehr"], None, "Lies Vers 21,22.",
               "21,22: Gott, der Allmächtige, und das Lamm sind ihr Tempel."),
        choice("Wozu dienen die Blätter des Baumes des Lebens?", ["Zur Heilung der Nationen", "Als Kleidung für die Heiligen", "Als Nahrung für die Engel", "Als Schmuck für die Braut"], None, "Lies Vers 22,2.",
               "22,2: Die Blätter sind zur Heilung der Nationen."),
        tf("Nach 22,4 werden Gottes Knechte sein Angesicht sehen.", True, None, "Lies Vers 22,4.",
           "22,4: Sie sehen sein Angesicht, und sein Name steht an ihren Stirnen. Mose durfte Gottes Angesicht nicht sehen (2Mo 33,20)."),
    ],
    explain=[
        E("Welche Bezüge zu 1Mo 1–3 gibt es?", "Der Baum des Lebens stand im Garten Eden; nach dem Fall wurde der Weg zu ihm versperrt (1Mo 3,22–24). Ein Strom ging von Eden aus (1Mo 2,10). Der Fluch aus 1Mo 3,17 ist aufgehoben (22,3). Die Nacht, die Gott am ersten Tag von Licht schied, ist nicht mehr (22,5). Auch Hes 47,1–12 beschreibt einen Strom aus dem Tempel mit heilenden Bäumen."),
        E("Wer sind die Nationen und Könige?", "Sie bringen ihre Herrlichkeit in die Stadt (21,24.26) – ein Bild aus Jes 60,3–11. Manche Ausleger lesen daraus, dass das Gute der menschlichen Kulturen nicht verloren geht. Wer genau die Nationen sind, wenn doch nach 20,15 gerichtet wurde, wird unterschiedlich beantwortet."),
        E("Ist der Himmel eine Stadt?", "Am Ende des Buches gehen die Menschen nicht in den Himmel, sondern Gott kommt mit der Stadt auf die neue Erde (21,2–3). Viele Ausleger aller Traditionen betonen das: Die christliche Hoffnung richtet sich auf eine erneuerte Schöpfung, nicht nur auf einen Ort jenseits der Welt."),
    ],
    try_="Lies 1Mo 2,8–10 und dann Offb 22,1–3. Notiere, was in beiden Texten vorkommt – und was am Ende anders ist als am Anfang.",
    teaser="Zum Schluss ein Gebet aus der allerersten Gemeinde, in einer Sprache, die schon damals nur noch wenige sprachen.")

sec("ende", [R(OFFB, 22, 12, 21)], "Komm, Herr Jesus!",
    "Jesus sagt: Ich komme bald, ich bin das Alpha und das Omega. Glückselig, die ihre Kleider waschen und durch die Tore in die Stadt gehen. Er nennt sich die Wurzel Davids und den hellen Morgenstern. Der Geist und die Braut rufen: Komm! Wer durstig ist, soll kommen und das Wasser des Lebens umsonst nehmen. Das Buch endet mit dem Ruf: Komm, Herr Jesus!",
    bridge="Der Engel versichert, dass die Worte wahr sind; Johannes will ihn anbeten und wird wieder zurückgewiesen. Das Buch soll nicht versiegelt werden, denn die Zeit ist nahe (22,6–11).",
    quiz=[
        who("Ich bin die Wurzel und das Geschlecht Davids, der glänzende Morgenstern", R(OFFB, 22, 16), ["Jesus", "Johannes", "Der Engel", "Der Geist"],
            "V. 16: Jesus spricht hier selbst und nennt sich mit Namen."),
        choice("Wer ruft in V. 17 „Komm!“?", ["Der Geist und die Braut", "Die vier lebendigen Wesen", "Die Könige der Erde", "Der Engel und Johannes"], 17, "Lies Vers 17.",
               "V. 17: der Geist und die Braut – und jeder, der es hört, soll einstimmen."),
        tf("Das Buch endet mit einer Warnung vor dem Gericht.", False, 21, "Lies den letzten Vers.",
           "V. 21: Es endet mit einem Segenswunsch: Die Gnade des Herrn Jesus sei mit allen – wie ein Brief."),
    ],
    explain=[
        E("Wer spricht hier?", "Die Stimmen wechseln schnell: Jesus (V. 12–13.16.20), ein Segensspruch (V. 14), der Geist und die Braut (V. 17), Johannes selbst (V. 18–21). Am Ende antwortet die Gemeinde auf das Versprechen Jesu mit ihrem Ruf. So wurde der Text wohl im Gottesdienst vorgelesen."),
        E("Was bedeuten V. 18–19?", "Eine damals übliche Schutzformel gegen das Verändern einer Schrift beim Abschreiben (vgl. 5Mo 4,2). Sie bezieht sich auf dieses Buch, nicht auf die ganze Bibel, die damals noch nicht als Sammlung vorlag."),
        E("Was ist Maranatha?", "Der Ruf „Komm, Herr Jesus“ (V. 20) entspricht dem aramäischen maranatha, „Unser Herr, komm!“. Paulus zitiert es unübersetzt in 1Kor 16,22, also schon die griechisch sprechenden Gemeinden beteten es in der Muttersprache Jesu."),
    ],
    fact="Martin Luther schrieb 1522 in der Vorrede zur Offenbarung, er könne das Buch weder für apostolisch noch für prophetisch halten. 1530 schrieb er eine neue, deutlich freundlichere Vorrede. In der orthodoxen Kirche wird die Offenbarung bis heute nicht in den Gottesdiensten gelesen.",
    memory_verse=MV(R(OFFB, 22, 20), "Amen; komm, Herr Jesus!"),
    prayer={"text": "Es komme die Gnade, und es vergehe diese Welt. Hosianna dem Gott Davids! Wer heilig ist, der komme; wer es nicht ist, der kehre um. Maranatha. Amen.",
            "source": "Didache 10,6, um 100 n. Chr. (eigene Übersetzung)"})

P.write()
