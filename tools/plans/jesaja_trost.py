#!/usr/bin/env python3
"""Source for the reading plan „Jesaja 40–55 – Tröstet mein Volk“ (generates assets/plans/jesaja-trost.json).

python3 -I tools/plans/jesaja_trost.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/jesaja-trost.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

JES, PS = 23, 19

P = PlanBuilder(
    "jesaja-trost", "jt", "Jesaja 40–55", "Tröstet mein Volk",
    "Jerusalem liegt in Trümmern, ein großer Teil des Volkes lebt verschleppt in Babylon, und viele fragen, ob Gott sie vergessen hat. "
    "In diese Lage hinein sprechen Jesaja 40–55: von einem Weg durch die Wüste, von selbstgemachten Göttern, von einem Perserkönig mit Namen Kyrus "
    "und von einem rätselhaften Knecht Gottes. 26 Abschnitte durch einen der meistzitierten Texte des Alten Testaments.",
    "hoffnung",
    stages=[("trost", "Tröstet mein Volk"), ("neues", "Der Knecht und das Neue"), ("kyrus", "Kyrus und der Fall Babels"),
            ("knecht", "Zion und der Knecht"), ("wasser", "Kommt zu den Wassern")],
    cards=[
        ("jesaja", "person", "Jesaja", "Prophet in Jerusalem, etwa 740–700 v. Chr., unter den Königen Usija, Jotam, Ahas und Hiskia (Jes 1,1). Sein Name bedeutet „der HERR ist Rettung“. Ab Kap. 40 ist Jerusalem zerstört und das Volk in Babel. Manche gläubige Leser verstehen das als Vorausschau Jesajas, andere, auch in den großen Kirchen, rechnen mit einem späteren Propheten in Jesajas Tradition.", "Jes 1,1; 6,1–8; 40,1"),
        ("verbannung", "ereignis", "Die Babylonische Verbannung", "Babylon eroberte Jerusalem 597 v. Chr. und zerstörte es 587/586 samt Tempel. Ein großer Teil der Oberschicht wurde nach Babylonien verschleppt (2Kön 24–25). Knapp 50 Jahre später, 539 v. Chr., nahm der Perserkönig Kyrus Babylon ein und erlaubte die Rückkehr (Esr 1). Jes 40–55 spricht in diese Lage hinein.", "2Kön 25; Ps 137; Esr 1"),
        ("zion", "ort", "Zion", "Ursprünglich die Burg der Jebusiter, die David eroberte (2Sam 5,7), dann der Tempelberg und schließlich ein Name für ganz Jerusalem. In Jes 40–55 wird Zion als Frau angesprochen: als Botin froher Botschaft (40,9), als verlassene Mutter (49,14), als Unfruchtbare und Witwe (54,1–6).", "Jes 40,9; 49,14; 52,1–2"),
        ("heiliger-israels", "begriff", "Der Heilige Israels", "Ein Gottestitel, der fast nur bei Jesaja vorkommt – etwa 25-mal, in allen Teilen des Buches, sonst nur selten. In Jes 6 hört Jesaja die Serafim dreimal „heilig“ rufen. Heilig heißt: abgesondert, ganz anders. Der Titel verbindet beides: den ganz anderen Gott und ein bestimmtes Volk.", "Jes 6,3; 41,14; 43,3"),
        ("jakob-israel", "person", "Jakob / Israel", "Jakob, Enkel Abrahams, bekam den Namen Israel (1Mo 32,29); seine zwölf Söhne gelten als Väter der Stämme. In Jes 40–55 stehen „Jakob“ und „Israel“ fast immer als Paar und meinen das ganze Volk. Dazu kommt der seltene Ehrenname Jeschurun (44,2).", "1Mo 32,29; Jes 41,8; 44,1–2"),
        ("gottesknecht", "begriff", "Der Gottesknecht", "Hebräisch ebed, Knecht oder Diener – auch ein Ehrentitel für Mose und David. In Jes 40–55 ist der Knecht zuerst das Volk Israel (41,8). In vier Liedern (42; 49; 50; 52–53) tritt ein Knecht mit eigenem Auftrag an Israel und an die Völker auf. Gelesen wird er als das Volk, als der Prophet oder als kommender Messias; das Neue Testament bezieht die Lieder auf Jesus.", "Jes 42,1–9; 49,1–7; 50,4–11; 52,13–53,12"),
        ("goel", "begriff", "Erlöser (go'el)", "Hebräisch go'el, „Löser“: der nahe Verwandte, der verkauftes Familienland zurückkauft oder einen in Schuldsklaverei Verkauften freikauft (3Mo 25,25.47–49; Rut 4). In Jes 40–55 nennt sich Gott immer wieder so: Er tritt für Israel ein wie ein Verwandter, der für die Seinen bezahlt.", "3Mo 25,25; Rut 4,1–10; Jes 41,14"),
        ("kyrus", "person", "Kyrus", "Kyrus II. (gest. 530 v. Chr.), König der Perser und Gründer des Perserreiches. 539 v. Chr. nahm er Babylon ein. Nach Esr 1,1–4 erlaubte er den Juden die Heimkehr und den Bau des Tempels. Jesaja nennt ihn Gottes Hirten und Gesalbten (44,28; 45,1). Die Elberfelder schreibt den Namen „Kores“, nach dem hebräischen Koresch.", "Jes 44,28; 45,1; Esr 1,1–4"),
        ("bel-nebo", "begriff", "Bel und Nebo", "Bel („Herr“) ist ein Titel Marduks, des Stadtgottes von Babylon; Nebo (Nabu) galt als sein Sohn, Gott der Schreiber und der Weisheit. Beim Neujahrsfest wurden ihre Bilder in Prozessionen getragen. Ihre Namen stecken in Königsnamen wie Nebukadnezar (Nabu-kudurri-usur) und Belsazar.", "Jes 46,1; Jer 50,2"),
        ("babel", "ort", "Babel", "Hauptstadt des neubabylonischen Reiches am Euphrat, unter Nebukadnezar II. (605–562 v. Chr.) eine der größten Städte der Welt, mit dem Ischtar-Tor und dem Stufenturm Etemenanki. Jes 47 nennt sie Herrin der Königreiche. 539 v. Chr. fiel sie an Kyrus. In der Offenbarung wird „Babylon“ zum Namen einer gottfeindlichen Macht (Offb 17–18).", "Jes 47; Offb 18"),
        ("rahab", "begriff", "Rahab, das Seeungeheuer", "Ein Ungeheuer der Urzeit, Bild für das tobende Meer, das Gott bezwingt (Hiob 26,12; Ps 89,11). Auch ein dichterischer Name für Ägypten (Ps 87,4; Jes 30,7). Im Hebräischen anders geschrieben als Rahab aus Jericho (Jos 2) – die beiden haben nichts miteinander zu tun.", "Jes 51,9; Ps 89,11"),
        ("freudenbote", "begriff", "Freudenbote", "Hebräisch mebasser: jemand, der eine gute Nachricht bringt, etwa die von einem Sieg (2Sam 18,19–27). Die griechische Übersetzung des Alten Testaments verwendet dafür das Verb euangelizesthai – daher kommt das Wort „Evangelium“. Paulus zitiert Jes 52,7 für die Verkündigung von Christus (Röm 10,15).", "Jes 40,9; 52,7; Röm 10,15"),
        ("jesajarolle", "begriff", "Die große Jesajarolle", "1947 in einer Höhle bei Qumran am Toten Meer gefunden, geschrieben wohl im 2. Jahrhundert v. Chr. Sie enthält alle 66 Kapitel – die einzige fast vollständige biblische Buchrolle unter den Qumranfunden – und ist rund 1000 Jahre älter als die zuvor ältesten bekannten hebräischen Jesaja-Handschriften. Heute im Israel-Museum in Jerusalem.", "Jes 1–66"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Tröstet mein Volk ─────────────────────────
sec("trost", [R(JES, 40, 1, 11)], "Tröstet mein Volk",
    "Gott gibt den Auftrag, Jerusalem zu trösten: Ihre Mühsal ist zu Ende, ihre Schuld abgetragen. Eine Stimme ruft, in der Wüste einen Weg für Gott zu bahnen; eine andere sagt, der Mensch vergeht wie Gras, Gottes Wort aber bleibt. Zion soll den Städten Judas ankündigen, dass Gott kommt – mit Kraft und wie ein Hirte, der die Lämmer trägt.",
    place="babylon",
    focus="Achte darauf, wie viele Stimmen in diesem Abschnitt rufen und sprechen.",
    quiz=[
        choice("Was soll man Jerusalem nach V. 2 zurufen?", ["Ihre Mühsal ist zu Ende und ihre Schuld abgetragen", "Ihre Mauern werden bald fallen", "Sie soll mehr Opfer bringen", "Sie soll nach Ägypten fliehen"], 2, "Lies Vers 2.",
               "V. 2: Ihre Mühsal ist vollendet, ihre Schuld ist abgetragen."),
        order("In welcher Reihenfolge sprechen die Stimmen?", ["Gott: Tröstet mein Volk", "Eine Stimme: Bahnt einen Weg in der Wüste", "Eine Stimme: Der Mensch ist wie Gras", "Zion: Seht, da ist euer Gott"],
              "V. 1, 3, 6–8 und 9: erst Gottes Auftrag, dann zwei rufende Stimmen, dann Zion als Botin.", "Lies Vers 1, 3, 6 und 9."),
        choice("Wie kommt Gott nach V. 11?", ["Wie ein Hirte, der die Lämmer im Arm trägt", "Wie ein König mit Wagen und Pferden", "Wie ein Sturm aus der Wüste", "Wie ein Richter mit der Waage"], 11, "Lies Vers 11.",
               "V. 11: Er weidet seine Herde wie ein Hirte, nimmt die Lämmer in den Arm und führt die Muttertiere sanft."),
    ],
    explain=[
        E("Warum klingt ab Kapitel 40 alles anders?", "Jes 1–39 spielt meist in der Zeit der Assyrer, um 700 v. Chr. Ab Kap. 40 ist Jerusalem zerstört und das Volk in Babel; Jesaja selbst wird nicht mehr genannt. Viele gläubige Leser sehen darin eine Vorausschau Jesajas über 150 Jahre hinweg. Viele Ausleger, auch katholische und evangelische, rechnen mit einem späteren Propheten, der in Jesajas Tradition in der Verbannung sprach. Die Frage ist umstritten."),
        E("Was heißt „Zweifaches empfangen“?", "Das hebräische Wort kann „doppelt“ heißen, aber auch „das genaue Gegenstück“, wie zwei Hälften eines gefalteten Blattes. Manche lesen: Jerusalem hat mehr als genug gelitten. Andere: Die Strafe entspricht genau der Schuld und ist nun ausgeglichen."),
        E("Wer ist die Stimme in der Wüste?", "Alle vier Evangelien beziehen V. 3 auf Johannes den Täufer (Mt 3,3; Mk 1,3; Lk 3,4–6; Joh 1,23). Sie folgen der griechischen Übersetzung, in der die Stimme in der Wüste ruft. Im Hebräischen gehört „in der Wüste“ eher zum Weg, der dort gebahnt werden soll."),
        E("Was ist ein „Gewandbausch“?", "Der Bausch ist der Stoff, der sich über dem Gürtel nach vorn wölbt. Hirten trugen darin neugeborene Lämmer, die noch nicht mit der Herde laufen konnten.", "elbbk"),
    ],
    cards=["jesaja", "verbannung", "zion"],
    fact="Der Sabbat nach dem jüdischen Trauertag Tischa beAv, an dem der Zerstörung des Tempels gedacht wird, heißt Schabbat Nachamu – nach dem ersten Wort von V. 1, „tröstet“. An ihm wird in der Synagoge Jes 40,1–26 gelesen.",
    memory_verse=MV(R(JES, 40, 8), "Das Gras ist verdorrt, die Blume ist abgefallen; aber das Wort unseres Gottes besteht in Ewigkeit."),
    teaser="Der nächste Abschnitt fragt, wer den Himmel ausgemessen hat – und nennt dafür ein Maß, das du an deiner eigenen Hand findest.")

sec("trost", [R(JES, 40, 12, 20)], "Wem wollt ihr Gott vergleichen?",
    "Wer hat das Wasser mit der hohlen Hand gemessen und die Berge gewogen? Niemand hat Gott beraten. Die Nationen sind vor ihm wie ein Tropfen am Eimer, und der ganze Libanon reicht nicht für ein Opfer. Dagegen ein Götterbild: gegossen, vergoldet oder aus Holz, das nicht fault, und so befestigt, dass es nicht wackelt.",
    quiz=[
        choice("Womit vergleicht V. 15 die Nationen?", ["Mit einem Tropfen am Eimer", "Mit den Sternen am Himmel", "Mit den Bäumen des Libanon", "Mit den Wellen im Meer"], 15, "Lies Vers 15.",
               "V. 15: wie ein Tropfen am Eimer und wie ein Sandkorn auf der Waagschale."),
        tf("Nach V. 16 reichen Holz und Wild des Libanon für ein angemessenes Opfer.", False, 16, "Lies Vers 16.",
           "V. 16: Der Libanon reicht nicht als Brennholz, sein Wild nicht als Brandopfer."),
        choice("Worauf achtet der Arme in V. 20 bei seinem Götterbild?", ["Dass das Holz nicht fault und das Bild nicht wackelt", "Dass es mit Gold überzogen ist", "Dass es größer ist als das des Nachbarn", "Dass ein Priester es segnet"], 20, "Lies Vers 20.",
               "V. 20: Er wählt Holz, das nicht fault, und einen geschickten Handwerker, damit das Bild nicht wackelt."),
    ],
    explain=[
        E("Was ist eine „Spanne“?", "Ein altes Längenmaß: der Abstand zwischen der Spitze des Daumens und der des kleinen Fingers bei gespreizter Hand, etwa 22 cm, eine halbe Elle."),
        E("Was sind die „Inseln“?", "Gemeint sind die Inseln und Küstenländer am Mittelmeer. Für Israel lagen sie am Rand der bekannten Welt; das Wort steht in Jes 40–55 oft für die fernsten Völker."),
        E("Warum der Spott über Götterbilder?", "In Babylon sahen die Verbannten prächtige Tempel und vergoldete Götterbilder, die in Prozessionen durch die Stadt getragen wurden. Jes 40–48 kommt immer wieder auf diese Bilder zurück und stellt sie dem Schöpfer gegenüber (40,19–20; 44,9–20; 46,1–7)."),
    ],
    cards=["heiliger-israels"],
    try_="Spreiz deine Hand und schau dir die Spanne vom Daumen bis zum kleinen Finger an. Lies dann V. 12 noch einmal.",
    teaser="Ein Volk sagt im nächsten Abschnitt: Gott sieht nicht mehr, was mit uns ist. Die Antwort beginnt mit dem Sternenhimmel.")

sec("trost", [R(JES, 40, 21, 31)], "Er wird nicht müde",
    "Gott thront über dem Kreis der Erde, spannt den Himmel aus wie ein Zelt, lässt Fürsten verdorren und ruft alle Sterne mit Namen. Israel klagt, sein Weg sei vor Gott verborgen. Die Antwort: Der ewige Gott wird nicht müde. Er gibt den Müden Kraft; selbst junge Männer stolpern, aber wer auf den HERRN harrt, steigt auf wie ein Adler.",
    focus="Achte auf die Klage in V. 27 – und darauf, womit die Antwort in V. 28 beginnt.",
    quiz=[
        who("Mein Weg ist verborgen vor dem HERRN", R(JES, 40, 27), ["Jakob / Israel", "Die Fürsten der Erde", "Die Tochter Babel", "Die Götzenmacher"],
            "V. 27: So spricht Jakob, so redet Israel – das Volk in der Verbannung fühlt sich von Gott übersehen."),
        choice("Was tut Gott nach V. 26 mit dem Heer der Sterne?", ["Er ruft sie alle mit Namen, keiner fehlt", "Er lässt sie verlöschen", "Er überlässt sie den Göttern Babels", "Er verhüllt sie mit Wolken"], 26, "Lies Vers 26.",
               "V. 26: Er führt ihr Heer nach der Zahl heraus und ruft sie alle mit Namen; keiner bleibt aus."),
        tf("Nach V. 30 werden selbst junge Männer müde.", True, 30, "Lies Vers 30.",
           "V. 30: Junge Leute werden müde und matt, junge Männer stürzen."),
    ],
    explain=[
        E("Was heißt „harren“?", "Hebräisch qawah: warten, gespannt hoffen. Das Wort wird mit dem hebräischen Wort für eine gespannte Schnur in Verbindung gebracht. Gemeint ist kein untätiges Abwarten, sondern ein Ausschauen nach jemandem."),
        E("Was ist ein „Flor“?", "Ein dünner, durchsichtiger Stoff, ein Schleier. Der Himmel wird wie ein feines Tuch oder ein Zeltdach über die Erde gespannt.", "elbbk"),
        E("Was ist der „Kreis der Erde“?", "Hebräisch chug, ein Kreis oder Gewölbe. Ob damit der runde Horizont, das Himmelsgewölbe oder eine Scheibe gemeint ist, wird verschieden gesehen. Die Bildsprache stammt aus der Weltsicht ihrer Zeit."),
        E("Adler oder Geier?", "Das hebräische nescher kann den Adler meinen, aber auch den Gänsegeier, der in Israel häufig ist. Beide segeln stundenlang in der aufsteigenden warmen Luft, fast ohne Flügelschlag."),
    ],
    memory_verse=MV(R(JES, 40, 31), "aber die auf den HERRN harren, gewinnen neue Kraft"),
    prayer={"ref": R(PS, 90, 2), "source": "Psalm 90,2"},
    teaser="Gott nennt sein Volk im nächsten Abschnitt mit einem Wort, das kaum jemand als Kompliment hören würde.")

sec("trost", [R(JES, 41, 8, 16)], "Fürchte dich nicht, du Wurm Jakob",
    "Gott spricht Israel als seinen Knecht an, als Nachkommen Abrahams, seines Freundes: Er hat es erwählt und nicht verworfen. Es soll sich nicht fürchten, denn Gott ist bei ihm und hält es. Die Gegner werden zu nichts. Der „Wurm Jakob“ wird zu einem scharfen Dreschschlitten, der Berge zermalmt.",
    quiz=[
        choice("Wie nennt Gott Abraham in V. 8?", ["Meinen Freund", "Meinen Erstgeborenen", "Meinen Propheten", "Meinen König"], 8, "Lies Vers 8.",
               "V. 8: Israel ist Nachkomme Abrahams, den Gott seinen Freund nennt."),
        estimate("Wie oft steht in V. 10–14 die Aufforderung, sich nicht zu fürchten?", 1, 6, 3, "mal",
                 "V. 10, 13 und 14: dreimal.", None, "Zähl in Vers 10–14."),
        error("Gott sagt: Ich habe dich zu einem scharfen, neuen [Schwert] gemacht; du wirst Berge dreschen.", "Dreschschlitten", 15,
              "V. 15: ein scharfer, neuer Dreschschlitten mit doppelten Schneiden."),
    ],
    explain=[
        E("Warum „Wurm“?", "Hebräisch tola'at, ein kleiner Wurm oder eine Made – ein Bild für Schwäche und Verachtung. Ps 22,7 und Hiob 25,6 benutzen es ebenso. In V. 14 steht daneben das „Häuflein“ Israel."),
        E("Was ist ein Dreschschlitten?", "Ein schweres Holzbrett, auf der Unterseite mit Steinen oder Eisen besetzt. Ochsen zogen es über das Getreide auf dem Dreschplatz, um die Körner aus den Ähren zu lösen."),
        E("Wer ist hier der Knecht?", "In V. 8–9 sagt der Text es ausdrücklich: Israel, Jakob. „Knecht“ heißt Diener eines Herrn oder Königs und war auch ein Ehrentitel, etwa für Mose und David."),
    ],
    cards=["jakob-israel", "goel"],
    fact="Abraham heißt auch in 2Chr 20,7 und Jak 2,23 „Freund Gottes“. Die Stadt Hebron, wo Abrahams Grab verehrt wird, heißt auf Arabisch bis heute al-Chalil – „der Freund“.",
    memory_verse=MV(R(JES, 41, 10), "fürchte dich nicht, denn ich bin mit dir"),
    teaser="Jetzt tritt ein Knecht auf, der so gar nichts von einem Dreschschlitten hat.")

# ───────────────────────── 2 · Der Knecht und das Neue ─────────────────────────
sec("neues", [R(JES, 42, 1, 9)], "Das geknickte Rohr",
    "Gott stellt seinen Knecht vor: Er trägt Gottes Geist und bringt den Nationen das Recht. Er schreit nicht, zerbricht das geknickte Rohr nicht und löscht den glimmenden Docht nicht aus, bis das Recht auf der Erde gegründet ist. Gott setzt ihn zum Bund für das Volk und zum Licht der Nationen, um Blinden die Augen zu öffnen und Gefangene zu befreien.",
    focus="Achte darauf, was der Knecht alles nicht tut.",
    quiz=[
        choice("Was tut der Knecht mit dem geknickten Rohr?", ["Er zerbricht es nicht", "Er richtet es wieder auf", "Er wirft es ins Feuer", "Er pflanzt es neu ein"], 3, "Lies Vers 3.",
               "V. 3: Das geknickte Rohr zerbricht er nicht, den glimmenden Docht löscht er nicht aus."),
        tf("Nach V. 4 wird der Knecht müde, bevor das Recht gegründet ist.", False, 4, "Lies Vers 4.",
           "V. 4: Er wird nicht ermatten und nicht zusammenbrechen, bis er das Recht auf der Erde gegründet hat."),
        choice("Wozu setzt Gott ihn nach V. 6–7?", ["Zum Licht der Nationen, um Blinde sehend zu machen und Gefangene zu befreien", "Zum König über Babel", "Zum Priester im neuen Tempel", "Zum Richter über die Götzenmacher"], 6, "Lies Vers 6–7.",
               "V. 6–7: zum Bund des Volkes und zum Licht der Nationen, um blinde Augen zu öffnen und Gefangene herauszuführen."),
    ],
    explain=[
        E("Wer ist dieser Knecht?", "In 41,8 war der Knecht Israel. Jüdische Ausleger wie Raschi lesen auch hier das Volk, andere den Propheten oder einen gerechten König; manche denken an Kyrus. Mt 12,18–21 zitiert V. 1–4 für Jesus, und die Himmelsstimme bei seiner Taufe erinnert an V. 1 (Mk 1,11). Diese Sicht teilen alle christlichen Kirchen."),
        E("Was ist ein „glimmender Docht“?", "Der Docht einer Öllampe aus Leinen, der nur noch glimmt und raucht und kurz vor dem Erlöschen ist. Das geknickte Rohr ist ein Schilfrohr, das schon beschädigt ist."),
        E("Was meint „Recht“?", "Hebräisch mischpat: nicht nur ein Gerichtsurteil, sondern eine gerechte Ordnung, in der jeder bekommt, was ihm zusteht. Das Wort kommt in V. 1–4 dreimal vor."),
    ],
    cards=["gottesknecht"],
    fact="Der Begriff „Gottesknechtslieder“ stammt von dem Theologen Bernhard Duhm. 1892 hob er vier Texte als eigene Gruppe heraus: 42,1–4, 49,1–6, 50,4–9 und 52,13–53,12. Wo die Lieder genau beginnen und enden, wird seither unterschiedlich gesehen.",
    teaser="Im selben Kapitel taucht noch ein Knecht auf. Er hat Augen und Ohren – und trotzdem ein Problem.")

sec("neues", [R(JES, 42, 18, 25)], "Blind und taub",
    "Gott ruft die Tauben und Blinden. Niemand ist so blind wie sein eigener Knecht: Er hat viel gesehen und nichts beachtet. Das Volk ist ausgeplündert und eingesperrt. Wer hat es den Räubern ausgeliefert? Der HERR selbst, weil sie nicht auf seinen Wegen gingen. Doch auch im Brand des Krieges haben sie es nicht zu Herzen genommen.",
    quiz=[
        choice("Wen nennt Gott in V. 19 blind?", ["Seinen Knecht und Boten", "Die Babylonier", "Die Götzenmacher", "Die Völker auf den Inseln"], 19, "Lies Vers 19.",
               "V. 19: Wer ist blind, wenn nicht mein Knecht, und taub wie mein Bote, den ich sende?"),
        choice("Wer hat Jakob nach V. 24 den Räubern ausgeliefert?", ["Der HERR", "Die Götter Babels", "Ägypten", "Niemand, es war Zufall"], 24, "Lies Vers 24.",
               "V. 24: der HERR, gegen den wir gesündigt haben – sie wollten nicht auf seinen Wegen gehen."),
        tf("Nach V. 25 hat das Volk aus dem Krieg seine Lehre gezogen.", False, 25, "Lies Vers 25.",
           "V. 25: Das Feuer brannte rings um ihn, aber er kam nicht zur Erkenntnis und nahm es nicht zu Herzen."),
    ],
    explain=[
        E("Zwei Knechte in einem Kapitel?", "Kap. 42 spricht zweimal von Gottes Knecht: von einem, der Blinden die Augen öffnet (V. 7), und von einem, der selbst blind ist (V. 19). Wie beide zusammenhängen, ist eine der Kernfragen dieser Kapitel; Ausleger beantworten sie verschieden."),
        E("Was meint V. 21?", "Gott wollte seine Weisung (hebräisch tora) groß und herrlich machen. Der Satz ist schwer zu übersetzen und wird verschieden verstanden. Im Zusammenhang steht er gegen V. 24: Das Volk hörte nicht auf diese Weisung."),
        E("Wer sagt „wir“ in V. 24?", "Mitten in der Gottesrede spricht plötzlich ein „Wir“, das sich zu den Schuldigen zählt – wohl der Prophet zusammen mit seinem Volk. Danach geht es wieder in der dritten Person weiter."),
    ],
    try_="Lies 42,7 und 42,19 direkt nacheinander. Was fällt dir auf?",
    teaser="Nach so einem Urteil erwartet man die Strafe. Das nächste Kapitel beginnt mit zwei Worten: Und nun …")

sec("neues", [R(JES, 43, 1, 7)], "Bei deinem Namen gerufen",
    "Gott, der Israel geschaffen hat, sagt: Fürchte dich nicht, ich habe dich erlöst und beim Namen gerufen, du gehörst mir. Durch Wasser und Feuer ist er dabei. Er gibt Ägypten und Kusch als Lösegeld, weil Israel in seinen Augen wertvoll ist, und holt seine Söhne und Töchter aus allen Himmelsrichtungen zurück.",
    quiz=[
        choice("Was sagt Gott für den Weg durch Wasser und Feuer zu?", ["Er ist dabei, und sie werden Israel nicht schaden", "Er wird Israel diesen Weg ersparen", "Er schickt einen Engel voraus", "Er trocknet alles Wasser aus"], 2, "Lies Vers 2.",
               "V. 2: Ich bin bei dir; die Ströme überfluten dich nicht, die Flamme verbrennt dich nicht."),
        order("In welcher Reihenfolge nennt Gott die Himmelsrichtungen?", ["Osten (Aufgang)", "Westen (Niedergang)", "Norden", "Süden"],
              "V. 5–6: vom Aufgang und vom Niedergang, dann zum Norden und zum Süden.", "Lies Vers 5–6."),
        tf("Nach V. 4 gibt Gott Menschen hin, weil Israel in seinen Augen wertvoll ist.", True, 4, "Lies Vers 4.",
           "V. 4: Weil du teuer und wertvoll bist in meinen Augen und ich dich lieb habe."),
    ],
    explain=[
        E("Was heißt „erlöst“?", "Das hebräische Verb ga'al gehört zum go'el, dem Verwandten, der einen verkauften Angehörigen freikauft (siehe Karte „Erlöser“). Hier ist das Verb in der Vergangenheit gesagt: Die Erlösung wird schon als geschehen angesprochen."),
        E("Ägypten als Lösegeld?", "Hebräisch kopher, der Preis, mit dem man ein Leben auslöst. Kusch (bei Elberfelder „Äthiopien“) ist das Land südlich von Ägypten, im heutigen Sudan; Seba lag wohl in derselben Gegend. Manche Ausleger denken an die Eroberung Ägyptens durch Kyrus’ Sohn Kambyses 525 v. Chr."),
        E("Was ist ein „Heiland“?", "Ein altes Wort für Retter. Hebräisch moschia, vom selben Wortstamm wie der Name Jesaja („der HERR ist Rettung“) und wie Jeschua, Jesus.", "elbbk"),
    ],
    memory_verse=MV(R(JES, 43, 1), "ich habe dich bei deinem Namen gerufen, du bist mein."),
    teaser="Gleich sagt Gott: Denkt nicht mehr an das Frühere. Gemeint ist das wichtigste Ereignis in Israels Geschichte.")

sec("neues", [R(JES, 43, 14, 25)], "Siehe, ich wirke Neues",
    "Um Israels willen schickt Gott gegen Babel. Er, der einst einen Weg durchs Meer bahnte und Wagen und Pferde versinken ließ, sagt: Denkt nicht an das Frühere – ich mache etwas Neues, einen Weg durch die Wüste. Doch Israel hat Gott nicht gesucht, sondern ihm mit seinen Sünden Mühe gemacht. Und Gott tilgt seine Übertretungen um seinetwillen.",
    focus="Achte auf das Wort „ermüden“ in V. 22–24. Wer ermüdet hier wen?",
    quiz=[
        choice("An welches frühere Ereignis erinnern V. 16–17?", ["An den Weg durchs Meer beim Auszug aus Ägypten", "An die Sintflut", "An den Turmbau zu Babel", "An die Eroberung Jerichos"], 16, "Lies Vers 16–17.",
               "V. 16–17: ein Weg im Meer, Wagen und Pferd, Heer und Held liegen da – Bilder vom Durchzug durchs Schilfmeer (2Mo 14)."),
        tf("Gott sagt in V. 23, er habe Israel mit Opfervorschriften ermüdet.", False, 23, "Lies Vers 23–24.",
           "V. 23–24: Er hat Israel nicht mit Opfern und Weihrauch ermüdet – Israel hat ihn mit seinen Sünden ermüdet."),
        choice("Warum tilgt Gott nach V. 25 die Übertretungen?", ["Um seinetwillen", "Weil Israel genug geopfert hat", "Weil Israel sich gebessert hat", "Weil Babel gefallen ist"], 25, "Lies Vers 25.",
               "V. 25: Ich, ich bin es, der deine Übertretungen tilgt um meinetwillen."),
    ],
    explain=[
        E("Wer sind die Chaldäer?", "Ein Volk im Süden Mesopotamiens. Die Königsfamilie Nebukadnezars stammte von ihnen ab; deshalb steht „Chaldäer“ in der Bibel oft für die Babylonier überhaupt."),
        E("Warum soll man das Frühere vergessen?", "V. 16–17 erinnern ausdrücklich an den Auszug aus Ägypten – und V. 18 sagt gleich danach, man solle nicht daran denken. Manche lesen: Das Neue wird so groß, dass es den alten Exodus übertrifft. Andere: Israel soll nicht nur in der Vergangenheit leben, sondern jetzt hinsehen (V. 19)."),
        E("Was ist „Würzrohr“?", "Kalmus, ein duftendes Schilfgewächs, das aus fernen Ländern teuer eingeführt wurde. Es gehörte zum heiligen Salböl (2Mo 30,23).", "elbbk"),
        E("Wer ist der „erste Vater“ (V. 27)?", "Meist wird an Jakob gedacht, dessen Lebensgeschichte voller List war; manche denken an Abraham oder an Adam."),
    ],
    try_="Lies 2Mo 14,21–28 und vergleiche mit Jes 43,16–17. Welche Wörter tauchen wieder auf?",
    teaser="Im nächsten Abschnitt schreiben sich Menschen etwas auf die Hand.")

sec("neues", [R(JES, 44, 1, 8)], "Wasser auf das Durstige",
    "Gott spricht Israel als Knecht und als Jeschurun an: Er gießt Wasser auf das durstige Land und seinen Geist auf Israels Nachkommen. Sie wachsen wie Weiden am Bach. Einer sagt, er gehöre dem HERRN, ein anderer schreibt es sich auf die Hand. Gott ist der Erste und der Letzte; einen anderen Fels gibt es nicht.",
    quiz=[
        choice("Was gießt Gott nach V. 3 auf die Nachkommen?", ["Seinen Geist und seinen Segen", "Öl und Wein", "Feuer vom Himmel", "Salz und Asche"], 3, "Lies Vers 3.",
               "V. 3: Ich gieße meinen Geist auf deine Nachkommen und meinen Segen auf deine Sprösslinge."),
        tf("Nach V. 5 schreibt sich jemand auf die Hand, dass er dem HERRN gehört.", True, 5, "Lies Vers 5.",
           "V. 5: Einer schreibt mit seiner Hand – oder auf seine Hand –, dass er dem HERRN gehört."),
        choice("Wie bezeichnet sich Gott in V. 6?", ["Als den Ersten und den Letzten", "Als den Gott der Berge", "Als den Jüngsten der Götter", "Als den König Babels"], 6, "Lies Vers 6.",
               "V. 6: Ich bin der Erste und der Letzte, und außer mir ist kein Gott."),
    ],
    explain=[
        E("Was heißt „Jeschurun“?", "Ein seltener Ehrenname für Israel, wohl abgeleitet von jaschar, „aufrecht, gerade“. Er kommt sonst nur im Lied und Segen des Mose vor (5Mo 32,15; 33,5.26)."),
        E("Auf die Hand schreiben?", "Der hebräische Satz lässt beides zu: Man schreibt mit der Hand, oder man schreibt auf die Hand. Im Alten Orient trugen Sklaven manchmal ein Zeichen ihres Besitzers. Ob hier an Tinte oder an ein dauerhaftes Zeichen gedacht ist, ist unklar; 3Mo 19,28 verbietet Tätowierungen."),
        E("Woher kommt „der Erste und der Letzte“?", "Jesaja benutzt den Ausdruck dreimal (41,4; 44,6; 48,12). Die Offenbarung greift ihn auf: Dort spricht ihn Christus (Offb 1,17; 2,8; 22,13)."),
    ],
    teaser="Der nächste Abschnitt ist eine der bissigsten Satiren der Bibel. Es geht um ein Stück Holz.")

sec("neues", [R(JES, 44, 9, 20)], "Die Hälfte im Feuer",
    "Wer Götterbilder macht, ist nichtig. Der Schmied arbeitet, bis er hungrig und müde wird; der Schnitzer formt ein Bild nach Menschengestalt. Aus demselben Baum heizt einer, backt Brot und brät Fleisch – und aus dem Rest macht er einen Gott, wirft sich davor nieder und bittet um Rettung. Keiner fragt sich: Soll ich ein Stück Holz anbeten?",
    quiz=[
        order("Was macht der Mann mit dem Holz?", ["Er fällt einen Baum", "Er wärmt sich und backt Brot", "Er brät Fleisch und wird satt", "Aus dem Rest macht er einen Gott"],
              "V. 14–17: Er haut Bäume ab, heizt und backt Brot, brät Fleisch und macht aus dem Übrigen einen Gott."),
        tf("Nach V. 12 wird selbst der Schmied, der den Gott herstellt, hungrig und müde.", True, 12, "Lies Vers 12.",
           "V. 12: Er wird hungrig und kraftlos, er hat kein Wasser getrunken und ermattet."),
        choice("Welche Frage stellt sich der Mann nach V. 19 nicht?", ["Ob er ein Stück Holz anbeten soll", "Ob das Holz trocken genug ist", "Ob der Schmied gut gearbeitet hat", "Ob das Brot gar ist"], 19, "Lies Vers 19.",
               "V. 19: Niemand nimmt es zu Herzen und sagt: Soll ich vor einem Holzklotz niederfallen?"),
    ],
    explain=[
        E("Ist das fair gegenüber Babylon?", "Babylonier hielten das Holz nicht selbst für den Gott. Sie glaubten, ein Gott nehme nach einem Weiheritual in seinem Bild Wohnung. Jesaja schreibt bewusst von außen, aus der Sicht dessen, der nur Holz und Gold sieht."),
        E("Was heißt „wer der Asche nachgeht“?", "Wörtlich etwa: wer sich von Asche nährt. Ein Bild für jemanden, der von etwas lebt, das nichts gibt – Asche ist das, was vom Brennholz übrig bleibt (V. 19)."),
        E("Welche Bäume sind gemeint?", "Zeder, Eiche und Steineiche sind recht sicher; bei anderen Namen raten die Übersetzungen. Elberfelder nennt eine Fichte, andere übersetzen Lorbeer oder Esche."),
    ],
    fact="Bei der babylonischen „Mundwaschung“, mit der ein neues Götterbild geweiht wurde, erklärten die Handwerker in einem Ritual, nicht sie hätten das Bild gemacht, sondern der Gott der Handwerker.",
    teaser="Der nächste Abschnitt endet mit einem Namen, den in einem Prophetenbuch niemand erwartet hätte.")

sec("neues", [R(JES, 44, 21, 28)], "Kores, mein Hirte",
    "Gott hat Israels Übertretungen weggewischt wie eine Wolke und ruft: Kehr um zu mir, ich habe dich erlöst. Himmel, Tiefen und Wälder sollen jubeln. Dann spricht der Schöpfer, der Wahrsager zu Narren macht: Jerusalem wird wieder bewohnt, Judas Städte werden aufgebaut – und Kores, den Gott seinen Hirten nennt, wird den Bau von Stadt und Tempel anordnen.",
    place="jerusalem",
    quiz=[
        choice("Womit vergleicht Gott in V. 22 das Tilgen der Sünden?", ["Mit Nebel und Wolken, die vergehen", "Mit Wasser, das abfließt", "Mit Schnee, der schmilzt", "Mit Spreu im Wind"], 22, "Lies Vers 22.",
               "V. 22: Ich habe deine Übertretungen getilgt wie Nebel und deine Sünden wie eine Wolke."),
        tf("In V. 22 ist die Reihenfolge: Erst soll Israel umkehren, dann wird Gott es erlösen.", False, 22, "Lies Vers 22 genau.",
           "V. 22: Kehr um zu mir, denn ich habe dich erlöst – die Erlösung wird als schon geschehen genannt, die Umkehr folgt."),
        error("Gott nennt Kores seinen [Feind], der all sein Wohlgefallen ausführt.", "Hirten", 28,
              "V. 28: Gott nennt Kores „mein Hirte“; er wird den Bau Jerusalems und des Tempels anordnen."),
    ],
    explain=[
        E("Wer ist Kores?", "Die Elberfelder gibt den hebräischen Namen Koresch als Kores wieder. Gemeint ist Kyrus II., der Perserkönig, der 539 v. Chr. Babylon einnahm (siehe Karte).", "elbbk"),
        E("Wie kann Jesaja Kyrus mit Namen nennen?", "Viele gläubige Leser sehen hier eine Vorhersage über rund 150 Jahre; der jüdische Geschichtsschreiber Josephus berichtet, Kyrus habe diese Stelle gelesen (Altertümer XI,1). Viele Ausleger, auch in den großen Kirchen, sehen hier einen Propheten, der zur Zeit des Kyrus spricht. Beide Gruppen lesen den Text als Gottes Wort."),
        E("Warum „Hirte“?", "Im Alten Orient war „Hirte“ ein üblicher Titel für Könige; auch David wird so genannt (2Sam 5,2). In 40,11 war Gott selbst der Hirte."),
    ],
    cards=["kyrus"],
    teaser="Im nächsten Abschnitt bekommt der persische König einen Titel, der sonst Israels Königen und Priestern vorbehalten ist.")

# ───────────────────────── 3 · Kyrus und der Fall Babels ─────────────────────────
sec("kyrus", [R(JES, 45, 1, 8)], "Ein Gesalbter, der Gott nicht kennt",
    "Gott spricht zu Kyrus, seinem Gesalbten: Er ergreift seine rechte Hand, öffnet ihm Tore, zerbricht kupferne Pforten und gibt ihm verborgene Schätze. Um Jakobs willen ruft er ihn beim Namen, obwohl Kyrus ihn nicht kennt. Er ist der HERR, außer ihm ist keiner – der Licht und Finsternis bildet, Frieden macht und Unheil schafft.",
    place="babylon",
    focus="Achte darauf, wie oft gesagt wird, dass Kyrus Gott nicht kennt.",
    quiz=[
        choice("Wie nennt Gott Kyrus in V. 1?", ["Seinen Gesalbten", "Seinen Sohn", "Seinen Propheten", "Seinen Feind"], 1, "Lies Vers 1.",
               "V. 1: So spricht der HERR zu seinem Gesalbten, zu Kyrus."),
        tf("Nach V. 4–5 kennt Kyrus den Gott Israels gut.", False, 4, "Lies Vers 4–5.",
           "V. 4 und 5: zweimal heißt es, du kanntest mich nicht."),
        choice("Um wessen willen ruft Gott Kyrus nach V. 4?", ["Um Jakobs, seines Knechtes, willen", "Um Babels willen", "Um des Perserreiches willen", "Um Kyrus’ eigenen Ruhmes willen"], 4, "Lies Vers 4.",
               "V. 4: um Jakobs, meines Knechtes, und Israels, meines Auserwählten, willen."),
    ],
    explain=[
        E("Was heißt „Gesalbter“?", "Hebräisch maschiach, daraus „Messias“, griechisch christos. Gesalbt wurden Könige und Priester Israels, als Zeichen, dass Gott sie einsetzt. Kyrus ist der einzige Nichtisraelit, den das Alte Testament so nennt."),
        E("Schafft Gott das Böse (V. 7)?", "Das hebräische ra' steht hier als Gegenstück zu „Frieden“ und meint Unheil, Unglück; ältere englische Übersetzungen sagen „evil“. Manche Ausleger lesen V. 7 als Antwort auf die Vorstellung zweier Urmächte von Licht und Finsternis. Wie Gott und das Unheil zusammenhängen, beantworten jüdische und christliche Theologen verschieden."),
        E("Was heißt „die Lenden entgürten“?", "Wer den Gürtel ablegte, konnte weder kämpfen noch laufen. Gott nimmt den Königen also ihre Kampfkraft.", "elbbk"),
    ],
    fact="Auf dem Kyrus-Zylinder, einem Tonzylinder im British Museum, lässt Kyrus über sich schreiben, Marduk, der Gott Babylons, habe ihn bei der Hand genommen und beim Namen gerufen. Jes 45,1–4 sagt dasselbe vom Gott Israels.",
    teaser="Ein Satz aus dem nächsten Abschnitt steht im Neuen Testament zweimal – einmal in einem der ältesten Christuslieder.")

sec("kyrus", [R(JES, 45, 18, 25)], "Jedes Knie wird sich beugen",
    "Gott hat die Erde nicht als Öde geschaffen, sondern damit sie bewohnt wird, und er hat nicht im Verborgenen geredet. Die Entkommenen der Völker sollen herbeikommen. Alle Enden der Erde sollen sich zu ihm wenden und gerettet werden. Gott hat bei sich selbst geschworen: Jedes Knie wird sich vor ihm beugen, jede Zunge ihm schwören.",
    quiz=[
        choice("Wozu hat Gott die Erde nach V. 18 gebildet?", ["Damit sie bewohnt wird", "Damit sie wüst und leer bleibt", "Nur als Wohnort für Israel", "Als Wohnung für die Götter"], 18, "Lies Vers 18.",
               "V. 18: Nicht als Öde hat er sie geschaffen; um bewohnt zu werden, hat er sie gebildet."),
        choice("Wen ruft Gott in V. 22, sich ihm zuzuwenden?", ["Alle Enden der Erde", "Nur das Haus Jakob", "Nur die Priester", "Nur Kyrus und sein Heer"], 22, "Lies Vers 22.",
               "V. 22: alle ihr Enden der Erde."),
        tf("Gott sagt in V. 19, er habe im Verborgenen geredet.", False, 19, "Lies Vers 19.",
           "V. 19: Nicht im Verborgenen habe ich geredet."),
    ],
    explain=[
        E("Was ist eine „Öde“?", "Hebräisch tohu, dasselbe Wort wie in 1Mo 1,2 („wüst und leer“). Der Vers sagt: Die Erde sollte nicht so bleiben."),
        E("Wo kommt V. 23 im Neuen Testament vor?", "Paulus zitiert ihn zweimal: in Röm 14,11 über das Gericht Gottes und im Christuslied Phil 2,10–11, wo sich jedes Knie im Namen Jesu beugt. Dort wird, was Jesaja über den HERRN sagt, auf Jesus bezogen."),
        E("Warum schwört Gott „bei sich selbst“?", "Man schwört beim Größeren. Gott hat niemanden über sich; so formuliert es auch Hebr 6,13 im Blick auf Abraham."),
    ],
    memory_verse=MV(R(JES, 45, 22), "Wendet euch zu mir und werdet gerettet, alle ihr Enden der Erde!"),
    teaser="Babels Götter gehen im nächsten Abschnitt auf Reisen. Freiwillig ist das nicht.")

sec("kyrus", [R(JES, 46, 1, 11)], "Getragene Götter",
    "Bel und Nebo sinken zusammen; ihre Bilder werden auf müde Lasttiere geladen und gehen in die Gefangenschaft. Israel dagegen wurde von Mutterleib an von Gott getragen, und er trägt es bis ins graue Haar. Ein Götterbild muss man auf die Schulter nehmen, es bewegt sich nicht und antwortet nicht. Gott verkündet von Anfang an das Ende und ruft einen Raubvogel aus dem Osten.",
    place="babylon",
    focus="Achte auf das Wort „tragen“. Wer trägt hier wen?",
    quiz=[
        choice("Was geschieht mit den Bildern von Bel und Nebo?", ["Sie werden auf Lasttiere geladen", "Sie werden im Tempel neu aufgestellt", "Sie werden mit Gold überzogen", "Sie sprechen zu den Priestern"], 1, "Lies Vers 1–2.",
               "V. 1–2: Ihre Bilder werden Last für das müde Vieh und ziehen selbst in die Gefangenschaft."),
        tf("Gott verspricht in V. 4, Israel bis ins hohe Alter zu tragen.", True, 4, "Lies Vers 4.",
           "V. 4: bis in euer Greisenalter, bis zum grauen Haar werde ich euch tragen."),
        choice("Wen ruft Gott nach V. 11 aus dem Osten?", ["Einen Raubvogel, den Mann seines Ratschlusses", "Einen Engel mit einem Schwert", "Den Pharao von Ägypten", "Einen Propheten aus Babel"], 11, "Lies Vers 11.",
               "V. 11: einen Raubvogel von Osten her, aus fernem Land den Mann meines Ratschlusses."),
    ],
    explain=[
        E("Was ist ein „Saumtier“?", "Ein Lasttier, das Waren auf dem Rücken trägt, etwa ein Esel oder Maultier.", "elbbk"),
        E("Wer ist der Raubvogel?", "Gemeint ist wohl Kyrus. Persien lag östlich von Babylon, und Kyrus wurde bereits in 41,2.25 als einer angekündigt, der vom Osten kommt."),
        E("Warum werden die Götter weggetragen?", "Wenn eine Stadt fiel, brachte man ihre Götterbilder in Sicherheit oder der Sieger nahm sie mit. Jesaja beschreibt das Bild: Die Götter retten nicht, sie müssen selbst gerettet werden. Historisch berichtet die Nabonid-Chronik, dass vor dem Fall Babylons Götterbilder anderer Städte in die Hauptstadt gebracht wurden; Kyrus ließ sie danach an ihre Orte zurückbringen."),
    ],
    cards=["bel-nebo"],
    fact="Das Bild des Gottes Nabu (Nebo) wurde zum babylonischen Neujahrsfest jedes Jahr aus der Nachbarstadt Borsippa nach Babylon gebracht. Die Nabonid-Chronik vermerkt für mehrere Jahre, dass das Fest ausfiel, weil der König nicht in der Stadt war.",
    memory_verse=MV(R(JES, 46, 4), "bis zu eurem grauen Haar werde ich euch tragen"),
    try_="Lies V. 1–7 und unterstreiche oder notiere jedes Mal, wenn vom Tragen, Heben oder Aufladen die Rede ist.",
    teaser="Die mächtigste Stadt der Welt muss jetzt im Staub sitzen. Und ein Satz aus ihrem Mund taucht in der Offenbarung wieder auf.")

sec("kyrus", [R(JES, 47, 1, 11)], "Steig herab, Tochter Babel",
    "Babel, die verwöhnte Herrin der Königreiche, soll vom Thron in den Staub steigen und wie eine Sklavin Mehl mahlen. Gott hatte sein Volk in ihre Hand gegeben, doch sie zeigte kein Erbarmen, nicht einmal mit den Alten. Sie sagt in ihrem Herzen: Ich und sonst keine. Doch Witwenschaft und Kinderlosigkeit werden an einem Tag über sie kommen, und keine Zauberei kann es abwenden.",
    place="babylon",
    quiz=[
        choice("Was wirft Gott Babel in V. 6 vor?", ["Sie hatte kein Erbarmen, nicht einmal mit den Alten", "Sie hat den Tempel nicht wieder aufgebaut", "Sie hat Kyrus nicht gewarnt", "Sie hat Israel nicht genug Land gegeben"], 6, "Lies Vers 6.",
               "V. 6: Du hast ihnen kein Erbarmen erwiesen; auch auf den Greis legtest du ein schweres Joch."),
        who("Ich bin es, und gar keine sonst!", R(JES, 47, 8), ["Babel", "Gott", "Zion", "Kyrus"],
            "V. 8 und 10: Babel sagt das in ihrem Herzen. Ganz ähnlich klingt, was Gott in 45,5–6.18 über sich selbst sagt.", "Wer redet in Kapitel 47 in ihrem Herzen?"),
        tf("Nach V. 9 kommen Witwenschaft und Kinderlosigkeit langsam über viele Jahre.", False, 9, "Lies Vers 9.",
           "V. 9: Beides kommt in einem Augenblick, an einem Tag."),
    ],
    explain=[
        E("Warum Mehl mahlen?", "Das Mahlen mit der Handmühle war die niedrigste Arbeit, meist von Sklavinnen getan (2Mo 11,5). Die Königin muss Schleier und Schleppe ablegen und wie eine Gefangene durch Flüsse waten."),
        E("Warum „Witwe“?", "Städte wurden als Frauen vorgestellt, ihre Götter oder Könige als Ehemänner, die Einwohner als Kinder. Witwe und kinderlos heißt: ohne Schutz und ohne Bevölkerung."),
        E("Ist das dieselbe Babylon wie in der Offenbarung?", "Offb 18,7 greift V. 7–8 fast wörtlich auf. Viele dispensationalistische Ausleger erwarten in der Endzeit eine konkrete Stadt oder ein Weltsystem namens Babylon. Amillenialistische und viele andere Ausleger lesen „Babylon“ dort als Sinnbild für jede gottfeindliche Macht durch die Geschichte; präteristische Ausleger denken vor allem an das Rom des 1. Jahrhunderts. Alle verbinden die Offenbarung mit Jes 47."),
    ],
    cards=["babel"],
    fact="Babylon fiel 539 v. Chr. nach der Nabonid-Chronik ohne Kampf: Die Truppen des Kyrus zogen in die Stadt ein, und kurz darauf kam Kyrus selbst.",
    teaser="Im nächsten Abschnitt sagt Gott einen Satz, der wie ein Seufzer klingt: Hättest du doch …")

sec("kyrus", [R(JES, 48, 12, 22)], "Zieht aus Babel!",
    "Gott, der Erste und der Letzte, hat den, den er liebt, gegen Babel gerufen. Dann ein Seufzer: Hätte Israel auf seine Gebote geachtet, wäre sein Friede wie ein Strom gewesen. Schließlich der Ruf: Zieht aus Babel, flieht mit Jubel und erzählt es bis ans Ende der Erde! Wie einst in der Wüste wird Wasser aus dem Felsen fließen. Am Ende ein Satz: Kein Friede den Gottlosen.",
    place="babylon",
    quiz=[
        choice("Wie wäre Israels Friede nach V. 18 gewesen?", ["Wie ein Strom", "Wie ein Fels", "Wie eine Mauer", "Wie ein Zelt"], 18, "Lies Vers 18.",
               "V. 18: Dein Friede wäre wie ein Strom gewesen und deine Gerechtigkeit wie die Wellen des Meeres."),
        order("Bring die Teile des Abschnitts in die richtige Reihenfolge.", ["Gott ruft den, den er liebt, gegen Babel", "Gott seufzt: Hättest du doch auf meine Gebote geachtet", "Der Ruf: Zieht aus Babel!", "Kein Friede den Gottlosen"],
              "V. 14–15, V. 18, V. 20 und V. 22."),
        tf("V. 21 erinnert an das Wasser aus dem Felsen in der Wüste.", True, 21, "Lies Vers 21.",
           "V. 21: Er ließ ihnen Wasser aus dem Felsen fließen – wie in 2Mo 17,6 und 4Mo 20,11."),
    ],
    explain=[
        E("Wer spricht in V. 16?", "Am Ende von V. 16 spricht plötzlich ein Ich, das der Herr mit seinem Geist gesandt hat. Viele denken an den Propheten selbst. Schon in der Alten Kirche lasen manche hier den Vater, den Sohn und den Geist zusammen."),
        E("Wer ist der, den der HERR liebt (V. 14)?", "Im Zusammenhang wohl Kyrus, der gegen Babel ausführt, was Gott will (vgl. 44,28; 46,11)."),
        E("Warum endet das Kapitel so knapp?", "Derselbe Satz steht fast gleich in 57,21. Viele Ausleger sehen darin einen Gliederungshinweis, der Jes 40–66 in drei Teile von je etwa neun Kapiteln teilt."),
    ],
    teaser="Ab jetzt redet plötzlich jemand selbst, in der Ich-Form – und zwar zu den fernen Völkern.")

# ───────────────────────── 4 · Zion und der Knecht ─────────────────────────
sec("knecht", [R(JES, 49, 1, 7)], "Licht der Nationen",
    "Der Knecht spricht selbst: Gott hat ihn vom Mutterleib an berufen, ihn wie ein scharfes Schwert im Schatten seiner Hand und wie einen Pfeil im Köcher verborgen. Gott nennt ihn Israel. Er klagt, er habe sich umsonst abgemüht, doch sein Recht ist bei Gott. Gott antwortet: Es ist zu wenig, nur die Stämme Jakobs aufzurichten – er soll Licht der Nationen sein bis ans Ende der Erde.",
    focus="Achte darauf, welchen Namen der Knecht in V. 3 bekommt und was er in V. 5–6 für Israel tun soll.",
    quiz=[
        who("Umsonst habe ich mich abgemüht", R(JES, 49, 4), ["Der Knecht", "Zion", "Kyrus", "Die Tochter Babel"],
            "V. 4: Der Knecht klagt – und hält zugleich fest, dass sein Recht beim HERRN ist."),
        choice("Was ist nach V. 6 „zu gering“?", ["Nur die Stämme Jakobs aufzurichten", "Babel zu besiegen", "Den Tempel zu bauen", "Die Inseln zu erreichen"], 6, "Lies Vers 6.",
               "V. 6: Es ist zu gering, nur Jakobs Stämme aufzurichten; ich mache dich zum Licht der Nationen."),
        tf("Der Knecht wird in V. 3 „Israel“ genannt.", True, 3, "Lies Vers 3.",
           "V. 3: Du bist mein Knecht, bist Israel, an dem ich mich verherrlichen werde."),
    ],
    explain=[
        E("Der Knecht heißt Israel – und soll Israel zurückbringen?", "V. 3 nennt ihn Israel, V. 5–6 geben ihm einen Auftrag an Israel. Jüdische Auslegung liest meist das Volk oder einen treuen Teil davon. Christliche Auslegung sieht in Jesus den, der Israels Berufung ganz erfüllt. Wieder andere denken an den Propheten, der für sein Volk spricht."),
        E("Wo kommt V. 6 im Neuen Testament vor?", "Paulus und Barnabas zitieren ihn in Apg 13,47 für ihre Sendung zu den Nichtjuden. Der alte Simeon nennt das Kind Jesus im Tempel ein Licht für die Völker (Lk 2,32)."),
        E("Warum Schwert und Pfeil?", "Beide sind Bilder für ein treffendes Wort (vgl. Hebr 4,12; Offb 1,16). Sie sind „versteckt“: bereit, aber noch nicht eingesetzt."),
    ],
    teaser="Zion sagt im nächsten Abschnitt etwas, das viele Psalmbeter auch sagen. Gottes Antwort kommt mit einem Bild aus dem Alltag einer Mutter.")

sec("knecht", [R(JES, 49, 14, 23)], "Zion sagt: Ich bin vergessen",
    "Zion klagt, Gott habe sie verlassen und vergessen. Gott antwortet: Kann eine Mutter ihren Säugling vergessen? Selbst wenn sie es könnte, er vergisst Zion nicht; er hat sie in seine Handflächen gezeichnet. Ihre Kinder kommen zurück, so viele, dass der Platz zu eng wird. Zion wundert sich, woher sie kommen. Völker und Könige tragen sie herbei.",
    place="jerusalem",
    quiz=[
        choice("Womit vergleicht Gott seine Treue in V. 15?", ["Mit einer Mutter, die ihr Kind nicht vergisst", "Mit einem Vater, der sein Erbe verteilt", "Mit einem Hirten, der sein Schaf sucht", "Mit einem König, der seine Stadt baut"], 15, "Lies Vers 15.",
               "V. 15: Kann eine Frau ihren Säugling vergessen? Selbst wenn sie vergäße – ich vergesse dich nicht."),
        choice("Wo hat Gott Zion nach V. 16 eingezeichnet?", ["In seine Handflächen", "In ein Buch im Himmel", "In die Tempelmauer", "In den Sternenhimmel"], 16, "Lies Vers 16.",
               "V. 16: In meine beiden Handflächen habe ich dich eingezeichnet."),
        error("Zion fragt: Wer hat mir diese Kinder geboren? Ich war doch kinderlos und [glücklich].", "unfruchtbar", 21,
              "V. 21: Zion war der Kinder beraubt und unfruchtbar, verbannt und allein übrig geblieben."),
    ],
    explain=[
        E("Was heißt „eingezeichnet“?", "Das hebräische chaqaq heißt einritzen, eingravieren – wie in Stein. Gemeint ist kein Notizzettel, sondern etwas Bleibendes. Die Mauern Zions stehen Gott ständig vor Augen."),
        E("Was ist ein „Panier“?", "Ein Feldzeichen, eine Fahne an einer Stange, die auf einem Hügel aufgestellt wurde, damit sich Menschen dort sammeln.", "elbbk"),
        E("Gott wie eine Mutter?", "Jesaja benutzt mehrmals Bilder einer Mutter für Gott: die Gebärende (42,14), die Mutter, die ihr Kind nicht vergisst (49,15), die Mutter, die tröstet (66,13). Daneben stehen Bilder vom Vater (63,16; 64,7)."),
    ],
    memory_verse=MV(R(JES, 49, 15), "Sollten selbst diese vergessen, ich werde deiner nicht vergessen."),
    prayer={"ref": R(PS, 13, 2), "source": "Psalm 13,2"},
    teaser="Der Knecht spricht wieder. Diesmal erzählt er, wie sein Morgen anfängt.")

sec("knecht", [R(JES, 50, 4, 11)], "Jeden Morgen ein offenes Ohr",
    "Der Knecht erzählt: Gott hat ihm eine geübte Zunge gegeben, um Müde mit einem Wort aufzurichten, und weckt ihm jeden Morgen das Ohr. Er ist nicht zurückgewichen; er hielt seinen Rücken den Schlägern hin und verbarg sein Gesicht nicht vor Schmach und Speichel. Gott hilft ihm – wer will ihn verurteilen? Wer im Dunkeln geht, soll dem Namen des HERRN vertrauen.",
    quiz=[
        choice("Wozu hat der Knecht nach V. 4 die geübte Zunge?", ["Um Müde mit einem Wort aufzurichten", "Um gegen Babel zu predigen", "Um Könige zu beraten", "Um neue Lieder zu dichten"], 4, "Lies Vers 4.",
               "V. 4: damit ich wisse, den Müden durch ein Wort aufzurichten."),
        tf("Nach V. 6 verbirgt der Knecht sein Gesicht vor Schmach und Speichel.", False, 6, "Lies Vers 6.",
           "V. 6: Mein Angesicht verbarg ich nicht vor Schmach und Speichel."),
        choice("Was legt V. 10 dem nahe, der im Finstern geht und kein Licht hat?", ["Auf den Namen des HERRN vertrauen und sich auf Gott stützen", "Ein eigenes Feuer anzünden", "Bis zum Morgen schlafen", "Nach Babel zurückkehren"], 10, "Lies Vers 10–11.",
               "V. 10: Er vertraue auf den Namen des HERRN und stütze sich auf seinen Gott. V. 11 warnt die, die sich ihr eigenes Feuer anzünden."),
    ],
    explain=[
        E("Was heißt „Wangen den Raufenden“?", "Gemeint ist das Ausreißen des Bartes, im Alten Orient eine schwere Demütigung (vgl. 2Sam 10,4; Neh 13,25)."),
        E("Was meint „Angesicht wie ein Kieselstein“?", "Ein Bild für Entschlossenheit: Das Gesicht wird hart wie Feuerstein, unbeirrbar. Lk 9,51 beschreibt Jesus ähnlich, als er sich entschlossen nach Jerusalem wendet."),
        E("Wer spricht hier?", "Manche lesen den Abschnitt als Erfahrung des Propheten, der für seine Botschaft angefeindet wurde. Christen sehen hier die Passion Jesu vorgezeichnet; die Evangelien berichten von Schlägen und Anspeien (Mk 14,65; 15,19)."),
    ],
    fact="Das hebräische Wort für „Belehrte“ in V. 4, limmudim, steht in Jes 8,16 für die Jünger oder Schüler Jesajas. Der Knecht spricht also wie ein Schüler, der jeden Morgen zuhört.",
    teaser="Im nächsten Abschnitt versucht jemand, Gott aufzuwecken.")

sec("knecht", [R(JES, 51, 9, 16)], "Wach auf, Arm des HERRN",
    "Ein Ruf an Gottes Arm: Wach auf wie in der Urzeit! Hast du nicht Rahab zerhauen und das Meer ausgetrocknet, damit die Erlösten hindurchziehen? So werden auch die Befreiten mit Jubel nach Zion kommen. Gott antwortet: Ich bin es, der euch tröstet. Warum fürchtest du sterbliche Menschen und vergisst deinen Schöpfer?",
    quiz=[
        choice("An welche Taten Gottes erinnert der Ruf in V. 9–10?", ["An den Sieg über Rahab und den Weg durchs Meer", "An die Erschaffung des Menschen", "An die Sintflut", "An die Berufung Abrahams"], 9, "Lies Vers 9–10.",
               "V. 9–10: Rahab zerhauen, das Seeungeheuer durchbohrt, das Meer zu einem Weg gemacht."),
        who("Ich, ich bin es, der euch tröstet.", R(JES, 51, 12), ["Gott", "Der Knecht", "Zion", "Kyrus"],
            "V. 12: Gott antwortet auf den Weckruf von V. 9 – mit dem Wort, mit dem das Buch in 40,1 begann."),
        tf("Nach V. 14 wird der Gefesselte bald freigelassen.", True, 14, "Lies Vers 14.",
           "V. 14: Der in Fesseln Gekrümmte wird bald losgelassen und stirbt nicht in der Grube."),
    ],
    explain=[
        E("Schläft Gott?", "Ps 121,4 sagt, Gott schläft nicht. Trotzdem benutzen Gebete in der Bibel dieses kühne Bild, wenn Gott nicht zu handeln scheint (Ps 44,24). Der Ruf in V. 9 steht in dieser Tradition."),
        E("Wer ruft hier?", "Der Ruf in V. 9–11 kommt wohl vom Propheten oder vom Volk. Ab V. 12 spricht Gott und antwortet darauf."),
        E("Warum wird der Mensch „Gras“ genannt?", "V. 12 greift 40,6–8 auf: Der Mensch vergeht wie Gras. Wer sich vor einem solchen Menschen fürchtet, so V. 13, vergisst den, der Himmel und Erde gemacht hat."),
    ],
    cards=["rahab"],
    prayer={"ref": R(PS, 44, 24), "source": "Psalm 44,24"},
    teaser="Ein Läufer kommt über die Berge auf eine zerstörte Stadt zu. Was er ruft, hat einem Wort im Neuen Testament den Namen gegeben.")

sec("knecht", [R(JES, 52, 7, 12)], "Wie lieblich sind die Füße",
    "Ein Freudenbote kommt über die Berge und ruft Zion zu: Dein Gott ist König! Die Wächter auf den Mauern jubeln, denn sie sehen mit eigenen Augen, wie der HERR nach Zion zurückkehrt. Auch die Trümmer Jerusalems sollen jubeln. Die Heimkehrer sollen ausziehen, nicht in Hast, denn Gott geht vor ihnen her und bildet ihre Nachhut.",
    place="jerusalem",
    quiz=[
        choice("Was ruft der Bote nach V. 7 Zion zu?", ["Dein Gott ist König", "Babel ist zerstört", "Der Tempel steht wieder", "Kyrus kommt"], 7, "Lies Vers 7.",
               "V. 7: der Frieden und Rettung verkündet und zu Zion sagt: Dein Gott herrscht als König."),
        tf("Nach V. 11 sollen sich die reinigen, die die Geräte des HERRN tragen.", True, 11, "Lies Vers 11.",
           "V. 11: Reinigt euch, die ihr die Geräte des HERRN tragt."),
        choice("Warum sollen sie nach V. 12 nicht in Hast ausziehen?", ["Weil Gott vor ihnen hergeht und ihre Nachhut ist", "Weil der Weg kurz ist", "Weil Kyrus sie mit Soldaten begleitet", "Weil sie erst den Tempel weihen müssen"], 12, "Lies Vers 12.",
               "V. 12: Der HERR zieht vor euch her, und eure Nachhut ist der Gott Israels."),
    ],
    explain=[
        E("Welche Geräte sind gemeint?", "Nebukadnezar hatte die Gefäße des Tempels nach Babel bringen lassen (2Kön 25,13–15). Nach Esr 1,7–11 gab Kyrus sie den Heimkehrern zurück."),
        E("Warum „nicht in Hast“?", "Beim Auszug aus Ägypten musste Israel in Eile aufbrechen (2Mo 12,11; 5Mo 16,3). Dieser neue Auszug wird bewusst anders beschrieben: ohne Flucht, mit Gott vorn und hinten."),
        E("Wo kommt V. 7 im Neuen Testament vor?", "Paulus zitiert ihn in Röm 10,15 für die Boten, die das Evangelium von Christus bringen."),
    ],
    cards=["freudenbote"],
    teaser="Jetzt beginnt der wohl am meisten diskutierte Text des Alten Testaments. Er fängt mit einem Erfolg an.")

sec("knecht", [R(JES, 52, 13, 15), R(JES, 53, 1, 6)], "Verachtet",
    "Gott kündigt an: Sein Knecht wird erhöht werden – obwohl viele über sein entstelltes Aussehen entsetzt waren. Dann spricht ein „Wir“: Er war unansehnlich, verachtet, ein Mann der Schmerzen, und wir hielten ihn für von Gott geschlagen. Doch er trug unsere Schmerzen; wegen unserer Übertretungen wurde er durchbohrt, und durch seine Wunden sind wir geheilt. Wir alle gingen in die Irre wie Schafe.",
    focus="Achte darauf, wer in 53,1–6 „wir“ sagt und wie sich das Urteil dieser Gruppe über den Knecht ändert.",
    quiz=[
        choice("Wofür hielten „wir“ den Knecht nach 53,4?", ["Für bestraft und von Gott geschlagen", "Für einen König", "Für einen großen Propheten", "Für einen Fremden aus Babel"], 4, "Lies Kapitel 53, Vers 4.",
               "53,4: Wir hielten ihn für bestraft, von Gott geschlagen und niedergebeugt."),
        order("Bring die Aussagen in die Reihenfolge des Textes.", ["Der Knecht wird erhöht werden", "Viele entsetzen sich über sein Aussehen", "Er war verachtet und verlassen", "Durch seine Wunden sind wir geheilt"],
              "52,13; 52,14; 53,3; 53,5."),
        tf("Nach 53,6 sind nur einige vom Weg abgeirrt.", False, 6, "Lies Kapitel 53, Vers 6.",
           "53,6: Wir alle irrten umher wie Schafe, jeder wandte sich seinem eigenen Weg zu."),
    ],
    explain=[
        E("Wer ist der Knecht in diesem Lied?", "Jüdische Ausleger seit dem Mittelalter, etwa Raschi, lesen meist das Volk Israel, das unter den Völkern leidet; die „Wir“ sind dann die Könige der Völker aus 52,15. Der Targum, eine alte aramäische Übersetzung, bezieht 52,13 auf den Messias. Das Neue Testament und alle christlichen Kirchen lesen das Lied als Beschreibung Jesu (Apg 8,35; 1Petr 2,22–25)."),
        E("Wie deuten die Kirchen sein Leiden?", "Gemeinsam ist allen: Der Knecht leidet für andere. Evangelische, besonders evangelikale Theologie betont oft die stellvertretende Strafe (53,5). Katholische Theologie spricht vom Sühnopfer und der Hingabe Christi, die in der Messe gegenwärtig wird. Orthodoxe Theologie betont stärker Heilung und Sieg über den Tod: Christus nimmt das Menschsein an und heilt es."),
        E("Was ist ein „Reis“?", "Ein junger Trieb, ein Schössling. Er wächst hier aus trockenem Boden – unscheinbar und ohne gute Aussichten. Vgl. 11,1, wo ein Reis aus dem Stumpf Isais hervorgeht.", "elbbk"),
        E("Staunen oder besprengen (52,15)?", "Das hebräische Verb heißt sonst „besprengen“, etwa mit Blut oder Wasser bei der Reinigung. Die alte griechische Übersetzung und viele heutige übersetzen „in Staunen setzen“, weil es zum Folgenden passt. Beide Übersetzungen sind verbreitet."),
    ],
    fact="Händels Oratorium „Messiah“ (1742) vertont 53,3–6 in vier Sätzen nacheinander, darunter den Chor „All we like sheep have gone astray“ nach 53,6.",
    memory_verse=MV(R(JES, 53, 5), "doch um unserer Übertretungen willen war er verwundet, um unserer Ungerechtigkeiten willen zerschlagen."),
    prayer={"text": "Was ist doch wohl die Ursach solcher Plagen? Ach, meine Sünden haben dich geschlagen; ich, mein Herr Jesu, habe dies verschuldet, was du erduldet.", "source": "Johann Heermann, „Herzliebster Jesu, was hast du verbrochen“ (1630), Strophe 3"},
    teaser="Den nächsten Teil las ein Hofbeamter aus Äthiopien auf der Heimreise – und stellte genau die Frage, die bis heute gestellt wird.")

sec("knecht", [R(JES, 53, 7, 12)], "Wie ein Lamm",
    "Der Knecht wird misshandelt und öffnet seinen Mund nicht, wie ein Lamm auf dem Weg zur Schlachtung. Er wird aus dem Land der Lebenden weggerissen; sein Grab wird bei Gottlosen bestimmt, doch im Tod ist er bei einem Reichen. Es gefiel dem HERRN, ihn zu zerschlagen; aber er wird Nachkommen sehen, lange leben und viele gerecht machen. Er trug die Sünde vieler und trat für die Übertreter ein.",
    quiz=[
        choice("Womit wird der Knecht in V. 7 verglichen?", ["Mit einem Lamm und einem Schaf vor seinen Scherern", "Mit einem Löwen, der schweigt", "Mit einem Hirten ohne Herde", "Mit einer Taube im Netz"], 7, "Lies Vers 7.",
               "V. 7: wie ein Lamm, das zur Schlachtung geführt wird, und wie ein Schaf, das vor seinen Scherern verstummt."),
        tf("Nach V. 10–11 ist mit dem Tod des Knechtes alles zu Ende.", False, 10, "Lies Vers 10–11.",
           "V. 10–11: Er wird Nachkommen sehen, seine Tage verlängern und nach der Mühsal seiner Seele Frucht sehen."),
        choice("Was tut der Knecht nach V. 12 für die Übertreter?", ["Er tritt fürbittend für sie ein", "Er richtet sie", "Er verlässt sie", "Er vertreibt sie aus dem Land"], 12, "Lies Vers 12.",
               "V. 12: Er hat die Sünde vieler getragen und für die Übertreter Fürbitte getan."),
    ],
    explain=[
        E("Was ist ein „Schuldopfer“?", "Hebräisch ascham, ein Opfer der Wiedergutmachung: Wer einem anderen oder Gott etwas schuldig geblieben war, brachte es dar (3Mo 5,14–26). Das Wort beschreibt hier das Leben des Knechtes selbst."),
        E("Welche Stellen zitiert das Neue Testament?", "Der Kämmerer aus Äthiopien liest V. 7–8 und fragt, von wem der Prophet spricht (Apg 8,32–35). Jesus bezieht V. 12 auf sich, er werde unter die Gesetzlosen gerechnet (Lk 22,37). Mt 27,57–60 berichtet vom Grab des reichen Josef von Arimathäa."),
        E("Was heißt „wer wird sein Geschlecht aussprechen“ (V. 8)?", "Ein schwieriger Satz. Mögliche Bedeutungen: Wer kümmert sich um sein Schicksal? Wer bedenkt seine Zeitgenossen? Oder: Er stirbt ohne Nachkommen. Die Übersetzungen gehen hier weit auseinander.", "elbbk"),
    ],
    cards=["jesajarolle"],
    fact="In V. 11 haben die große Jesajarolle aus Qumran und die alte griechische Übersetzung ein Wort mehr als der übliche hebräische Text: Nach der Mühsal seiner Seele wird er „Licht“ sehen.",
    try_="Lies Apg 8,30–35. Welche Frage stellt der Mann aus Äthiopien?",
    teaser="Nach diesem Lied wird eine kinderlose Frau aufgefordert, ihr Zelt zu vergrößern.")

# ───────────────────────── 5 · Kommt zu den Wassern ─────────────────────────
sec("wasser", [R(JES, 54, 1, 12)], "Mach weit den Raum deines Zeltes",
    "Die Unfruchtbare soll jubeln, denn sie wird mehr Kinder haben als die Verheiratete; sie soll ihr Zelt weit machen. Ihr Schöpfer ist ihr Mann. Einen kleinen Augenblick hat er sie verlassen, mit großem Erbarmen holt er sie zurück. Wie nach der Flut zu Noahs Zeit hat er geschworen: Berge mögen weichen, seine Güte weicht nicht. Die sturmgepeitschte Stadt wird auf Edelsteinen gebaut.",
    place="jerusalem",
    quiz=[
        choice("Was soll die Unfruchtbare nach V. 2 tun?", ["Den Raum ihres Zeltes weit machen", "Ein Haus aus Stein bauen", "Nach Babel ziehen", "Ein Opfer bringen"], 2, "Lies Vers 2.",
               "V. 2: Mach weit den Raum deines Zeltes, mach deine Seile lang und schlag die Pflöcke fest ein."),
        tf("Gott sagt in V. 7, er habe Zion für lange Zeit verlassen.", False, 7, "Lies Vers 7.",
           "V. 7: einen kleinen Augenblick – aber mit großem Erbarmen will ich dich sammeln."),
        choice("An welchen Schwur erinnert Gott in V. 9?", ["An den Schwur nach der Flut zu Noahs Zeit", "An den Bund mit Abraham", "An den Bund am Sinai", "An die Zusage an David"], 9, "Lies Vers 9.",
               "V. 9: wie die Wasser Noahs, als ich schwor, dass sie die Erde nicht mehr überfluten sollten."),
    ],
    explain=[
        E("Wer ist die Unfruchtbare?", "Zion, angeredet wie Sara, Rahel oder Hanna, die lange kinderlos waren. Paulus zitiert V. 1 in Gal 4,27 und bezieht ihn auf das „obere Jerusalem“."),
        E("Gott als Ehemann?", "Die Ehe ist ein häufiges Bild für Gottes Bund mit Israel (Hos 2; Jer 2,2). Die Verbannung erscheint hier wie eine Zeit, in der die Frau verlassen war – nun nimmt er sie wieder auf."),
        E("Wie wird die Stadt aus Edelsteinen gelesen (V. 11–12)?", "Offb 21,18–21 greift das Bild für das neue Jerusalem auf. Dispensationalistische Ausleger lesen beide Texte meist wörtlich, als künftige Stadt. Amillenialistische und viele andere Ausleger sehen darin ein Bild für das vollendete Volk Gottes in der neuen Schöpfung. Jüdische Auslegung bezieht V. 11–12 auf das wiederhergestellte Jerusalem."),
        E("Was sind „Bleiglanz“ und „Karfunkel“?", "Bleiglanz ist hier wohl dunkler Mörtel oder Schminke, in dem die Steine eingefasst werden. Karfunkel ist ein altes Wort für einen leuchtend roten Edelstein. Welche Steine genau gemeint sind, ist unsicher.", "elbbk"),
    ],
    memory_verse=MV(R(JES, 54, 10), "aber meine Güte wird nicht von dir weichen und mein Friedensbund nicht wanken"),
    teaser="Im nächsten Abschnitt ruft jemand wie ein Händler auf dem Markt. Nur verlangt er kein Geld.")

sec("wasser", [R(JES, 55, 1, 7)], "Kauft ohne Geld",
    "Ein Ausrufer lädt alle Durstigen ein: Kommt zu den Wassern, kauft ohne Geld Wein und Milch! Warum gebt ihr Geld aus für das, was nicht satt macht? Gott will einen ewigen Bund schließen, die verlässliche Güte, die David galt. Sucht den HERRN, solange er sich finden lässt; wer umkehrt, findet einen Gott, der reich an Vergebung ist.",
    quiz=[
        choice("Was kostet das Angebot nach V. 1?", ["Nichts, man kauft ohne Geld", "Einen Silberschekel", "Ein Opfer im Tempel", "Die halbe Ernte"], 1, "Lies Vers 1.",
               "V. 1: Kommt, kauft ohne Geld und ohne Kaufpreis Wein und Milch."),
        error("Gott fragt: Warum gebt ihr Geld aus für das, was nicht [schmeckt]?", "sättigt", 2,
              "V. 2: für das, was nicht Brot ist und nicht satt macht."),
        choice("Was gilt nach V. 7 für den, der umkehrt?", ["Gott erbarmt sich, er ist reich an Vergebung", "Er muss erst ein Schuldopfer bringen", "Er darf nicht nach Zion zurück", "Er muss sieben Jahre warten"], 7, "Lies Vers 7.",
               "V. 7: Er kehre um zum HERRN, so wird er sich seiner erbarmen, denn er ist reich an Vergebung."),
    ],
    explain=[
        E("Was sind die „gewissen Gnaden Davids“?", "Gemeint ist die Zusage an David, dass sein Königshaus Bestand haben soll (2Sam 7,12–16). Hier wird sie auf das ganze Volk ausgeweitet. Paulus zitiert V. 3 in Apg 13,34 im Blick auf die Auferstehung Jesu.", "elbbk"),
        E("Warum klingt V. 1 wie ein Markt?", "Der Vers ahmt den Ruf eines Händlers nach, der seine Ware anpreist – mit dem Unterschied, dass man ohne Geld kaufen soll. Wein und Milch standen für Fülle und Festessen."),
        E("Was heißt „solange er sich finden lässt“?", "Manche lesen eine Dringlichkeit: Die Gelegenheit ist jetzt, in der Zeit der Heimkehr. Andere betonen, dass Gott sich finden lassen will; V. 7 nennt ihn reich an Vergebung."),
    ],
    prayer={"text": "Spät habe ich dich geliebt, du Schönheit, so alt und so neu, spät habe ich dich geliebt. … Du hast gerufen und geschrien und meine Taubheit durchbrochen. … Ich habe gekostet, und nun hungere und dürste ich nach dir.", "source": "Augustinus, Bekenntnisse X,27 (eigene Übersetzung)"},
    teaser="Zum Schluss: ein Vergleich mit dem Wetter – und Bäume, die etwas tun, was Bäume nicht können.")

sec("wasser", [R(JES, 55, 8, 13)], "Mein Wort kehrt nicht leer zurück",
    "Gottes Gedanken und Wege sind höher als die der Menschen, so wie der Himmel höher ist als die Erde. Wie Regen und Schnee nicht zurückkehren, ohne die Erde getränkt zu haben, so kehrt auch sein Wort nicht leer zurück. In Freude werden sie ausziehen; Berge jubeln, Bäume klatschen in die Hände, und statt Dornen wachsen Zypressen.",
    quiz=[
        choice("Womit vergleicht Gott sein Wort in V. 10–11?", ["Mit Regen und Schnee, die die Erde tränken", "Mit einem Schwert", "Mit Feuer", "Mit einem Hammer"], 10, "Lies Vers 10–11.",
               "V. 10–11: Wie Regen und Schnee die Erde tränken und sprossen lassen, so richtet Gottes Wort aus, wozu er es sendet."),
        tf("Nach V. 12 klatschen die Bäume des Feldes in die Hände.", True, 12, "Lies Vers 12.",
           "V. 12: Berge und Hügel brechen in Jubel aus, und alle Bäume des Feldes klatschen in die Hände."),
        choice("Was wächst nach V. 13 statt der Dornsträucher?", ["Zypressen", "Weizen", "Weinstöcke", "Feigenbäume"], 13, "Lies Vers 13.",
               "V. 13: Statt Dornsträuchern Zypressen, statt Brennnesseln Myrten."),
    ],
    explain=[
        E("Worauf bezieht sich V. 8–9?", "Das „denn“ in V. 8 knüpft an V. 7 an, wo es um Erbarmen und Vergebung geht. Viele Ausleger lesen V. 8–9 deshalb so: Gottes Bereitschaft zu vergeben übersteigt menschliche Maßstäbe. Andere lesen die Verse allgemeiner, über Gottes Unbegreiflichkeit."),
        E("Was sind Myrten?", "Immergrüne, duftende Sträucher. Beim Laubhüttenfest wurden Zweige von Myrten und anderen Bäumen gebraucht (Neh 8,15)."),
        E("Wohin ziehen sie aus?", "Im Zusammenhang aus Babel zurück in die Heimat (vgl. 48,20; 52,11–12). Wie in 40,3–4 wird der Weg durch die Wüste zu einem festlichen Zug."),
    ],
    memory_verse=MV(R(JES, 55, 8), "Denn meine Gedanken sind nicht eure Gedanken, und eure Wege sind nicht meine Wege"),
    try_="Lies 40,6–8 und 55,10–11 direkt hintereinander. Womit beginnt und womit endet dieser Teil des Buches?")

P.write()
