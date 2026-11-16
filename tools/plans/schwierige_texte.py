#!/usr/bin/env python3
"""Source for the reading plan „Texte, die man lieber überspringt“ (generates assets/plans/schwierige-texte.json).

python3 -I tools/plans/schwierige_texte.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/schwierige-texte.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

GEN, RI, SAM2, KOE2, APG, MT, LK, PS, HEBR, KOR1, TIM1, ROEM, MK = 1, 7, 10, 12, 44, 40, 42, 19, 58, 46, 54, 45, 41

P = PlanBuilder(
    "schwierige-texte", "st", "Texte, die man lieber überspringt", "Ehrlich gelesen",
    "Isaak auf dem Altar, Jeftahs Tochter, die Bären des Elisa, „die Frau schweige“: Bei manchen Stellen blättert man lieber weiter. "
    "18 Abschnitte, die genau hinschauen – mit den Fragen, die diese Texte aufwerfen, und den Antworten, die Christen darauf gegeben haben.",
    "schwierig",
    stages=[("opfer", "Opfer und Gelübde"), ("zuschlagen", "Wenn Gott zuschlägt"),
            ("hart", "Harte Worte"), ("frauen", "„Die Frau schweige“")],
    cards=[
        ("isaak", "person", "Isaak", "Sohn Abrahams und Saras, geboren, als beide alt waren. Sein Name bedeutet „er lacht“ (1Mo 18,12; 21,6). Durch ihn sollte die Verheißung an Abraham weitergehen (1Mo 21,12). Er heiratete Rebekka und wurde Vater von Esau und Jakob. Im Judentum heißt 1Mo 22 „Akeda“, die Bindung Isaaks.", "1Mo 21–28"),
        ("morija", "ort", "Morija", "Das „Land Morija“ wird nur in 1Mo 22,2 genannt. 2Chr 3,1 nennt den Berg Morija in Jerusalem als den Ort, an dem Salomo den Tempel baute. Ob dieselbe Gegend gemeint ist, lässt sich nicht sicher sagen; jüdische und christliche Tradition verbinden beide Stellen.", "1Mo 22,2; 2Chr 3,1"),
        ("jeftah", "person", "Jeftah", "Richter aus Gilead, östlich des Jordan. Sohn einer Prostituierten, von seinen Halbbrüdern vertrieben, Anführer einer Schar besitzloser Männer. Die Ältesten Gileads holten ihn gegen die Ammoniter zurück. Er richtete Israel sechs Jahre. Hebr 11,32 nennt ihn unter den Menschen des Glaubens.", "Ri 11,1–12,7; Hebr 11,32"),
        ("geluebde", "begriff", "Gelübde", "Ein freiwilliges Versprechen an Gott, oft mit Bedingung: Wenn du …, dann will ich … Wer gelobte, war daran gebunden (4Mo 30,3; Pred 5,3–4). Menschen, die Gott gelobt wurden, konnten nach 3Mo 27 mit Geld ausgelöst werden. Jesus warnt vor leichtfertigem Schwören (Mt 5,33–37).", "4Mo 30; 3Mo 27"),
        ("bundeslade", "begriff", "Bundeslade", "Ein mit Gold überzogener Kasten aus Akazienholz, gut einen Meter lang (2Mo 25,10–22). Darin lagen die Gesetzestafeln. Der Deckel mit zwei Cherubim galt als Thron Gottes. Sie wurde an Stangen getragen und stand später im Allerheiligsten des Tempels. Nach der Zerstörung Jerusalems 586 v. Chr. verliert sich ihre Spur.", "2Mo 25; 2Sam 6"),
        ("elisa", "person", "Elisa", "Prophet im Nordreich Israel im 9. Jahrhundert v. Chr., Schüler und Nachfolger Elias. Er bat um einen doppelten Anteil von Elias Geist (2Kön 2,9). Von ihm werden viele Wunder erzählt: das Öl der Witwe, die Auferweckung eines Kindes, die Heilung des Syrers Naaman, die Jesus in Lk 4,27 erwähnt.", "2Kön 2–13"),
        ("barnabas", "person", "Barnabas", "Joseph, ein Levit aus Zypern, von den Aposteln Barnabas genannt. Er führte den frisch bekehrten Paulus bei den Aposteln ein (Apg 9,27), holte ihn nach Antiochia und reiste mit ihm auf der ersten Missionsreise. Später trennten sie sich im Streit über Markus, seinen Vetter (Apg 15,39; Kol 4,10).", "Apg 4,36; 9,27; 13–15"),
        ("hananias-saphira", "person", "Hananias und Saphira", "Ehepaar der ersten Gemeinde in Jerusalem. Die Namen bedeuten etwa „der HERR ist gnädig“ und „die Schöne“. Ihre Geschichte folgt direkt auf den Bericht über den gemeinsamen Besitz. Nicht zu verwechseln mit Hananias in Damaskus, der Paulus die Hände auflegte (Apg 9,10–18).", "Apg 5,1–11"),
        ("kanaanaeerin", "person", "Die kanaanäische Frau", "Mutter einer kranken Tochter aus der Gegend von Tyrus und Sidon, also keine Jüdin. Matthäus nennt sie Kanaanäerin, Markus eine Griechin aus Syrophönizien (Mk 7,24–30). Die Bibel nennt ihren Namen nicht; spätere Legenden (die Pseudo-Klementinen) nennen sie Justa.", "Mt 15,21–28; Mk 7,24–30"),
        ("fluchpsalmen", "begriff", "Fluchpsalmen", "Psalmen oder Verse, in denen der Beter Gott um Vergeltung an seinen Feinden bittet, etwa Ps 58, Ps 109 und Ps 137,7–9. Sie gehören zu den Klagepsalmen. Christen gehen unterschiedlich mit ihnen um: vollständig mitbeten, sie geistlich-bildhaft deuten oder sie im Gottesdienst auslassen.", "Ps 58; 109; 137"),
        ("beharrlichkeit", "begriff", "Kann man das Heil verlieren?", "Eine alte Streitfrage. Reformierte Kirchen lehren die „Beharrlichkeit der Heiligen“: Wer wirklich glaubt, wird von Gott bis ans Ende bewahrt. Lutherische, methodistische, katholische und orthodoxe Kirchen lehren, dass ein Christ vom Glauben abfallen kann. Beide Seiten lehren, dass Gott jeden annimmt, der umkehrt.", "Hebr 6,4–12; Joh 10,28–29"),
        ("rollen", "begriff", "Komplementär und egalitär", "Zwei Sichtweisen unter Christen, die die Bibel als Gottes Wort lesen. Komplementär: Mann und Frau sind gleich wertvoll, haben aber nach der Schrift verschiedene Aufgaben; Lehre und Leitung der Gemeinde sind Männern vorbehalten. Egalitär: Die Einschränkungen gehören in ihre damalige Lage; Frauen können alle Dienste übernehmen. Dazwischen gibt es viele Abstufungen.", "1Kor 11; 14; 1Tim 2"),
        ("phoebe", "person", "Phöbe", "Dienerin oder Diakonin der Gemeinde in Kenchreä, dem Osthafen von Korinth. Paulus nennt sie Beistand vieler und auch seiner selbst (griechisch prostatis, auch „Förderin, Schutzherrin“). Wahrscheinlich brachte sie den Römerbrief nach Rom.", "Röm 16,1–2"),
        ("priska", "person", "Priska und Aquila", "Jüdisches Ehepaar, Zeltmacher wie Paulus, unter Kaiser Claudius aus Rom ausgewiesen. Paulus wohnte und arbeitete bei ihnen in Korinth. In Ephesus erklärten sie dem Prediger Apollos den Weg Gottes genauer (Apg 18,26). In Ephesus und in Rom traf sich eine Gemeinde in ihrem Haus. Die Apg nennt Priska Priszilla.", "Apg 18; Röm 16,3–5; 1Kor 16,19"),
        ("junia", "person", "Junia", "Von Paulus zusammen mit Andronikus gegrüßt, vermutlich ein Ehepaar: jüdische Christen („meine Verwandten“), schon vor Paulus gläubig und mit ihm im Gefängnis. Ob der Name weiblich (Junia) oder männlich (Junias) ist, war lange umstritten. Die alte Kirche las fast einhellig Junia.", "Röm 16,7"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Opfer und Gelübde ─────────────────────────
sec("opfer", [R(GEN, 22, 1, 8)], "Der Auftrag und der Weg",
    "Gott stellt Abraham auf die Probe: Er soll seinen Sohn Isaak im Land Morija als Brandopfer darbringen. Drei Tage sind sie unterwegs. Auf Isaaks Frage nach dem Lamm antwortet Abraham, Gott werde es sich aussuchen.",
    bridge="Dieser Plan liest Texte, die viele lieber überspringen – langsam und mit den Fragen, die sie aufwerfen. Den Anfang macht Abraham. Er hat lange auf einen Sohn gewartet; Isaak ist der Sohn der Verheißung (1Mo 21,1–12).",
    place="jerusalem",
    focus="Achte darauf, was Abraham den Knechten sagt und was er Isaak sagt.",
    quiz=[
        tf("Der Leser erfährt gleich am Anfang, dass Gott Abraham auf die Probe stellt.", True, 1, "Lies Vers 1.",
           "V. 1: Gott prüft Abraham. Der Leser weiß das von Anfang an; ob Abraham es weiß, sagt der Text nicht."),
        choice("Was sagt Abraham zu seinen Knechten?", ["Er und der Junge wollen anbeten und dann zu ihnen zurückkommen", "Sie sollen in drei Tagen nachkommen", "Er wird allein zurückkommen", "Sie sollen das Holz zum Berg tragen"], 5, "Lies Vers 5.",
               "V. 5: Abraham spricht in der Mehrzahl – wir wollen anbeten und zu euch zurückkehren."),
        who("Gott wird sich das Schaf zum Brandopfer auswählen, mein Sohn.", R(GEN, 22, 8), ["Abraham", "Isaak", "Der Engel des HERRN", "Einer der Knechte"],
            "V. 8: Abrahams Antwort auf Isaaks Frage aus V. 7."),
    ],
    explain=[
        E("Was heißt hier „versuchen“?", "Hebräisch nissah, „prüfen, auf die Probe stellen“. Gemeint ist keine Verführung zum Bösen (vgl. Jak 1,13), sondern eine Prüfung.", "elbbk"),
        E("Warum ist der Auftrag so verstörend?", "Kinderopfer gab es bei Nachbarvölkern Israels (2Kön 3,27); das Gesetz verbietet sie später ausdrücklich (3Mo 18,21; 5Mo 12,31). Dazu kommt: Gott selbst hatte verheißen, dass Abrahams Nachkommen durch Isaak kommen sollen (1Mo 21,12)."),
        E("Wie alt war Isaak?", "Der Text sagt es nicht. Er trägt das Holz für ein Brandopfer, war also kein kleines Kind mehr. Der jüdische Historiker Josephus nennt 25 Jahre, die rabbinische Überlieferung 37."),
    ],
    cards=["isaak", "morija"],
    fact="Im Judentum heißt diese Geschichte „Akeda“, „die Bindung“ – nach V. 9. Sie wird am jüdischen Neujahrsfest Rosch ha-Schana in der Synagoge gelesen.",
    teaser="Wer kommt am Ende vom Berg zurück? Der Text ist an dieser Stelle auffallend knapp.")

sec("opfer", [R(GEN, 22, 9, 19)], "Der Altar und der Widder",
    "Abraham bindet Isaak auf den Altar und nimmt das Messer. Der Engel des HERRN hält ihn zurück; Abraham opfert einen Widder an Isaaks Stelle. Gott schwört, ihn zu segnen und durch seine Nachkommen alle Völker zu segnen.",
    place="jerusalem",
    quiz=[
        order("Bring die Ereignisse in die richtige Reihenfolge.",
              ["Abraham bindet Isaak auf den Altar", "Abraham nimmt das Messer", "Der Engel ruft vom Himmel", "Abraham opfert den Widder", "Der Engel ruft ein zweites Mal"],
              "V. 9–15: Altar, Messer, der erste Ruf, der Widder – dann der zweite Ruf mit dem Schwur."),
        choice("Was weiß Gott nun, laut dem Engel?", ["Dass Abraham Gott fürchtet", "Dass Isaak gehorsam ist", "Dass Abraham ein großes Volk wird", "Dass dieser Ort heilig ist"], 12, "Lies Vers 12.",
               "V. 12: Nun weiß ich, dass du Gott fürchtest – du hast mir deinen einzigen Sohn nicht vorenthalten."),
        tf("In V. 19 kehrt Abraham zu seinen Knechten zurück, ohne dass Isaak erwähnt wird.", True, 19, "Lies Vers 19.",
           "V. 19 nennt nur Abraham. Jüdische Ausleger haben dazu viel erzählt, etwa dass Isaak zum Lernen bei Sem blieb. Viele halten es schlicht für knappe Erzählweise."),
    ],
    explain=[
        E("Was bedeutet der Ortsname in V. 14?", "Hebräisch Jahwe jir’e: wörtlich „der HERR sieht“, im Sinn von „er sieht vor, er sorgt“. Das greift Abrahams Antwort aus V. 8 auf. Bekannt ist der Name auch als „Jehova Jireh“."),
        E("Wie lesen Christen diese Geschichte?", "Hebr 11,17–19 sagt, Abraham habe damit gerechnet, dass Gott auch Tote auferwecken kann. Kirchenväter wie Melito von Sardes sahen in Isaak, der das Holz trägt, und im Widder an seiner Stelle ein Vorausbild auf Christus. Jak 2,21–23 nennt die Tat als Beispiel für Glauben, der handelt."),
        E("Und wie liest das Judentum sie?", "Für viele jüdische Ausleger zeigt die Akeda Abrahams völlige Hingabe, und sie wird im Gebet als Grund angeführt, Gott um Erbarmen zu bitten. Andere betonen den Schluss: Der Gott Israels nimmt kein Menschenopfer an."),
        E("Hat das schon früher Gläubige verstört?", "Ja. Der dänische Christ Søren Kierkegaard schrieb 1843 ein ganzes Buch darüber („Furcht und Zittern“). Er fragt, wie man Abraham als Vater des Glaubens bewundern kann, ohne über diese drei Tage zu erschrecken."),
    ],
    memory_verse=MV(R(GEN, 22, 14), "Und Abraham gab diesem Ort den Namen: Der HERR wird auswählen"),
    teaser="Ein Anführer verspricht Gott etwas – und weiß nicht, was es ihn kosten wird.")

sec("opfer", [R(RI, 11, 29, 33)], "Jeftahs Gelübde",
    "Der Geist des HERRN kommt über Jeftah. Vor dem Kampf gelobt er: Was ihm bei der Rückkehr aus der Tür seines Hauses entgegenkommt, will er dem HERRN als Brandopfer darbringen. Er besiegt die Ammoniter.",
    bridge="Viele Jahrhunderte später, zur Zeit der Richter: Die Ammoniter bedrängen Israel. Die Ältesten von Gilead holen Jeftah zurück, den seine Halbbrüder vertrieben hatten, und machen ihn zum Anführer (Ri 11,1–11).",
    place="mizpa-gilead",
    quiz=[
        choice("Was geschieht, bevor Jeftah sein Gelübde ablegt?", ["Der Geist des HERRN kommt über ihn", "Er verliert eine erste Schlacht", "Ein Prophet fordert ihn zu einem Gelübde auf", "Seine Tochter bittet ihn, für sie zu beten"], 29, "Lies Vers 29.",
               "V. 29: Der Geist des HERRN kommt über Jeftah, er zieht durch Gilead – und dann folgt in V. 30 das Gelübde."),
        tf("Gott verlangt von Jeftah ein Gelübde.", False, 30, "Lies Vers 30.",
           "V. 30: Das Gelübde geht von Jeftah aus. Eine Antwort Gottes darauf berichtet der Text nicht."),
        error("Jeftah gelobt: Was ihm aus der Tür seines [Zeltes] entgegenkommt, soll dem HERRN gehören.", "Hauses", 31,
              "V. 31: aus der Tür seines Hauses, wenn er in Frieden zurückkehrt."),
    ],
    explain=[
        E("Woran hat Jeftah gedacht?", "Das hebräische Wort kann „was“ oder „wer“ heißen. In israelitischen Häusern lebten Tiere oft im Erdgeschoss mit, deshalb denken manche Ausleger an ein Tier. Andere halten für wahrscheinlicher, dass Jeftah mit einem Menschen rechnete, weil jemandem „entgegengehen“ eher etwas ist, das Menschen tun."),
        E("Was sagt das Gesetz über Gelübde?", "Ein Gelübde musste gehalten werden (4Mo 30,3). Wurde ein Mensch Gott gelobt, sah das Gesetz vor, ihn mit Geld auszulösen (3Mo 27,1–8). Menschenopfer verbietet es ausdrücklich (5Mo 12,31)."),
        E("Wer waren die Ammoniter?", "Ein Volk östlich des Jordan, mit der Hauptstadt Rabba – dem heutigen Amman in Jordanien. Nach 1Mo 19,38 stammten sie von Lot ab, waren also mit Israel verwandt."),
    ],
    cards=["jeftah", "geluebde"],
    teaser="Ein ganzes Volk erinnert sich jedes Jahr an eine junge Frau, deren Namen niemand kennt.")

sec("opfer", [R(RI, 11, 34, 40)], "Die Tochter",
    "Als Erste kommt Jeftah seine einzige Tochter mit Tamburinen und Reigen entgegen. Er zerreißt seine Kleider. Sie bittet um zwei Monate, um mit ihren Freundinnen auf den Bergen zu weinen. Danach vollzieht er das Gelübde. Seitdem gedenken die Töchter Israels ihrer jedes Jahr.",
    place="mizpa-gilead",
    focus="Achte darauf, wie viel der Text sagt – und was er nicht sagt.",
    quiz=[
        who("Mein Vater, hast du deinen Mund gegen den HERRN aufgetan", R(RI, 11, 36), ["Jeftahs Tochter", "Jeftahs Frau", "Eine ihrer Freundinnen", "Ein Ältester aus Gilead"],
            "V. 36: Die Tochter spricht – sie drängt den Vater nicht, das Gelübde zu brechen."),
        choice("Worum bittet die Tochter?", ["Um zwei Monate mit ihren Freundinnen auf den Bergen", "Dass ihr Vater das Gelübde zurücknimmt", "Um einen Priester, der für sie betet", "Dass sie vorher heiraten darf"], 37, "Lies Vers 37.",
               "V. 37: zwei Monate, um mit ihren Freundinnen ihre Jungfrauschaft zu beweinen."),
        estimate("Wie viele Tage im Jahr gedenken die Töchter Israels der Tochter Jeftahs?", 1, 10, 4, "Tage",
                 "V. 40: vier Tage im Jahr.", 40, "Lies Vers 40."),
    ],
    explain=[
        E("Wurde sie wirklich geopfert?", "Darüber sind Gläubige seit Jahrhunderten uneins. Die meisten alten jüdischen und christlichen Ausleger (z. B. Josephus und viele Kirchenväter) verstehen: ja. Seit dem Mittelalter (z. B. der jüdische Ausleger David Kimchi) lesen andere: Sie wurde Gott geweiht und blieb unverheiratet. Dafür führen sie V. 37–39 an, wo es um ihre Jungfrauschaft geht; dagegen steht, dass V. 31 ausdrücklich ein Brandopfer nennt."),
        E("Billigt der Text, was Jeftah tut?", "Er bewertet es nicht ausdrücklich. Manche Ausleger lesen die Geschichte im Zusammenhang des ganzen Richterbuchs, das mit dem Satz schließt, jeder habe getan, was in seinen Augen recht war (Ri 17,6; 21,25). Hebr 11,32 nennt Jeftah dennoch unter den Glaubenden."),
        E("Hätte er das Gelübde lösen können?", "Nach 3Mo 27,1–8 konnte ein Mensch, der Gott gelobt war, mit Geld ausgelöst werden. Ein jüdischer Midrasch erzählt, Jeftah und der Hohepriester Pinhas hätten beide aus Stolz darauf gewartet, dass der andere zu ihm kommt – und so sei die Tochter gestorben."),
    ],
    try_="Lies Ri 11,30–31 und 1Mo 28,20–22 nebeneinander. Was haben die beiden Gelübde gemeinsam, was unterscheidet sie?",
    teaser="Ein großes Fest mit Musik und 30.000 Mann – und plötzlich ist es still.")

# ───────────────────────── 2 · Wenn Gott zuschlägt ─────────────────────────
sec("zuschlagen", [R(SAM2, 6, 1, 11)], "Ussa und die Lade",
    "David will die Bundeslade nach Jerusalem holen. Sie fährt auf einem neuen Wagen, alle musizieren. Als die Rinder sich losreißen, fasst Ussa die Lade an und stirbt. David ist zornig und fürchtet sich; die Lade bleibt drei Monate bei Obed-Edom, und Gott segnet sein Haus.",
    bridge="David ist König über ganz Israel geworden und hat Jerusalem erobert (2Sam 5). Die Bundeslade steht seit vielen Jahren im Haus Abinadabs in Kirjat-Jearim, auch Baale-Juda genannt (1Sam 7,1–2).",
    place="kirjat-jearim",
    focus="Achte darauf, wie David reagiert.",
    quiz=[
        choice("Worauf wird die Lade transportiert?", ["Auf einem neuen Wagen", "Auf den Schultern der Leviten", "Auf einem Esel", "In einem Zelt auf Stangen"], 3, "Lies Vers 3.",
               "V. 3: auf einem neuen Wagen. Nach 4Mo 4,15 und 7,9 sollte die Lade an Stangen getragen werden; 1Chr 15,13–15 sieht später darin den Fehler."),
        tf("David reagiert auf Ussas Tod mit Zorn und mit Furcht.", True, 8, "Lies Vers 8–9.",
           "V. 8–9: David ist zornig über den „Bruch“ an Ussa – und fürchtet sich zugleich vor dem HERRN."),
        choice("Was geschieht im Haus Obed-Edoms?", ["Der HERR segnet ihn und sein ganzes Haus", "Auch Obed-Edom stirbt", "Die Lade wird beschädigt", "David besucht die Lade jeden Tag"], 11, "Lies Vers 11.",
               "V. 11: Drei Monate bleibt die Lade dort, und der HERR segnet Obed-Edom und sein ganzes Haus."),
    ],
    explain=[
        E("Warum stirbt Ussa?", "Der Text nennt nur ein „Vergehen“; das hebräische Wort ist selten und unklar. Nach 4Mo 4,15 durften selbst die Leviten die heiligen Geräte nicht berühren, sonst würden sie sterben. 1Chr 15,13 sagt rückblickend, man habe Gott nicht nach der Vorschrift gesucht."),
        E("Was heißt „einen Bruch machen“?", "Hebräisch perez, „Riss, Durchbruch“; Perez-Ussa heißt „Ussas Riss“. Kurz vorher hatte David einen Ort Baal-Perazim genannt, weil Gott dort seine Feinde „durchbrochen“ hatte (2Sam 5,20) – dasselbe Wort."),
        E("Wie gehen Ausleger mit dieser Geschichte um?", "Viele lesen sie als Erzählung über Gottes Heiligkeit, die man nicht beiläufig behandeln kann. Andere heben hervor, dass auch David mit dem Geschehen ringt und der Text seinen Zorn nicht verschweigt. 2Sam 6,12–15 erzählt, wie die Lade drei Monate später doch nach Jerusalem kommt."),
    ],
    cards=["bundeslade"],
    fact="Obed-Edom wird „Gatiter“ genannt, also wohl jemand aus der Philisterstadt Gat – vermutlich ein Ausländer. Manche Ausleger denken stattdessen an die Levitenstadt Gat-Rimmon (Jos 21,24).",
    teaser="Ein Prophet, Spötter am Wegrand und zwei Bären. Aber wer genau waren diese „Kinder“?")

sec("zuschlagen", [R(KOE2, 2, 19, 25)], "Elisa und die Bären",
    "In Jericho macht Elisa schlechtes Wasser gesund. Auf dem Weg nach Bethel verspotten ihn junge Leute als Kahlkopf. Er verflucht sie im Namen des HERRN; zwei Bärinnen kommen aus dem Wald und zerreißen 42 von ihnen.",
    bridge="Etwa 150 Jahre nach David: Der Prophet Elia ist in einem Sturm in den Himmel aufgefahren. Sein Schüler Elisa hat Elias Mantel aufgehoben und ist nach Jericho zurückgekehrt (2Kön 2,1–18).",
    place="bethel",
    quiz=[
        choice("Womit macht Elisa das Wasser gesund?", ["Mit Salz in einer neuen Schale", "Mit Öl aus einem Krug", "Mit dem Mantel des Elia", "Mit einem Stück Holz"], 20, "Lies Vers 20–21.",
               "V. 20–21: Er wirft Salz in die Quelle und spricht ein Wort des HERRN."),
        estimate("Wie viele von ihnen werden von den Bären zerrissen?", 1, 100, 42, "",
                 "V. 24: 42.", 24, "Lies Vers 24."),
        tf("Der Text sagt, dass Elisa die Bären herbeiruft.", False, 24, "Lies Vers 24.",
           "V. 24: Elisa flucht im Namen des HERRN. Dass die Bären kommen, wird danach nur berichtet."),
    ],
    explain=[
        E("Waren das kleine Kinder?", "In V. 23 steht hebräisch ne’arim qetannim. Na’ar kann einen kleinen Jungen meinen, aber auch junge Männer bis ins Erwachsenenalter, etwa Diener oder Soldaten (1Sam 17,33; 2Sam 2,14). Auch das Wort in V. 24 (jeladim) bezeichnet in 1Kön 12,8 die jungen Berater des Königs. Manche Ausleger denken an eine Bande junger Männer, andere bleiben bei Kindern."),
        E("Was bedeutet „Komm herauf, Kahlkopf“?", "Eine Glatze galt als Schande; vielleicht war Elisa einfach kahl. Manche Ausleger hören in „Komm herauf“ eine Anspielung auf Elias Himmelfahrt (V. 11): Fahr doch auch auf! Dann wäre es Spott über den Propheten und seinen Auftrag."),
        E("Warum Bethel?", "Bethel war seit König Jerobeam ein Heiligtum mit einem goldenen Stierbild (1Kön 12,28–29), ein Zentrum des Gottesdienstes, gegen den die Propheten auftraten."),
    ],
    cards=["elisa"],
    teaser="Eine Gemeinde, in der niemand Not leidet – und ein Mann bekommt dabei einen neuen Namen.")

sec("zuschlagen", [R(APG, 4, 32, 37)], "Ein Herz und eine Seele",
    "Die Gläubigen sind ein Herz und eine Seele und betrachten ihren Besitz als gemeinsam. Wer Äcker oder Häuser hat, verkauft sie und legt den Erlös den Aposteln zu Füßen; niemand leidet Not. Auch Barnabas verkauft einen Acker.",
    bridge="Über 800 Jahre nach Elisa: Nach Pfingsten wächst die Gemeinde in Jerusalem schnell. Petrus und Johannes sind gerade vom Hohen Rat verhört und wieder freigelassen worden (Apg 4,1–31).",
    place="jerusalem",
    quiz=[
        tf("Unter den Gläubigen gab es niemanden, der Not litt.", True, 34, "Lies Vers 34.",
           "V. 34–35: Niemand war bedürftig, denn jedem wurde zugeteilt, was er brauchte."),
        choice("Was bedeutet der Name Barnabas laut V. 36?", ["Sohn des Trostes", "Sohn des Donners", "Freund Gottes", "Fels"], 36, "Lies Vers 36.",
               "V. 36: Sohn des Trostes. „Söhne des Donners“ nennt Jesus Jakobus und Johannes (Mk 3,17)."),
        choice("Woher stammt Barnabas?", ["Aus Zypern", "Aus Galiläa", "Aus Rom", "Aus Ägypten"], 36, "Lies Vers 36.",
               "V. 36: ein Levit, der aus Zypern stammt."),
    ],
    explain=[
        E("War das eine Pflicht?", "Der Text beschreibt, er befiehlt nicht. In Apg 5,4 sagt Petrus ausdrücklich, dass das Feld und der Erlös im eigenen Besitz bleiben durften. Apg 12,12 erwähnt später, dass Maria, die Mutter des Markus, weiter ein eigenes Haus hatte."),
        E("Haben Christen das nachgeahmt?", "Ja. Klöster leben seit dem 4. Jahrhundert mit gemeinsamem Besitz und berufen sich auch auf diese Stelle. Täufergemeinden wie die Hutterer leben seit dem 16. Jahrhundert in Gütergemeinschaft."),
    ],
    cards=["barnabas"],
    teaser="Ein Ehepaar tut scheinbar dasselbe wie Barnabas. Fast.")

sec("zuschlagen", [R(APG, 5, 1, 11)], "Hananias und Saphira",
    "Hananias und Saphira verkaufen ein Grundstück, behalten heimlich einen Teil des Erlöses und bringen den Rest. Petrus stellt erst ihn, Stunden später sie zur Rede. Beide fallen tot um. Große Furcht kommt über die ganze Gemeinde.",
    place="jerusalem",
    focus="Achte darauf, was Petrus Hananias genau vorwirft.",
    quiz=[
        choice("Was wirft Petrus Hananias vor?", ["Dass er den Heiligen Geist belogen hat", "Dass er nicht alles gegeben hat", "Dass er überhaupt verkauft hat", "Dass er Barnabas beneidet hat"], 3, "Lies Vers 3–4.",
               "V. 3–4: Feld und Geld blieben in seiner Verfügung. Der Vorwurf ist die Lüge – nicht Menschen, sondern Gott belogen."),
        error("Etwa drei [Tage] später kommt Saphira herein und weiß nicht, was geschehen ist.", "Stunden", 7,
              "V. 7: etwa drei Stunden später."),
        tf("Saphira wusste davon, dass ihr Mann einen Teil zurückbehielt.", True, 2, "Lies Vers 2.",
           "V. 2: Die Frau wusste davon; V. 9 nennt es eine Absprache der beiden."),
    ],
    explain=[
        E("Hat Petrus die beiden getötet?", "Das sagt der Text nicht. Bei Hananias spricht Petrus kein Urteil aus; er fällt hin, als er die Worte hört (V. 5). Bei Saphira kündigt Petrus den Tod an (V. 9). Die meisten Ausleger verstehen es als Gericht Gottes."),
        E("Gibt es ähnliche Geschichten in der Bibel?", "Ausleger erinnern an Achan in Jos 7: Auch am Anfang der Landnahme behält jemand heimlich etwas zurück und wird bestraft. Lukas benutzt in V. 2 für „beiseiteschaffen“ dasselbe seltene griechische Wort (nosphizomai), das die griechische Übersetzung des Alten Testaments in Jos 7,1 verwendet."),
        E("Gingen die beiden verloren?", "Darüber schweigt der Text. Schon die Kirchenväter waren nicht einig. Manche sahen hier die ewige Verdammnis. Andere verstanden es als Strafe in diesem Leben, die Gottes Gnade danach nicht ausschließt, und verweisen auf 1Kor 5,5 und 11,30–32."),
        E("Was ist „die Versammlung“?", "Griechisch ekklēsia, andere Übersetzungen sagen „Gemeinde“. Nach den ältesten Handschriften steht das Wort hier zum ersten Mal in der Apostelgeschichte.", "elbbk"),
    ],
    cards=["hananias-saphira"],
    teaser="Eine verzweifelte Mutter bittet Jesus um Hilfe. Er antwortet – zuerst gar nicht.")

# ───────────────────────── 3 · Harte Worte ─────────────────────────
sec("hart", [R(MT, 15, 21, 28)], "Die Frau und die „Hündchen“",
    "Eine kanaanäische Frau bittet Jesus, ihre Tochter zu heilen. Er schweigt zuerst, dann sagt er, er sei nur zu Israel gesandt, und spricht vom Brot der Kinder und den Hündchen. Sie greift das Bild auf. Jesus nennt ihren Glauben groß, und die Tochter wird gesund.",
    bridge="Jesus hat mit Pharisäern aus Jerusalem über rein und unrein gestritten (Mt 15,1–20). Nun zieht er sich in die Gegend von Tyrus und Sidon zurück, außerhalb des jüdischen Landes.",
    place="tyrus",
    focus="Achte darauf, wie die Frau mit Jesu Antworten umgeht.",
    quiz=[
        order("Bring den Ablauf in die richtige Reihenfolge.",
              ["Jesus antwortet ihr nicht", "Die Jünger wollen sie wegschicken", "Jesus spricht vom Brot der Kinder", "Die Frau spricht von den Brotkrumen", "Jesus nennt ihren Glauben groß"],
              "V. 23–28: Schweigen, die Bitte der Jünger, das Wort vom Brot, die Antwort der Frau – und Jesu Lob."),
        choice("Wie redet die Frau Jesus in V. 22 an?", ["Herr, Sohn Davids", "Rabbi", "Prophet aus Nazareth", "Meister"], 22, "Lies Vers 22.",
               "V. 22: „Sohn Davids“ ist ein Titel für den Messias Israels – aus dem Mund einer Nichtjüdin."),
    ],
    explain=[
        E("Warum „kanaanäisch“?", "Markus nennt sie eine Griechin aus Syrophönizien (Mk 7,26). Matthäus wählt das alte Wort „Kanaaniter“: So hießen die Bewohner des Landes vor Israel, die Gegner aus den Büchern Mose und Josua."),
        E("Ist „Hündchen“ eine Beleidigung?", "„Hund“ war ein verbreitetes abwertendes Wort für Nichtjuden. Jesus benutzt aber die Verkleinerungsform (kynaria), also Haushündchen unter dem Tisch. Ob das die Härte mildert, sehen Ausleger unterschiedlich."),
        E("Wie verstehen Ausleger Jesu Zögern?", "Seit den Kirchenvätern (z. B. Johannes Chrysostomus) sagen viele: Jesus prüft die Frau, damit ihr Glaube sichtbar wird. Andere betonen V. 24: Sein Auftrag galt zuerst Israel (vgl. Mt 10,5–6), die Völker kommen erst nach der Auferstehung in den Blick (Mt 28,19). Manche lesen auch, dass Jesus sich vom Einwand der Frau bewegen lässt."),
    ],
    cards=["kanaanaeerin"],
    fact="Nur zu dieser Frau sagt Jesus bei Matthäus ausdrücklich, ihr Glaube sei groß. Ähnlich hebt er sonst nur den Glauben eines anderen Nichtjuden hervor: den des Hauptmanns von Kapernaum (Mt 8,10).",
    teaser="Jesus spricht von Vater, Mutter, Frau und Kindern – und benutzt dabei ein Wort, das man nicht erwartet.")

sec("hart", [R(LK, 14, 25, 33)], "Wer nicht hasst …",
    "Zu den großen Mengen, die ihm folgen, sagt Jesus: Wer nicht Vater, Mutter, Frau, Kinder und sogar sein eigenes Leben hasst und sein Kreuz trägt, kann nicht sein Jünger sein. Dazu zwei Bilder: ein Turmbau und ein König vor dem Krieg – beide überschlagen zuerst, was es kostet.",
    bridge="Jesus ist auf dem Weg nach Jerusalem (Lk 9,51). Kurz vorher hat er beim Essen im Haus eines Pharisäers das Gleichnis vom großen Abendmahl erzählt (Lk 14,15–24).",
    quiz=[
        choice("Zu wem spricht Jesus hier?", ["Zu großen Volksmengen, die mit ihm gehen", "Nur zu den Zwölf", "Zu Pharisäern beim Essen", "Zu einer einzelnen Familie"], 25, "Lies Vers 25.",
               "V. 25: Große Volksmengen gehen mit ihm; er dreht sich zu ihnen um."),
        error("Ein König mit 10.000 Mann überlegt, ob er dem entgegentreten kann, der mit [30.000] kommt.", "20.000", 31,
              "V. 31: mit 20.000 – doppelt so viele."),
        tf("Beide Bilder, Turm und König, handeln davon, vorher die Kosten zu überschlagen.", True, 28, "Lies Vers 28–32.",
           "V. 28–32: Der Bauherr berechnet die Kosten, der König berät sich – und V. 33 zieht daraus den Schluss."),
    ],
    explain=[
        E("Heißt „hassen“ hier wirklich hassen?", "Viele Ausleger verweisen auf eine hebräische Ausdrucksweise: „Lieben und hassen“ heißt oft „vorziehen und zurücksetzen“ (vgl. 1Mo 29,30–31; Mal 1,2–3). Die Parallele Mt 10,37 sagt: wer Vater oder Mutter mehr liebt als mich. Andere betonen, dass Lukas das harte Wort bewusst stehen lässt."),
        E("Was hieß „sein Kreuz tragen“?", "Verurteilte mussten den Querbalken ihres Kreuzes selbst zur Hinrichtungsstätte tragen. Für die Hörer war das kein frommes Bild, sondern eine Szene, die sie von römischen Hinrichtungen kannten."),
        E("Wie passt das zum Gebot, die Eltern zu ehren?", "Jesus hält am Gebot fest und kritisiert, wer es mit frommen Begründungen umgeht (Mk 7,9–13). Am Kreuz vertraut er seine Mutter dem Jünger Johannes an (Joh 19,26–27)."),
    ],
    try_="Lies Lk 14,26 und Mt 10,37 nebeneinander. Was ist gleich, was ist anders?",
    teaser="Das bekannteste Lied der Verbannten beginnt mit Tränen am Fluss – und endet mit einem Satz, den kaum jemand mitsingt.")

sec("hart", [R(PS, 137, 1, 9)], "An den Flüssen Babels",
    "Die Verbannten sitzen weinend an den Flüssen Babels; ihre Bewacher verlangen Lieder von Zion. Sie schwören, Jerusalem nicht zu vergessen. Am Ende bitten sie Gott, sich an Edom zu erinnern, und preisen den glücklich, der Babels Kinder an den Felsen schmettert.",
    bridge="Im Jahr 587/586 v. Chr. zerstörten die Babylonier Jerusalem und den Tempel und verschleppten einen großen Teil des Volkes nach Babylon (2Kön 25).",
    place="babylon",
    quiz=[
        choice("Was verlangen die Bewacher von den Verbannten?", ["Ein Lied von Zion", "Ein Opfer für ihre Götter", "Die Namen ihrer Anführer", "Ein Loblied auf Babel"], 3, "Lies Vers 3.",
               "V. 3: Sie fordern ein Lied, Freude – eines von Zions Liedern."),
        tf("Der Psalm bittet Gott, an Edom zu denken, was es am Tag Jerusalems gesagt hat.", True, 7, "Lies Vers 7.",
           "V. 7: Die Edomiter riefen, man solle Jerusalem bis auf den Grund niederreißen."),
    ],
    explain=[
        E("Wer war Edom?", "Ein Nachbarvolk im Südosten. Nach 1Mo 36 stammten die Edomiter von Esau ab, waren also Verwandte Israels. Nach Obadja 10–14 freuten sie sich über den Fall Jerusalems und lieferten Flüchtlinge aus."),
        E("Wie können Gläubige so beten?", "Viele Ausleger betonen: Der Beter übt die Rache nicht selbst aus, sondern legt sie in Gottes Hand (vgl. 5Mo 32,35; Röm 12,19). Dietrich Bonhoeffer schrieb 1940 („Das Gebetbuch der Bibel“), Gottes Rache sei am Kreuz an Christus vollzogen worden, der für seine Feinde betete – darum könne die Gemeinde auch diese Psalmen mitbeten."),
        E("Werden diese Verse in Kirchen gebetet?", "Unterschiedlich. Das katholische Stundengebet lässt V. 7–9 seit der Reform nach dem Zweiten Vatikanischen Konzil aus. Die orthodoxe Kirche singt den Psalm in der Vorfastenzeit vollständig. Kirchenväter wie Augustinus deuteten die „kleinen Kinder“ Babels als aufkeimende böse Gedanken, die man früh am Felsen – Christus – zerschlagen soll."),
    ],
    cards=["fluchpsalmen"],
    fact="Die ersten Verse wurden als „Rivers of Babylon“ (The Melodians 1970, Boney M. 1978) weltbekannt. Das Lied endet nicht mit V. 7–9, sondern mit Ps 19,15.",
    teaser="Ein Satz im Hebräerbrief hat Christen jahrhundertelang beunruhigt. Er beginnt mit dem Wort „unmöglich“.")

sec("hart", [R(HEBR, 6, 4, 12)], "Unmöglich?",
    "Es sei unmöglich, die, die erleuchtet waren, den Heiligen Geist empfangen haben und dann abgefallen sind, wieder zur Umkehr zu bringen. Dazu das Bild vom Land, das Frucht oder Dornen trägt. Dann: Von euch sind wir Besseres überzeugt; Gott vergisst eure Liebe nicht.",
    bridge="Der Hebräerbrief richtet sich an Christen, die unter Druck stehen und müde geworden sind (Hebr 10,32–36). Kurz vorher tadelt der Verfasser, dass sie im Verstehen nicht weitergekommen sind (Hebr 5,11–14).",
    focus="Achte darauf, wie sich der Ton ab V. 9 verändert.",
    quiz=[
        choice("Mit welchem Bild unterstreicht der Verfasser seine Warnung?", ["Mit Land, das Nutzpflanzen oder Dornen trägt", "Mit einem Haus auf Sand", "Mit einem Weinstock und seinen Reben", "Mit einem Schiff im Sturm"], 7, "Lies Vers 7–8.",
               "V. 7–8: Land, das den Regen trinkt und Nützliches hervorbringt, wird gesegnet; trägt es Dornen, ist es dem Fluch nahe."),
        tf("Direkt nach der Warnung schreibt der Verfasser, er sei bei seinen Lesern von Besserem überzeugt.", True, 9, "Lies Vers 9.",
           "V. 9: Wir sind von besseren Dingen überzeugt, auch wenn wir so reden."),
        choice("Was vergisst Gott laut V. 10 nicht?", ["Ihr Werk und ihre Liebe, mit der sie den Heiligen dienen", "Ihre Opfer im Tempel", "Den Tag ihrer Taufe", "Ihre Gebete für die Verfolger"], 10, "Lies Vers 10.",
               "V. 10: ihr Werk und die Liebe, die sie im Dienst an den Heiligen gezeigt haben und noch zeigen."),
    ],
    explain=[
        E("Wovor warnt der Text?", "Die meisten Ausleger verstehen „abfallen“ nicht als einzelne Sünden, sondern als bewusstes Abwenden von Christus. V. 6 beschreibt es so, als stelle man sich auf die Seite derer, die Jesus gekreuzigt haben."),
        E("Waren das echte Christen? – reformierte Sicht", "Reformierte Ausleger in der Linie Calvins sagen meist: Wer wirklich wiedergeboren ist, fällt nicht endgültig ab. Die Beschriebenen hätten viel vom Wirken Gottes erlebt, aber keinen rettenden Glauben gehabt. Sie verweisen auf V. 9, wo der Verfasser von „besseren“ Dingen spricht."),
        E("Waren das echte Christen? – andere Sichtweisen", "Arminianische, wesleyanische und lutherische Ausleger, ebenso die katholische und die orthodoxe Kirche, lesen V. 4–5 als Beschreibung echter Gläubiger: Ein Christ kann vom Glauben abfallen. Viele von ihnen verstehen „unmöglich“ als Aussage über menschliche Möglichkeiten, nicht über Gottes. Wieder andere lesen die Verse als hypothetische Warnung: So wäre es, wenn – und gerade die Warnung bewahre vor dem Abfall."),
        E("Warum war die Stelle in der Kirchengeschichte so umstritten?", "Im 3. Jahrhundert beriefen sich die Novatianer auf sie, um Christen, die in der Verfolgung abgefallen waren, nie wieder aufzunehmen; die Mehrheit der Kirche lehnte das ab. Luther stellte den Hebräerbrief auch wegen dieser Stelle in seiner Bibel ans Ende des Neuen Testaments."),
    ],
    cards=["beharrlichkeit"],
    try_="Lies V. 4–6 und dann V. 9–12. Wie verändert der zweite Teil den Klang des ersten?",
    prayer={"ref": R(MK, 9, 24), "source": "Markus 9,24"},
    teaser="Kopfbedeckung, Haare und Engel: ein Abschnitt, bei dem selbst erfahrene Ausleger zugeben, dass sie nicht alles verstehen.")

# ───────────────────────── 4 · „Die Frau schweige“ ─────────────────────────
sec("frauen", [R(KOR1, 11, 2, 10)], "Frauen, die beten und weissagen",
    "Paulus lobt die Korinther, dass sie an den Überlieferungen festhalten. Christus ist das Haupt jedes Mannes, der Mann das Haupt der Frau, Gott das Haupt Christi. Ein Mann soll beim Beten und Weissagen den Kopf nicht bedecken, eine Frau soll ihn bedecken, auch mit Blick auf die Engel (V. 10).",
    bridge="Paulus schreibt an die Gemeinde in Korinth, die er selbst gegründet hat. Ab Kapitel 11 geht es um Fragen des Gottesdienstes.",
    place="korinth",
    focus="Achte darauf, was Männer und Frauen im Gottesdienst tun.",
    quiz=[
        choice("Was tun Frauen nach V. 5 im Gottesdienst?", ["Sie beten und weissagen", "Sie schweigen", "Sie singen nur", "Sie hören nur zu"], 5, "Lies Vers 5.",
               "V. 5: Paulus spricht von der Frau, die betet oder weissagt – und regelt, wie sie dabei aussehen soll."),
        tf("Paulus schreibt, ein Mann solle beim Beten etwas auf dem Kopf tragen.", False, 4, "Lies Vers 4.",
           "V. 4: Umgekehrt – ein Mann, der mit bedecktem Haupt betet, entehrt sein Haupt."),
        choice("Wer ist nach V. 3 das Haupt Christi?", ["Gott", "Der Mann", "Die Gemeinde", "Der Geist"], 3, "Lies Vers 3.",
               "V. 3: Christus ist das Haupt jedes Mannes, der Mann das Haupt der Frau, Gott das Haupt Christi."),
    ],
    explain=[
        E("Was heißt „Haupt“?", "Griechisch kephalē. Ob es hier vor allem „Oberhaupt, Autorität“ oder „Ursprung, Quelle“ meint, gehört zu den meistdiskutierten Fragen dieses Textes. V. 8 (die Frau vom Mann) wird oft für die zweite Bedeutung angeführt, V. 10 (eine „Macht“ auf dem Haupt) für die erste."),
        E("Was bedeutet „um der Engel willen“?", "Niemand weiß es sicher. Viele Kirchenväter dachten an Engel, die am Gottesdienst teilnehmen und auf Ordnung achten; ähnliche Vorstellungen kennt man aus Texten der Gemeinschaft von Qumran. Andere denken an die „Gottessöhne“ in 1Mo 6,2."),
        E("Kopfbedeckung – wie halten es Kirchen heute?", "Unterschiedlich. In vielen orthodoxen Gemeinden, bei manchen Brüdergemeinden, Mennoniten und Amischen tragen Frauen im Gottesdienst ein Tuch. Die meisten Kirchen verstehen die Anweisung als an die damalige Kultur gebunden, in der eine unbedeckte verheiratete Frau als anstößig galt, und suchen das Anliegen dahinter."),
    ],
    teaser="Im nächsten Abschnitt setzt Paulus seiner eigenen Begründung einen Gedanken entgegen.")

sec("frauen", [R(KOR1, 11, 11, 16)], "Haar, Natur und Gewohnheit",
    "Im Herrn ist weder die Frau ohne den Mann noch der Mann ohne die Frau; die Frau ist vom Mann, der Mann durch die Frau, alles aber von Gott. Paulus fragt, was sich gehört und was die Natur lehrt, und verweist auf die Gewohnheit der Gemeinden.",
    place="korinth",
    quiz=[
        error("Wie die Frau vom Mann ist, so ist auch der Mann durch die [Engel]; alles aber ist von Gott.", "Frau", 12,
              "V. 12: Der Mann ist durch die Frau – jeder Mann wird von einer Frau geboren."),
        choice("Worauf beruft sich Paulus in V. 14–15?", ["Auf das, was die Natur lehrt", "Auf ein Wort Jesu", "Auf das Gesetz des Mose", "Auf eine Vision"], 14, "Lies Vers 14.",
               "V. 14: Lehrt euch nicht schon die Natur …?"),
        tf("Paulus schließt mit dem Hinweis, dass die Gemeinden Gottes keine andere Gewohnheit haben.", True, 16, "Lies Vers 16.",
           "V. 16: Wer streiten will – wir und die Gemeinden Gottes haben eine solche Gewohnheit nicht."),
    ],
    explain=[
        E("Was meint „Natur“?", "Griechisch physis: das, was als selbstverständlich gilt. In der griechisch-römischen Welt trugen Männer meist kurzes Haar. Zugleich kennt die Bibel Männer mit Gelübde, die ihr Haar lang wachsen ließen (4Mo 6,5; Ri 13,5). Ob Paulus eine Schöpfungsordnung oder eine Sitte seiner Zeit meint, verstehen Ausleger verschieden."),
        E("Wie passen V. 3–10 und V. 11–12 zusammen?", "Komplementäre Ausleger: Paulus beschreibt eine Ordnung mit verschiedenen Aufgaben bei gleichem Wert; V. 11–12 bewahren davor, daraus Geringschätzung abzuleiten. Egalitäre Ausleger: Das „im Herrn“ in V. 11 relativiert die Begründung aus der Schöpfungsreihenfolge."),
    ],
    cards=["rollen"],
    teaser="Drei Kapitel später: ein Gottesdienst, in dem jeder etwas mitbringt – und Paulus Ordnung hineinbringen will.")

sec("frauen", [R(KOR1, 14, 26, 33)], "Ordnung im Gottesdienst",
    "Wenn die Gemeinde zusammenkommt, bringt jeder etwas mit: einen Psalm, eine Lehre, eine Sprachenrede, eine Offenbarung, eine Auslegung. Paulus ordnet: höchstens zwei oder drei Sprachenredner nacheinander, mit Auslegung; Propheten reden, die anderen prüfen. Gott ist ein Gott des Friedens.",
    place="korinth",
    quiz=[
        choice("Was soll ein Sprachenredner tun, wenn niemand auslegen kann?", ["In der Versammlung schweigen und für sich zu Gott reden", "Trotzdem laut weiterreden", "Die Versammlung verlassen", "Einen Propheten um Hilfe bitten"], 28, "Lies Vers 28.",
               "V. 28: Er soll in der Versammlung schweigen und zu sich selbst und zu Gott reden."),
        choice("Wer soll nach V. 30 schweigen?", ["Der erste Prophet, wenn ein anderer eine Offenbarung bekommt", "Alle Frauen", "Alle Sprachenredner", "Die Zuhörer"], 30, "Lies Vers 30.",
               "V. 30: Bekommt ein anderer, der dasitzt, eine Offenbarung, soll der erste schweigen."),
        tf("Paulus schreibt, dass alle der Reihe nach weissagen können.", True, 31, "Lies Vers 31.",
           "V. 31: Ihr könnt alle nacheinander weissagen, damit alle lernen und getröstet werden."),
    ],
    explain=[
        E("Was ist „in einer Sprache reden“?", "Gemeint ist die Zungenrede (griechisch glōssa): Beten oder Gotteslob in einer Sprache, die der Redende nicht gelernt hat (vgl. 1Kor 14,2.14). Pfingstliche und charismatische Kirchen praktizieren sie heute. Andere Kirchen verstehen sie als Gabe der Anfangszeit oder sind zurückhaltend."),
        E("Was heißt hier „weissagen“?", "Prophetisches Reden: Worte, die die Gemeinde nach V. 3 aufbauen, ermahnen und trösten. Paulus erwartet, dass sie geprüft werden (V. 29)."),
    ],
    memory_verse=MV(R(KOR1, 14, 33), "Denn Gott ist nicht ein Gott der Unordnung, sondern des Friedens"),
    teaser="Ein Satz, der in Kirchen bis heute zitiert wird – und in einigen alten Handschriften an einer anderen Stelle steht.")

sec("frauen", [R(KOR1, 14, 33, 40)], "„Die Frauen sollen schweigen“",
    "Die Frauen sollen in den Versammlungen schweigen und, wenn sie etwas lernen wollen, zu Hause ihre Männer fragen. Paulus nennt das, was er schreibt, ein Gebot des Herrn. Am Ende: Strebt nach dem Weissagen, verbietet die Sprachenrede nicht, alles geschehe anständig und geordnet.",
    place="korinth",
    focus="Achte auf den Zusammenhang: Wovon handelt das ganze Kapitel?",
    quiz=[
        choice("Was sollen Frauen tun, wenn sie etwas lernen wollen?", ["Zu Hause ihre eigenen Männer fragen", "Einen Propheten fragen", "Nach der Versammlung die Apostel fragen", "Die Ältesten fragen"], 35, "Lies Vers 35.",
               "V. 35: daheim ihre eigenen Männer fragen."),
        choice("Worauf beruft sich Paulus in V. 34?", ["Auf das Gesetz", "Auf ein Wort Jesu", "Auf eine Offenbarung", "Auf die Sitte der Griechen"], 34, "Lies Vers 34.",
               "V. 34: wie auch das Gesetz sagt."),
        tf("Am Ende des Kapitels fordert Paulus dazu auf, nach dem Weissagen zu streben.", True, 39, "Lies Vers 39.",
           "V. 39: Eifert danach zu weissagen, und wehrt der Sprachenrede nicht."),
    ],
    explain=[
        E("Wie passt das zu 1Kor 11,5?", "Dort setzt Paulus voraus, dass Frauen im Gottesdienst beten und weissagen. Ausleger lösen die Spannung verschieden: Manche beziehen das Schweigen auf eine bestimmte Art des Redens, etwa das Beurteilen der Prophetien (V. 29) oder Zwischenfragen (V. 35). Andere sehen in 1Kor 11 einen anderen Rahmen als die Versammlung der ganzen Gemeinde."),
        E("Welches Gesetz meint Paulus?", "Das bleibt offen, denn das Alte Testament enthält kein Gebot, dass Frauen schweigen sollen. Manche denken an 1Mo 3,16, andere an die Ordnung der Schrift insgesamt, wieder andere an jüdische Synagogenregeln."),
        E("Was steht in den Handschriften?", "In allen erhaltenen Handschriften stehen V. 34–35. In einer Gruppe westlicher Handschriften (z. B. dem Codex Claromontanus) stehen sie aber nicht hier, sondern nach V. 40. Einige Ausleger, etwa der pfingstkirchliche Neutestamentler Gordon Fee, halten sie deshalb für eine spätere Randnotiz; die meisten halten sie für ursprünglich und erklären die Umstellung anders."),
        E("Wie gehen Kirchen damit um?", "Die katholische und die orthodoxe Kirche weihen nur Männer zu Priestern; Frauen lesen, lehren und leiten aber in vielen Bereichen. Die evangelischen Landeskirchen ordinieren Frauen seit dem 20. Jahrhundert. In Freikirchen gibt es beides: Gemeinden, in denen Frauen predigen und leiten, und solche, die Lehre und Leitung Männern vorbehalten."),
    ],
    fact="Das griechische Wort für „schweigen“ (sigaō) steht in diesem Kapitel dreimal: für Sprachenredner ohne Ausleger (V. 28), für einen Propheten, wenn ein anderer redet (V. 30), und für die Frauen (V. 34).",
    teaser="Ein anderer Brief, ein ähnliches Thema – und eine Begründung, die bis zu Adam und Eva zurückgeht.")

sec("frauen", [R(TIM1, 2, 8, 15)], "Nicht lehren?",
    "Die Männer sollen ohne Zorn beten, die Frauen sich schlicht kleiden und mit guten Werken schmücken. Eine Frau soll in Stille lernen; Paulus erlaubt ihr nicht, zu lehren oder über den Mann zu herrschen, und begründet das mit Adam und Eva. Sie werde durch das Kindergebären gerettet, wenn sie im Glauben bleibt.",
    bridge="Paulus schreibt an seinen Mitarbeiter Timotheus, den er in Ephesus zurückgelassen hat, um dort gegen Irrlehrer vorzugehen (1Tim 1,3–7).",
    place="ephesus",
    quiz=[
        choice("Womit sollen sich Frauen nach V. 9–10 schmücken?", ["Mit guten Werken", "Mit Gold und Perlen", "Mit geflochtenem Haar", "Mit kostbarer Kleidung"], 10, "Lies Vers 9–10.",
               "V. 9–10: nicht mit Haarflechten, Gold, Perlen oder teurer Kleidung, sondern mit guten Werken."),
        tf("Nach V. 11 soll eine Frau lernen.", True, 11, "Lies Vers 11.",
           "V. 11: Sie soll lernen – in Stille und Unterordnung. Dass Frauen religiös unterrichtet wurden, war in der Antike nicht selbstverständlich."),
        choice("Womit begründet Paulus V. 12?", ["Mit Adam und Eva", "Mit der Sitte in Ephesus", "Mit einem Wort Jesu", "Mit den Erfahrungen in Korinth"], 13, "Lies Vers 13–14.",
               "V. 13–14: Adam wurde zuerst gebildet, und nicht Adam, sondern die Frau wurde getäuscht."),
    ],
    explain=[
        E("Was heißt „über den Mann herrschen“?", "Griechisch authentein, im Neuen Testament nur hier. Ob es neutral „Autorität ausüben“ oder negativ „sich anmaßen, bestimmen über“ bedeutet, ist umstritten. Komplementäre Ausleger lesen V. 12 als bleibende Regel für Lehre und Leitung in der Gemeinde; egalitäre beziehen ihn auf eine besondere Lage in Ephesus mit Irrlehren (vgl. 1Tim 5,13–15; 2Tim 3,6–7)."),
        E("Gerettet durch Kindergebären?", "Einer der rätselhaftesten Verse des Neuen Testaments. Deutungen: Frauen werden in ihrer Lebensaufgabe bewahrt; sie werden durch die Geburt des einen Kindes gerettet – Christus, mit Blick auf 1Mo 3,15; oder sie werden bei der Geburt bewahrt. Der Nachsatz bindet es an Glauben, Liebe und Heiligkeit."),
        E("Gilt das mit Schmuck und Haaren heute?", "Kunstvoll geflochtenes Haar mit Gold und Perlen war bei reichen Frauen im Römischen Reich Mode; ähnlich spricht 1Petr 3,3–4. Die meisten Kirchen lesen das heute nicht als Schmuckverbot; einige Gemeinschaften wie die Amischen schon."),
    ],
    teaser="Einer der Namen im nächsten Abschnitt hat in Bibelübersetzungen über Jahrhunderte sein Geschlecht gewechselt.")

sec("frauen", [R(ROEM, 16, 1, 7)], "Phöbe, Priska und Junia",
    "Paulus empfiehlt Phöbe, Dienerin der Gemeinde in Kenchreä, die vielen beigestanden hat. Er grüßt Priska und Aquila, seine Mitarbeiter, und die Gemeinde in ihrem Haus – und Andronikus und Junia, die unter den Aposteln angesehen sind.",
    bridge="Paulus schreibt den Römerbrief wohl in Korinth, kurz vor seiner Reise nach Jerusalem (Röm 15,25–26). Am Ende stehen Empfehlungen und Grüße an viele Menschen in Rom.",
    place="kenchreae",
    quiz=[
        choice("Was ist Phöbe laut V. 1?", ["Dienerin der Gemeinde in Kenchreä", "Apostelin in Rom", "Die Frau des Aquila", "Prophetin in Jerusalem"], 1, "Lies Vers 1.",
               "V. 1: eine Dienerin (griechisch diakonos) der Gemeinde in Kenchreä."),
        tf("Paulus nennt Priska und Aquila seine Mitarbeiter.", True, 3, "Lies Vers 3.",
           "V. 3: meine Mitarbeiter in Christus Jesus."),
        choice("Was haben Priska und Aquila für Paulus riskiert?", ["Ihr Leben", "Ihr Vermögen", "Ihre Ehe", "Ihren Platz in der Synagoge"], 4, "Lies Vers 4.",
               "V. 4: Sie haben für sein Leben den eigenen Hals hingehalten."),
    ],
    explain=[
        E("Was war Phöbe?", "Griechisch diakonos – dasselbe Wort, das Paulus für sich selbst (1Kor 3,5) und für Gemeindeämter (Phil 1,1; 1Tim 3,8) benutzt. Ob es hier ein Amt (Diakonin) oder allgemein einen Dienst meint, ist umstritten. Wahrscheinlich brachte sie den Brief nach Rom."),
        E("Junia oder Junias?", "Im Griechischen steht Iounian, das beides sein kann. Die Kirchenväter lasen fast einhellig einen Frauennamen; Johannes Chrysostomus staunt über diese Frau, die würdig war, Apostelin genannt zu werden. Ab dem Mittelalter setzte sich die Männerform „Junias“ durch, die in antiken Quellen aber nicht belegt ist. Neuere Übersetzungen wie Luther 2017 und die Einheitsübersetzung 2016 schreiben wieder Junia."),
        E("„Unter den Aposteln ausgezeichnet“?", "Das Griechische kann heißen: „angesehen unter den Aposteln“ (also selbst Apostel im weiteren Sinn) oder „bei den Aposteln angesehen“ (bekannt bei ihnen). Beide Lesarten haben heute Vertreter; die Kirchenväter lasen meist die erste."),
    ],
    cards=["phoebe", "priska", "junia"],
    fact="Priska wird im Neuen Testament sechsmal zusammen mit Aquila genannt – viermal zuerst. Für antike Texte, die meist den Mann voranstellen, ist das ungewöhnlich.",
    try_="Lies Apg 18,1–3 und 18,24–26. Was erfährst du dort über Priska und Aquila?")

P.write()
