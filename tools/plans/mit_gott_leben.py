#!/usr/bin/env python3
"""Source for the reading plan „Mit Gott leben“ (generates assets/plans/mit-gott-leben.json).

python3 -I tools/plans/mit_gott_leben.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/mit-gott-leben.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

GEN, EX, SAM1, PS, PRED, JES, JER, DAN, HOS = 1, 2, 9, 19, 21, 23, 24, 27, 28
MT, LK, JOH, KOR1, KOL, JAK, JOH1 = 40, 42, 43, 46, 51, 59, 62

P = PlanBuilder(
    "mit-gott-leben", "mgl", "Mit Gott leben", "Wie Beziehung mit Gott aussieht",
    "Wen nennt die Bibel einen Freund Gottes? Was ist Gott wichtig? Wie reden Menschen mit ihm – im Alltag, in der Not, wenn er fern scheint? "
    "27 kurze Abschnitte, in denen biblische Menschen mit Gott leben. Fragen und Hintergrund statt Antworten von außen.",
    "leben",
    stages=[("freunde", "Freunde Gottes"), ("wichtig", "Was Gott wichtig ist"), ("reden", "Mit Gott reden"),
            ("alltag", "Im Alltag"), ("fern", "Wenn Gott fern scheint"), ("lieben", "Gott lieben – Menschen lieben")],
    cards=[
        ("freund-gottes", "begriff", "Freund Gottes", "So nennt die Bibel ausdrücklich Abraham (2Chr 20,7; Jes 41,8; Jak 2,23). Von Mose heißt es, Gott rede mit ihm wie mit einem Freund (2Mo 33,11). Jesus nennt seine Jünger Freunde (Joh 15,15). In der islamischen Tradition trägt Abraham bis heute den Beinamen „Freund Gottes“ (al-Chalil).", "Jes 41,8; Jak 2,23; Joh 15,15"),
        ("wandeln", "begriff", "Wandeln", "Ein biblisches Bild für die Art, wie jemand lebt: „mit Gott wandeln“, „auf seinen Wegen gehen“. Im späteren Judentum heißt die Lehre vom richtigen Leben „Halacha“ – vom hebräischen Wort für „gehen“.", "1Mo 5,24; 6,9; Mi 6,8"),
        ("henoch", "person", "Henoch", "Siebter Mensch in der Geschlechterfolge von Adam, Vater Methusalems. Die Bibel sagt über ihn nur, dass er mit Gott wandelte und nicht starb, sondern „nicht mehr war“. Hebräer 11,5 zählt ihn zu den Vorbildern des Glaubens. Nach ihm sind spätere jüdische Schriften benannt, die nicht zur Bibel gehören (das Henochbuch, zitiert in Jud 14).", "1Mo 5,21–24; Hebr 11,5"),
        ("zelt-begegnung", "begriff", "Zelt der Begegnung", "Ein Zelt außerhalb des Lagers, in dem Mose Gott begegnete; die Elberfelder nennt es „Zelt der Zusammenkunft“. Später heißt so auch das große Heiligtum (Stiftshütte), in dem die Bundeslade stand. Wer den HERRN suchen wollte, konnte hinausgehen.", "2Mo 33,7–11"),
        ("chesed", "begriff", "Chesed", "Ein hebräisches Schlüsselwort, schwer zu übersetzen: Treue, Güte, Liebe, Verlässlichkeit in einer Beziehung. Die Elberfelder übersetzt je nach Stelle „Gnade“, „Güte“ oder „Frömmigkeit“, Luther oft „Liebe“ oder „Barmherzigkeit“. Es steht über 240-mal im Alten Testament.", "Hos 6,6; Mi 6,8; Ps 136"),
        ("fasten", "begriff", "Fasten", "Bewusster Verzicht auf Essen für eine Zeit, im Alten Testament oft verbunden mit Trauer, Buße oder dringendem Gebet. Am Versöhnungstag war es für ganz Israel vorgeschrieben (3Mo 16,29). Jesus setzt voraus, dass seine Jünger fasten werden (Mt 6,16; Mk 2,20).", "Jes 58; Mt 6,16–18"),
        ("hanna", "person", "Hanna", "Frau des Elkana aus dem Gebirge Ephraim, lange kinderlos und von der zweiten Frau ihres Mannes gekränkt. Sie betet im Heiligtum von Silo um einen Sohn und bekommt Samuel, den späteren Propheten. Ihr Danklied (1Sam 2,1–10) klingt im Lobgesang der Maria nach (Lk 1,46–55).", "1Sam 1–2"),
        ("vaterunser", "begriff", "Vaterunser", "Das Gebet, das Jesus seine Jünger lehrt, in zwei Fassungen überliefert (Mt 6,9–13; Lk 11,2–4). Der Schluss „Denn dein ist das Reich …“ steht nicht in den ältesten Handschriften, wurde aber früh im Gottesdienst gebetet. Die Didache, eine Gemeindeordnung um 100 n. Chr., empfiehlt, es dreimal am Tag zu beten.", "Mt 6,9–13; Lk 11,2–4"),
        ("daniel", "person", "Daniel", "Als junger Mann aus Jerusalem nach Babylon verschleppt und dort am Hof ausgebildet. Er dient mehreren Königen, auch nach dem Fall Babylons an die Perser. Das Buch erzählt von seiner Treue im Alltag eines fremden Landes und überliefert seine Visionen.", "Dan 1; 6"),
        ("gebetszeiten", "begriff", "Gebetszeiten", "Schon im Alten Testament gibt es feste Zeiten: morgens, mittags, abends (Ps 55,18; Dan 6,11). Die ersten Christen gingen zur Gebetsstunde in den Tempel (Apg 3,1). Daraus entstand das Stundengebet der Klöster und Kirchen. Viele Freikirchen kennen die „Stille Zeit“ am Morgen, andere beten frei, wann es sich ergibt.", "Ps 55,18; Dan 6,11; Apg 3,1"),
        ("marta-maria", "person", "Marta und Maria", "Zwei Schwestern, bei denen Jesus einkehrt. Nach dem Johannesevangelium wohnten sie mit ihrem Bruder Lazarus in Betanien bei Jerusalem. Dort ist es Marta, die das Bekenntnis zu Jesus als Christus ausspricht (Joh 11,27), und Maria, die ihn mit Öl salbt (Joh 12,3).", "Lk 10,38–42; Joh 11–12"),
        ("kohelet", "begriff", "Prediger (Kohelet)", "Hebräisch Kohelet, etwa „der zur Versammlung spricht“. Das Buch prüft nüchtern, was im Leben bleibt, und nennt vieles „Hauch“ (Elberfelder: „Eitelkeit“). Gelesen wird es sehr verschieden: als Buch des Zweifels, als Weisheit für ein Leben ohne Illusionen oder als Einladung, das Leben aus Gottes Hand zu nehmen.", "Pred 1,2; 9,7–10; 12,13"),
        ("korachiter", "begriff", "Söhne Korachs", "Eine Familie von Tempelsängern aus dem Stamm Levi. Elf Psalmen tragen ihren Namen: Ps 42; 44–49; 84–85; 87–88. Ihr Stammvater Korach hatte sich gegen Mose aufgelehnt (4Mo 16) – seine Söhne aber starben nicht (4Mo 26,11).", "Ps 42; 84; 4Mo 26,11"),
        ("asaf", "person", "Asaf", "Ein Levit und Sänger zur Zeit Davids (1Chr 16,4–7). Zwölf Psalmen tragen seinen Namen (Ps 50; 73–83), viele davon ringen mit der Frage, warum es Gottlosen gut geht und Gottes Volk leidet.", "Ps 73; 1Chr 16,5"),
        ("weinstock", "begriff", "Weinstock", "Im Alten Testament ein Bild für Israel, das Gott gepflanzt hat (Ps 80,9; Jes 5,1–7). Ein Weinstock braucht jahrelange Pflege, bevor er Frucht bringt, und wird jedes Jahr zurückgeschnitten. Jesus nennt sich selbst den „wahren“ Weinstock.", "Joh 15,1–8; Jes 5,1–7"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Freunde Gottes ─────────────────────────
sec("freunde", [R(GEN, 5, 21, 24), R(GEN, 6, 9)], "Mit Gott gehen",
    "In einer langen Liste von Namen und Lebensjahren steht plötzlich etwas anderes: Henoch wandelte mit Gott – und war nicht mehr, denn Gott nahm ihn. Später wird dasselbe über Noah gesagt.",
    bridge="Dieser Plan liest Texte, in denen Menschen mit Gott leben. Er beginnt in einer Liste, die die meisten überblättern: der Geschlechterfolge von Adam bis Noah in 1. Mose 5.",
    focus="Achte darauf, welcher Satz in dieser Liste nicht wie die anderen klingt.",
    quiz=[
        tf("Der Text erzählt ausführlich, was Henoch getan hat.", False, 24, "Lies Vers 22 und 24.",
           "V. 22 und 24: Zweimal steht nur, dass er mit Gott wandelte. Was das konkret hieß, sagt der Text nicht."),
        choice("Was geschieht am Ende mit Henoch?", ["Er war nicht mehr, denn Gott nahm ihn weg", "Er starb alt und lebenssatt", "Er wurde in seinem Garten begraben", "Er zog in ein fernes Land"], 24, "Lies Vers 24.",
               "V. 24: Bei fast allen anderen in der Liste heißt es „und er starb“ – bei Henoch nicht."),
        choice("Was sagt 6,9 über Noah?", ["Er war gerecht, vollkommen unter seinen Zeitgenossen und wandelte mit Gott", "Er war der älteste Mensch seiner Zeit", "Er baute als Erster einen Altar", "Er war Priester des Höchsten"], None, "Lies 6,9.",
               "6,9: dieselbe Wendung wie bei Henoch – er wandelte mit Gott."),
    ],
    explain=[
        E("Was heißt „wandeln“?", "Ein altes Wort für „gehen, umhergehen“. Im Hebräischen steht eine Form, die ein dauerndes Hin- und Hergehen ausdrückt – dieselbe Form, mit der Gott im Garten „wandelt“ (1Mo 3,8)."),
        E("Was ist mit Henoch passiert?", "Der Text sagt nur: Gott nahm ihn. Hebräer 11,5 versteht das so, dass er den Tod nicht sah. Ähnlich wird später Elia in den Himmel aufgenommen (2Kön 2,11)."),
        E("Warum diese langen Lebensjahre?", "Christen lesen die Zahlen verschieden: als tatsächliche Lebensalter, als Zahlen mit symbolischem Wert oder als Ausdruck einer anderen Zeit vor der Flut. Henochs 365 Jahre entsprechen den Tagen eines Sonnenjahres – ob das gewollt ist, weiß man nicht."),
    ],
    cards=["wandeln", "henoch"],
    teaser="Gott will etwas tun – und fragt sich laut, ob er es vor Abraham verbergen soll.")

sec("freunde", [R(GEN, 18, 16, 21)], "Soll ich es verbergen?",
    "Die drei Männer brechen nach Sodom auf, Abraham begleitet sie ein Stück. Gott überlegt laut, ob er vor Abraham verbergen soll, was er vorhat – und weiht ihn ein.",
    bridge="Gott ist Abraham in Gestalt von drei Männern begegnet und hat ihm einen Sohn versprochen (1Mo 18,1–15). Nun brechen die Männer auf.",
    place="mamre",
    focus="Achte darauf, mit wem Gott in V. 17 eigentlich spricht.",
    quiz=[
        choice("Warum will Gott Abraham einweihen?", ["Weil Abraham ein großes Volk werden und seinen Kindern den Weg des HERRN lehren soll", "Weil Abraham in Sodom wohnt", "Weil Abraham ihn darum gebeten hat", "Weil Lot sein Neffe ist"], 19, "Lies Vers 17–19.",
               "V. 18–19: Abraham soll seinen Nachkommen Gerechtigkeit und Recht weitergeben."),
        tf("Gott sagt, er wolle hinabgehen und selbst sehen, wie es in Sodom steht.", True, 21, "Lies Vers 21.",
           "V. 21: Er will sehen, ob das Geschrei stimmt – und wenn nicht, will er es wissen."),
    ],
    explain=[
        E("Mit wem redet Gott in V. 17?", "Offenbar mit sich selbst – der Leser hört Gottes Überlegung mit. Ob Abraham sie hört, sagt der Text nicht. Erst in V. 20 spricht Gott ihn an."),
        E("Warum muss Gott „hinabgehen und sehen“?", "Die Bibel beschreibt Gott oft in menschlichen Bildern. Ausleger verstehen das meist so: Gott urteilt nicht nach Hörensagen. Ähnlich beim Turmbau zu Babel (1Mo 11,5)."),
    ],
    cards=["freund-gottes"],
    teaser="Abraham bleibt stehen – und beginnt zu verhandeln.")

sec("freunde", [R(GEN, 18, 22, 33)], "Abraham verhandelt",
    "Abraham bleibt vor Gott stehen und fragt: Willst du den Gerechten mit dem Gottlosen umbringen? Von 50 Gerechten handelt er Gott bis auf 10 herunter.",
    place="mamre",
    quiz=[
        choice("Was hält Abraham Gott in V. 25 entgegen?", ["Der Richter der ganzen Erde muss doch Recht üben", "Lot ist mein Neffe", "Du hast mir das Land versprochen", "Die Stadt hat dir Opfer gebracht"], 25, "Lies Vers 25.",
               "V. 25: Sollte der Richter der ganzen Erde nicht Recht üben?"),
        order("In welchen Schritten verhandelt Abraham?", ["50", "45", "40", "30", "20"],
              "V. 24–31: 50, 45, 40, 30, 20 – und zuletzt 10 (V. 32)."),
        tf("Gott wird zornig über Abrahams Fragen und beendet das Gespräch.", False, 33, "Lies Vers 26–33.",
           "V. 26–33: Gott geht auf jede Zahl ein. Er geht erst, als er mit Abraham ausgeredet hat (V. 33)."),
    ],
    explain=[
        E("Ändert Abraham Gottes Plan?", "Darüber denken Christen verschieden. Viele sagen: Gott lässt sich wirklich auf das Gespräch ein. Andere betonen, dass Gott schon wusste, wie es ausgeht, und Abraham so an seinem Denken teilhaben lässt. In 1Mo 19,29 heißt es: Gott gedachte an Abraham und rettete Lot."),
        E("Warum spricht Abraham von „Staub und Asche“?", "Eine Redewendung für die eigene Kleinheit und Vergänglichkeit (vgl. 1Mo 3,19; Hiob 42,6)."),
    ],
    fact="In der jüdischen Tradition gilt diese Szene als Vorbild für Fürbitte: für andere eintreten, auch für Menschen, die einem fremd sind.",
    teaser="Ein Zelt außerhalb des Lagers. Wer hineingeht, wird von allen beobachtet.")

sec("freunde", [R(EX, 33, 7, 17)], "Wie mit einem Freund",
    "Mose schlägt ein Zelt außerhalb des Lagers auf. Dort redet Gott mit ihm von Angesicht zu Angesicht. Mose bittet: Lass mich deinen Weg wissen – und wenn du nicht mitgehst, dann führe uns nicht von hier weg.",
    bridge="Israel hat am Sinai das goldene Kalb gemacht. Gott kündigt an, er werde einen Engel vor ihnen hersenden, selbst aber nicht mitziehen (2Mo 33,1–3).",
    place="horeb",
    focus="Achte darauf, was Mose von Gott erbittet – und was er ablehnt.",
    quiz=[
        choice("Was tut das Volk, wenn Mose zum Zelt geht?", ["Sie stehen am Eingang ihrer Zelte und schauen ihm nach", "Sie folgen ihm hinein", "Sie bringen Opfer dar", "Sie gehen schlafen"], 8, "Lies Vers 8–10.",
               "V. 8–10: Sie schauen ihm nach, und wenn die Wolkensäule kommt, werfen sie sich nieder."),
        who("Wenn dein Angesicht nicht mitgeht, so führe uns nicht von hier hinauf.", R(EX, 33, 15), ["Mose", "Josua", "Aaron", "Gott"],
            "V. 15: Mose will lieber bleiben als ohne Gott weiterziehen."),
        tf("Josua bleibt im Zelt, als Mose ins Lager zurückkehrt.", True, 11, "Lies Vers 11.",
           "V. 11: Der junge Josua weicht nicht aus dem Zelt."),
    ],
    explain=[
        E("„Von Angesicht zu Angesicht“ – und doch nicht?", "Wenige Verse später sagt Gott, kein Mensch könne sein Angesicht sehen und leben (V. 20). Ausleger verstehen V. 11 meist als Ausdruck großer Nähe und direkter Rede, nicht als Schau von Gottes Gestalt."),
        E("Was heißt „mein Angesicht wird mitgehen“?", "„Angesicht“ steht für Gottes persönliche Gegenwart. Gott nimmt hier seine Ankündigung aus V. 3 zurück."),
        E("Was heißt „ich kenne dich mit Namen“?", "In der Bibel heißt „kennen“ oft mehr als wissen: eine persönliche Beziehung, Auswahl, Zuwendung (vgl. Jer 1,5)."),
    ],
    cards=["zelt-begegnung"],
    memory_verse=MV(R(EX, 33, 14), "Mein Angesicht wird mitgehen, und ich werde dir Ruhe geben."),
    teaser="Zwei Bibelstellen nennen Abraham „Freund Gottes“. Was haben sie im Blick?")

sec("freunde", [R(JES, 41, 8, 10), R(JAK, 2, 21, 24)], "Abraham, mein Freund",
    "Gott nennt Israel die Nachkommen Abrahams, „meines Freundes“, und sagt ihnen: Fürchte dich nicht, ich bin mit dir. Jakobus erklärt, warum Abraham Freund Gottes genannt wurde: Sein Glaube zeigte sich in seinem Tun.",
    bridge="Jahrhunderte nach Abraham: Israel ist im Exil in Babylon. Ein Prophet im Buch Jesaja tröstet das Volk. Danach springt der Abschnitt ins Neue Testament, zum Jakobusbrief.",
    quiz=[
        choice("Was sagt Gott in Jes 41,10 zu Israel?", ["Fürchte dich nicht, ich bin mit dir", "Kehrt um, sonst werdet ihr vernichtet", "Baut den Tempel wieder auf", "Zieht in ein anderes Land"], None, "Lies Jes 41,10.",
               "Jes 41,10: Fürchte dich nicht – ich stärke dich, ich helfe dir, ich stütze dich."),
        choice("An welche Tat Abrahams erinnert Jakobus?", ["Dass er Isaak auf dem Altar opferte", "Dass er aus Haran aufbrach", "Dass er für Sodom bat", "Dass er Lot rettete"], 21, "Lies Jak 2,21.",
               "Jak 2,21: die Bindung Isaaks (1Mo 22)."),
        tf("Jakobus zitiert den Satz, dass Abraham Gott glaubte und es ihm zur Gerechtigkeit gerechnet wurde.", True, 23, "Lies Jak 2,23.",
           "Jak 2,23 zitiert 1Mo 15,6 – denselben Vers, den auch Paulus anführt (Röm 4,3)."),
    ],
    explain=[
        E("Jakobus und Paulus – ein Widerspruch?", "Paulus sagt, der Mensch werde durch Glauben gerecht ohne Werke des Gesetzes (Röm 3,28), Jakobus: aus Werken und nicht aus Glauben allein (Jak 2,24). Evangelische Ausleger sagen meist: Beide meinen Verschiedenes mit „Werken“ und „gerecht“. Katholische Ausleger betonen, dass Glaube und Liebe zusammengehören. 1999 erklärten Lutheraner und Katholiken gemeinsam: Rechtfertigung geschieht aus Gnade, und gute Werke folgen ihr. Mehr im Plan „Gerecht vor Gott“."),
        E("Wo heißt Abraham noch „Freund“?", "In 2. Chronik 20,7 betet König Josafat: Du hast das Land den Nachkommen Abrahams, deines Freundes, gegeben."),
    ],
    teaser="„Ich nenne euch nicht mehr Knechte.“ Was ist der Unterschied?")

sec("freunde", [R(JOH, 15, 9, 17)], "Ihr seid meine Freunde",
    "Am letzten Abend sagt Jesus: Wie der Vater mich liebt, so liebe ich euch – bleibt in meiner Liebe. Er nennt seine Jünger nicht mehr Knechte, sondern Freunde, weil er ihnen alles gesagt hat, was er vom Vater gehört hat.",
    bridge="Jesus ist mit seinen Jüngern beim letzten Mahl vor seiner Verhaftung (Joh 13–17). Johannes überliefert lange Abschiedsreden.",
    place="jerusalem",
    focus="Achte darauf, womit Jesus begründet, dass er sie Freunde nennt.",
    quiz=[
        choice("Warum nennt Jesus sie Freunde und nicht Knechte?", ["Weil er ihnen alles mitgeteilt hat, was er vom Vater gehört hat", "Weil sie ihn zuerst erwählt haben", "Weil sie ihm treu geblieben sind", "Weil sie mit ihm gegessen haben"], 15, "Lies Vers 15.",
               "V. 15: Ein Knecht weiß nicht, was sein Herr tut – Freunden sagt man, was man vorhat."),
        tf("Laut V. 16 haben die Jünger Jesus erwählt.", False, 16, "Lies Vers 16.",
           "V. 16: Umgekehrt – ich habe euch auserwählt."),
        choice("Welches Gebot nennt Jesus hier?", ["Dass ihr einander liebt, wie ich euch geliebt habe", "Dass ihr den Sabbat haltet", "Dass ihr täglich betet", "Dass ihr alles verkauft"], 12, "Lies Vers 12 und 17.",
               "V. 12 und 17: zweimal dasselbe – einander lieben."),
    ],
    explain=[
        E("Bedingung oder Beschreibung?", "V. 14 sagt: Ihr seid meine Freunde, wenn ihr tut, was ich gebiete. Manche Ausleger lesen das als Bedingung, andere als Beschreibung dessen, woran man Freundschaft erkennt. V. 16 betont dagegen, dass die Wahl von Jesus ausging."),
        E("Erinnert V. 15 an Abraham?", "Gott fragt sich in 1Mo 18,17, ob er vor Abraham verbergen soll, was er tun will. Ob Johannes daran denkt, ist nicht sicher – die Parallele ist vielen Auslegern aufgefallen."),
    ],
    memory_verse=MV(R(JOH, 15, 9), "Wie der Vater mich geliebt hat, habe auch ich euch geliebt; bleibt in meiner Liebe."),
    teaser="Ein Psalm stellt eine Frage, auf die man eine fromme Antwort erwartet. Sie fällt anders aus.")

# ───────────────────────── 2 · Was Gott wichtig ist ─────────────────────────
sec("wichtig", [R(PS, 15, 1, 5)], "Wer darf bei dir wohnen?",
    "David fragt: HERR, wer darf in deinem Zelt weilen? Die Antwort ist eine Liste: aufrichtig leben, die Wahrheit sagen, nicht verleumden, Wort halten, kein Wucher, keine Bestechung.",
    bridge="Neue Etappe: Was ist Gott wichtig? Psalm 15 wurde vermutlich beim Eintritt ins Heiligtum gesprochen – eine Frage am Tor und eine Antwort.",
    quiz=[
        choice("Welche Art von Antwort gibt der Psalm auf die Frage aus V. 1?", ["Eine Liste von Verhaltensweisen im Umgang mit anderen", "Eine Liste von Opfern", "Eine Liste von Gebeten", "Eine Liste von Festtagen"], 2, "Lies Vers 2–5.",
               "V. 2–5: Fast alles betrifft Reden, Geld und den Umgang mit Mitmenschen."),
        error("Wer in Gottes Zelt wohnen darf, redet die Wahrheit von [außen].", "Herzen", 2,
              "V. 2: Wahrheit reden von Herzen."),
        tf("Der Psalm erwähnt Opfer oder Rituale.", False, 5, "Lies den Psalm noch einmal.",
           "Kein einziges Mal – obwohl es um das Heiligtum geht."),
    ],
    explain=[
        E("Zins und Bestechung?", "Das Gesetz verbot, armen Israeliten Geld gegen Zins zu leihen (2Mo 22,24; 3Mo 25,35–37). Bestechung von Richtern traf vor allem die, die sich nichts leisten konnten (2Mo 23,8)."),
        E("Wie lesen Christen solche Listen?", "Manche lesen sie als Beschreibung derer, die Gott schon angenommen hat, andere als Maßstab, an dem man sich messen soll. Ähnliche Fragen am Tempeltor stellen Ps 24,3–6 und Jes 33,14–16."),
    ],
    teaser="Ein Volk singt ein schönes Lied über Umkehr. Gott antwortet: Was soll ich mit dir tun?")

sec("wichtig", [R(HOS, 6, 1, 6)], "Wie Tau am Morgen",
    "Das Volk sagt: Kommt, lasst uns zum HERRN umkehren, er wird uns heilen. Gott antwortet: Eure Treue ist wie eine Morgenwolke und wie der Tau, der früh verschwindet. Ich habe Gefallen an Treue, nicht an Opfern.",
    bridge="Hosea war Prophet im Nordreich Israel im 8. Jahrhundert v. Chr., kurz vor dessen Untergang. Ephraim ist ein anderer Name für das Nordreich.",
    focus="Achte darauf, wo die Rede des Volkes endet und Gottes Antwort beginnt.",
    quiz=[
        choice("Womit vergleicht Gott die Frömmigkeit des Volkes?", ["Mit einer Morgenwolke und dem Tau, der früh verschwindet", "Mit einem Baum am Wasser", "Mit einem Feuer, das ausgeht", "Mit einem Haus ohne Fundament"], 4, "Lies Vers 4.",
               "V. 4: Morgenwolke und Tau – beides ist da und schnell wieder weg."),
        choice("Woran hat Gott laut V. 6 Gefallen?", ["An Treue und Erkenntnis Gottes mehr als an Opfern", "An vielen Brandopfern", "An langen Gebeten", "An festlichen Liedern"], 6, "Lies Vers 6.",
               "V. 6: an Treue (Frömmigkeit) und Erkenntnis Gottes."),
    ],
    explain=[
        E("Was heißt hier „Frömmigkeit“?", "Im Hebräischen steht chesed: Treue, Güte, Verlässlichkeit in einer Beziehung. Andere Übersetzungen haben „Liebe“ oder „Barmherzigkeit“.", translation="elbbk"),
        E("Ist die Umkehr in V. 1–3 echt?", "Ausleger sind sich nicht einig. Viele lesen V. 4 als Gottes Antwort, die zeigt: Das Lied klang gut, hielt aber nicht. Andere verstehen V. 1–3 als Einladung des Propheten selbst."),
        E("Der „dritte Tag“ in V. 2?", "Christliche Ausleger haben den Vers seit der Alten Kirche auf die Auferstehung Jesu am dritten Tag bezogen. Im Zusammenhang geht es zunächst um die baldige Wiederherstellung des Volkes."),
    ],
    cards=["chesed"],
    fact="Jesus zitiert V. 6 bei Matthäus zweimal: als man ihm vorwirft, mit Sündern zu essen (Mt 9,13), und im Streit um den Sabbat (Mt 12,7).",
    memory_verse=MV(R(HOS, 6, 6), "Denn an Frömmigkeit habe ich Gefallen und nicht am Schlachtopfer"),
    teaser="Ein Volk fastet und beschwert sich, dass Gott es nicht bemerkt.")

sec("wichtig", [R(JES, 58, 3, 11)], "Ein Fasten, das Gott gefällt",
    "Das Volk fragt: Warum fasten wir, und du siehst es nicht? Gott antwortet: Am Fasttag treibt ihr eure Arbeiter an und streitet. Das Fasten, das ich will: Fesseln lösen, Brot teilen, Obdachlose aufnehmen.",
    bridge="Dieser Teil des Jesajabuches richtet sich an das Volk nach der Rückkehr aus dem Exil, als man die Gottesdienste wieder aufnahm.",
    quiz=[
        choice("Was tun die Leute an ihrem Fasttag?", ["Sie gehen ihren Geschäften nach und treiben ihre Arbeiter an", "Sie beten den ganzen Tag", "Sie geben den Armen ihr Essen", "Sie bleiben zu Hause"], 3, "Lies Vers 3–4.",
               "V. 3–4: Geschäfte, Druck auf die Arbeiter, Streit und Zank."),
        order("Was nennt Gott als Fasten, das ihm gefällt? In der Reihenfolge von V. 6–7:",
              ["Fesseln der Bosheit lösen", "Unterdrückte freilassen", "Brot mit Hungrigen teilen", "Obdachlose aufnehmen", "Nackte kleiden"],
              "V. 6–7: Jede Zeile betrifft andere Menschen."),
        choice("Was verspricht Gott laut V. 9?", ["Wenn du rufst, wird der HERR antworten", "Du wirst reich werden", "Deine Feinde werden fliehen", "Du wirst nie mehr fasten müssen"], 9, "Lies Vers 9.",
               "V. 9: Du rufst – und er sagt: Hier bin ich."),
    ],
    explain=[
        E("Lehnt Gott das Fasten ab?", "Der Text sagt es nicht. Er fragt, welches Fasten Gott gefällt, und beschreibt es neu. Die meisten Ausleger lesen das nicht als Absage an das Fasten selbst, sondern an Fasten ohne Gerechtigkeit."),
        E("Wie fasten Christen heute?", "Orthodoxe Christen fasten an vielen Tagen im Jahr, besonders mittwochs und freitags. Katholiken kennen Aschermittwoch und Karfreitag als Fasttage und die Fastenzeit vor Ostern. In Freikirchen ist Fasten meist freiwillig und persönlich, oft verbunden mit besonderem Gebet."),
        E("„Dich deinem Fleisch nicht entziehen“?", "Gemeint sind die eigenen Verwandten, die eigenen Leute (V. 7) – die man nicht im Stich lassen soll."),
    ],
    cards=["fasten"],
    teaser="Weisheit, Stärke, Reichtum – worauf darf man stolz sein?")

sec("wichtig", [R(JER, 9, 22, 23), R(KOR1, 1, 26, 31)], "Worauf man stolz sein kann",
    "Jeremia: Der Weise rühme sich nicht seiner Weisheit, der Starke nicht seiner Stärke, der Reiche nicht seines Reichtums – sondern dass er Gott kennt. Paulus erinnert die Korinther daran, wer sie waren, als Gott sie rief.",
    bridge="Jeremia sprach in Jerusalem kurz vor der Eroberung durch Babylon. Über 600 Jahre später greift Paulus seine Worte in einem Brief nach Korinth auf.",
    quiz=[
        choice("Wessen soll man sich laut Jeremia rühmen?", ["Dass man Gott kennt und versteht", "Seiner Weisheit", "Seiner Stärke", "Seines Reichtums"], 23, "Lies Jer 9,23.",
               "Jer 9,23: Einsicht zu haben und Gott zu erkennen."),
        choice("Was übt Gott laut Jer 9,23 auf der Erde – und daran hat er Gefallen?", ["Güte, Recht und Gerechtigkeit", "Macht, Ehre und Herrschaft", "Gericht, Zorn und Strafe", "Weisheit, Reichtum und Stärke"], 23, "Lies Jer 9,23.",
               "Jer 9,23: Güte (chesed), Recht und Gerechtigkeit."),
        tf("Paulus sagt, in Korinth seien nicht viele Weise, Mächtige und Vornehme berufen worden.", True, 26, "Lies 1Kor 1,26.",
           "1Kor 1,26: nicht viele – und Gott hat das Schwache erwählt (V. 27)."),
    ],
    explain=[
        E("Was heißt „sich rühmen“?", "Sich auf etwas berufen, worauf man stolz ist und worauf man sich verlässt. Paulus fasst Jer 9,22–23 in einem Satz zusammen (1Kor 1,31)."),
        E("Warum gerade Korinth?", "Korinth war eine reiche Handelsstadt, in der Bildung und Redekunst viel galten. In der Gemeinde stritten Gruppen darüber, wer der bessere Lehrer sei (1Kor 1,10–17)."),
    ],
    place="korinth",
    teaser="„Wenn ihr mich liebt …“ – Jesus verbindet zwei Dinge, die viele lieber getrennt hätten.")

sec("wichtig", [R(JOH, 14, 15, 24)], "Lieben und Halten",
    "Jesus sagt: Wenn ihr mich liebt, haltet meine Gebote. Er verspricht einen anderen Beistand, den Geist der Wahrheit. Wer ihn liebt, bei dem werden er und der Vater Wohnung nehmen.",
    bridge="Noch einmal beim letzten Abend. Jesus hat angekündigt, dass er weggeht, und die Jünger sind verunsichert (Joh 14,1–14).",
    place="jerusalem",
    quiz=[
        choice("Was verspricht Jesus in V. 16?", ["Einen anderen Beistand, der für immer bei ihnen bleibt", "Dass er bald nach Galiläa zurückkehrt", "Dass sie nicht leiden werden", "Dass sie Wunder tun werden"], 16, "Lies Vers 16–17.",
               "V. 16–17: einen anderen Beistand, den Geist der Wahrheit."),
        who("Herr, wie ist es, dass du dich uns offenbar machen willst und nicht der Welt?", R(JOH, 14, 22), ["Judas, nicht der Iskariot", "Petrus", "Thomas", "Philippus"],
            "V. 22: Ein anderer Judas aus dem Kreis der Zwölf fragt."),
        choice("Was geschieht laut V. 23 bei dem, der Jesus liebt und sein Wort hält?", ["Vater und Sohn kommen und nehmen Wohnung bei ihm", "Er wird nie mehr traurig sein", "Er bekommt einen Platz im Tempel", "Er muss nicht mehr beten"], 23, "Lies Vers 23.",
               "V. 23: Wir werden zu ihm kommen und Wohnung bei ihm machen."),
    ],
    explain=[
        E("Was ist ein „Sachwalter“?", "Griechisch parakletos: einer, der herbeigerufen wird, um beizustehen – Anwalt, Tröster, Helfer. Andere Übersetzungen haben „Tröster“ oder „Beistand“.", translation="elbbk"),
        E("Ist Gehorsam die Bedingung für Gottes Liebe?", "Der Text verbindet Lieben und Halten sehr eng (V. 15, 21, 23–24). Lutherische Ausleger betonen, dass Gottes Liebe zuerst kommt und das Halten folgt (vgl. 1Joh 4,19). Andere Traditionen betonen stärker, dass Liebe sich im Tun bewährt. Beide berufen sich auf diesen Text."),
    ],
    teaser="Eine Frau betet so leidenschaftlich, dass der Priester sie für betrunken hält.")

# ───────────────────────── 3 · Mit Gott reden ─────────────────────────
sec("reden", [R(SAM1, 1, 9, 18)], "Hanna betet",
    "Hanna ist kinderlos und gekränkt. Im Heiligtum von Silo betet sie weinend und leise; nur ihre Lippen bewegen sich. Der Priester Eli hält sie für betrunken. Sie sagt: Ich habe meine Seele vor dem HERRN ausgeschüttet.",
    bridge="Neue Etappe: Mit Gott reden. Die Geschichte spielt in der Zeit der Richter. Hannas Mann Elkana hat eine zweite Frau, Peninna, die Kinder hat und Hanna jedes Jahr kränkt (1Sam 1,1–8).",
    place="silo",
    quiz=[
        choice("Warum hält Eli Hanna für betrunken?", ["Weil sich nur ihre Lippen bewegen und man ihre Stimme nicht hört", "Weil sie laut schreit", "Weil sie Wein dabei hat", "Weil sie auf dem Boden liegt"], 13, "Lies Vers 12–13.",
               "V. 13: Sie redet in ihrem Herzen. Laut zu beten war damals üblich."),
        choice("Was verspricht Hanna Gott?", ["Den Sohn dem HERRN zu geben für sein ganzes Leben", "Jedes Jahr ein Opfer zu bringen", "Nie mehr zu klagen", "Den Tempel zu schmücken"], 11, "Lies Vers 11.",
               "V. 11: Er soll Gott gehören, und kein Schermesser soll auf sein Haupt kommen."),
        tf("Nach dem Gespräch mit Eli ist Hannas Gesicht nicht mehr dasselbe.", True, 18, "Lies Vers 18.",
           "V. 18: Sie isst wieder, und ihr Gesicht ist verändert – bevor sich an ihrer Lage etwas geändert hat."),
    ],
    explain=[
        E("Was heißt „kein Schermesser“?", "Ein Zeichen des Nasiräergelübdes (4Mo 6,1–21): Wer Gott besonders geweiht war, ließ sein Haar wachsen. Simson war ebenfalls Nasiräer (Ri 13,5)."),
        E("Was ist eine „Tochter Belials“?", "„Belial“ bedeutet etwa Nichtsnutz, Verderben. Hanna will nicht für eine nichtswürdige Frau gehalten werden.", translation="elbbk"),
        E("Wo lag Silo?", "Im Bergland nördlich von Jerusalem. Dort stand damals die Bundeslade, bevor Jerusalem zum Zentrum wurde."),
    ],
    cards=["hanna"],
    fact="Der Talmud (Berachot 31a) leitet aus Hannas Gebet Regeln für das Beten ab: mit Hingabe, mit bewegten Lippen und ohne die Stimme laut zu erheben.",
    teaser="Ein Psalm, der zweimal fast denselben Satz sagt – mit einem kleinen Unterschied.")

sec("reden", [R(PS, 62, 2, 9)], "Schüttet euer Herz aus",
    "Der Beter wird von Gegnern bedrängt. Zweimal sagt er: Nur bei Gott ist meine Seele still, er ist mein Fels. Am Ende ruft er alle auf: Vertraut ihm, schüttet euer Herz vor ihm aus.",
    focus="Vergleiche V. 2 und V. 6 – und V. 3 und V. 7.",
    quiz=[
        choice("Welcher Unterschied besteht zwischen V. 3 und V. 7?", ["In V. 3 heißt es „nicht viel wanken“, in V. 7 „nicht wanken“", "In V. 7 fehlt das Wort „Fels“", "V. 7 spricht von Feinden, V. 3 nicht", "Es gibt keinen Unterschied"], 7, "Lies V. 3 und V. 7 nebeneinander.",
               "V. 3: nicht viel wanken – V. 7: nicht wanken. Ein kleines Wort fällt weg."),
        choice("Wozu fordert der Beter das Volk in V. 9 auf?", ["Vertraut auf Gott und schüttet euer Herz vor ihm aus", "Bringt mehr Opfer", "Kämpft gegen die Feinde", "Schweigt vor Gott"], 9, "Lies Vers 9.",
               "V. 9: Vertrauen und ausschütten – beides in einem Satz."),
    ],
    explain=[
        E("Was beschreiben V. 4–5?", "Gegner, die einen Menschen umstoßen wollen wie eine schiefe Mauer – freundlich im Reden, feindlich im Herzen. Der Psalm sagt nicht, wer sie waren."),
        E("Was heißt „Sela“?", "Ein Wort, dessen Bedeutung unsicher ist, wahrscheinlich eine musikalische Anweisung, etwa eine Pause."),
    ],
    memory_verse=MV(R(PS, 62, 9), "Vertraut auf ihn allezeit, o Volk! Schüttet vor ihm aus euer Herz!"),
    teaser="Bevor Jesus das bekannteste Gebet der Welt lehrt, sagt er, wie man nicht beten soll.")

sec("reden", [R(MT, 6, 5, 15)], "Das Vaterunser",
    "Jesus warnt davor, zu beten, um gesehen zu werden, und davor, viele Worte zu machen. Euer Vater weiß, was ihr braucht. Dann lehrt er das Vaterunser und betont am Ende die Vergebung.",
    bridge="Mitten in der Bergpredigt spricht Jesus über Geben, Beten und Fasten – alles drei ohne Publikum (Mt 6,1–18).",
    quiz=[
        choice("Wo soll man laut V. 6 beten?", ["In der Kammer, bei geschlossener Tür", "An den Straßenecken", "Nur im Tempel", "Unter freiem Himmel"], 6, "Lies Vers 6.",
               "V. 6: in der Kammer, zum Vater, der im Verborgenen ist."),
        tf("Jesus sagt, man müsse Gott ausführlich erklären, was man braucht.", False, 8, "Lies Vers 7–8.",
           "V. 8: Euer Vater weiß, was ihr bedürft, ehe ihr ihn bittet."),
        order("Bring die Bitten des Vaterunsers in die Reihenfolge von Matthäus.",
              ["Dein Name werde geheiligt", "Dein Reich komme", "Dein Wille geschehe", "Gib uns unser Brot", "Vergib uns unsere Schuld"],
              "V. 9–12: erst drei Bitten über Gott, dann Bitten für uns."),
    ],
    explain=[
        E("Heißt das: nie öffentlich beten?", "Die meisten Ausleger sagen nein. Jesus selbst betet öffentlich (Joh 11,41–42), und die Gemeinde betet gemeinsam (Apg 4,24). Es geht um das Motiv: gesehen werden (V. 5)."),
        E("Wo ist der Schluss „Denn dein ist das Reich …“?", "Er fehlt in den ältesten Handschriften von Matthäus, wurde aber schon früh im Gottesdienst angefügt. Katholiken sprechen ihn in der Messe etwas abgesetzt, evangelische und freikirchliche Gemeinden meist direkt dazu."),
        E("Feste Gebete oder freie Worte?", "Katholische, orthodoxe und viele evangelische Christen beten das Vaterunser wörtlich, oft täglich. In vielen Freikirchen ist freies Gebet üblicher, und das Vaterunser gilt auch als Muster. Beide berufen sich auf V. 9."),
    ],
    cards=["vaterunser"],
    teaser="Es ist Mitternacht, ein Gast steht vor der Tür, und im Haus ist kein Brot.")

sec("reden", [R(LK, 11, 5, 13)], "Der Freund um Mitternacht",
    "Jesus erzählt von einem Mann, der um Mitternacht beim Nachbarn Brot leihen will. Der steht schließlich auf – nicht aus Freundschaft, sondern weil der andere nicht lockerlässt. Bittet, sucht, klopft an.",
    bridge="Bei Lukas haben die Jünger Jesus gerade gebeten: Herr, lehre uns beten. Er hat ihnen eine kürzere Fassung des Vaterunsers gegeben (Lk 11,1–4).",
    quiz=[
        choice("Warum steht der Nachbar laut V. 8 schließlich auf?", ["Wegen der Unverschämtheit des Bittenden", "Weil er sein Freund ist", "Weil die Kinder wach geworden sind", "Weil er Angst vor Ärger hat"], 8, "Lies Vers 8.",
               "V. 8: nicht weil er sein Freund ist, sondern um seiner Unverschämtheit willen."),
        order("Welche drei Verben stehen in V. 9?", ["Bittet", "Sucht", "Klopft an"],
              "V. 9: bitten, suchen, anklopfen – und V. 10 wiederholt alle drei."),
        choice("Was gibt der Vater im Himmel laut V. 13 denen, die ihn bitten?", ["Den Heiligen Geist", "Alles, was sie wollen", "Reichtum", "Ein langes Leben"], 13, "Lies Vers 13.",
               "V. 13: Bei Matthäus heißt es an dieser Stelle „Gutes“ (Mt 7,11), bei Lukas „den Heiligen Geist“."),
    ],
    explain=[
        E("„Unverschämtheit“?", "Das griechische Wort anaideia heißt Schamlosigkeit, Hartnäckigkeit. Manche Ausleger beziehen es auf den Nachbarn: Er will nicht als jemand dastehen, der einem Gast nicht hilft – Gastfreundschaft war eine Frage der Ehre des ganzen Dorfes."),
        E("Bekommt man alles, worum man bittet?", "V. 11–13 vergleicht Gott mit einem Vater, der keine schlechten Dinge gibt. Christen haben dazu verschiedene Erfahrungen und Antworten. Jesus selbst bittet in Gethsemane um etwas, das nicht geschieht (Lk 22,42)."),
    ],
    fact="Gastfreundschaft war im Orient so wichtig, dass ein Gast, der nachts ankam, versorgt werden musste – notfalls mit Brot aus dem ganzen Dorf. Gebacken wurde meist am Morgen für den Tag.",
    teaser="Ein hoher Beamter erfährt, dass Beten ab sofort verboten ist. Er geht nach Hause und öffnet die Fenster.")

# ───────────────────────── 4 · Im Alltag ─────────────────────────
sec("alltag", [R(DAN, 6, 1, 11)], "Dreimal am Tag",
    "Daniel ist einer der drei obersten Beamten im Perserreich und so zuverlässig, dass seine Neider nichts gegen ihn finden – außer seinem Glauben. Sie lassen ein Gebetsverbot erlassen. Daniel betet weiter, wie er es immer getan hat.",
    bridge="Neue Etappe: Im Alltag. Daniel kam als junger Mann nach Babylon (Dan 1). Inzwischen ist er alt, und das babylonische Reich ist an die Meder und Perser gefallen.",
    place="babylon",
    focus="Achte auf die letzten Worte von Vers 11.",
    quiz=[
        choice("Warum finden die Neider keinen Anklagegrund in Daniels Arbeit?", ["Weil er treu war und kein Vergehen an ihm gefunden wurde", "Weil der König ihn schützte", "Weil er kaum Aufgaben hatte", "Weil sie Angst vor ihm hatten"], 5, "Lies Vers 5.",
               "V. 5: Er war treu – sie finden nichts."),
        estimate("Wie oft am Tag betet Daniel?", 1, 10, 3, "Mal", "V. 11: dreimal am Tag, auf den Knien, mit offenen Fenstern nach Jerusalem.", 11, "Lies Vers 11."),
        tf("Daniel beginnt erst wegen des Verbots, öffentlich zu beten.", False, 11, "Lies das Ende von Vers 11.",
           "V. 11: wie er es vorher getan hatte. Er ändert nichts."),
    ],
    explain=[
        E("Warum nach Jerusalem?", "Salomo hatte bei der Tempelweihe gebetet: Wenn dein Volk in der Gefangenschaft zu diesem Haus hin betet, dann höre (1Kön 8,46–49). Auch heute beten Juden in Richtung Jerusalem."),
        E("Wer war Darius der Meder?", "Er ist außerhalb der Bibel nicht eindeutig belegt. Ausleger denken an einen Statthalter unter Kyrus, an einen Thronnamen des Kyrus selbst oder an einen anderen Herrscher."),
        E("Was sind Satrapen?", "Statthalter der Provinzen im Perserreich."),
    ],
    cards=["daniel", "gebetszeiten"],
    teaser="Ein Psalm, der beschreibt, wie es ist, wenn jemand dich ganz genau kennt.")

sec("alltag", [R(PS, 139, 1, 12)], "Du kennst mich",
    "David staunt: Gott kennt sein Sitzen und Aufstehen, seine Gedanken und Wege, jedes Wort, bevor er es sagt. Wohin er auch ginge – Himmel, Totenreich, Meer, Dunkelheit –, Gott wäre da.",
    quiz=[
        choice("Was weiß Gott laut V. 4?", ["Das Wort, bevor es auf der Zunge ist", "Wie lange der Beter leben wird", "Wer seine Feinde sind", "Wann er sterben wird"], 4, "Lies Vers 4.",
               "V. 4: Das Wort ist noch nicht auf meiner Zunge – und du weißt es schon."),
        order("Wohin könnte der Beter fliehen? In der Reihenfolge von V. 8–9:", ["Zum Himmel", "In den Scheol", "Zu den Flügeln der Morgenröte", "Ans äußerste Ende des Meeres"],
              "V. 8–9: oben, unten, Osten, Westen – überall ist Gott da."),
        tf("Für Gott ist die Finsternis wie das Licht.", True, 12, "Lies Vers 12.",
           "V. 12: Die Nacht leuchtet wie der Tag."),
    ],
    explain=[
        E("Trost oder Bedrängnis?", "V. 5 klingt beides: Gott umgibt den Beter von hinten und vorn und legt seine Hand auf ihn. Manche Ausleger hören darin Schutz, andere das Gefühl, nicht entkommen zu können. Der Psalm selbst sagt in V. 6: zu wunderbar, zu hoch."),
        E("Was ist der Scheol?", "Hebräisch für das Totenreich, die Unterwelt.", translation="elbbk"),
    ],
    prayer={"ref": R(PS, 139, 23, 24), "source": "Psalm 139,23–24"},
    teaser="Ein Bibeltext, der dazu auffordert, gut zu essen und das Leben zu genießen.")

sec("alltag", [R(PRED, 9, 7, 10)], "Iss dein Brot mit Freude",
    "Der Prediger rät: Iss dein Brot mit Freude, trink deinen Wein mit frohem Herzen, genieße das Leben mit dem Menschen, den du liebst. Was du tun kannst, tu mit deiner Kraft – im Totenreich gibt es kein Tun mehr.",
    bridge="Das Buch Prediger fragt immer wieder, was im Leben bleibt. Direkt vor diesem Abschnitt stellt es fest, dass alle Menschen sterben, Gerechte wie Gottlose (Pred 9,1–6).",
    quiz=[
        choice("Was ist laut V. 7 der Grund, sein Brot mit Freude zu essen?", ["Gott hat längst Wohlgefallen an deinem Tun", "Morgen ist alles vorbei", "Es ist Festtag", "Man hat es sich verdient"], 7, "Lies Vers 7.",
               "V. 7: denn längst hat Gott Wohlgefallen an deinem Tun."),
        tf("Der Prediger nennt das Leben in V. 9 „eitel“.", True, 9, "Lies Vers 9.",
           "V. 9: alle Tage deines eitlen Lebens – und doch soll man es genießen."),
    ],
    explain=[
        E("Was heißt „eitel“?", "Hebräisch hebel: Hauch, Dunst, etwas Flüchtiges. Andere Übersetzungen haben „vergänglich“ oder „flüchtig“. Gemeint ist eher Vergänglichkeit als Sinnlosigkeit.", translation="elbbk"),
        E("Weiße Kleider und Öl?", "Zeichen für Festtage und Wohlbefinden – im Gegensatz zu Trauerkleidung und ungesalbtem Haar (vgl. 2Sam 14,2)."),
        E("Wie lesen Christen den Prediger?", "Sehr verschieden: Manche lesen das Buch als Darstellung eines Lebens ohne Blick auf Gott, das am Ende zu Gott führt (12,13). Andere lesen gerade solche Stellen wie 9,7–10 als ernst gemeinten Rat: das gewöhnliche Leben als Gabe Gottes annehmen."),
    ],
    cards=["kohelet"],
    try_="Lies Prediger 2,24 und 3,12–13. Wie oft kehrt der Gedanke aus diesem Abschnitt im Buch wieder?",
    teaser="Zwei Schwestern, ein Gast, viel Arbeit – und eine Frage, die Jesus anders beantwortet als erwartet.")

sec("alltag", [R(LK, 10, 38, 42)], "Marta und Maria",
    "Jesus kehrt bei Marta ein. Ihre Schwester Maria setzt sich zu seinen Füßen und hört zu, während Marta mit der Bewirtung beschäftigt ist. Marta beschwert sich. Jesus antwortet: Du sorgst dich um vieles, eins aber ist nötig – Maria hat das gute Teil gewählt.",
    bridge="Jesus ist auf dem Weg nach Jerusalem. Direkt davor erzählt Lukas das Gleichnis vom barmherzigen Samariter (Lk 10,25–37).",
    place="betanien",
    quiz=[
        choice("Was tut Maria?", ["Sie sitzt zu Jesu Füßen und hört seinem Wort zu", "Sie bereitet das Essen vor", "Sie holt Wasser vom Brunnen", "Sie lädt die Nachbarn ein"], 39, "Lies Vers 39.",
               "V. 39: Sie setzt sich zu seinen Füßen und hört zu."),
        who("Herr, kümmert es dich nicht, dass meine Schwester mich allein gelassen hat zu dienen?", R(LK, 10, 40), ["Marta", "Maria", "Ein Jünger", "Eine Nachbarin"],
            "V. 40: Marta wendet sich nicht an Maria, sondern an Jesus."),
        tf("Jesus schickt Maria in die Küche, um Marta zu helfen.", False, 42, "Lies Vers 41–42.",
           "V. 42: Das gute Teil soll nicht von ihr genommen werden."),
    ],
    explain=[
        E("Was ist das Besondere an Marias Platz?", "Zu Füßen eines Lehrers zu sitzen war die Haltung eines Schülers (vgl. Apg 22,3: Paulus zu Füßen Gamaliels). Dass eine Frau diesen Platz einnimmt, war ungewöhnlich."),
        E("Ist Marta im Unrecht?", "Der Text tadelt nicht ihr Dienen, sondern nennt sie „besorgt und beunruhigt“ (V. 41). Wie man das gewichtet, ist alt umstritten: Die Kirchenväter sahen in den Schwestern zwei Lebensformen, das tätige und das betrachtende Leben, und gaben meist Maria den Vorzug. Meister Eckhart deutete um 1300 dagegen Marta als die Reifere, die Tun und Hören schon verbindet."),
        E("Was ist das „eine“?", "Jesus sagt es nicht ausdrücklich. Viele lesen es aus dem Zusammenhang: das Hören auf sein Wort (V. 39). Manche alte Handschriften lesen „weniges ist nötig oder nur eines“, was an die Mahlzeit denken lässt."),
    ],
    cards=["marta-maria"],
    prayer={"ref": R(PS, 27, 4), "source": "Psalm 27,4"},
    teaser="Ein Brief, der sagt: alles, was ihr tut – Reden und Arbeiten.")

sec("alltag", [R(KOL, 3, 12, 17)], "Alles im Namen Jesu",
    "Paulus beschreibt, was die Gemeinde „anziehen“ soll: Erbarmen, Güte, Demut, Milde, Geduld, Vergebung – und über allem die Liebe. Wort Christi, Lieder, Dankbarkeit. Und alles, was ihr tut, im Namen des Herrn Jesus.",
    bridge="Paulus schreibt aus der Haft an eine Gemeinde in Kolossä (heutige Türkei), die er wohl nie besucht hat. Kurz vorher spricht er davon, den alten Menschen abzulegen (Kol 3,5–11).",
    focus="Achte darauf, wie oft in diesen Versen von Dankbarkeit die Rede ist.",
    quiz=[
        choice("Was soll man laut V. 14 über alles andere „anziehen“?", ["Die Liebe", "Die Demut", "Die Geduld", "Den Glauben"], 14, "Lies Vers 14.",
               "V. 14: die Liebe, das Band der Vollkommenheit."),
        choice("Wodurch soll das Wort Christi laut V. 16 in der Gemeinde wohnen?", ["Durch gegenseitiges Lehren und Ermahnen und durch Lieder", "Durch tägliches Auswendiglernen", "Durch die Predigt der Ältesten", "Durch Fasten"], 16, "Lies Vers 16.",
               "V. 16: einander lehren und ermahnen, mit Psalmen, Lobgesängen und geistlichen Liedern."),
        tf("V. 17 bezieht „alles im Namen des Herrn“ nur auf Gebete und Gottesdienste.", False, 17, "Lies Vers 17.",
           "V. 17: alles, was ihr tut, im Wort oder im Werk."),
    ],
    explain=[
        E("Was heißt „im Namen“ tun?", "Im Auftrag und im Sinne von jemandem handeln, so dass es zu ihm passt. Wie man das im Alltag versteht, beschreiben Christen sehr verschieden – von Gebet vor der Arbeit bis zu einer Haltung, die alles umfasst."),
        E("Psalmen, Lobgesänge, geistliche Lieder?", "Ob das drei verschiedene Arten von Liedern sind oder drei Wörter für dasselbe, ist unsicher. Die frühen Gemeinden sangen jedenfalls Psalmen und eigene Lieder (vgl. Eph 5,19)."),
    ],
    teaser="„Wo ist nun dein Gott?“ – ein Mensch, der Durst hat und keine Antwort bekommt.")

# ───────────────────────── 5 · Wenn Gott fern scheint ─────────────────────────
sec("fern", [R(PS, 42, 1, 6)], "Wie ein Hirsch",
    "Der Beter dürstet nach Gott wie ein Hirsch nach Wasser. Tränen sind sein Brot, und man fragt ihn täglich: Wo ist dein Gott? Er erinnert sich an Feste im Haus Gottes und redet sich selbst zu: Harre auf Gott.",
    bridge="Neue Etappe: Wenn Gott fern scheint. Psalm 42 und 43 bilden wohl ursprünglich ein Lied – beide haben denselben Kehrvers.",
    quiz=[
        choice("Womit vergleicht sich der Beter?", ["Mit einem Hirsch, der nach Wasser lechzt", "Mit einem Baum am Wasser", "Mit einem Vogel ohne Nest", "Mit einem Schaf ohne Hirten"], 2, "Lies Vers 2.",
               "V. 2: wie ein Hirsch, der nach Wasserbächen lechzt."),
        choice("Mit wem redet der Beter in V. 6?", ["Mit seiner eigenen Seele", "Mit dem Volk", "Mit seinen Feinden", "Mit dem Priester"], 6, "Lies Vers 6.",
               "V. 6: Was beugst du dich nieder, meine Seele? Er spricht sich selbst an."),
        tf("Der Beter sagt, er habe früher nie Gottesdienste gefeiert.", False, 5, "Lies Vers 5.",
           "V. 5: Er erinnert sich, wie er mit der feiernden Menge zum Haus Gottes zog."),
    ],
    explain=[
        E("Was ist ein „Maskil“?", "Eine Psalmüberschrift, deren Bedeutung unsicher ist – vielleicht „Lehrgedicht“ oder ein kunstvolles Lied."),
        E("Wer sagt „Wo ist dein Gott?“", "Der Psalm nennt Spötter und Bedränger (V. 4.11). Die Frage kommt in der Bibel öfter vor (Ps 79,10; Joel 2,17) – als Spott über einen Gott, der scheinbar nicht hilft."),
    ],
    cards=["korachiter"],
    teaser="Tiefe ruft der Tiefe – und dann fragt der Beter Gott direkt: Warum hast du mich vergessen?")

sec("fern", [R(PS, 42, 7, 12)], "Tiefe ruft der Tiefe",
    "Der Beter ist fern, im Norden am Hermon. Wellen gehen über ihn hinweg. Er sagt zu Gott, seinem Fels: Warum hast du mich vergessen? Und noch einmal der Kehrvers: Harre auf Gott, ich werde ihn noch preisen.",
    place="hermon",
    quiz=[
        choice("Wo befindet sich der Beter laut V. 7?", ["Im Land des Jordan und des Hermon", "In Jerusalem", "In Babylon", "In Ägypten"], 7, "Lies Vers 7.",
               "V. 7: im Norden, an den Quellen des Jordan – weit weg vom Tempel."),
        tf("Mitten in der Klage steht ein Vers über Gottes Güte bei Tag und sein Lied bei Nacht.", True, 9, "Lies Vers 9.",
           "V. 9 – direkt gefolgt von der Frage: Warum hast du mich vergessen? (V. 10)."),
        error("Harre auf Gott, denn ich werde ihn [niemals] preisen.", "noch", 12,
              "V. 12: Ich werde ihn noch preisen – derselbe Kehrvers wie in V. 6."),
    ],
    explain=[
        E("„Tiefe ruft der Tiefe“?", "Ein Bild aus der Landschaft: Am Hermon stürzen Wasser in Kaskaden herab. Für den Beter wird daraus ein Bild der Überflutung – alle deine Wogen gehen über mich (V. 8)."),
        E("Endet der Psalm mit einer Lösung?", "Nein. Der Kehrvers kommt zurück (V. 12, dann noch einmal in Ps 43,5), aber die Lage ist unverändert. Ausleger sehen darin ein Gebet, das zwischen Klage und Hoffnung hin- und hergeht."),
    ],
    try_="Lies Psalm 43 direkt anschließend. Welcher Vers kommt dir bekannt vor?",
    teaser="Ein Mann beneidet Menschen, denen es ohne Gott gut geht – bis er in den Tempel geht.")

sec("fern", [R(PS, 73, 1, 3), R(PS, 73, 16, 28)], "Gott nahe zu sein",
    "Asaf gibt zu: Fast wäre ich gestrauchelt, denn ich beneidete die Gottlosen, denen es gut geht. Er versteht es nicht, bis er ins Heiligtum geht. Am Ende sagt er: Wen habe ich im Himmel? Gott nahe zu sein ist mir gut.",
    bridge="Zwischen V. 3 und V. 16 beschreibt Asaf ausführlich, wie gut es den Übermütigen geht und wie sinnlos ihm sein eigenes reines Leben vorkam (Ps 73,4–15).",
    focus="Achte auf den Wendepunkt in V. 17.",
    quiz=[
        choice("Was hätte Asaf fast zu Fall gebracht?", ["Der Neid auf das Wohlergehen der Gottlosen", "Eine schwere Krankheit", "Verfolgung durch den König", "Der Tod eines Freundes"], 3, "Lies Vers 2–3.",
               "V. 3: Er beneidete die Übermütigen."),
        choice("Wann ändert sich sein Blick?", ["Als er in die Heiligtümer Gottes hineingeht", "Als er krank wird", "Als ein Prophet ihn besucht", "Als die Gottlosen sterben"], 17, "Lies Vers 16–17.",
               "V. 17: bis ich hineinging in die Heiligtümer Gottes."),
        tf("Asaf beschreibt sich selbst in V. 22 als klug und weise.", False, 22, "Lies Vers 21–22.",
           "V. 22: dumm, ein Tier war ich bei dir – und doch: Ich bin stets bei dir (V. 23)."),
    ],
    explain=[
        E("Was ist im Heiligtum geschehen?", "Der Psalm erzählt es nicht. Er sagt nur, dass Asaf dort „das Ende“ der Gottlosen erkannte (V. 17). Ob er einen Gottesdienst erlebte, ein Wort hörte oder in der Stille nachdachte, bleibt offen."),
        E("„Nach der Herrlichkeit aufnehmen“ (V. 24)?", "Christliche Ausleger lesen den Vers oft als Hoffnung über den Tod hinaus. Viele jüdische Ausleger verstehen ihn als Ehre in diesem Leben. Der hebräische Text lässt beides zu."),
    ],
    cards=["asaf"],
    memory_verse=MV(R(PS, 73, 28), "Ich aber, Gott zu nahen ist mir gut"),
    teaser="Ein Weinstock wird geschnitten – auch die Reben, die Frucht bringen.")

sec("fern", [R(JOH, 15, 1, 8)], "Bleibt in mir",
    "Jesus sagt: Ich bin der wahre Weinstock, ihr seid die Reben. Der Vater schneidet die Reben, damit sie mehr Frucht bringen. Wer in mir bleibt, bringt viel Frucht; ohne mich könnt ihr nichts tun.",
    bridge="Zurück zum letzten Abend, unmittelbar vor den Worten über die Freundschaft, die am Anfang dieses Plans standen.",
    place="jerusalem",
    quiz=[
        choice("Was tut der Weingärtner mit Reben, die Frucht bringen?", ["Er reinigt sie, damit sie mehr Frucht bringen", "Er lässt sie in Ruhe", "Er schneidet sie ab", "Er pflanzt sie um"], 2, "Lies Vers 2.",
               "V. 2: Er reinigt (beschneidet) sie."),
        estimate("Wie oft kommt das Wort „bleiben“ in V. 4–7 vor?", 1, 12, 7, "Mal",
                 "V. 4–7: Je nach Zählung sechs- bis siebenmal (Elberfelder: 7) – das tragende Wort des Abschnitts.", 7, "Zähle in V. 4–7.", tol=1),
        tf("Laut V. 8 wird der Vater dadurch verherrlicht, dass die Jünger viel Frucht bringen.", True, 8, "Lies Vers 8.",
           "V. 8: Hierin wird mein Vater verherrlicht."),
    ],
    explain=[
        E("Was ist mit „Frucht“ gemeint?", "Jesus sagt es hier nicht ausdrücklich. Ausleger denken an Liebe (V. 12), an ein Leben, das Gottes Wesen zeigt (vgl. Gal 5,22), oder an Menschen, die zum Glauben kommen. Der Zusammenhang betont vor allem die Liebe."),
        E("Kann man herausfallen (V. 6)?", "Hier unterscheiden sich die Traditionen. Calvinistische Ausleger: Wer wirklich in Christus ist, bleibt bewahrt – V. 6 beschreibt die, die nur äußerlich dazugehörten. Arminianische und viele methodistische und pfingstliche Ausleger: Ein Glaubender kann sich wirklich abwenden. Katholische und lutherische Lehre rechnen ebenfalls damit, dass die Gnade verloren werden kann, und betonen, dass Umkehr möglich bleibt."),
    ],
    cards=["weinstock"],
    prayer={"text": "Mein Herr und mein Gott, nimm alles von mir, was mich hindert zu dir. Mein Herr und mein Gott, gib alles mir, was mich fördert zu dir. Mein Herr und mein Gott, nimm mich mir und gib mich ganz zu eigen dir.",
            "source": "Niklaus von Flüe (1417–1487)"},
    teaser="„Wir lieben, weil …“ – ein Brief, der Gottesliebe und Nächstenliebe nicht auseinanderhalten will.")

# ───────────────────────── 6 · Gott lieben – Menschen lieben ─────────────────────────
sec("lieben", [R(JOH1, 4, 7, 12), R(JOH1, 4, 16, 21)], "Weil er uns zuerst geliebt hat",
    "Johannes schreibt: Gott ist Liebe. Darin zeigt sie sich, dass Gott uns zuerst geliebt hat. Liebe vertreibt die Furcht. Und wer sagt, er liebe Gott, aber seinen Bruder hasst, ist ein Lügner.",
    bridge="Neue Etappe. Der erste Johannesbrief richtet sich an Gemeinden, in denen es Streit und Spaltung gab (1Joh 2,19).",
    focus="Achte darauf, wer in diesem Text zuerst liebt.",
    quiz=[
        choice("Worin zeigt sich laut 4,10 die Liebe?", ["Dass Gott uns geliebt und seinen Sohn gesandt hat", "Dass wir Gott geliebt haben", "Dass wir einander helfen", "Dass wir die Gebote halten"], 10, "Lies 4,9–10.",
               "4,10: nicht dass wir Gott geliebt haben, sondern dass er uns geliebt hat."),
        tf("Laut 4,18 gehören Liebe und Furcht zusammen.", False, 18, "Lies 4,18.",
           "4,18: Furcht ist nicht in der Liebe; die vollkommene Liebe treibt sie aus."),
        choice("Was fragt Johannes in 4,20?", ["Wie kann jemand Gott lieben, den er nicht sieht, wenn er den Bruder nicht liebt, den er sieht?", "Warum Gott unsichtbar ist", "Wer der Bruder ist", "Ob man Gott überhaupt lieben kann"], 20, "Lies 4,20.",
               "4,20: vom Sichtbaren zum Unsichtbaren."),
    ],
    explain=[
        E("Was ist eine „Sühnung“ (4,10)?", "Griechisch hilasmos: etwas, das Schuld bedeckt und Versöhnung schafft. Wie das genau zu verstehen ist, ist Thema im Plan „Warum das Kreuz?“."),
        E("Wer ist der „Bruder“?", "Im Brief zunächst die Glaubensgeschwister in der Gemeinde. Viele Ausleger beziehen es weiter auf jeden Mitmenschen (vgl. Lk 10,29–37)."),
    ],
    memory_verse=MV(R(JOH1, 4, 19), "Wir lieben, weil er uns zuerst geliebt hat."),
    teaser="Ein Gericht, bei dem beide Seiten überrascht sind.")

sec("lieben", [R(MT, 25, 31, 40)], "Das habt ihr mir getan",
    "Der Menschensohn kommt als König und scheidet alle Völker wie ein Hirte Schafe und Böcke. Zu denen zur Rechten sagt er: Ich war hungrig, durstig, fremd, nackt, krank, im Gefängnis – und ihr habt mir geholfen. Sie fragen erstaunt: Wann?",
    bridge="Die letzte große Rede Jesu bei Matthäus, kurz vor seinem Leiden, auf dem Ölberg (Mt 24,3). Sie endet mit diesem Bild vom Gericht.",
    place="oelberg",
    quiz=[
        order("Welche Nöte nennt der König? In der Reihenfolge von V. 35–36:", ["Hungrig", "Durstig", "Fremd", "Nackt", "Krank"],
              "V. 35–36: hungrig, durstig, fremd, nackt, krank – und im Gefängnis."),
        tf("Die Gerechten wissen genau, wann sie dem König geholfen haben.", False, 37, "Lies Vers 37–39.",
           "V. 37–39: Sie fragen: Wann haben wir dich gesehen?"),
        choice("Was antwortet der König in V. 40?", ["Was ihr einem der geringsten meiner Brüder getan habt, habt ihr mir getan", "Ihr habt es für euch selbst getan", "Ich habe euch dabei beobachtet", "Ihr habt es im Tempel getan"], 40, "Lies Vers 40.",
               "V. 40: einem der geringsten dieser meiner Brüder."),
    ],
    explain=[
        E("Wer sind „die geringsten Brüder“?", "Drei Hauptdeutungen: alle Notleidenden (heute die häufigste Lesart); die Jünger und Boten Jesu (vgl. Mt 10,40–42; 12,49–50), so viele ältere und manche heutige Ausleger; oder das jüdische Volk – so lesen es viele Dispensationalisten, die hier ein Gericht über die Völker nach der Trübsal sehen."),
        E("Wird man durch gute Taten gerettet?", "Katholische Ausleger sehen hier, dass Liebe und Werke zum Heil gehören. Evangelische Ausleger betonen, dass die Gerechten ihre Taten gar nicht berechnen (V. 37) – die Taten zeigen, wer zu Christus gehört. Beide lesen den Text als ernsten Maßstab."),
    ],
    teaser="Die andere Seite des Gerichts – und dieselbe Überraschung.")

sec("lieben", [R(MT, 25, 41, 46)], "Wann haben wir dich gesehen?",
    "Zu denen zur Linken sagt der König: Ich war in Not, und ihr habt mir nicht geholfen. Auch sie fragen: Wann haben wir dich gesehen? Die Antwort ist dieselbe – nur umgekehrt.",
    place="oelberg",
    quiz=[
        choice("Was fragen die zur Linken?", ["Wann haben wir dich in Not gesehen und dir nicht gedient?", "Warum hast du uns nicht gewarnt?", "Wer sind deine Brüder?", "Dürfen wir es noch einmal versuchen?"], 44, "Lies Vers 44.",
               "V. 44: dieselbe Frage wie die Gerechten in V. 37–39."),
        tf("Die zur Linken werden für böse Taten verurteilt, die sie begangen haben.", False, 45, "Lies Vers 42–45.",
           "V. 42–45: Es geht um das, was sie nicht getan haben."),
    ],
    explain=[
        E("„Ewiges Feuer“ und „ewige Pein“?", "Wie Christen das verstehen, ist unterschiedlich: als ewige Strafe (die verbreitetste Sicht), als endgültige Vernichtung oder – als Hoffnung, nicht als Lehre – als Strafe, die am Ende zur Versöhnung führt. Mehr dazu im Plan „Gericht und Hölle“."),
        E("Warum Schafe und Böcke?", "Schafe und Ziegen weideten oft gemeinsam und wurden abends getrennt. Das Bild vom Hirten, der seine Herde scheidet, kennt schon Hesekiel 34,17."),
    ],
    try_="Lies noch einmal Psalm 15 und Jesaja 58,6–7 vom Anfang dieses Plans. Welche Nöte aus Matthäus 25 tauchen dort schon auf?")

P.write()
