#!/usr/bin/env python3
"""Source for the reading plan „Die unsichtbare Welt – Gottes Rat, Mächte und Gewalten“ (generates assets/plans/unsichtbare-welt.json).

Liest die Texte bewusst mit dem Weltbild von Michael S. Heiser („The Unseen Realm“) und nennt andere Sichtweisen.

python3 -I tools/plans/unsichtbare_welt.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/unsichtbare-welt.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

GEN, EX, LEV, NUM, DTN = 1, 2, 3, 4, 5
KOEN1, HIOB, PS, JES, HES, DAN = 11, 18, 19, 23, 26, 27
MT, MK, LK, JOH, APG, ROEM, EPH, HEBR, PETR1, PETR2, JUD = 40, 41, 42, 43, 44, 45, 49, 58, 60, 61, 65

P = PlanBuilder(
    "unsichtbare-welt", "uw", "Die unsichtbare Welt", "Gottes Rat, Mächte und Gewalten",
    "Götter, die sterben werden, Söhne Gottes, die Kinder zeugen, ein Fürst von Persien, der einen Engel aufhält: Die Bibel erzählt von einer unsichtbaren Welt, "
    "über die man selten spricht. Dieser Plan liest die Texte bewusst mit dem Weltbild des Alttestamentlers Michael S. Heiser („The Unseen Realm“) "
    "und nennt dazu, wie andere Ausleger sie verstehen. 25 Abschnitte vom himmlischen Rat bis zu Gottes neuer Familie.",
    "glauben",
    stages=[("rat", "Gottes Rat"), ("aufstand", "Drei Aufstände"), ("sichtbar", "Der Gott, den man sehen kann"),
            ("maechte", "Riesen, Fürsten, fremde Götter"), ("jesus", "Jesus und die Mächte"), ("familie", "Gottes neue Familie")],
    cards=[
        ("heiser", "person", "Michael S. Heiser", "Amerikanischer Alttestamentler (1963–2023) mit Doktortitel in Hebräischer Bibel und semitischen Sprachen. In „The Unseen Realm“ (2015) liest er die ganze Bibel vor dem Hintergrund des himmlischen Rats. Vieles davon hat Wurzeln in alter jüdischer und christlicher Auslegung; einzelne Deutungen sind unter Auslegern umstritten. Dieser Plan folgt seinem Ansatz.", "Ps 82; 5Mo 32,8"),
        ("rat", "begriff", "Der himmlische Rat", "Die Bibel beschreibt Gott umgeben von himmlischen Wesen, die vor ihm stehen und mit ihm beraten: Söhne Gottes, Heer des Himmels, Heilige (Ps 82,1; 89,6–8; 1Kön 22,19; Hiob 1,6). Nach Heiser ist Gott unter ihnen einzigartig: der Einzige, der nicht geschaffen ist. Die anderen sind seine Geschöpfe und Diener, keine Gleichrangigen.", "Ps 82,1; 89,6–8"),
        ("elohim", "begriff", "Elohim", "Das häufigste hebräische Wort für Gott, der Form nach Mehrzahl. Je nach Zusammenhang meint es den Gott Israels, fremde Götter, himmlische Wesen (Ps 82,1.6) oder sogar den Geist des toten Samuel (1Sam 28,13). Heiser versteht es deshalb als Bezeichnung für Bewohner der unsichtbaren Welt, nicht als Name für ein bestimmtes Wesen.", "Ps 82; 1Sam 28,13"),
        ("satan", "begriff", "Der Satan", "Hebräisch satan heißt „Widersacher, Ankläger“. In Hiob 1–2 und Sach 3,1–2 steht es mit Artikel: „der Satan“, also wohl ein Titel oder eine Rolle. Im Neuen Testament ist Satan der Name des Teufels, des Gegenspielers Gottes, und wird mit der Schlange aus Eden gleichgesetzt (Offb 12,9). Ob der Satan in Hiob schon dieselbe Gestalt ist, wird verschieden gesehen.", "Hiob 1,6; Offb 12,9"),
        ("nachasch", "begriff", "Die Schlange (nachasch)", "Das hebräische Wort für Schlange klingt an „glänzend“ und „wahrsagen“ an. Heiser liest die Schlange in Eden als strahlendes Wesen aus Gottes Rat, nicht als gewöhnliches Tier. Ähnlich heißen „brennende“ Schlangen in 4Mo 21,6 Seraphim. Offb 12,9 nennt die alte Schlange den Teufel und Satan.", "1Mo 3,1; Offb 12,9"),
        ("nephilim", "begriff", "Nephilim", "Hebräisch, nach 1Mo 6,4 Kinder der Söhne Gottes und der Menschentöchter; in 4Mo 13,33 sehen die Kundschafter sie im Land. Die Bedeutung ist umstritten: „Gefallene“ (von hebräisch fallen) oder, nach einem aramäischen Wort, „Riesen“. Die Septuaginta übersetzt gigantes, die Elberfelder „Riesen“.", "1Mo 6,4; 4Mo 13,33"),
        ("henoch", "begriff", "Das Henochbuch", "Eine jüdische Schrift aus den letzten Jahrhunderten vor Christus; Bruchstücke fand man in Qumran. Sie erzählt, wie 200 „Wächter“ auf den Hermon herabstiegen, Frauen nahmen und Riesen zeugten (1Hen 6–10). Der Judasbrief zitiert sie (Jud 14–15). In der äthiopisch-orthodoxen Kirche gehört sie zur Bibel, sonst nicht.", "Jud 14–15"),
        ("tartaros", "begriff", "Tartaros", "In 2Petr 2,4 steht ein griechisches Verb, das wörtlich „in den Tartaros werfen“ heißt. Für die Griechen war der Tartaros der tiefste Abgrund, noch unter dem Hades, in dem die Titanen gefangen lagen. Die griechische Fassung des Henochbuchs nennt den Tartaros als Ort der gefallenen Wächter. Im Neuen Testament kommt das Wort nur hier vor.", "2Petr 2,4"),
        ("dtn32", "begriff", "Das Weltbild von 5. Mose 32", "Heisers Name für einen Gedanken, den er durch die Bibel verfolgt: Nach Babel hat Gott die Völker den Söhnen Gottes zugeteilt und Israel für sich behalten (5Mo 32,8–9; 4,19–20). Die Götter der Völker sind darum echte Mächte, aber Geschöpfe, die abfielen (Ps 82). Das Neue Testament erzählt nach Heiser, wie Gott die Völker zurückholt.", "5Mo 32,8–9; 4,19–20"),
        ("engel-des-herrn", "begriff", "Der Engel des HERRN", "Eine Gestalt, die als Bote Gottes auftritt und doch in der Ich-Form als Gott spricht (1Mo 16,7–13; 22,11–18; 2Mo 3,2–6; Ri 13). Viele Kirchenväter, etwa Justin, sahen in ihm den Sohn Gottes vor seiner Menschwerdung. Heiser spricht vom „sichtbaren“ oder „zweiten“ Jahwe. Jüdische Ausleger sehen meist einen Engel, durch den Gott spricht.", "2Mo 3,2; 23,20–23"),
        ("menschensohn", "begriff", "Der Menschensohn", "In Dan 7,13 kommt „einer wie ein Menschensohn“ mit den Wolken des Himmels zum Alten an Tagen. Auf Wolken fährt im Alten Testament sonst Gott selbst (5Mo 33,26; Ps 104,3; Jes 19,1). Jesus nennt sich am häufigsten so; vor dem Hohen Rat bezieht er Dan 7,13 auf sich (Mk 14,62).", "Dan 7,13; Mk 14,62"),
        ("rephaiter", "begriff", "Rephaiter", "Ein Volk großer Menschen im Ostjordanland, zu dem Og von Basan gehörte (5Mo 2,11; 3,11). Dasselbe hebräische Wort, Rephaim, bezeichnet in der Poesie die Schatten der Toten (Jes 14,9; 26,14). Auch in Texten aus Ugarit sind die rpum verstorbene Könige. Heiser verbindet die Riesenvölker mit den Nephilim (4Mo 13,33).", "5Mo 3,11; Jes 14,9"),
        ("hermon", "ort", "Hermon und Basan", "Der Hermon (rund 2800 m) ist der höchste Berg der Region; nach 5Mo 3,9 hieß er auch Sirjon und Senir. Südlich liegt Basan, fruchtbares Land mit starken Stieren (Ps 22,13). Nach dem Henochbuch stiegen die Wächter auf den Hermon herab (1Hen 6,6). Am Fuß des Hermon lag später Cäsarea Philippi.", "5Mo 3,8–11; Mt 16,13"),
        ("asasel", "begriff", "Asasel", "Hebräisch Azazel, nur in 3Mo 16. Drei Deutungen: Name eines Wüstendämons (so das Henochbuch und viele heutige Ausleger, auch Heiser); „der Bock, der weggeht“ (daher Luthers „ledig“ und das Wort „Sündenbock“); oder, nach jüdischer Tradition, Name eines schroffen Felsens in der Wüste.", "3Mo 16,8–10.21–22"),
        ("maechte", "begriff", "Mächte und Gewalten", "Paulus nennt unsichtbare Mächte mit Wörtern der Herrschaft: Fürstentümer (archai), Gewalten (exousiai), Weltbeherrscher, Throne (Röm 8,38; Eph 1,21; 6,12; Kol 1,16; 2,15). Heiser liest sie als die geistlichen Herrscher über die Völker aus 5Mo 32. Andere verstehen allgemeiner böse Geister oder auch Mächte, die in irdischen Ordnungen wirken.", "Eph 6,12; Kol 2,15"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Gottes Rat ─────────────────────────
sec("rat", [R(PS, 82, 1, 8)], "Gott richtet inmitten der Götter",
    "Gott steht in seiner Versammlung und richtet die „Götter“: Sie richten ungerecht und lassen Arme und Waisen im Stich. Er hat sie Söhne des Höchsten genannt, doch sie werden sterben wie Menschen. Am Ende wird Gott gebeten, selbst die Erde zu richten.",
    focus="Achte darauf, was Gott den „Göttern“ vorwirft und was er ihnen ankündigt.",
    quiz=[
        choice("Was wirft Gott den „Göttern“ in V. 2–4 vor?", ["Dass sie ungerecht richten und die Schwachen nicht schützen", "Dass sie sich vor anderen Göttern beugen", "Dass sie keine Opfer bringen", "Dass sie Israel verlassen haben"], 2, "Lies Vers 2–4.",
               "V. 2–4: Sie richten ungerecht, ziehen die Gottlosen vor und retten den Geringen, die Waise und den Armen nicht."),
        tf("Nach V. 7 werden diese „Götter“ ewig leben.", False, 7, "Lies Vers 7.",
           "V. 7: Wie ein Mensch werden sie sterben und fallen wie einer der Fürsten."),
        choice("Worum wird Gott in V. 8 gebeten?", ["Die Erde zu richten, denn alle Nationen sind sein Erbteil", "Israel von den Völkern zu trennen", "Den Göttern zu vergeben", "Einen König einzusetzen"], 8, "Lies Vers 8.",
               "V. 8: Steh auf, Gott, richte die Erde – alle Nationen sollen dein Erbteil sein."),
    ],
    explain=[
        E("Was ist das für ein Leseplan?", "Er liest die Bibel bewusst mit dem Weltbild von Michael S. Heiser, einem Alttestamentler, der die Texte über Gottes „Rat“ ernst nimmt (Karte „Michael Heiser“). Seine Deutungen werden hier ausführlicher erklärt, als es sonst in Manna üblich ist. Wo Christen anders lesen, steht das dabei."),
        E("Wer sind die „Götter“?", "Heiser versteht sie als himmlische Wesen, denen Gott die Völker anvertraut hatte (5Mo 32,8, kommt später) und die ihr Amt missbraucht haben. So lasen schon viele jüdische Texte der Zeit Jesu. Andere Ausleger, etwa Calvin, sehen menschliche Richter, die Gottes Recht vertreten sollten; eine rabbinische Deutung denkt an Israel am Sinai."),
        E("Wie kann Gott „inmitten der Götter“ stehen?", "Für Heiser heißt elohim nicht „allmächtiger Gott“, sondern: ein Wesen aus der unsichtbaren Welt. Der Gott Israels ist unter ihnen einzigartig – der Einzige, der richtet, und der Einzige, der nicht stirbt."),
    ],
    cards=["heiser", "rat", "elohim"],
    fact="In V. 1 steht das hebräische Wort elohim zweimal: zuerst mit einem Verb in der Einzahl für den einen Gott, dann für die vielen, in deren Mitte er richtet.",
    prayer={"ref": R(PS, 82, 8), "source": "Psalm 82,8"},
    teaser="Ein Prophet erzählt einem König, was er im Thronsaal Gottes gesehen hat: eine Beratung, an deren Ende ein Geist sich freiwillig meldet.")

sec("rat", [R(KOEN1, 22, 13, 23)], "Ein Blick in den Thronsaal",
    "Vierhundert Propheten sagen König Ahab den Sieg voraus; Micha ben Jimla soll dasselbe sagen. Er erzählt eine Vision: Gott sitzt auf dem Thron, das ganze Heer des Himmels um ihn. Gott fragt, wer Ahab betören will, ein Geist meldet sich und wird zum Lügengeist im Mund der Propheten.",
    quiz=[
        choice("Was soll Micha nach dem Wunsch des Boten tun?", ["Dasselbe Gute sagen wie die anderen Propheten", "Den König verfluchen", "Schweigen", "Nach Ramot-Gilead mitziehen"], 13, "Lies Vers 13.",
               "V. 13: Die Propheten sagen einstimmig Gutes; Micha soll reden wie sie."),
        order("Bring die Vision in die Reihenfolge des Textes.", ["Gott sitzt auf dem Thron, das Heer des Himmels steht bei ihm", "Gott fragt, wer Ahab bereden will", "Einer sagt dies, ein anderer das", "Ein Geist tritt vor und bietet sich an"],
              "V. 19–21: Thron, Frage, Beratung, ein Geist meldet sich.", "Lies Vers 19–21."),
        who("Ich will ausgehen und will ein Lügengeist sein in dem Mund aller seiner Propheten.", R(KOEN1, 22, 22), ["Ein Geist vor dem Thron", "Micha ben Jimla", "Einer der 400 Propheten", "Der König Ahab"],
            "V. 21–22: Ein Geist tritt vor den HERRN und macht diesen Vorschlag."),
    ],
    explain=[
        E("Was sieht Micha hier?", "Nach Heiser eine Sitzung des himmlischen Rats: Gott entscheidet, aber er lässt die Seinen beraten und beteiligt sie an der Ausführung. Ähnliche Szenen stehen in Hiob 1 und Jes 6."),
        E("Schickt Gott hier Lügen?", "Der Text sagt, dass Gott es zulässt und Micha es dem König offen ankündigt (V. 23). Viele Ausleger lesen es als Gericht über Ahab, der Lügen hören wollte (vgl. V. 8; 2Thess 2,11). Manche verstehen die Vision als Gleichnis, in dem Micha erklärt, warum alle anderen Propheten sich irren."),
        E("Wer ist Micha ben Jimla?", "Ein Prophet im Nordreich zur Zeit Ahabs, im 9. Jahrhundert v. Chr. – nicht derselbe wie der spätere Prophet Micha aus Moreschet."),
    ],
    teaser="Unter den Söhnen Gottes, die sich vor Gott stellen, ist einer, dessen Name eigentlich eine Berufsbezeichnung ist.")

sec("rat", [R(HIOB, 1, 6, 12)], "Der Ankläger im Rat",
    "Die Söhne Gottes treten vor den HERRN, unter ihnen der Satan. Gott weist auf Hiob hin. Der Satan behauptet, Hiob fürchte Gott nur, weil es sich lohnt. Gott erlaubt ihm, Hiobs Besitz anzutasten, aber nicht ihn selbst.",
    quiz=[
        choice("Was behauptet der Satan über Hiob?", ["Hiob fürchte Gott nur, weil Gott ihn schützt und segnet", "Hiob sei heimlich ein Götzendiener", "Hiob sei nicht so reich, wie alle denken", "Hiob habe den Satan verflucht"], 9, "Lies Vers 9–11.",
               "V. 9–11: Ist es umsonst, dass Hiob Gott fürchtet? Nimm ihm alles, dann wird er sich lossagen."),
        tf("Gott erlaubt dem Satan in V. 12, auch Hiob selbst anzutasten.", False, 12, "Lies Vers 12.",
           "V. 12: Alles, was er hat, ist in deiner Hand – nur nach ihm selbst strecke die Hand nicht aus."),
    ],
    explain=[
        E("Ist „der Satan“ hier der Teufel?", "Im Hebräischen steht ha-satan, mit Artikel: „der Ankläger“. Heiser liest das als Rolle im Rat, wie ein Staatsanwalt; ob diese Gestalt schon der Teufel des Neuen Testaments ist, lässt er offen. Viele Christen und die meisten Kirchenväter lesen Hiob 1 dagegen von Anfang an als Auftritt des Teufels (vgl. Offb 12,10)."),
        E("Wer sind die „Söhne Gottes“?", "Himmlische Wesen, die zu Gottes Hof gehören. In Hiob 38,7 jubeln sie schon bei der Erschaffung der Erde. Die Septuaginta übersetzt hier „Engel Gottes“."),
        E("Wo kommt der Satan her?", "V. 7: vom Umherstreifen auf der Erde. In Sach 3,1–2 tritt der Satan ähnlich als Ankläger vor Gottes Engel auf."),
    ],
    cards=["satan"],
    fact="Nach Hiob 38,7 waren die Söhne Gottes schon dabei, als Gott die Erde gründete – sie jubelten, bevor es Menschen gab.",
    try_="Lies Sach 3,1–5. Was haben die Szene dort und Hiob 1,6–12 gemeinsam?",
    teaser="Ein Prophet sieht Wesen mit sechs Flügeln – und hört Gott eine Frage stellen, in der „uns“ vorkommt.")

sec("rat", [R(JES, 6, 1, 8)], "Wer wird für uns gehen?",
    "Jesaja sieht den Herrn auf einem hohen Thron, Seraphim mit sechs Flügeln rufen das Dreimal-Heilig. Er hält sich für verloren, doch ein Seraph berührt seine Lippen mit einer glühenden Kohle. Dann fragt Gott, wen er senden soll, und Jesaja meldet sich.",
    place="jerusalem",
    quiz=[
        estimate("Wie viele Flügel hat jeder Seraph?", 2, 12, 6, "Flügel",
                 "V. 2: sechs – zwei bedecken das Gesicht, zwei die Füße, mit zweien fliegt er.", 2, "Lies Vers 2."),
        choice("Womit berührt der Seraph Jesajas Mund?", ["Mit einer glühenden Kohle vom Altar", "Mit seinem Flügel", "Mit einer Schriftrolle", "Mit Öl"], 6, "Lies Vers 6–7.",
               "V. 6–7: eine glühende Kohle vom Altar; dadurch ist Jesajas Schuld gesühnt."),
        tf("In V. 8 fragt Gott, wer „für uns“ gehen wird.", True, 8, "Lies Vers 8.",
           "V. 8: Wen soll ich senden, und wer wird für uns gehen?"),
    ],
    explain=[
        E("Was sind Seraphim?", "Das Wort heißt „Brennende“. Dasselbe Wort steht für die feurigen Schlangen in 4Mo 21,6 und für eine fliegende Schlange in Jes 30,6. Heiser schließt daraus, dass Wesen aus dem Rat schlangenartig beschrieben werden konnten – wichtig für 1Mo 3."),
        E("Warum „für uns“?", "Gott spricht in der Mehrzahl, wie in 1Mo 1,26 und 11,7. Kirchenväter sahen darin einen Hinweis auf die Dreieinigkeit; andere denken an eine Mehrzahl der Majestät. Heiser – und schon der jüdische Ausleger Raschi zu 1Mo 1,26 – sehen Gott im Gespräch mit seinem himmlischen Hof."),
        E("Warum hält Jesaja sich für verloren?", "Wer Gott sieht, muss nach alter Überzeugung sterben (2Mo 33,20). Jesaja nennt dazu seine unreinen Lippen, gerade vor Wesen, die Gott ununterbrochen loben."),
    ],
    try_="Lies 1Mo 1,26–27. Wo spricht Gott in der Mehrzahl, wo wird in der Einzahl erzählt, was er tut?",
    teaser="Die erste Gestalt aus der unsichtbaren Welt, die in der Bibel spricht, stellt eine Frage – und verdreht dabei, was Gott gesagt hat.")

# ───────────────────────── 2 · Drei Aufstände ─────────────────────────
sec("aufstand", [R(GEN, 3, 1, 15)], "Die Schlange im Garten Gottes",
    "Die Schlange fragt die Frau, ob Gott wirklich alle Bäume verboten habe, und verspricht: Ihr werdet nicht sterben, sondern sein wie Gott. Die Menschen essen und verstecken sich. Gott verflucht die Schlange und kündigt Feindschaft zwischen ihren Nachkommen und denen der Frau an.",
    focus="Achte darauf, was die Schlange über Gott behauptet.",
    quiz=[
        choice("Was verspricht die Schlange in V. 5?", ["Dass sie sein werden wie Gott und Gut und Böse erkennen", "Dass sie ewig im Garten bleiben dürfen", "Dass sie über die Tiere herrschen werden", "Dass Gott ihnen vergeben wird"], 5, "Lies Vers 5.",
               "V. 5: Eure Augen werden aufgetan, und ihr werdet sein wie Gott, erkennend Gutes und Böses."),
        order("Wer schiebt die Schuld wem zu? Bring die Antworten in die Reihenfolge des Textes.", ["Der Mann nennt die Frau", "Die Frau nennt die Schlange", "Gott spricht zur Schlange"],
              "V. 12–14: Der Mann verweist auf die Frau, die Frau auf die Schlange – und Gott wendet sich zuerst der Schlange zu.", "Lies Vers 12–14."),
        tf("Nach V. 15 wird die Feindschaft auch die Nachkommen betreffen.", True, 15, "Lies Vers 15.",
           "V. 15: Feindschaft zwischen dir und der Frau, zwischen deinen Nachkommen und ihren Nachkommen."),
    ],
    explain=[
        E("Wer ist die Schlange?", "Der Text nennt nur „die Schlange“, klüger als alle Tiere. Heiser liest sie als strahlendes Wesen aus Gottes Rat, das Gottes Plan mit den Menschen ablehnte; Eden ist für ihn Gottes Wohnort und Ratsberg (vgl. Hes 28,13–14). Jüdische Ausleger sahen oft ein Tier oder einen Engel in Schlangengestalt; das Neue Testament nennt sie den Teufel (Offb 12,9)."),
        E("Was bedeutet V. 15?", "Seit Irenäus im 2. Jahrhundert lesen viele Christen den Vers als erste Ankündigung des Erlösers, der der Schlange den Kopf zertritt (vgl. Röm 16,20); die katholische Tradition spricht vom Protoevangelium. Andere lesen ihn als Beschreibung des dauernden Kampfes zwischen Menschen und dem Bösen."),
        E("Warum heißt es „wie Gott“?", "Hebräisch kann elohim hier „wie Gott“ oder „wie Götter“ heißen. Nach Heiser lockt die Schlange die Menschen, die als Gottes Bild schon zu seiner Familie gehören sollten, zu einer eigenmächtigen Gottgleichheit."),
    ],
    cards=["nachasch"],
    teaser="Ein Klagelied über einen König, der in Eden gewesen sein soll – auf einem heiligen Berg, zwischen feurigen Steinen.")

sec("aufstand", [R(HES, 28, 11, 19)], "Der Cherub in Eden",
    "Hesekiel soll ein Klagelied über den König von Tyrus anstimmen: Er war vollkommen, voll Weisheit, in Eden, ein gesalbter Cherub auf Gottes heiligem Berg. Durch seinen Handel kam Gewalt in ihn, sein Herz wurde hochmütig. Gott stieß ihn vom Berg und machte ihn zu Asche.",
    place="tyrus",
    quiz=[
        choice("Wo war der Angesprochene nach V. 13–14?", ["In Eden, auf Gottes heiligem Berg", "Im Tempel in Jerusalem", "Am Hof in Babel", "Auf dem Meer vor Tyrus"], 13, "Lies Vers 13–14.",
               "V. 13–14: Du warst in Eden, dem Garten Gottes … du warst auf Gottes heiligem Berg."),
        error("Dein Herz hat sich erhoben wegen deiner [Stärke].", "Schönheit", 17,
              "V. 17: Dein Herz hat sich erhoben wegen deiner Schönheit; deine Weisheit hast du wegen deines Glanzes zunichte gemacht."),
        tf("Nach V. 16 kam Gewalttat durch den großen Handel in ihn.", True, 16, "Lies Vers 16.",
           "V. 16: Durch die Größe deines Handels wurde dein Inneres mit Gewalttat erfüllt."),
    ],
    explain=[
        E("Ist das der König oder ein Engel?", "Drei Lesarten: Viele Kirchenväter wie Tertullian und Origenes sahen hier den Fall Satans. Andere lesen ein Bild, mit dem Hesekiel den stolzen König von Tyrus beschreibt; Tyrus war tatsächlich eine reiche Handelsstadt (V. 16). Heiser meint: Hesekiel benutzt eine bekannte Geschichte von einem gefallenen Wesen aus Eden, um den König daran zu messen."),
        E("Was ist ein Cherub?", "Ein Wesen, das Gottes Gegenwart bewacht: vor dem Garten Eden (1Mo 3,24), auf der Bundeslade (2Mo 25,18–22). Nicht das pausbäckige Engelchen der Barockmalerei."),
        E("Was ist mit Jes 14 gemeint?", "Jes 14,12–15 spricht vom König von Babel als „Glanzstern, Sohn der Morgenröte“, der auf den Versammlungsberg will und in die Grube stürzt. Die lateinische Bibel übersetzt Glanzstern mit Lucifer – daher wurde das ein Name für den Teufel."),
    ],
    fact="Die Edelsteine in V. 13 entsprechen zu einem großen Teil den Steinen auf der Brusttasche des Hohenpriesters (2Mo 28,17–20), besonders in der griechischen Übersetzung, wo es genau die zwölf sind.",
    try_="Lies Jes 14,12–15. Welche Bilder ähneln Hes 28, welche sind anders?",
    teaser="Ein kurzer, rätselhafter Text: Söhne Gottes, Menschentöchter und Kinder, die man nie vergaß.")

sec("aufstand", [R(GEN, 6, 1, 8)], "Söhne Gottes und Töchter der Menschen",
    "Die Söhne Gottes sehen, dass die Menschentöchter schön sind, und nehmen sich Frauen. Gott begrenzt die Lebenszeit des Menschen. Aus diesen Verbindungen kommen die Nephilim, die berühmten Helden der Vorzeit. Gott sieht die Bosheit der Menschen und beschließt, sie zu vertilgen – nur Noah findet Gnade.",
    focus="Achte darauf, wer in V. 2 handelt und wer in V. 5 das Problem ist.",
    quiz=[
        choice("Was sehen die Söhne Gottes nach V. 2?", ["Dass die Töchter der Menschen schön waren", "Dass die Menschen Gott vergaßen", "Dass die Erde voller Gewalt war", "Dass Noah gerecht war"], 2, "Lies Vers 2.",
               "V. 2: Sie sahen, dass die Töchter der Menschen schön waren, und nahmen sich Frauen."),
        estimate("Auf wie viele Jahre begrenzt Gott die Tage des Menschen?", 40, 200, 120, "Jahre",
                 "V. 3: Seine Tage seien 120 Jahre – manche lesen das als Lebensdauer, andere als Frist bis zur Flut.", 3, "Lies Vers 3."),
        tf("Nach V. 8 fand Noah Gnade in den Augen des HERRN.", True, 8, "Lies Vers 8.",
           "V. 8: Noah aber fand Gnade in den Augen des HERRN."),
    ],
    explain=[
        E("Wer sind die „Söhne Gottes“?", "Drei Deutungen: (1) Himmlische Wesen – so die ältesten jüdischen Ausleger (Henochbuch, Josephus) und die meisten frühen Kirchenväter wie Justin und Irenäus; diese Sicht vertritt Heiser. (2) Nachkommen des frommen Seth, die sich mit Kains Linie mischen – so Augustinus, Calvin und viele Evangelikale. (3) Könige und Mächtige – so die Targume und viele Rabbinen."),
        E("Was meint Heiser mit „drei Aufständen“?", "Er sieht in 1Mo 3, 1Mo 6 und 1Mo 11 drei Auflehnungen gegen Gottes Plan: die Schlange in Eden, die Söhne Gottes, die Grenzen überschreiten, und Babel. Jedes Mal antwortet Gott mit Gericht und einem neuen Anfang."),
        E("Warum steht hier „Riesen“?", "Die Elberfelder übersetzt das hebräische nephilim mit „Riesen“, wie die griechische Übersetzung (gigantes). Die Wortbedeutung ist umstritten.", "elbbk"),
    ],
    cards=["nephilim", "henoch"],
    teaser="Was geschah mit den Söhnen Gottes? Zwei Briefe im Neuen Testament wissen es – und benutzen dafür ein Wort aus der griechischen Sagenwelt.")

sec("aufstand", [R(PETR2, 2, 4, 9), R(JUD, 1, 6, 7)], "Im Tartaros",
    "Petrus nennt drei Beispiele für Gottes Gericht: Engel, die gesündigt haben und gefesselt in der Finsternis auf das Gericht warten; die Welt zur Zeit Noahs; Sodom und Gomorra. Gerettet werden Noah und Lot. Judas schreibt von Engeln, die ihre eigene Wohnung verlassen haben und in ewigen Ketten verwahrt sind.",
    quiz=[
        order("Welche Beispiele nennt Petrus? Bring sie in seine Reihenfolge.", ["Engel, die gesündigt hatten", "Die alte Welt zur Zeit Noahs", "Sodom und Gomorra"],
              "2Petr 2,4–6: zuerst die Engel, dann die Flut, dann Sodom und Gomorra – dieselbe Reihenfolge wie in 1. Mose.", "Lies 2Petr 2,4–6."),
        choice("Was ist nach 2Petr 2,4 mit den Engeln geschehen?", ["Sie wurden Ketten der Finsternis übergeben und für das Gericht aufbewahrt", "Sie wurden sofort vernichtet", "Sie wurden zu Menschen", "Sie dürfen frei auf der Erde umherziehen"], 4, "Lies 2Petr 2,4.",
               "2Petr 2,4: Gott stürzte sie in den tiefsten Abgrund und übergab sie Ketten der Finsternis, aufbewahrt für das Gericht."),
        tf("Nach Judas 6 haben diese Engel ihre eigene Behausung verlassen.", True, None, "Lies Judas 6.",
           "Jud 6: Sie haben ihren ersten Zustand nicht bewahrt und ihre eigene Wohnung verlassen."),
    ],
    explain=[
        E("Welche Engel sind gemeint?", "Heiser und viele Ausleger sehen die Söhne Gottes aus 1Mo 6: Die Reihenfolge Engel – Flut – Sodom folgt 1. Mose, und Jud 7 sagt, Sodom sei „ebenso wie jene“ fremdem Fleisch nachgegangen. Das Henochbuch erzählt dieselbe Geschichte. Wer 1Mo 6 anders liest, denkt hier an einen Fall von Engeln vor der Schöpfung des Menschen."),
        E("Was heißt „tiefster Abgrund“?", "Im Griechischen steht ein Verb, das wörtlich „in den Tartaros werfen“ bedeutet – der Kerker unter der Unterwelt aus der griechischen Sage (siehe Karte).", "elbbk"),
        E("Und die „Geister im Gefängnis“?", "1Petr 3,19–20 sagt, Christus habe Geistern im Gefängnis gepredigt, die zur Zeit Noahs ungehorsam waren. Heiser liest: Christus verkündete den gefangenen Wächtern seinen Sieg (vgl. 1Petr 3,22). Augustinus las: Christus sprach durch Noah zu dessen Zeitgenossen. Katholische und orthodoxe Tradition verbinden die Stelle mit Christi Abstieg ins Reich des Todes."),
    ],
    cards=["tartaros"],
    fact="Der Judasbrief zitiert ein paar Verse später das Henochbuch fast wörtlich (Jud 14–15 = 1Hen 1,9).",
    try_="Lies 1Petr 3,18–22. Wer ist dort am Ende wem unterworfen?",
    teaser="Nach der Flut bauen Menschen eine Stadt mit einem Turm – und Gott sagt wieder „uns“.")

sec("aufstand", [R(GEN, 11, 1, 9)], "Babel",
    "Alle Menschen haben eine Sprache. In der Ebene Sinear bauen sie eine Stadt und einen Turm bis an den Himmel, um sich einen Namen zu machen und nicht zerstreut zu werden. Gott fährt herab, verwirrt ihre Sprache und zerstreut sie über die Erde.",
    place="babylon",
    quiz=[
        choice("Warum wollen die Menschen nach V. 4 bauen?", ["Um sich einen Namen zu machen und nicht zerstreut zu werden", "Um Gott ein Opfer zu bringen", "Um sich vor einer Flut zu schützen", "Um einen König zu krönen"], 4, "Lies Vers 4.",
               "V. 4: Wir wollen uns einen Namen machen, damit wir nicht über die ganze Erde zerstreut werden."),
        error("Der HERR sprach: Lasst uns herabfahren und ihre [Stadt] dort verwirren.", "Sprache", 7,
              "V. 7: Gott will ihre Sprache verwirren, sodass einer den anderen nicht versteht."),
    ],
    explain=[
        E("Was war der Turm?", "Wohl ein Stufentempel (Zikkurat), wie sie in Mesopotamien gebaut wurden: ein künstlicher Berg, auf dem man den Göttern begegnen wollte. Gebaut wurde mit gebrannten Ziegeln und Asphalt (V. 3), wie es dort üblich war."),
        E("Warum ist Babel so wichtig?", "Nach Heiser ist es der dritte Aufstand. 5Mo 32,8 (übernächster Abschnitt) erzählt, wie Gott danach die Völker verteilt. Die Völkertafel in 1Mo 10 zählt in der hebräischen Bibel 70 Völker."),
        E("Was bedeutet „Babel“?", "Im Babylonischen etwa „Tor der Götter“. Der Text spielt mit dem hebräischen Wort balal, „verwirren“ (V. 9)."),
    ],
    teaser="Gott verteilt die Völker. Bei einem Satzteil sind sich die alten Handschriften nicht einig – und das ändert viel.")

sec("aufstand", [R(DTN, 32, 7, 17)], "Die Verteilung der Völker",
    "Mose erinnert: Als der Höchste den Völkern ihr Erbe zuteilte, legte er ihre Grenzen fest. Israel aber ist Gottes eigener Anteil; er fand es in der Wüste und trug es wie ein Adler. Doch Israel wurde satt, verließ Gott und opferte fremden Göttern und Dämonen.",
    focus="Achte auf V. 8–9: Wer bekommt die Völker, wer bekommt Israel?",
    quiz=[
        choice("Was ist nach V. 9 der Anteil des HERRN?", ["Sein Volk Jakob", "Die ganze Erde", "Der Berg Zion", "Die Völker ringsum"], 9, "Lies Vers 9.",
               "V. 9: Des HERRN Teil ist sein Volk, Jakob sein zugemessenes Erbteil."),
        tf("Nach V. 12 war ein fremder Gott mit Israel in der Wüste.", False, 12, "Lies Vers 12.",
           "V. 12: Der HERR allein leitete ihn, kein fremder Gott war mit ihm."),
        choice("Wem opferten sie nach V. 17?", ["Dämonen und neuen Göttern", "Dem HERRN auf den Höhen", "Ihren Vorfahren", "Den Königen von Moab"], 17, "Lies Vers 17.",
               "V. 17: Sie opferten Dämonen, die nicht Gott sind, Göttern, die sie nicht kannten."),
    ],
    explain=[
        E("„Kinder Israel“ oder „Söhne Gottes“?", "Hier unterscheiden sich die Handschriften. Der hebräische Standardtext (Masoretischer Text, danach die Elberfelder) zählt in V. 8 nach den „Kindern Israel“. Eine Handschrift aus Qumran (4QDtn j) liest „Söhne Gottes“, die Septuaginta „Engel Gottes“. Heiser hält sie für die ursprüngliche; manche neuere Übersetzungen folgen ihr, etwa die englische ESV."),
        E("Was folgt daraus für Heiser?", "Gott hat nach Babel die Völker den Söhnen Gottes zugeteilt und Israel für sich behalten. Dasselbe sagt 5Mo 4,19–20 über das Heer des Himmels, das Gott den Völkern zugeteilt hat. Die Götter der Völker sind darum für ihn keine bloßen Holzfiguren, sondern abgefallene Wesen (Ps 82)."),
        E("Was sind die „Dämonen“?", "Hebräisch schedim, ein seltenes Wort (nur hier und Ps 106,37), verwandt mit einem babylonischen Wort für Schutzgeister. Die Elberfelder hält fest: Sie sind „Nicht-Gott“."),
    ],
    cards=["dtn32"],
    fact="Paulus greift V. 17 auf, als er den Korinthern erklärt, was hinter Götzenopfern steht (1Kor 10,20).",
    teaser="Ein Mann ringt eine ganze Nacht mit einem Unbekannten. Am Morgen sagt er, er habe Gott gesehen.")

# ───────────────────────── 3 · Der Gott, den man sehen kann ─────────────────────────
sec("sichtbar", [R(GEN, 32, 23, 33)], "Jakob ringt mit Gott",
    "Jakob bleibt allein am Jabbok zurück, ein Mann ringt mit ihm bis zum Morgen. Der Mann verrenkt ihm die Hüfte; Jakob lässt ihn nicht los, ohne gesegnet zu sein. Er bekommt den Namen Israel. Den Ort nennt er Pniel, denn er hat Gott von Angesicht gesehen.",
    place="pniel",
    focus="Achte darauf, wie der Text den Gegner nennt und wie Jakob ihn am Ende nennt.",
    quiz=[
        choice("Was verlangt Jakob, bevor er den Mann loslässt?", ["Dass er ihn segnet", "Dass er ihm seinen Namen sagt", "Dass er Esau besiegt", "Dass er ihn heilt"], 27, "Lies Vers 27.",
               "V. 27: Ich lasse dich nicht los, du habest mich denn gesegnet."),
        error("Jakob nannte den Ort Pniel, denn er hatte einen [Engel] von Angesicht zu Angesicht gesehen.", "Gott", 31,
              "V. 31: Ich habe Gott von Angesicht zu Angesicht gesehen."),
        tf("Der Mann sagt Jakob in V. 30 seinen Namen.", False, 30, "Lies Vers 30.",
           "V. 30: Er fragt zurück, warum Jakob nach seinem Namen fragt – und segnet ihn."),
    ],
    explain=[
        E("Wer ist der Mann?", "Der Text sagt „ein Mann“, Jakob sagt „Gott“, Hos 12,4–5 sagt „Gott“ und „Engel“. Heiser sieht hier Gott selbst in Menschengestalt – den sichtbaren Gott, der auch als Engel des HERRN auftritt. Kirchenväter sahen den Sohn vor seiner Menschwerdung; jüdische Tradition oft einen Engel, etwa Esaus Schutzengel."),
        E("Was bedeuten Israel und Pniel?", "Israel wird im Text erklärt als „mit Gott gerungen“ (V. 29). Pniel (auch Penuel) heißt „Angesicht Gottes“."),
    ],
    cards=["engel-des-herrn"],
    fact="Bis heute essen viele Juden die Spannader am Hüftgelenk nicht – zur Erinnerung an diese Nacht (V. 33).",
    try_="Lies Hos 12,4–6. Wie nennt Hosea den, mit dem Jakob gerungen hat?",
    teaser="Ein Engel erscheint im Feuer – aber wer spricht dann aus dem Dornbusch?")

sec("sichtbar", [R(EX, 3, 1, 10)], "Der Engel im Dornbusch",
    "Mose hütet Schafe am Horeb. Der Engel des HERRN erscheint ihm in einer Flamme aus einem Dornbusch, der nicht verbrennt. Gott ruft ihn aus dem Busch, stellt sich als Gott Abrahams, Isaaks und Jakobs vor und sendet ihn zum Pharao.",
    place="horeb",
    quiz=[
        tf("Nach V. 2 erscheint Mose zuerst der Engel des HERRN.", True, 2, "Lies Vers 2.",
           "V. 2: Der Engel des HERRN erschien ihm in einer Feuerflamme mitten aus dem Dornbusch."),
        choice("Wer ruft nach V. 4 aus dem Dornbusch?", ["Gott", "Ein Seraph", "Aaron", "Eine Stimme vom Berg"], 4, "Lies Vers 4.",
               "V. 4: Gott rief ihm mitten aus dem Dornbusch zu: Mose! Mose!"),
        choice("Warum verbirgt Mose sein Gesicht?", ["Er fürchtet sich, Gott anzuschauen", "Das Feuer blendet ihn", "Er schämt sich wegen Ägypten", "Er will nicht erkannt werden"], 6, "Lies Vers 6.",
               "V. 6: Mose fürchtete sich, Gott anzuschauen."),
    ],
    explain=[
        E("Engel oder Gott?", "V. 2 nennt den Engel des HERRN, V. 4 sagt, Gott ruft, V. 6 sagt „Ich bin der Gott Abrahams“. Für Heiser ist das gewollt: Der Engel des HERRN ist Gott in sichtbarer Gestalt, von Gott unterschieden und doch Gott. Jüdische Ausleger lesen meist: Gott spricht durch seinen Boten."),
        E("Was heißt „mein Name ist in ihm“?", "In 2Mo 23,20–23 sendet Gott einen Engel vor Israel her; man soll auf ihn hören, denn Gottes Name ist in ihm. „Name“ steht in der Bibel oft für Gottes Gegenwart selbst (5Mo 12,5). Heiser sieht hier dieselbe Gestalt wie im Dornbusch."),
        E("Warum die Schuhe ausziehen?", "Der Ort ist heilig, weil Gott dort gegenwärtig ist. Auch Priester taten ihren Dienst wohl barfuß; Josua erlebt dasselbe vor Jericho (Jos 5,15)."),
    ],
    try_="Lies 2Mo 23,20–23. Was sagt Gott über den Engel, den er vor Israel hersendet?",
    teaser="Throne werden aufgestellt, nicht nur einer – und jemand kommt auf den Wolken.")

sec("sichtbar", [R(DAN, 7, 9, 14)], "Der Alte an Tagen und der Menschensohn",
    "Daniel sieht, wie Throne aufgestellt werden und ein Alter an Tagen sich setzt; Tausende dienen ihm, das Gericht beginnt. Das Tier wird getötet. Dann kommt einer wie ein Menschensohn mit den Wolken des Himmels und bekommt ewige Herrschaft über alle Völker.",
    quiz=[
        choice("Was ist nach V. 9 das Erste, was Daniel sieht?", ["Throne werden aufgestellt", "Ein Tier steigt aus dem Meer", "Ein Engel bläst die Posaune", "Ein Tempel wird gebaut"], 9, "Lies Vers 9.",
               "V. 9: Throne wurden aufgestellt, und ein Alter an Tagen setzte sich."),
        tf("Der Menschensohn kommt nach V. 13 mit den Wolken des Himmels.", True, 13, "Lies Vers 13.",
           "V. 13: Mit den Wolken des Himmels kam einer wie eines Menschen Sohn."),
        choice("Was bekommt der Menschensohn nach V. 14?", ["Herrschaft, Herrlichkeit und ein Königtum, das nie zerstört wird", "Ein Schwert, um das Tier zu töten", "Ein Buch mit sieben Siegeln", "Einen Platz unter den Engeln"], 14, "Lies Vers 14.",
               "V. 14: Ihm wurden Herrschaft, Herrlichkeit und Königtum gegeben, und alle Völker dienten ihm."),
    ],
    explain=[
        E("Warum „Throne“ in der Mehrzahl?", "Der Text sagt nicht, wer auf den anderen Thronen sitzt. Heiser sieht den himmlischen Rat beim Gericht (V. 10: das Gericht setzte sich); vgl. Offb 4,4 mit 24 Thronen."),
        E("Wer ist der Menschensohn?", "Auf Wolken reitet in der hebräischen Bibel sonst nur Gott (5Mo 33,26; Ps 104,3). Heiser sieht darum eine zweite göttliche Gestalt neben dem Alten an Tagen, wie in anderen Texten den Engel des HERRN. Jesus bezieht die Stelle auf sich (Mk 14,62). Einige Ausleger lesen den Menschensohn zuerst als Bild für das Volk der Heiligen (Dan 7,18.27)."),
        E("Wussten das schon jüdische Ausleger?", "Rabbiner späterer Jahrhunderte stritten über die Lehre von „zwei Mächten im Himmel“, die sie ablehnten; einige gingen dabei auf Dan 7 ein. Heiser sieht darin ein Echo einer älteren jüdischen Lesart dieser Texte."),
    ],
    cards=["menschensohn"],
    try_="Lies Mk 14,61–64. Warum zerreißt der Hohepriester sein Gewand?",
    teaser="Kundschafter kommen mit einer Riesentraube zurück – und mit einer Nachricht, die ein ganzes Volk lähmt.")

# ───────────────────────── 4 · Riesen, Fürsten, fremde Götter ─────────────────────────
sec("maechte", [R(NUM, 13, 25, 33)], "Riesen im Land",
    "Die Kundschafter kehren nach 40 Tagen zurück: Das Land fließt von Milch und Honig, aber die Städte sind befestigt und die Kinder Enaks wohnen dort. Kaleb will hinaufziehen. Die anderen verbreiten ein böses Gerücht: Sie hätten Riesen gesehen und sich wie Heuschrecken gefühlt.",
    place="paran",
    quiz=[
        estimate("Wie viele Tage waren die Kundschafter unterwegs?", 7, 100, 40, "Tage",
                 "V. 25: nach 40 Tagen kehrten sie zurück.", 25, "Lies Vers 25."),
        choice("Was sagt Kaleb in V. 30?", ["Lasst uns hinaufziehen, wir werden das Land überwältigen", "Lasst uns nach Ägypten zurückkehren", "Lasst uns um ein Zeichen bitten", "Lasst uns mit den Riesen verhandeln"], 30, "Lies Vers 30.",
               "V. 30: Lasst uns hinaufziehen und es in Besitz nehmen, wir werden es gewiss überwältigen."),
        tf("Die Kundschafter sagen, sie seien sich wie Heuschrecken vorgekommen.", True, 33, "Lies Vers 33.",
           "V. 33: Wir waren in unseren Augen wie Heuschrecken, und so waren wir auch in ihren Augen."),
    ],
    explain=[
        E("Wer sind die Kinder Enaks?", "Die Anakiter, ein Volk großer Menschen bei Hebron (Jos 15,13–14). V. 33 verbindet sie mit den Nephilim aus 1Mo 6. Goliat aus Gat stammte nach Jos 11,22 wohl aus ihren Resten."),
        E("Wie liest Heiser die Landnahme?", "Für ihn ist die Eroberung Kanaans auch ein Kampf gegen Sippen, die mit den Nephilim verbunden waren; daher die besondere Härte gegen bestimmte Völker. Andere Ausleger betonen, dass V. 32 den Bericht selbst ein „böses Gerücht“ nennt – die Kundschafter könnten übertrieben haben."),
        E("Wie können Nephilim nach der Flut leben?", "1Mo 6,4 sagt, es gab sie „auch nachher“. Ob das heißt, dass sich so etwas wiederholte, oder ob die Kundschafter einen alten Schreckensnamen benutzen, wird verschieden gesehen."),
    ],
    teaser="Ein König, dessen eisernes Bett man noch Generationen später besichtigen konnte.")

sec("maechte", [R(DTN, 3, 1, 11)], "Og von Basan",
    "Israel zieht nach Basan; König Og stellt sich bei Edrei zum Kampf. Gott gibt ihn in Israels Hand, 60 befestigte Städte werden eingenommen, das Land bis zum Hermon. Og war der letzte der Rephaiter; sein eisernes Bett, neun Ellen lang, steht in Rabba.",
    quiz=[
        estimate("Wie lang war Ogs Bett?", 3, 20, 9, "Ellen",
                 "V. 11: neun Ellen lang und vier breit, nach gewöhnlichem Ellenmaß – etwa vier Meter.", 11, "Lies Vers 11."),
        tf("Nach V. 11 war Og der letzte Übriggebliebene der Riesen (Rephaiter).", True, 11, "Lies Vers 11.",
           "V. 11: Nur Og war vom Überrest der Rephaiter übrig geblieben."),
        choice("Wie viele Städte nahm Israel nach V. 4 ein?", ["60", "12", "7", "100"], 4, "Lies Vers 4.",
               "V. 4: 60 Städte, die ganze Gegend Argob."),
    ],
    explain=[
        E("Warum ist Basan besonders?", "Basan, das Land um den Hermon, galt als fruchtbar und gefährlich; die Stiere Basans stehen in Ps 22,13 für bedrohliche Feinde. In Texten aus Ugarit werden Aschtarot und Edrei – Ogs Städte (5Mo 1,4) – als Wohnsitz eines Gottes der Toten genannt. Heiser sieht Basan deshalb als Gegend, die mit der Unterwelt verbunden war."),
        E("Was sind Rephaiter?", "Ein Riesenvolk im Ostjordanland (5Mo 2,11.20). Dasselbe Wort bezeichnet anderswo die Schatten der Toten (Jes 14,9). Siehe Karte."),
        E("Was heißt „verbannen“?", "Hebräisch cherem: etwas ganz Gott übergeben, bei Städten ihre völlige Vernichtung. Die Texte gehören zu den schwersten der Bibel; der Plan „Texte, die man lieber überspringt“ geht auf solche Fragen ein. Heiser sieht in der Verbindung mit den Riesenvölkern einen Grund dafür.", "elbbk"),
    ],
    cards=["rephaiter", "hermon"],
    teaser="Zwei Ziegenböcke, zwei Lose: eins für den HERRN, eins für jemanden namens Asasel.")

sec("maechte", [R(LEV, 16, 7, 10), R(LEV, 16, 20, 22)], "Ein Bock für Asasel",
    "Am Versöhnungstag nimmt Aaron zwei Böcke und wirft Lose: einer für den HERRN, einer für Asasel. Der erste wird als Sündopfer geschlachtet. Auf den zweiten legt Aaron beide Hände und bekennt alle Schuld Israels; dann wird der Bock lebendig in die Wüste geschickt.",
    quiz=[
        choice("Wofür werden nach V. 8 die Lose geworfen?", ["Ein Los für den HERRN, eins für Asasel", "Eins für Aaron, eins für das Volk", "Eins für das Heiligtum, eins für den Altar", "Eins für Israel, eins für die Fremden"], 8, "Lies Vers 8.",
               "V. 8: ein Los für den HERRN und ein Los für Asasel."),
        tf("Der Bock für Asasel wird geschlachtet und auf dem Altar verbrannt.", False, 10, "Lies Vers 10 und 21–22.",
           "V. 10 und 21–22: Er wird lebendig vor den HERRN gestellt und dann in die Wüste geschickt."),
        choice("Was tut Aaron nach V. 21 mit dem lebendigen Bock?", ["Er legt die Hände auf seinen Kopf und bekennt die Schuld Israels", "Er sprengt sein Blut an den Altar", "Er schenkt ihn den Priestern", "Er lässt ihn im Heiligtum frei"], 21, "Lies Vers 21.",
               "V. 21: Er legt beide Hände auf den Kopf des Bockes und bekennt auf ihn alle Ungerechtigkeiten Israels."),
    ],
    explain=[
        E("Wer oder was ist Asasel?", "Das Los „für den HERRN“ steht parallel zum Los „für Asasel“ – das spricht nach Heiser für einen Namen, wohl den eines Wüstendämons. Das Henochbuch nennt einen der Wächter Asael und lässt ihn in der Wüste gefesselt werden (1Hen 10,4–5). Luther übersetzte „ledigen Bock“, daher kommt unser Wort „Sündenbock“; Raschi dachte an einen schroffen Felsen."),
        E("Wird hier einem Dämon geopfert?", "Nein, betont auch Heiser: Geopfert wird nur dem HERRN (V. 9), und 3Mo 17,7 verbietet Opfer an Bocksdämonen. Der Bock wird nicht geschlachtet, sondern trägt die Schuld fort – nach Heiser zurück in das Gebiet, das für das Böse steht, die Wüste."),
        E("Wie lesen Christen diesen Tag?", "Der Hebräerbrief deutet den Versöhnungstag auf Jesus, der mit seinem eigenen Blut ins Heiligtum ging (Hebr 9,11–12) und außerhalb des Lagers litt (Hebr 13,11–12). Viele sehen im fortgeschickten Bock ein Bild für Jes 53,6: Gott warf unsere Schuld auf ihn."),
    ],
    cards=["asasel"],
    fact="Nach der Mischna (Traktat Joma 6) wurde der Bock in späterer Zeit zu einer Felsklippe in der Wüste geführt; Boten meldeten von Station zu Station nach Jerusalem, dass er die Wüste erreicht hatte.",
    teaser="Ein Engel kommt drei Wochen zu spät, weil ihn jemand aufgehalten hat: der Fürst eines Weltreichs.")

sec("maechte", [R(DAN, 10, 10, 21)], "Der Fürst von Persien",
    "Ein himmlischer Bote richtet den zitternden Daniel auf: Seine Gebete wurden vom ersten Tag an erhört. Doch der Fürst des Königreichs Persien stand dem Boten 21 Tage entgegen, bis Michael, einer der ersten Fürsten, half. Danach wird er wieder gegen Persien kämpfen, und der Fürst von Griechenland wird kommen.",
    place="babylon",
    focus="Achte darauf, wer hier alles „Fürst“ genannt wird.",
    quiz=[
        estimate("Wie viele Tage stand der Fürst von Persien dem Boten entgegen?", 3, 70, 21, "Tage",
                 "V. 13: 21 Tage – so lange hatte Daniel auch getrauert und gefastet (V. 2–3).", 13, "Lies Vers 13."),
        choice("Wer kam dem Boten nach V. 13 zu Hilfe?", ["Michael, einer der ersten Fürsten", "Gabriel", "Der Fürst von Griechenland", "Daniel durch sein Gebet"], 13, "Lies Vers 13.",
               "V. 13: Michael, einer der ersten Fürsten, kam mir zu helfen."),
        tf("Nach V. 21 ist Michael „euer Fürst“, also der Fürst Israels.", True, 21, "Lies Vers 21.",
           "V. 21: niemand steht mir bei außer Michael, eurem Fürsten."),
    ],
    explain=[
        E("Wer ist der „Fürst von Persien“?", "Kein menschlicher König – ein Mensch hätte keinen Engel drei Wochen aufhalten können. Heiser sieht hier die Söhne Gottes aus 5Mo 32,8, die über Völker gesetzt sind: Persien und Griechenland haben ihre unsichtbaren Herrscher, Israel hat Michael (vgl. Dan 12,1). Viele Ausleger sprechen von Engeln über den Völkern; schon die Septuaginta liest 5Mo 32,8 so."),
        E("Wer ist Michael?", "Sein Name heißt „Wer ist wie Gott?“. In Daniel ist er der Fürst, der für Israel eintritt (10,21; 12,1); im Neuen Testament heißt er Erzengel (Jud 9) und kämpft gegen den Drachen (Offb 12,7)."),
        E("Wer spricht mit Daniel?", "Der Text sagt es nicht genau. Viele denken an Gabriel (vgl. Dan 9,21), manche an den Mann in Leinen aus V. 5–6, der an Hes 1 und Offb 1,13–15 erinnert."),
    ],
    prayer={"text": "Ich bitte dich, du wollest mich diese Nacht behüten vor allem Schaden und Gefahr … Denn ich befehle mich, meinen Leib und Seele und alles in deine Hände. Dein heiliger Engel sei mit mir, dass der böse Feind keine Macht an mir finde.", "source": "Martin Luther, Abendsegen (Kleiner Katechismus, 1529)"},
    teaser="Jesus führt seine Jünger an einen Ort am Fuß eines Berges, den das Henochbuch schon kennt – und stellt dort eine Frage.")

# ───────────────────────── 5 · Jesus und die Mächte ─────────────────────────
sec("jesus", [R(MT, 16, 13, 20)], "Am Fuß des Hermon",
    "In der Gegend von Cäsarea Philippi fragt Jesus, für wen die Leute ihn halten, und dann: Wer sagt ihr, dass ich bin? Petrus bekennt ihn als Christus, den Sohn des lebendigen Gottes. Jesus will auf diesen Felsen seine Gemeinde bauen; die Pforten des Hades werden sie nicht überwältigen.",
    place="caesarea-philippi",
    quiz=[
        choice("Für wen halten die Leute Jesus nach V. 14 nicht?", ["Für Mose", "Für Johannes den Täufer", "Für Elia", "Für Jeremia"], 14, "Lies Vers 14.",
               "V. 14: Johannes der Täufer, Elia, Jeremia oder einer der Propheten – Mose wird nicht genannt."),
        who("Du bist der Christus, der Sohn des lebendigen Gottes.", R(MT, 16, 16), ["Simon Petrus", "Johannes", "Jakobus", "Andreas"],
            "V. 16: Simon Petrus antwortet für die Jünger."),
        error("Des [Todes] Pforten werden sie nicht überwältigen.", "Hades", 18,
              "V. 18: Die Pforten des Hades werden die Gemeinde nicht überwältigen."),
    ],
    explain=[
        E("Warum gerade hier?", "Cäsarea Philippi lag am Fuß des Hermon, bei einer Höhle mit Quelle, die dem griechischen Gott Pan geweiht war. Heiser meint: Jesus spricht von den „Pforten des Hades“ an einem Ort, der für viele als Eingang zur Unterwelt galt, in der Gegend, wo nach dem Henochbuch die Wächter herabstiegen. Kritiker wenden ein, dass kein antiker Text die Höhle so nennt."),
        E("Was ist der Fels?", "Katholische Tradition: Petrus selbst und seine Nachfolger, die Bischöfe von Rom. Orthodoxe: der Glaube des Petrus, den alle rechtgläubigen Bischöfe teilen. Viele Evangelische: das Bekenntnis zu Christus oder Christus selbst (1Kor 3,11). Im Griechischen ist es ein Wortspiel: Petros und petra."),
        E("Wo war die Verklärung?", "Wenige Tage später führt Jesus drei Jünger auf einen „hohen Berg“ (Mt 17,1). Die Tradition nennt seit dem 4. Jahrhundert den Tabor; Heiser und andere denken an den nahen Hermon."),
    ],
    fact="Der heutige Name des Ortes, Banias, geht auf Paneas zurück, den alten Namen nach dem Gott Pan.",
    teaser="Ein Mann, den keine Kette halten kann, fällt vor Jesus nieder – und was aus ihm spricht, hat Angst.")

sec("jesus", [R(MK, 5, 1, 13)], "Legion",
    "Im Land der Gadarener kommt Jesus ein Mann aus den Gräbern entgegen, den niemand bändigen kann. Er wirft sich vor Jesus nieder und schreit: Quäle mich nicht! Der unreine Geist nennt sich Legion, denn sie sind viele. Sie bitten, nicht aus der Gegend weggeschickt zu werden, und fahren in eine Herde Schweine, die in den See stürzt.",
    place="gadarener",
    focus="Achte darauf, worum die Geister Jesus bitten – und was sie fürchten.",
    quiz=[
        choice("Wo wohnte der Mann?", ["In den Grabstätten", "In einer Höhle am See", "Im Haus seiner Familie", "In der Synagoge"], 3, "Lies Vers 3.",
               "V. 3: Er hatte seine Wohnung in den Grabstätten."),
        who("Was habe ich mit dir zu schaffen, Jesus, Sohn Gottes, des Höchsten?", R(MK, 5, 7), ["Der Mann mit dem unreinen Geist", "Einer der Schweinehirten", "Ein Jünger", "Ein Mann aus der Dekapolis"],
            "V. 7: Der Besessene schreit es mit lauter Stimme und bittet: Quäle mich nicht!"),
        estimate("Wie viele Schweine waren es etwa?", 100, 5000, 2000, "Schweine",
                 "V. 13: etwa 2000.", 13, "Lies Vers 13.", 300),
    ],
    explain=[
        E("Warum fürchten sie sich?", "Der Geist bittet, nicht gequält zu werden (V. 7); nach Mt 8,29 fragen sie, ob Jesus sie „vor der Zeit“ quälen will, nach Lk 8,31 bitten sie, nicht in den Abgrund geschickt zu werden. Sie wissen also von einem Gericht, das noch aussteht – und von einem Ort, an dem andere schon gefangen sind (2Petr 2,4)."),
        E("Was sind Dämonen nach Heiser?", "Heiser folgt einer alten jüdischen Deutung: Die Dämonen sind die Geister der toten Nephilim. Nach dem Henochbuch gingen aus den Riesen nach ihrem Tod böse Geister hervor, die auf der Erde umherziehen (1Hen 15,8–12). Ihre Väter, die Wächter, sind im Abgrund gefesselt – das erklärt für ihn, warum die Geister den Abgrund fürchten. Viele Christen sehen in Dämonen dagegen gefallene Engel (vgl. Offb 12,9)."),
        E("Warum „Legion“?", "Eine römische Legion zählte mehrere tausend Soldaten. Der Name sagt: Es sind viele, und sie treten wie eine Besatzungsmacht auf."),
        E("Warum Gräber und Schweine?", "Gräber und Schweine waren nach jüdischem Gesetz unrein (4Mo 19,16; 3Mo 11,7). Das Ostufer war heidnisches Gebiet der Dekapolis, nahe dem alten Basan."),
    ],
    try_="Lies Lk 8,31. Worum bitten die Geister dort?",
    teaser="Jesus sendet siebzig Jünger aus – eine Zahl, die schon in 1. Mose vorkommt.")

sec("jesus", [R(LK, 10, 1, 2), R(LK, 10, 17, 20)], "Die Siebzig",
    "Jesus sendet siebzig Jünger zu zweit voraus in die Orte, in die er kommen will. Sie kehren voller Freude zurück: Selbst die Dämonen gehorchen ihnen in seinem Namen. Jesus sagt, er habe den Satan wie einen Blitz vom Himmel fallen sehen. Doch freuen sollen sie sich, dass ihre Namen im Himmel stehen.",
    quiz=[
        choice("Was berichten die Siebzig nach V. 17?", ["Selbst die Dämonen sind ihnen in Jesu Namen untertan", "Alle Städte haben sie aufgenommen", "Sie haben Tote auferweckt", "Die Pharisäer sind ihnen gefolgt"], 17, "Lies Vers 17.",
               "V. 17: Herr, auch die Dämonen sind uns untertan in deinem Namen."),
        tf("Jesus sagt in V. 20, sie sollen sich vor allem über ihre Macht über die Geister freuen.", False, 20, "Lies Vers 20.",
           "V. 20: Freut euch nicht darüber, sondern dass eure Namen in den Himmeln angeschrieben sind."),
    ],
    explain=[
        E("Siebzig oder zweiundsiebzig?", "Die Handschriften sind sich nicht einig: Manche lesen 70, andere 72. Die Völkertafel in 1Mo 10 zählt in der hebräischen Bibel 70 Völker, in der griechischen Übersetzung 72. Heiser sieht darin ein Zeichen: Jesus sendet seine Boten symbolisch zu allen Völkern, die Gott in Babel aufgegeben hatte."),
        E("Was meint der Satz über den Satan?", "Ausleger lesen ihn als Vision eines Sturzes vor Urzeiten, als Bild für das, was gerade durch die Jünger geschieht, oder als Vorausblick auf das Kreuz (Joh 12,31). Heiser liest ihn als Zeichen, dass Gottes Herrschaft in das Gebiet der Mächte eindringt."),
        E("Schlangen und Skorpione?", "V. 19 greift wohl Ps 91,13 auf. Für Heiser erinnert die Schlange auch an 1Mo 3,15."),
    ],
    fact="Auch der Hohe Rat in Jerusalem, der Sanhedrin, hatte nach der Überlieferung 70 oder 71 Mitglieder – angelehnt an die 70 Ältesten, die Mose halfen (4Mo 11,16).",
    memory_verse=MV(R(LK, 10, 20), "freut euch aber, dass eure Namen in den Himmeln angeschrieben sind"),
    teaser="Menschen aus vielen Völkern hören Galiläer in ihrer eigenen Sprache reden – das Gegenstück zu einer Geschichte, die du schon kennst.")

sec("jesus", [R(APG, 2, 1, 13)], "Pfingsten",
    "Am Pfingsttag kommt ein Brausen vom Himmel, Zungen wie von Feuer verteilen sich auf die Jünger, und sie reden in anderen Sprachen. Juden aus vielen Völkern hören die großen Taten Gottes in ihrer eigenen Sprache. Einige staunen, andere spotten, sie seien betrunken.",
    place="jerusalem",
    focus="Achte auf die Liste in V. 9–11. Was erinnert dich an Babel?",
    quiz=[
        choice("Was erscheint nach V. 3?", ["Zerteilte Zungen wie von Feuer", "Eine Taube", "Ein Engel", "Eine Wolke"], 3, "Lies Vers 3.",
               "V. 3: zerteilte Zungen wie von Feuer, die sich auf jeden setzten."),
        tf("Nach V. 6 hörte jeder die Jünger in seiner eigenen Sprache reden.", True, 6, "Lies Vers 6.",
           "V. 6: Jeder hörte sie in seiner eigenen Mundart reden."),
        choice("Was sagen die Spötter in V. 13?", ["Sie sind voll süßen Weines", "Sie sind verrückt geworden", "Sie lügen", "Sie sind Zauberer"], 13, "Lies Vers 13.",
               "V. 13: Sie sind voll süßen Weines."),
    ],
    explain=[
        E("Was hat Pfingsten mit Babel zu tun?", "In Babel wurden die Sprachen verwirrt und die Völker zerstreut; hier hört jeder Gottes Taten in seiner Sprache. Heiser weist zusätzlich darauf hin, dass Lukas für die „zerteilten“ Zungen dasselbe griechische Verb benutzt wie die Septuaginta in 5Mo 32,8 für das Verteilen der Völker. Die Liste in V. 9–11 nennt Völker in alle Himmelsrichtungen."),
        E("Was ist Pfingsten?", "Das jüdische Wochenfest (Schawuot), 50 Tage nach dem Passa; griechisch pentekoste, „der fünfzigste“. Im späteren Judentum erinnerte man an diesem Fest auch an die Gabe der Tora am Sinai – auch dort waren Feuer und Stimme (2Mo 19,18)."),
        E("Andere Sprachen oder Zungenrede?", "Lukas beschreibt verständliche Sprachen. Ob das dieselbe Gabe ist wie die Zungenrede in 1Kor 14, wird in Pfingstgemeinden, charismatischen Bewegungen und anderen Kirchen unterschiedlich gesehen."),
    ],
    try_="Lies 1Mo 11,7–9 und dann Apg 2,6–8. Was ist umgekehrt?",
    teaser="Paulus beschreibt einen Kampf, dessen Gegner man nicht sehen kann – und zählt sie mit Titeln auf.")

sec("jesus", [R(EPH, 6, 10, 18)], "Mächte und Gewalten",
    "Paulus fordert auf, stark zu sein im Herrn und die ganze Waffenrüstung Gottes anzuziehen. Der Kampf geht nicht gegen Menschen, sondern gegen Fürstentümer, Gewalten und Weltbeherrscher der Finsternis in der himmlischen Welt. Er zählt die Rüstung auf: Wahrheit, Gerechtigkeit, Evangelium, Glaube, Heil, das Wort Gottes – und das Gebet.",
    quiz=[
        choice("Gegen wen geht der Kampf nach V. 12 nicht?", ["Gegen Fleisch und Blut", "Gegen die Fürstentümer", "Gegen die Gewalten", "Gegen die Mächte der Bosheit"], 12, "Lies Vers 12.",
               "V. 12: nicht gegen Fleisch und Blut, sondern gegen Fürstentümer, Gewalten und geistliche Mächte."),
        order("Bring die Teile der Rüstung in die Reihenfolge des Textes.", ["Gürtel der Wahrheit", "Brustpanzer der Gerechtigkeit", "Schuhe der Bereitschaft für das Evangelium", "Schild des Glaubens", "Helm des Heils"],
              "V. 14–17: Wahrheit, Gerechtigkeit, Evangelium, Glaube, Heil – dann das Schwert des Geistes.", "Lies Vers 14–17."),
        error("Nehmt das Schwert des Geistes, das [Gebet] ist.", "Gottes Wort", 17,
              "V. 17: das Schwert des Geistes, das Gottes Wort ist."),
    ],
    explain=[
        E("Wer sind die Fürstentümer und Gewalten?", "Heiser liest die Titel als Namen für die abgefallenen Herrscher über die Völker aus 5Mo 32 und Dan 10 – Paulus benutzt Herrschaftswörter. Viele Ausleger verstehen allgemeiner böse Geister unter Führung des Teufels (V. 11). Manche denken auch an Mächte, die durch irdische Strukturen wirken."),
        E("Was hat das Kreuz damit zu tun?", "Kol 2,15 sagt, Christus habe die Gewalten am Kreuz entwaffnet und öffentlich zur Schau gestellt; Eph 1,20–22 setzt ihn über alle Mächte. Für Heiser ist das der Grund, warum die Gemeinde „stehen“ kann (V. 13–14): Der Sieg ist schon errungen."),
        E("Woher kommt das Bild der Rüstung?", "Paulus kannte römische Soldaten. Er greift aber auch Jesaja auf, wo Gott selbst Gerechtigkeit als Panzer und Heil als Helm trägt (Jes 59,17)."),
    ],
    cards=["maechte"],
    prayer={"text": "Christus mit mir, Christus vor mir, Christus hinter mir, Christus in mir, Christus unter mir, Christus über mir, Christus zu meiner Rechten, Christus zu meiner Linken.", "source": "„Lorica“, dem heiligen Patrick zugeschrieben (altirisch, frühes Mittelalter), eigene Übersetzung"},
    try_="Lies Jes 59,17. Welche Teile der Rüstung trägt dort Gott selbst?",
    teaser="Jesus wird fast gesteinigt – und verteidigt sich mit dem Psalm, mit dem dieser Plan begonnen hat.")

# ───────────────────────── 6 · Gottes neue Familie ─────────────────────────
sec("familie", [R(JOH, 10, 31, 39)], "„Ihr seid Götter“",
    "Die Juden wollen Jesus steinigen, weil er sich als Mensch zu Gott mache. Jesus antwortet mit Ps 82: Wenn die Schrift schon jene Götter nennt, zu denen das Wort Gottes kam, wie können sie ihm Lästerung vorwerfen, weil er sich Gottes Sohn nennt? Sie wollen ihn festnehmen, doch er entkommt.",
    place="jerusalem",
    quiz=[
        choice("Warum wollen sie Jesus nach V. 33 steinigen?", ["Weil er sich als Mensch zu Gott macht", "Weil er am Sabbat geheilt hat", "Weil er den Tempel kritisiert hat", "Weil er die Römer unterstützt"], 33, "Lies Vers 33.",
               "V. 33: wegen Lästerung, weil du, ein Mensch, dich selbst zu Gott machst."),
        tf("Jesus zitiert in V. 34 den Satz „Ihr seid Götter“.", True, 34, "Lies Vers 34.",
           "V. 34: Steht nicht in eurem Gesetz: Ich habe gesagt, ihr seid Götter? – Ps 82,6."),
        choice("Wie nennt Jesus sich in V. 36?", ["Gottes Sohn", "Der Menschensohn", "Der Prophet", "Der König Israels"], 36, "Lies Vers 36.",
               "V. 36: … weil ich sagte: Ich bin Gottes Sohn."),
    ],
    explain=[
        E("Wen meint Jesus mit „jene Götter“?", "Jesus beschreibt sie als die, zu denen das Wort Gottes kam (V. 35). Viele Ausleger, schon rabbinische, lesen: die Richter Israels oder Israel am Sinai, das Gottes Wort empfing. Heiser liest: die Söhne Gottes aus Ps 82 – Jesus schließt vom Geringeren aufs Größere: Wenn schon sie elohim heißen dürfen, dann erst recht er."),
        E("Warum „in eurem Gesetz“?", "„Gesetz“ steht hier für die ganze Schrift, nicht nur die fünf Bücher Mose; Ps 82 gehört zu den Psalmen."),
    ],
    try_="Lies Ps 82 noch einmal. Was ist bei Jesus anders als bei den „Göttern“ dort?",
    teaser="Die Schöpfung wartet – nicht auf Engel, sondern auf Söhne Gottes, die man noch nicht sieht.")

sec("familie", [R(ROEM, 8, 14, 23)], "Söhne Gottes",
    "Wer sich vom Geist Gottes leiten lässt, ist Gottes Sohn; der Geist der Sohnschaft ruft Abba, Vater. Als Kinder sind sie Erben, Miterben Christi. Die ganze Schöpfung wartet sehnsüchtig darauf, dass die Söhne Gottes offenbar werden, und seufzt wie in Geburtswehen.",
    quiz=[
        choice("Was ruft der Geist der Sohnschaft nach V. 15?", ["Abba, Vater!", "Heilig, heilig, heilig!", "Herr, erbarme dich!", "Halleluja!"], 15, "Lies Vers 15.",
               "V. 15: ein Geist der Sohnschaft, in dem wir rufen: Abba, Vater!"),
        error("Die Schöpfung wartet auf die Offenbarung der [Engel] Gottes.", "Söhne", 19,
              "V. 19: Das sehnsüchtige Harren der Schöpfung wartet auf die Offenbarung der Söhne Gottes."),
        tf("Nach V. 23 seufzen auch die Glaubenden und warten noch.", True, 23, "Lies Vers 23.",
           "V. 23: Auch wir seufzen und erwarten die Sohnschaft, die Erlösung unseres Leibes."),
    ],
    explain=[
        E("Warum „Söhne Gottes“?", "Im Alten Testament heißen so die himmlischen Wesen (Hiob 1,6) und Israel (2Mo 4,22). Heiser sieht hier den Bogen: Gott schafft sich eine neue Familie aus Menschen, die einmal den Platz der abgefallenen Söhne Gottes einnehmen soll. Paulus meint ausdrücklich Frauen und Männer (vgl. Gal 3,26–28)."),
        E("Was ist „Sohnschaft“?", "Griechisch hyiothesia, ein Begriff aus dem römischen Recht: die Adoption. Ein adoptierter Sohn bekam alle Rechte eines Erben."),
        E("Was heißt Abba?", "Das aramäische Wort für „Vater“, mit dem Jesus selbst betet (Mk 14,36)."),
    ],
    memory_verse=MV(R(ROEM, 8, 19), "Denn das sehnsüchtige Harren der Schöpfung wartet auf die Offenbarung der Söhne Gottes."),
    teaser="Der letzte Text sagt, wem Gott die künftige Welt nicht unterworfen hat.")

sec("familie", [R(HEBR, 2, 5, 13)], "Nicht den Engeln",
    "Die kommende Welt hat Gott nicht Engeln unterstellt, sondern dem Menschen, wie Ps 8 sagt. Noch ist ihm nicht alles unterworfen, aber Jesus ist mit Herrlichkeit gekrönt, nachdem er für alle den Tod geschmeckt hat. Er führt viele Söhne zur Herrlichkeit und schämt sich nicht, sie Brüder zu nennen.",
    focus="Achte darauf, wem die künftige Welt nach V. 5 nicht gehört – und wem dann?",
    quiz=[
        choice("Wem hat Gott nach V. 5 die künftige Welt nicht unterworfen?", ["Den Engeln", "Den Menschen", "Den Propheten", "Den Königen"], 5, "Lies Vers 5.",
               "V. 5: Nicht Engeln hat er den zukünftigen Erdkreis unterworfen."),
        tf("Nach V. 8 sehen wir schon jetzt dem Menschen alles unterworfen.", False, 8, "Lies Vers 8.",
           "V. 8: Jetzt aber sehen wir ihm noch nicht alles unterworfen."),
        choice("Wie nennt Jesus die, die er heiligt, nach V. 11?", ["Brüder", "Diener", "Freunde", "Jünger"], 11, "Lies Vers 11.",
               "V. 11: Er schämt sich nicht, sie Brüder zu nennen."),
    ],
    explain=[
        E("Warum „unter die Engel“?", "Hebr 2,7 zitiert Ps 8,6 nach der Septuaginta, die „Engel“ sagt. Im Hebräischen steht dort elohim – der Mensch ist ein wenig geringer gemacht als die Wesen der unsichtbaren Welt."),
        E("Was heißt das für Heiser?", "Die Menschen sollten von Anfang an zu Gottes Familie und seinem Rat gehören. Nach dem Neuen Testament werden die Glaubenden einmal mit Christus herrschen, über Völker (Offb 2,26–27), auf seinem Thron (Offb 3,21), und sogar Engel richten (1Kor 6,3). Das ist für Heiser das Ziel der ganzen Geschichte."),
        E("Sehen das alle so?", "Dass die Glaubenden mit Christus herrschen, sagen viele Traditionen. Wie und wann, hängt von der Endzeitsicht ab: Prämillenialisten denken an ein künftiges Tausendjähriges Reich, Amillenialisten an die Herrschaft der Heiligen schon jetzt mit Christus und vollendet in der neuen Schöpfung. Heisers Verbindung mit dem himmlischen Rat ist eine Deutung."),
    ],
    prayer={"ref": R(PS, 8, 2), "source": "Psalm 8,2"},
    try_="Lies Ps 8,4–7 und vergleiche es mit Hebr 2,6–8. Wen sieht der Hebräerbrief in dem Psalm?")

P.write()
