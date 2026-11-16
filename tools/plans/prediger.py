#!/usr/bin/env python3
"""Source for the reading plan „Prediger – Wozu das alles?“ (generates assets/plans/prediger.json).

python3 -I tools/plans/prediger.py && python3 -I tools/validate_plan.py app/src/main/assets/plans/prediger.json --review
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from planlib import *

PRED = 21

P = PlanBuilder(
    "prediger", "pr", "Prediger", "Wozu das alles?",
    "Ein Weiser probiert alles aus – Wissen, Vergnügen, Arbeit, Reichtum – und fragt, was davon bleibt. "
    "Das Buch Prediger (Kohelet) ist das unbequemste Weisheitsbuch der Bibel: ehrlich über Tod, Ungerechtigkeit und Zufall, "
    "und trotzdem voller Freude am Brot, am Wein und am Licht. 23 Abschnitte, in denen du selbst herausfindest, was er meint.",
    "weisheit",
    stages=[("hauch", "Alles ist Hauch"), ("zeit", "Alles hat seine Zeit"), ("geld", "Worte und Geld"),
            ("besser", "Besser als …"), ("schnur", "Bevor die silberne Schnur reißt")],
    cards=[
        ("kohelet", "person", "Kohelet, der Prediger", "Hebräisch Kohelet, wohl „der, der versammelt“ – eine Gemeinde oder Sprüche. Die Septuaginta übersetzt Ekklesiastes, Luther „Prediger“. Er nennt sich Sohn Davids und König in Jerusalem. Ob Salomo selbst schreibt oder ein späterer Weiser in Salomos Rolle spricht, wird unter gläubigen Auslegern verschieden gesehen.", "Pred 1,1.12; 12,9–10"),
        ("hevel", "begriff", "Hauch (hevel)", "Das Schlüsselwort des Buches, etwa 38-mal: hebräisch hevel, „Hauch, Dunst, Atem“. Es steht für das Flüchtige, Ungreifbare, auch das Rätselhafte. Übersetzungen sagen „Eitelkeit“, „Windhauch“, „vergänglich“ oder „sinnlos“ – jede betont etwas anderes. Derselbe Name trägt Abel (hebräisch Hevel, 1Mo 4,2).", "Pred 1,2; 12,8"),
        ("unter-der-sonne", "begriff", "Unter der Sonne", "Eine Wendung, die im Alten Testament nur im Prediger vorkommt, dort fast 30-mal. Sie beschreibt das Leben, wie man es auf der Erde beobachten kann. Ausleger fragen, ob der Prediger damit bewusst den Blick ohne Offenbarung einnimmt oder einfach „hier auf der Welt“ meint.", "Pred 1,3.9; 9,11"),
        ("salomo", "person", "Salomo", "Sohn Davids und Batsebas, König über Israel im 10. Jahrhundert v. Chr. Berühmt für seine Weisheit (1Kön 5,9–14) und seinen Reichtum; er baute den Tempel in Jerusalem. Nach 1Kön 11 wandten seine vielen Frauen sein Herz anderen Göttern zu. Ihm werden Sprüche, Hoheslied und Prediger zugeschrieben.", "1Kön 3–11"),
        ("weisheit", "begriff", "Weisheitsliteratur", "Hiob, Sprüche und Prediger (dazu einige Psalmen und in der katholischen und orthodoxen Bibel Weisheit und Jesus Sirach). Sie fragen, wie man klug lebt, und beobachten die Welt genau. Die Sprüche zeigen meist, wie es in der Regel läuft; Hiob und Prediger fragen, was ist, wenn es nicht so läuft.", "Spr 1,7; Pred 12,9"),
        ("tor", "begriff", "Der Tor", "In der Weisheitsliteratur nicht einfach ein Dummkopf, sondern jemand, der nicht hören und lernen will und ohne Gottesfurcht lebt (Spr 1,7; Ps 14,1). Der Gegenbegriff ist der Weise. Der Prediger stellt die Frage, was der Weise am Ende vor dem Toren voraushat.", "Pred 2,14–16; 10,1–3"),
        ("teil", "begriff", "Das Teil", "Hebräisch cheleq, „Anteil“ – ursprünglich das Stück Land, das jeder Familie zugeteilt war. Der Prediger benutzt es für das, was dem Menschen gegeben ist: die Freude an Essen, Trinken und Arbeit, solange er lebt. Es ist kein bleibender Gewinn, aber ein Geschenk.", "Pred 2,10; 3,22; 9,9"),
        ("gottesfurcht", "begriff", "Gottesfurcht", "Nicht Angst, sondern Ehrfurcht: Gott ernst nehmen als den, der größer ist und richtet. Für die Sprüche ist sie der Anfang der Weisheit (Spr 1,7). Im Prediger taucht sie mehrfach auf (3,14; 5,6; 7,18; 8,12) und steht im letzten Satz des Buches.", "Pred 12,13"),
        ("scheol", "begriff", "Scheol", "Im Alten Testament der Ort der Toten, ein Ort der Stille, unter der Erde vorgestellt. Die Bibel schildert ihn meist schattenhaft (Ps 6,6; Pred 9,10). Erst in späteren Texten wird die Hoffnung auf Auferstehung deutlicher (Dan 12,2). Die Septuaginta übersetzt Hades.", "Pred 9,10; Ps 88,4–13"),
        ("laubhuettenfest", "ereignis", "Laubhüttenfest", "Das Herbstfest Israels nach der Ernte, eine Woche lang in Hütten aus Zweigen, zur Erinnerung an die Wüstenzeit (3Mo 23,33–43). Es gilt als das fröhlichste Fest des Jahres. In vielen Synagogen wird an diesem Fest das Buch Prediger gelesen.", "3Mo 23,33–43"),
    ],
)
sec = P.sec

# ───────────────────────── 1 · Alles ist Hauch ─────────────────────────
sec("hauch", [R(PRED, 1, 1, 11)], "Nichts Neues unter der Sonne",
    "Der Prediger beginnt mit einem Ausruf: Alles ist Hauch. Was gewinnt der Mensch mit seiner Mühe? Generationen kommen und gehen, Sonne, Wind und Flüsse kreisen, nichts ist neu, und an niemanden erinnert man sich.",
    place="jerusalem",
    focus="Achte auf die Bilder aus der Natur. Was haben sie gemeinsam?",
    quiz=[
        choice("Welche Frage stellt der Prediger in V. 3?", ["Was der Mensch von all seiner Mühe gewinnt", "Warum Gott die Welt geschaffen hat", "Wer nach ihm König wird", "Wie man weise wird"], 3, "Lies Vers 3.",
               "V. 3: Welchen Gewinn hat der Mensch bei all seiner Mühe unter der Sonne?"),
        order("In welcher Reihenfolge nennt der Prediger die Bilder aus der Natur?", ["Die Sonne", "Der Wind", "Die Flüsse"],
              "V. 5–7: Die Sonne geht auf und unter, der Wind dreht sich, die Flüsse laufen ins Meer, das nicht voll wird.", "Lies Vers 5–7."),
        tf("Nach V. 11 erinnern sich spätere Generationen an die früheren.", False, 11, "Lies Vers 11.",
           "V. 11: An die Früheren erinnert man sich nicht – und an die Späteren wird man sich auch nicht erinnern."),
    ],
    explain=[
        E("Was heißt „Eitelkeit der Eitelkeiten“?", "Hebräisch hevel havalim, wörtlich „Hauch der Hauche“ – die stärkste Form, wie „Lied der Lieder“. Gemeint ist nicht Selbstverliebtheit, sondern etwas Flüchtiges, Ungreifbares wie Atem in kalter Luft.", "elbbk"),
        E("Wer ist der „Prediger“?", "Hebräisch Kohelet, wohl „der, der (eine Gemeinde) versammelt“. Der Titel in V. 1 – Sohn Davids, König in Jerusalem – deutet auf Salomo. Ob Salomo selbst schreibt oder ein späterer Weiser in Salomos Rolle spricht, ist unter gläubigen Auslegern offen; mehr dazu im nächsten Abschnitt."),
        E("Was meint „Gewinn“?", "Hebräisch jitron, ein Wort aus der Geschäftswelt: der Überschuss, der nach Abzug aller Kosten bleibt. Es kommt im Alten Testament nur im Prediger vor."),
    ],
    cards=["kohelet", "hevel", "unter-der-sonne"],
    fact="Derselbe Name, den das hebräische Wort hevel („Hauch“) trägt, gehört auch Abel, dem ersten Menschen, der in der Bibel stirbt (1Mo 4,2.8).",
    teaser="Der klügste Mann seiner Zeit setzt sich ein Ziel – und erklärt es dann selbst für ein Problem.")

sec("hauch", [R(PRED, 1, 12, 18)], "Der Versuch mit der Weisheit",
    "Der Prediger, König in Jerusalem, will mit Weisheit alles erforschen, was unter dem Himmel geschieht. Er sammelt mehr Weisheit als alle vor ihm – und kommt zu dem Schluss: Auch das ist ein Haschen nach Wind; mit viel Weisheit kommt viel Kummer.",
    place="jerusalem",
    quiz=[
        choice("Wie nennt der Prediger das Erforschen der Welt in V. 13?", ["Ein übles Geschäft, das Gott den Menschen gegeben hat", "Den Weg zum Glück", "Eine Aufgabe nur für Könige", "Ein Geschenk für die Weisen"], 13, "Lies Vers 13.",
               "V. 13: ein mühsames Geschäft, das Gott den Menschen gegeben hat, damit sie sich damit plagen."),
        error("Der Prediger sagt: Wer Erkenntnis vermehrt, vermehrt [Freude].", "Kummer", 18,
              "V. 18: Bei viel Weisheit ist viel Verdruss, und wer Erkenntnis vermehrt, vermehrt Kummer."),
    ],
    explain=[
        E("Hat Salomo das geschrieben?", "Die jüdische und christliche Tradition schrieb das Buch lange Salomo zu; V. 12 und 16 passen zu ihm. Der Talmud (Baba Batra 15a) nennt „Hiskia und seine Männer“ als die, die es aufschrieben. Sprache und Wortschatz gehören eher in eine spätere Zeit, das betonen auch konservative Ausleger wie Franz Delitzsch im 19. Jahrhundert. Viele lesen daher: Ein Weiser spricht bewusst mit der Stimme Salomos."),
        E("Was heißt „Haschen nach Wind“?", "Das hebräische Wort kann „Jagen nach Wind“ oder „Weiden des Windes“ heißen – man versucht, etwas festzuhalten, das sich nicht halten lässt. Der Ausdruck steht im Buch oft neben hevel."),
        E("Was meint V. 15?", "Wohl ein Sprichwort: Was krumm ist, lässt sich nicht gerade machen, was fehlt, nicht zählen. 7,13 greift es auf und nennt Gott als den, der gekrümmt hat."),
    ],
    cards=["salomo"],
    teaser="Häuser, Gärten, Musik, Reichtum: Der Prediger gönnt sich alles. Was er danach sagt, steht in einem einzigen Vers.")

sec("hauch", [R(PRED, 2, 1, 11)], "Der Versuch mit dem Vergnügen",
    "Der Prediger prüft die Freude: Wein, große Bauten, Gärten, Teiche, Knechte, Herden, Silber, Gold, Musik und Frauen. Er versagt sich nichts und hat Freude an seiner Arbeit. Doch als er auf alles schaut, findet er keinen Gewinn unter der Sonne.",
    place="jerusalem",
    quiz=[
        tf("Der Prediger sagt, er habe seinem Herzen keine Freude versagt.", True, 10, "Lies Vers 10.",
           "V. 10: Was seine Augen wünschten, hat er ihnen nicht verweigert."),
        choice("Was stellt der Prediger fest, als er sich seinen Werken zuwendet?", ["Es gibt keinen Gewinn unter der Sonne", "Er ist glücklicher als alle vor ihm", "Er hat noch nicht genug gebaut", "Gott ist zornig über ihn"], 11, "Lies Vers 11.",
               "V. 11: Alles war Hauch und Haschen nach Wind; es gibt keinen Gewinn unter der Sonne."),
        tf("Nach V. 9 bleibt ihm bei allem seine Weisheit.", True, 9, "Lies Vers 9.",
           "V. 9: Er wurde größer als alle vor ihm in Jerusalem, und seine Weisheit blieb bei ihm."),
    ],
    explain=[
        E("Wird hier Genuss verurteilt?", "Der Text sagt in V. 10, dass er Freude hatte – das wird nicht bestritten. Er fragt in V. 11 nach dem bleibenden Gewinn. Ausleger lesen das verschieden: als Absage an ein Leben, das nur genießt, oder als nüchterne Feststellung, dass auch Freude nicht festzuhalten ist."),
        E("Passt das zu Salomo?", "Die Liste erinnert an 1Kön 5–10: Bauten, Reichtum, Gold, Hofstaat. Viele Ausleger sehen darin ein bewusstes Rollenspiel: Wenn irgendjemand alles ausprobieren konnte, dann Salomo."),
    ],
    fact="Das Wort für „Parkanlagen“ in V. 5 ist pardes, ein Lehnwort aus dem Persischen. Über das Griechische wurde daraus unser Wort „Paradies“.",
    teaser="Weise oder dumm – am Ende trifft beide dasselbe. Und der Prediger findet das unerträglich.")

sec("hauch", [R(PRED, 2, 12, 17)], "Weise und Tor sterben gleich",
    "Weisheit ist besser als Torheit, wie Licht besser ist als Finsternis. Aber den Weisen trifft dasselbe Geschick wie den Toren: Beide sterben und werden vergessen. Da hasst der Prediger das Leben.",
    quiz=[
        choice("Womit vergleicht der Prediger den Vorzug der Weisheit?", ["Mit dem Vorzug des Lichts vor der Finsternis", "Mit Gold gegenüber Silber", "Mit einem Turm gegenüber einem Zelt", "Mit dem Wein gegenüber dem Wasser"], 13, "Lies Vers 13.",
               "V. 13: wie das Licht vor der Finsternis."),
        tf("Der Prediger sagt, dem Weisen werde ein ewiges Andenken zuteil.", False, 16, "Lies Vers 16.",
           "V. 16: Weder dem Weisen noch dem Toren bleibt ein ewiges Andenken."),
        choice("Wie reagiert der Prediger in V. 17?", ["Er hasst das Leben", "Er betet um Weisheit", "Er gibt seinen Reichtum weg", "Er schreibt ein Buch"], 17, "Lies Vers 17.",
               "V. 17: Da hasste ich das Leben, denn das Tun unter der Sonne missfiel mir."),
    ],
    explain=[
        E("Darf ein biblisches Buch so etwas sagen?", "Es steht da. Ähnlich ehrliche Sätze finden sich bei Hiob (Hiob 3; 10,1) und Jeremia (Jer 20,14–18). Die Rabbinen stritten im 1. Jahrhundert darüber, ob das Buch zur Heiligen Schrift gehört; nach dem Talmud (Schabbat 30b) wurde es behalten, weil Anfang und Ende Gottes Weisung enthalten."),
        E("Wer ist „der Mensch, der nach dem König kommt“ (V. 12)?", "Der Satz ist schwer zu übersetzen. Gemeint ist wohl: Ein Nachfolger kann nichts anderes tun als das, was schon getan wurde. Im nächsten Abschnitt wird der Nachfolger zum Problem."),
    ],
    cards=["tor"],
    teaser="Ein Leben lang gearbeitet – und wer bekommt es am Ende?")

sec("hauch", [R(PRED, 2, 18, 26)], "Für wen mühe ich mich?",
    "Der Prediger muss alles einem Nachfolger hinterlassen, von dem er nicht weiß, ob er weise oder töricht ist. Seine Tage sind Kummer, selbst nachts findet er keine Ruhe. Dann der erste Gegenklang: Essen, trinken und Freude an der Arbeit – das kommt aus Gottes Hand.",
    focus="Achte darauf, wie sich der Ton ab V. 24 ändert.",
    quiz=[
        choice("Was quält den Prediger in V. 18–19?", ["Dass er seine Mühe einem Nachfolger hinterlassen muss", "Dass er keine Kinder hat", "Dass sein Reich bedroht ist", "Dass er zu wenig verdient"], 18, "Lies Vers 18–19.",
               "V. 18–19: Er muss alles einem Menschen hinterlassen, von dem niemand weiß, ob er weise oder töricht sein wird."),
        tf("Nach V. 23 ruht das Herz des Menschen selbst in der Nacht nicht.", True, 23, "Lies Vers 23.",
           "V. 23: Seine Tage sind Kummer, selbst nachts ruht sein Herz nicht."),
        choice("Wovon hängt nach V. 24 das Genießen ab?", ["Von der Hand Gottes", "Vom eigenen Fleiß", "Vom Reichtum", "Von der Weisheit"], 24, "Lies Vers 24–25.",
               "V. 24–25: Auch das kommt aus der Hand Gottes – wer kann essen und genießen ohne ihn?"),
    ],
    explain=[
        E("Ist V. 24 ein Widerspruch zu V. 17?", "Ausleger lesen das verschieden. Manche sehen ein Ringen: Der Prediger schwankt zwischen Verzweiflung und Dankbarkeit. Andere sehen in diesen Freude-Versen, die immer wiederkehren (3,12–13; 5,17; 8,15; 9,7), die eigentliche Linie des Buches. Wieder andere lesen sie als bittere Resignation: Mehr bleibt eben nicht."),
        E("Was bedeutet V. 26?", "Gott gibt dem, der ihm gefällt, Weisheit und Freude; der Sünder sammelt für andere. Auch dieser Satz endet mit „auch das ist Hauch“. Ob sich das auf den Sünder oder auf alles Vorherige bezieht, ist unklar."),
    ],
    cards=["teil"],
    teaser="Der bekannteste Text des Buches – über die Zeit. Er wurde in den 1960ern ein Hit im Radio.")

# ───────────────────────── 2 · Alles hat seine Zeit ─────────────────────────
sec("zeit", [R(PRED, 3, 1, 8)], "Eine Zeit für alles",
    "Alles hat seine Zeit: geboren werden und sterben, pflanzen und ausreißen, weinen und lachen, schweigen und reden, lieben und hassen, Krieg und Frieden – vierzehn Gegensatzpaare.",
    quiz=[
        estimate("Wie viele Gegensatzpaare zählt der Prediger in V. 2–8 auf?", 5, 20, 14, "Paare",
                 "V. 2–8: 14 Paare, zweimal sieben – im Hebräischen jeweils zwei pro Zeile.", 2, "Zähl die Paare in Vers 2–8."),
        choice("Womit endet die Liste?", ["Mit Krieg und Frieden", "Mit Geburt und Tod", "Mit Lieben und Hassen", "Mit Schweigen und Reden"], 8, "Lies Vers 8.",
               "V. 8: Krieg hat seine Zeit, Frieden hat seine Zeit – das letzte Wort ist Frieden."),
    ],
    explain=[
        E("Ist das ein Trost oder eine Klage?", "Beides wird darin gehört. Manche lesen: Alles hat seinen guten Platz. Andere betonen, dass der Mensch die Zeiten nicht bestimmt, sondern ihnen ausgesetzt ist – V. 9–11 im nächsten Abschnitt greifen das auf."),
        E("Was heißt „Steinewerfen“ und „Steinesammeln“?", "Das ist unklar. Vorschläge: Steine vom Acker sammeln und Felder unbrauchbar machen (vgl. 2Kön 3,19.25); Bauen und Abreißen; im jüdischen Midrasch auch ein Bild für die eheliche Gemeinschaft, weil das nächste Paar vom Umarmen spricht."),
    ],
    fact="Der amerikanische Folk-Sänger Pete Seeger vertonte V. 1–8 als „Turn! Turn! Turn!“. In der Version der Byrds wurde es 1965 ein Nummer-eins-Hit in den USA – fast nur mit Bibeltext.",
    try_="Lies V. 2–8 langsam und such dir das Paar aus, das am besten zu deiner jetzigen Lebenszeit passt.",
    teaser="Gott hat etwas in das Herz des Menschen gelegt, das ihn nie ganz zur Ruhe kommen lässt.")

sec("zeit", [R(PRED, 3, 9, 15)], "Die Ewigkeit im Herzen",
    "Gott hat alles schön gemacht zu seiner Zeit und dem Menschen die Ewigkeit ins Herz gelegt – aber er kann Gottes Werk nicht von Anfang bis Ende erfassen. Sich freuen, essen und trinken ist eine Gabe Gottes. Was Gott tut, bleibt.",
    quiz=[
        choice("Was hat Gott nach V. 11 in das Herz der Menschen gelegt?", ["Die Ewigkeit", "Die Furcht vor dem Tod", "Das Gesetz", "Die Weisheit"], 11, "Lies Vers 11.",
               "V. 11: Er hat die Ewigkeit in ihr Herz gelegt – und doch kann der Mensch Gottes Werk nicht ganz erfassen."),
        tf("Nach V. 14 kann man dem, was Gott tut, noch etwas hinzufügen.", False, 14, "Lies Vers 14.",
           "V. 14: Man kann nichts hinzufügen und nichts wegnehmen."),
        who("Alles hat er schön gemacht zu seiner Zeit", R(PRED, 3, 11), ["Der Prediger über Gott", "Gott über den Menschen", "Salomo über den Tempel", "Der Prediger über den Weisen"],
            "V. 11: Der Prediger spricht über Gottes Werk."),
    ],
    explain=[
        E("Was heißt „Ewigkeit“ in V. 11?", "Hebräisch olam: die weite, unüberschaubare Zeit, Vergangenheit und Zukunft. Manche übersetzen „Sinn für die Dauer“, andere „Weltlauf“. Viele Christen hören darin eine Sehnsucht, die über das Leben hinausgeht – Augustinus hat diesen Gedanken berühmt formuliert (siehe Gebet)."),
        E("Was heißt „damit man sich vor ihm fürchte“ (V. 14)?", "Gemeint ist Gottesfurcht: Gott als den ernst nehmen, der größer ist. Das Wort taucht hier zum ersten Mal im Buch auf und kommt im letzten Satz wieder."),
    ],
    cards=["gottesfurcht"],
    prayer={"text": "Groß bist du, Herr, und hoch zu loben … Du hast uns zu dir hin geschaffen, und unruhig ist unser Herz, bis es ruht in dir.", "source": "Augustinus, Bekenntnisse I,1"},
    teaser="Ist der Mensch mehr als ein Tier? Der Prediger stellt die Frage – und lässt sie offen.")

sec("zeit", [R(PRED, 3, 16, 22)], "Mensch und Tier",
    "Selbst an der Stätte des Rechts findet der Prediger Unrecht. Gott wird richten. Doch Mensch und Tier haben dasselbe Geschick: Beide sterben, beide kehren zum Staub zurück. Wer weiß, wohin der Atem des Menschen geht?",
    quiz=[
        choice("Was findet der Prediger an der Stätte des Rechts?", ["Gottlosigkeit", "Weisheit", "Arme, die Recht bekommen", "Einen gerechten König"], 16, "Lies Vers 16.",
               "V. 16: Dort, wo Recht gesprochen werden sollte, war Unrecht."),
        error("Alles ist aus dem [Wasser] geworden, und alles kehrt dorthin zurück.", "Staub", 20,
              "V. 20: aus dem Staub – vgl. 1Mo 3,19."),
        tf("Der Prediger stellt in V. 21 eine Frage, statt eine Antwort zu geben.", True, 21, "Lies Vers 21.",
           "V. 21: Wer weiß, ob der Atem des Menschen nach oben fährt?"),
    ],
    explain=[
        E("Was heißt „Odem“?", "Hebräisch ruach: Atem, Wind, Geist. Dasselbe Wort steht in 12,7, wo der Geist zu Gott zurückkehrt. Die Übersetzung entscheidet, ob man hier eher „Atem“ oder „Geist“ liest.", "elbbk"),
        E("Ist V. 21 eine Frage?", "Die meisten Übersetzungen lesen eine Frage. Die jüdischen Gelehrten, die im Mittelalter die Vokale in den hebräischen Text setzten (Masoreten), lasen dagegen eine Aussage: der Atem des Menschen, der nach oben fährt. Beide Lesarten sind sprachlich möglich."),
        E("Was glaubten Israeliten über das Leben nach dem Tod?", "Das Alte Testament spricht meist zurückhaltend und schattenhaft vom Ort der Toten (Scheol). Die Hoffnung auf Auferstehung tritt erst in späteren Texten deutlich hervor (Jes 26,19; Dan 12,2). Christen lesen den Prediger deshalb oft zusammen mit dem Neuen Testament, etwa 1Kor 15."),
    ],
    teaser="Tränen, und niemand tröstet. Der Prediger beneidet sogar die, die nie geboren wurden.")

sec("zeit", [R(PRED, 4, 1, 8)], "Tränen ohne Tröster",
    "Der Prediger sieht die Tränen der Unterdrückten, die keinen Tröster haben. Er preist die Toten und noch mehr die Ungeborenen. Arbeit entsteht aus Neid; besser eine Handvoll Ruhe als zwei Fäuste voll Mühe. Und da ist einer allein, der arbeitet ohne Ende und nicht weiß, für wen.",
    quiz=[
        tf("Der Prediger sagt zweimal, dass die Unterdrückten keinen Tröster haben.", True, 1, "Lies Vers 1.",
           "V. 1: Zweimal steht derselbe Satz – sie hatten keinen Tröster."),
        choice("Was ist nach V. 6 besser?", ["Eine Handvoll Ruhe als zwei Fäuste voll Mühe", "Viel Arbeit als wenig Brot", "Ein voller Speicher als ein leerer Magen", "Ein Freund als ein Bruder"], 6, "Lies Vers 6.",
               "V. 6: eine Hand voll Ruhe statt beider Fäuste voll Mühe und Haschen nach Wind."),
        choice("Welche Frage stellt sich der Einzelne in V. 8?", ["Für wen er sich eigentlich abmüht", "Wie er noch reicher werden kann", "Wann er sterben wird", "Wer sein Feind ist"], 8, "Lies Vers 8.",
               "V. 8: Für wen mühe ich mich und gönne mir selbst nichts Gutes?"),
    ],
    explain=[
        E("Woher kommt Arbeit laut V. 4?", "Aus Eifersucht oder Rivalität: Man will mehr haben als der andere. Das hebräische Wort kann Eifer, Neid oder Konkurrenz bedeuten."),
        E("Warum zwei Sprichwörter nebeneinander (V. 5–6)?", "Der Tor faltet die Hände und verzehrt sich selbst – Faulheit ist keine Lösung. Aber zwei Fäuste voll Mühe auch nicht. Der Prediger stellt die beiden Sprüche nebeneinander, ohne den Mittelweg zu benennen."),
    ],
    teaser="Ein Bild, das bis heute bei Hochzeiten vorgelesen wird – obwohl es gar nicht um Hochzeit geht.")

sec("zeit", [R(PRED, 4, 9, 16)], "Zwei sind besser als einer",
    "Zwei sind besser als einer: Fällt einer, hilft ihm der andere auf; zu zweit wird man warm, zu zweit widersteht man. Eine dreifache Schnur reißt nicht so schnell. Dann eine Geschichte von einem jungen König, der einen alten ablöst – und auch er wird vergessen.",
    quiz=[
        order("In welcher Reihenfolge nennt der Prediger die Vorteile von zweien?", ["Einer hilft dem anderen auf", "Zu zweit wird man warm", "Zu zweit widersteht man einem Angreifer"],
              "V. 10–12: aufhelfen, wärmen, widerstehen – und dann die dreifache Schnur.", "Lies Vers 10–12."),
        choice("Wer ist nach V. 13 besser als ein alter, törichter König?", ["Ein armer, weiser junger Mann", "Ein reicher Kaufmann", "Ein Prophet", "Ein mutiger Soldat"], 13, "Lies Vers 13.",
               "V. 13: ein armer und weiser Jüngling, der sich noch warnen lässt."),
    ],
    explain=[
        E("Wer ist die dritte Schnur?", "Der Text sagt es nicht. Er spricht von zweien und steigert dann zu drei – eine typische Form in Sprichwörtern (vgl. Spr 30,15–31). Christliche Ausleger sehen darin oft Gott als den Dritten, besonders bei Hochzeiten; andere lesen es einfach als: Je mehr, desto stärker."),
        E("Wer ist der junge König in V. 13–16?", "Die Geschichte nennt keine Namen. Ausleger haben an Josef (aus dem Gefängnis zum Herrscher) oder an David und Saul gedacht. Vielleicht ist es ein Gleichnis. Ihr Schluss: Auch der Beliebte wird von der nächsten Generation vergessen."),
    ],
    try_="Lies V. 9–12 und zähl, wie oft „einer“ und „zwei“ vorkommen.",
    teaser="Der Prediger geht in den Tempel – und rät, vor allem den Mund zu halten.")

# ───────────────────────── 3 · Worte und Geld ─────────────────────────
sec("geld", [R(PRED, 4, 17), R(PRED, 5, 1, 6)], "Wenige Worte vor Gott",
    "Geh mit Bedacht zum Haus Gottes; hören ist besser als die Opfer der Toren. Sei nicht vorschnell mit dem Mund, denn Gott ist im Himmel und du auf der Erde: Darum seien deine Worte wenige. Ein Gelübde soll man halten – besser gar nicht geloben.",
    quiz=[
        choice("Warum sollen die Worte vor Gott wenige sein?", ["Weil Gott im Himmel ist und der Mensch auf der Erde", "Weil Gott schon alles weiß", "Weil im Tempel Stille geboten ist", "Weil die Priester sonst zürnen"], 1, "Lies Vers 5,1.",
               "Pred 5,1: Gott ist im Himmel, du bist auf der Erde – darum seien deiner Worte wenige."),
        tf("Der Prediger rät: Besser nicht geloben als geloben und nicht halten.", True, 4, "Lies Vers 5,4.",
           "Pred 5,4: Besser, du gelobst nicht, als dass du gelobst und nicht erfüllst."),
        choice("Was ist nach 4,17 besser als die Schlachtopfer der Toren?", ["Herzukommen, um zu hören", "Ein größeres Opfer", "Ein langes Gebet", "Zu Hause zu bleiben"], 17, "Lies Vers 4,17.",
               "Pred 4,17: Nahen, um zu hören, ist besser."),
    ],
    explain=[
        E("Warum fängt das Kapitel mit 4,17 an?", "In vielen englischen Bibeln ist 4,17 schon 5,1. Die deutsche und hebräische Zählung verschiebt sich hier um einen Vers; der Gedanke gehört zu Kapitel 5."),
        E("Wer ist der „Bote Gottes“ (5,5)?", "Wahrscheinlich ein Priester, der das Gelübde entgegennahm (vgl. Mal 2,7, wo der Priester „Bote des HERRN“ heißt). Die Septuaginta liest „vor Gott“."),
        E("Gibt es Parallelen im Neuen Testament?", "Jesus warnt vor vielen Worten beim Beten (Mt 6,7–8) und vor leichtfertigem Schwören (Mt 5,33–37). Jak 1,19 rät, schnell zum Hören und langsam zum Reden zu sein."),
    ],
    teaser="Wer Geld liebt, wird nicht satt – und wer viel hat, kann nachts nicht schlafen.")

sec("geld", [R(PRED, 5, 7, 16)], "Wer Geld liebt",
    "Unterdrückung wundert den Prediger nicht: Über jedem Hohen lauert ein Höherer. Wer Geld liebt, wird nicht satt. Der Arbeiter schläft süß, den Reichen hält der Überfluss wach. Reichtum kann verloren gehen; nackt, wie er kam, geht der Mensch.",
    quiz=[
        choice("Wer schläft nach V. 11 süß?", ["Der Arbeiter, ob er wenig oder viel isst", "Der Reiche nach einem Fest", "Der König in seinem Palast", "Der Weise nach dem Studium"], 11, "Lies Vers 11.",
               "V. 11: Der Schlaf des Arbeiters ist süß; den Reichen lässt sein Überfluss nicht schlafen."),
        error("Wie er aus dem Leib seiner Mutter kam, so geht er [reich] wieder hin.", "nackt", 14,
              "V. 14: nackt, wie er gekommen ist – vgl. Hiob 1,21."),
        tf("Nach V. 9 wird satt, wer das Geld liebt.", False, 9, "Lies Vers 9.",
           "V. 9: Wer Geld liebt, wird des Geldes nicht satt."),
    ],
    explain=[
        E("Was meint V. 7?", "Ein Blick in die Verwaltung eines großen Reiches: Beamte über Beamten, jeder überwacht den unter ihm – und jeder nimmt seinen Teil. Ob das resigniert oder kritisch gemeint ist, bleibt offen."),
        E("Wo kommt der Gedanke von V. 14 noch vor?", "Hiob sagt nach dem Verlust seiner Kinder und seines Besitzes fast dasselbe (Hiob 1,21). Paulus greift es in 1Tim 6,7 auf: Wir haben nichts in die Welt gebracht und können nichts hinausbringen."),
    ],
    fact="V. 9 ist in vielen Sprachen sprichwörtlich geworden. Der Gedanke steht ähnlich in 1Tim 6,10: Die Liebe zum Geld ist eine Wurzel allen Übels.",
    teaser="Zwei Menschen, beide reich. Der eine kann genießen, der andere nicht. Was macht den Unterschied?")

sec("geld", [R(PRED, 5, 17, 19), R(PRED, 6, 1, 6)], "Genießen können ist eine Gabe",
    "Gut ist, zu essen, zu trinken und Freude an der Arbeit zu haben – wenn Gott es gewährt, ist es eine Gabe. Doch es gibt einen, dem Gott Reichtum gibt, aber nicht die Möglichkeit, ihn zu genießen. Lebt er auch tausend Jahre doppelt – eine Fehlgeburt hat es besser.",
    focus="Achte darauf, was Gott jeweils gibt – und was nicht.",
    quiz=[
        choice("Was nennt der Prediger in 5,18 eine Gabe Gottes?", ["Reichtum genießen und sich bei der Arbeit freuen können", "Reichtum zu besitzen", "Viele Söhne zu haben", "Ein langes Leben"], 18, "Lies Vers 5,18.",
               "Pred 5,18: Nicht nur Güter, sondern die Fähigkeit, sie zu genießen, ist Gottes Gabe."),
        tf("Nach 6,2 gibt es Menschen, denen Gott Reichtum gibt, aber nicht die Möglichkeit, ihn zu genießen.", True, 2, "Lies Vers 6,2.",
           "Pred 6,2: Gott ermächtigt ihn nicht, davon zu genießen – ein Fremder genießt es."),
    ],
    explain=[
        E("Ist 6,3 nicht grausam?", "Der Satz ist absichtlich drastisch. Hundert Söhne und ein langes Leben galten als höchster Segen (vgl. 1Mo 25,8). Der Prediger stellt dagegen: Ohne Freude am Guten wiegt das alles nichts. Ähnlich bitter wünscht sich Hiob, nie geboren zu sein (Hiob 3,11–16)."),
        E("Wie lesen Ausleger 5,19?", "Wem Gott Freude gibt, der denkt nicht viel über die Kürze seiner Tage nach. Manche lesen das als Trost: Freude füllt das Leben aus. Andere als Ablenkung: Die Freude lässt vergessen, wie kurz es ist."),
    ],
    try_="Lies 5,17–19 und 6,1–2 nacheinander. Welches Wort oder welche Wendung kommt in beiden Teilen vor?",
    teaser="Lieber auf eine Beerdigung als auf eine Party? Der Prediger meint das ernst.")

# ───────────────────────── 4 · Besser als … ─────────────────────────
sec("besser", [R(PRED, 7, 1, 10)], "Lieber ins Trauerhaus",
    "Eine Reihe von Sprüchen mit „besser als“: ein guter Name statt Salböl, der Todestag statt des Geburtstags, das Haus der Trauer statt des Festhauses, Schelte der Weisen statt Lieder der Toren. Und: Frag nicht, warum früher alles besser war.",
    bridge="Der Prediger hat in 6,7–12 gefragt, wer denn wissen kann, was für den Menschen gut ist. Kapitel 7 antwortet mit einer Reihe von Vergleichen.",
    quiz=[
        choice("Wohin zu gehen ist nach V. 2 besser?", ["In das Haus der Trauer", "In das Haus des Festes", "In den Tempel", "In das Haus der Weisen"], 2, "Lies Vers 2.",
               "V. 2: ins Haus der Trauer, denn dort sieht man das Ende aller Menschen."),
        tf("Der Prediger hält die Frage, warum früher alles besser war, für weise.", False, 10, "Lies Vers 10.",
           "V. 10: Du fragst nicht aus Weisheit danach."),
        choice("Womit vergleicht der Prediger das Lachen des Toren?", ["Mit dem Knistern von Dornen unter dem Topf", "Mit dem Rauschen des Meeres", "Mit dem Bellen eines Hundes", "Mit dem Wind in der Wüste"], 6, "Lies Vers 6.",
               "V. 6: wie das Knistern der Dornen unter dem Topf – laut, schnell und bald vorbei."),
    ],
    explain=[
        E("Warum der Todestag besser als der Geburtstag?", "Der Text begründet es in V. 2: Am Ende sieht man, was ein Leben war, und die Lebenden nehmen es sich zu Herzen. Ausleger lesen das unterschiedlich – als Lebensweisheit (das Ende gibt Klarheit) oder als Ausdruck von Lebensmüdigkeit wie in 4,2."),
        E("Was ist das Wortspiel in V. 1 und 6?", "Im Hebräischen klingen Name (schem) und Salböl (schemen) fast gleich. In V. 6 klingen Dornen (sirim) und Topf (sir) gleich – es knistert auch im Klang."),
    ],
    cards=["weisheit"],
    teaser="Ein Rat, den man in einem frommen Buch nicht erwartet: Sei nicht zu gerecht.")

sec("besser", [R(PRED, 7, 13, 22)], "Sei nicht allzu gerecht",
    "Gute und schlechte Tage hat Gott beide gemacht. Der Prediger sieht Gerechte, die umkommen, und Gottlose, die lange leben. Sein Rat: Sei nicht allzu gerecht und nicht allzu gottlos. Es gibt keinen Gerechten, der nicht sündigt – und du hast selbst oft über andere geflucht.",
    quiz=[
        choice("Was soll man nach V. 14 am Tag des Unglücks bedenken?", ["Dass Gott auch diesen Tag gemacht hat", "Dass das Glück bald zurückkommt", "Dass man selbst schuld ist", "Dass die Feinde bestraft werden"], 14, "Lies Vers 14.",
               "V. 14: Gott hat den einen wie den anderen gemacht."),
        tf("Nach V. 20 gibt es Menschen auf der Erde, die nur Gutes tun und nie sündigen.", False, 20, "Lies Vers 20.",
           "V. 20: Es gibt keinen Gerechten auf der Erde, der Gutes tut und nicht sündigt."),
        choice("Warum soll man nicht auf alles hören, was geredet wird (V. 21–22)?", ["Weil man sonst hört, wie der eigene Knecht flucht – und man selbst hat es auch getan", "Weil Gerüchte immer falsch sind", "Weil der König Spione hat", "Weil Weise nicht zuhören müssen"], 22, "Lies Vers 21–22.",
               "V. 21–22: Du weißt selbst, dass du anderen oft geflucht hast."),
    ],
    explain=[
        E("Was heißt „allzu gerecht“?", "Ausleger lesen das verschieden: als Warnung vor Selbstgerechtigkeit, die sich für besser hält; vor übertriebener Gewissenhaftigkeit, die sich selbst zerstört; oder als nüchterne Beobachtung, dass Gerechtigkeit allein kein langes Leben garantiert (V. 15). Der Schluss in V. 18 verweist auf die Gottesfurcht."),
        E("Wo zitiert das Neue Testament einen ähnlichen Gedanken?", "Paulus stellt in Röm 3,10–12 Verse aus den Psalmen zusammen: Keiner ist gerecht, auch nicht einer. Der Gedanke ähnelt Pred 7,20 und 1Kön 8,46."),
    ],
    teaser="Eine Stelle über Frauen, bei der man schlucken muss. Und gleich danach ein Satz, der alles noch einmal anders klingen lässt.")

sec("besser", [R(PRED, 7, 23, 29)], "„Bitterer als der Tod“",
    "Der Prediger will weise werden, aber die Weisheit bleibt fern. Er findet etwas, das bitterer ist als der Tod: eine Frau wie ein Netz. Einen Mann unter tausend habe er gefunden, eine Frau nicht. Doch dann: Gott hat den Menschen aufrichtig gemacht, aber sie suchen viele Künste.",
    focus="Lies V. 29 genau: Von wem ist dort die Rede?",
    quiz=[
        tf("Der Prediger sagt, er habe die Weisheit erreicht, die er suchte.", False, 23, "Lies Vers 23–24.",
           "V. 23–24: Er wollte weise werden, aber sie blieb fern – tief, tief, wer kann sie finden?"),
        choice("Was hat Gott nach V. 29 gemacht?", ["Den Menschen aufrichtig", "Die Frau als Netz", "Den Mann weiser als die Frau", "Die Weisheit unerreichbar"], 29, "Lies Vers 29.",
               "V. 29: Gott hat den Menschen (hebräisch adam, Mann und Frau) aufrichtig geschaffen; sie aber suchen viele Künste."),
    ],
    explain=[
        E("Wie lesen Ausleger V. 26–28?", "Verschieden. (1) Als bittere persönliche Erfahrung des Sprechers, die die Bibel ehrlich stehen lässt. (2) Als Rede über die „Frau Torheit“, die in Spr 7 und 9,13–18 als verführerische Frau auftritt. (3) Als zitierte Meinung, die der Prediger in V. 29 korrigiert: Nicht die Frauen sind das Problem, sondern alle Menschen."),
        E("Was bedeutet „Mensch“ in V. 29?", "Hebräisch adam, wie in 1Mo 1,27: der Mensch, Mann und Frau. In V. 28 steht dagegen ein anderes Wort, das nur den Mann meint. Viele Ausleger halten diesen Wechsel für bewusst."),
        E("„Einen unter tausend“ – eine Anspielung?", "Manche Ausleger erinnern an Salomo, der nach 1Kön 11,3 siebenhundert Frauen und dreihundert Nebenfrauen hatte – zusammen tausend. In der Rolle Salomos klingt der Satz dann wie ein Selbsturteil."),
    ],
    teaser="Böse Menschen werden in Ehren begraben, gute vergessen. Und der Prediger sagt: Ich weiß trotzdem etwas.")

sec("besser", [R(PRED, 8, 10, 17)], "Wenn es den Bösen gut geht",
    "Gottlose werden ehrenvoll begraben, Gerechte vergessen. Weil die Strafe auf sich warten lässt, tun Menschen Böses. Und doch weiß der Prediger, dass es den Gottesfürchtigen gut gehen wird. Er preist die Freude – und gibt zu: Gottes Werk kann niemand ganz erfassen.",
    bridge="In 8,1–9 hat der Prediger über den Umgang mit der Macht des Königs gesprochen: Man soll vorsichtig sein, denn niemand hat Macht über den Tag seines Todes.",
    quiz=[
        choice("Warum tun Menschen nach V. 11 leichter Böses?", ["Weil das Urteil über böse Taten nicht schnell vollzogen wird", "Weil es kein Gesetz gibt", "Weil der König selbst böse ist", "Weil sie arm sind"], 11, "Lies Vers 11.",
               "V. 11: Weil das Urteil nicht schnell kommt, ist das Herz der Menschen voll, Böses zu tun."),
        tf("In V. 12–13 sagt der Prediger, dass es den Gottesfürchtigen gut gehen wird.", True, 12, "Lies Vers 12–13.",
           "V. 12: obwohl ich weiß, dass es denen gut geht, die Gott fürchten."),
        choice("Was kann der Mensch nach V. 17 nicht?", ["Das Werk Gottes ganz erfassen", "Sich freuen", "Arbeiten", "Gott fürchten"], 17, "Lies Vers 17.",
               "V. 17: Selbst der Weise kann es nicht erfassen, auch wenn er meint, es zu kennen."),
    ],
    explain=[
        E("Widerspricht sich der Prediger in V. 12–14?", "Erst sagt er, es werde den Gottesfürchtigen gut gehen; dann, dass Gerechten widerfährt, was Gottlose verdienen. Manche Ausleger sehen hier ein Zitat der üblichen Lehre, das er prüft. Andere lesen ein Bekenntnis, das er trotz der Erfahrung festhält. Wieder andere sehen beides nebeneinander stehen – wie in vielen Psalmen (Ps 73)."),
    ],
    teaser="Ein Rat, der in einem alten babylonischen Epos fast genauso steht: Iss dein Brot mit Freude.")

sec("besser", [R(PRED, 9, 1, 10)], "Iss dein Brot mit Freude",
    "Gerechte und Weise sind in Gottes Hand, doch alle trifft dasselbe Geschick. Ein lebender Hund ist besser als ein toter Löwe; die Toten wissen nichts mehr. Darum: Iss dein Brot mit Freude, trink deinen Wein, genieße das Leben mit der Frau, die du liebst. Was du tun kannst, tu.",
    quiz=[
        choice("Was ist nach V. 4 besser als ein toter Löwe?", ["Ein lebendiger Hund", "Ein weiser Mann", "Ein voller Speicher", "Ein guter Name"], 4, "Lies Vers 4.",
               "V. 4: Wer zu den Lebenden gehört, hat Hoffnung – ein lebendiger Hund ist besser als ein toter Löwe."),
        order("Bring die Aufforderungen in V. 7–10 in die richtige Reihenfolge.",
              ["Iss dein Brot mit Freude", "Deine Kleider seien weiß", "Genieße das Leben mit der Frau, die du liebst", "Was du tun kannst, tu mit deiner Kraft"],
              "V. 7–10: Brot und Wein, weiße Kleider und Öl, das Leben mit der geliebten Frau, und tun, was man kann."),
        tf("Nach V. 7 hat Gott längst Gefallen an deinem Tun.", True, 7, "Lies Vers 7.",
           "V. 7: denn längst hat Gott Wohlgefallen an deinem Tun."),
    ],
    explain=[
        E("Was heißt „die Toten wissen gar nichts“ (V. 5)?", "Christen ordnen den Vers verschieden ein. Siebenten-Tags-Adventisten und Zeugen Jehovas verstehen ihn wörtlich: Die Toten sind bis zur Auferstehung ohne Bewusstsein. Die meisten anderen Kirchen lesen ihn vom Blick „unter der Sonne“ her (V. 6): Die Toten haben keinen Anteil mehr am Leben auf der Erde. Sie verweisen auf Stellen wie Lk 23,43 und Phil 1,23."),
        E("Was bedeuten weiße Kleider und Öl?", "Zeichen der Freude und des Festes. Weiß war die Farbe für Feiertage, Öl auf dem Kopf erfrischte in der Hitze und gehörte zu Festen (Ps 23,5; 104,15)."),
        E("Was ist der Scheol?", "Der Ort der Toten im Alten Testament, als still und schattenhaft gedacht. V. 10: Dort gibt es kein Tun, kein Planen, kein Wissen mehr.", "elbbk"),
    ],
    cards=["scheol"],
    fact="Im babylonischen Gilgamesch-Epos rät die Schankwirtin Siduri dem Helden fast dasselbe wie V. 7–9: Iss und trink, trag saubere Kleider, wasch dich und freu dich an deiner Frau. Der Prediger kannte solche Weisheit seiner Umwelt offenbar.",
    memory_verse=MV(R(PRED, 9, 7), "Geh, iss dein Brot mit Freude und trink deinen Wein mit frohem Herzen"),
    teaser="Ein armer Weiser rettet eine ganze Stadt. Wie dankt man es ihm?")

sec("besser", [R(PRED, 9, 11, 18)], "Zeit und Zufall",
    "Nicht die Schnellen gewinnen den Lauf und nicht die Helden den Krieg; Zeit und Zufall treffen alle. Eine kleine Stadt wird belagert, ein armer Weiser rettet sie – und niemand denkt mehr an ihn. Weisheit ist besser als Kraft, aber die Weisheit des Armen wird verachtet.",
    quiz=[
        choice("Was trifft nach V. 11 alle?", ["Zeit und Zufall", "Gottes Zorn", "Der Neid der anderen", "Die Strafe des Königs"], 11, "Lies Vers 11.",
               "V. 11: Zeit und Schicksal (Zufall) trifft sie alle."),
        error("Ein armer, weiser Mann rettete die Stadt, und alle [ehrten] ihn.", "vergaßen", 15,
              "V. 15: Kein Mensch dachte an diesen armen Mann."),
        tf("Der Prediger schließt, dass Kraft besser sei als Weisheit.", False, 16, "Lies Vers 16.",
           "V. 16: Weisheit ist besser als Kraft – auch wenn die Weisheit des Armen verachtet wird."),
    ],
    explain=[
        E("Was heißt „Zufall“ hier?", "Hebräisch pega’, „Begegnung, Vorfall“: das, was einem zustößt. Es ist kein Wort für blindes Schicksal gegen Gott; V. 1 desselben Kapitels sagt, dass alle in Gottes Hand sind. Der Mensch kann es nur nicht voraussehen (V. 12)."),
        E("Ist die Geschichte von der Stadt wirklich passiert?", "Der Text nennt weder Stadt noch König. Ausleger haben an 2Sam 20,14–22 gedacht, wo eine weise Frau ihre Stadt rettet. Meist liest man es als Beispielgeschichte."),
    ],
    teaser="Brot aufs Wasser werfen – Wahnsinn oder Weisheit?")

# ───────────────────────── 5 · Bevor die silberne Schnur reißt ─────────────────────────
sec("schnur", [R(PRED, 11, 1, 6)], "Wirf dein Brot aufs Wasser",
    "Wirf dein Brot auf das Wasser, nach vielen Tagen wirst du es finden. Verteile auf sieben, ja acht, denn du weißt nicht, was kommt. Wer auf den Wind achtet, sät nie. Du kennst Gottes Werk nicht – darum säe morgens und abends.",
    bridge="Kapitel 10 sammelt Sprüche über Weise und Toren, über Herrscher und über Arbeit: tote Fliegen verderben das Salböl, wer eine Grube gräbt, fällt hinein, ein stumpfes Eisen kostet mehr Kraft.",
    quiz=[
        choice("Wer wird nach V. 4 nicht säen?", ["Wer auf den Wind achtet", "Wer kein Saatgut hat", "Wer faul ist", "Wer in der Stadt wohnt"], 4, "Lies Vers 4.",
               "V. 4: Wer auf den Wind achtet, sät nicht; wer auf die Wolken sieht, erntet nicht."),
        tf("Nach V. 6 soll man morgens säen und abends die Hand nicht ruhen lassen.", True, 6, "Lies Vers 6.",
           "V. 6: Du weißt nicht, was gedeiht – dieses, jenes oder beides."),
        choice("Womit vergleicht V. 5 das Unwissen über Gottes Werk?", ["Mit dem Weg des Windes und dem Werden eines Kindes im Mutterleib", "Mit der Tiefe des Meeres", "Mit der Zahl der Sterne", "Mit dem Lauf der Sonne"], 5, "Lies Vers 5.",
               "V. 5: So wenig du weißt, wie die Gebeine im Leib der Schwangeren entstehen, so wenig kennst du Gottes Werk."),
    ],
    explain=[
        E("Was heißt „Brot aufs Wasser werfen“?", "Zwei alte Deutungen: Die jüdische Tradition liest es als Wohltätigkeit – gib, auch wenn du keinen Rückfluss erwartest. Andere denken an Handel über das Meer: Getreide auf Schiffe laden und erst nach langer Zeit Gewinn sehen. V. 2 (verteile auf sieben oder acht) passt zu beiden."),
        E("Ist das ein Aufruf zur Vorsicht oder zum Wagnis?", "Beides wird darin gehört: Weil man die Zukunft nicht kennt, soll man das Risiko verteilen (V. 2) – und trotzdem handeln, statt ewig auf das richtige Wetter zu warten (V. 4)."),
    ],
    teaser="Freu dich in deiner Jugend – aber mit einem Nachsatz, der hellhörig macht.")

sec("schnur", [R(PRED, 11, 7, 10), R(PRED, 12, 1)], "Freu dich in deiner Jugend",
    "Süß ist das Licht, gut tut es, die Sonne zu sehen. Wer lange lebt, soll sich an allen Jahren freuen und an die dunklen Tage denken. Freu dich, junger Mensch, folge deinem Herzen – und wisse, dass Gott dich für alles zur Rechenschaft zieht. Denk an deinen Schöpfer in deiner Jugend.",
    focus="Achte darauf, was der Prediger dem jungen Menschen zuerst sagt und was danach kommt.",
    quiz=[
        tf("Der Prediger fordert den jungen Menschen auf, sich zu freuen.", True, 9, "Lies Vers 11,9.",
           "Pred 11,9: Freue dich, junger Mann, in deiner Jugend, und dein Herz mache dich fröhlich."),
        choice("Woran soll man nach 12,1 in der Jugend denken?", ["An den Schöpfer", "An das Alter", "An die Eltern", "An den Reichtum"], 1, "Lies Vers 12,1.",
               "Pred 12,1: Gedenke deines Schöpfers in den Tagen deiner Jugend."),
        choice("Was ist nach 11,7 süß?", ["Das Licht", "Der Wein", "Die Liebe", "Der Schlaf"], 7, "Lies Vers 11,7.",
               "Pred 11,7: Süß ist das Licht, und gut für die Augen, die Sonne zu sehen."),
    ],
    explain=[
        E("Ist das Gericht in 11,9 eine Drohung?", "Ausleger lesen es unterschiedlich: als Warnung, die Freude nicht maßlos werden zu lassen; als Ermutigung, weil Gott sich für das Leben des Menschen interessiert; oder als Erinnerung, dass auch die Freude vor Gott verantwortet wird. Der Satz steht mitten in einer Aufforderung zur Freude."),
        E("Warum „Schöpfer“?", "Ein seltenes Wort, hier in Mehrzahlform (wie Elohim). Es erinnert an 1Mo 1 und an 12,7, wo der Geist zu Gott zurückkehrt. Einige jüdische Ausleger hörten darin auch ein Wortspiel mit „Brunnen“ und „Grube“ – Ursprung und Grab."),
    ],
    teaser="Ein Haus, dessen Wächter zittern und dessen Fenster dunkel werden. Was beschreibt der Prediger da wirklich?")

sec("schnur", [R(PRED, 12, 2, 8)], "Das Haus, das verfällt",
    "Bevor Sonne und Licht dunkel werden: Die Hüter des Hauses zittern, die Müllerinnen hören auf, die Fenster verdunkeln sich, der Mandelbaum blüht. Der Mensch geht in sein ewiges Haus. Bevor die silberne Schnur reißt und der Staub zur Erde und der Geist zu Gott zurückkehrt. Hauch der Hauche, alles ist Hauch.",
    quiz=[
        choice("Was kehrt nach V. 7 zu Gott zurück?", ["Der Geist", "Der Staub", "Der Name", "Die Weisheit"], 7, "Lies Vers 7.",
               "V. 7: Der Staub kehrt zur Erde zurück, der Geist zu Gott, der ihn gegeben hat."),
        tf("Das Buch endet in V. 8 mit denselben Worten, mit denen es in 1,2 begonnen hat.", True, 8, "Lies Vers 8 und 1,2.",
           "V. 8: Hauch der Hauche, alles ist Hauch – der Rahmen des Buches schließt sich."),
    ],
    explain=[
        E("Was bedeuten die Bilder?", "Schon der Talmud (Schabbat 151b–152a) liest V. 3–5 als Beschreibung des Alterns: Die Hüter des Hauses sind die zitternden Hände, die starken Männer die gebeugten Beine, die Müllerinnen die wenigen Zähne, die durch die Fenster Sehenden die Augen, der blühende Mandelbaum das weiße Haar. Andere lesen ein Bild für einen Sturm oder den Untergang einer Stadt."),
        E("Was ist die silberne Schnur?", "Wahrscheinlich ein Bild von einer Lampe: eine goldene Ölschale, die an einer silbernen Kette hängt. Reißt die Kette, zerbricht die Schale und das Licht geht aus. Eimer und Rad am Brunnen sind ein zweites Bild: Das Wasser kann nicht mehr geschöpft werden."),
        E("Wie passt V. 7 zu 3,21?", "In 3,21 fragt der Prediger, wer weiß, ob der Atem nach oben fährt. Hier sagt er, der Geist kehre zu Gott zurück. Manche lesen das als Antwort, andere schlicht als Umkehrung von 1Mo 2,7: Gott hat den Atem gegeben, nun nimmt er ihn zurück."),
    ],
    try_="Lies V. 3–5 und versuch, jedem Bild einen Körperteil zuzuordnen. Bei welchen klappt es, bei welchen nicht?",
    teaser="Am Ende spricht plötzlich jemand anderes – über den Prediger.")

sec("schnur", [R(PRED, 12, 9, 14)], "Das Ende der Sache",
    "Jemand spricht nun über den Prediger: Er war weise, lehrte das Volk, ordnete viele Sprüche und suchte gefällige, wahre Worte. Worte der Weisen sind wie Treibstacheln. Viel Büchermachen hat kein Ende. Das Ergebnis: Fürchte Gott und halte seine Gebote, denn Gott bringt jedes Werk ins Gericht.",
    focus="Achte darauf, wie hier über den Prediger gesprochen wird.",
    quiz=[
        choice("Womit werden die Worte der Weisen in V. 11 verglichen?", ["Mit Treibstacheln und eingeschlagenen Nägeln", "Mit Honig und Milch", "Mit Gold und Silber", "Mit Licht und Salz"], 11, "Lies Vers 11.",
               "V. 11: wie Treibstacheln, wie eingeschlagene Nägel – sie treiben an und halten fest."),
        tf("Der Sprecher in V. 12 rät, möglichst viele Bücher zu schreiben.", False, 12, "Lies Vers 12.",
           "V. 12: Des vielen Büchermachens ist kein Ende, und viel Studieren ermüdet den Leib."),
        choice("Was ist nach V. 13 das Endergebnis?", ["Fürchte Gott und halte seine Gebote", "Alles ist Hauch", "Iss und trink mit Freude", "Suche Weisheit"], 13, "Lies Vers 13.",
               "V. 13: Fürchte Gott und halte seine Gebote, denn das ist der ganze Mensch."),
    ],
    explain=[
        E("Wer spricht hier?", "Ab V. 9 wird über den Prediger in der dritten Person gesprochen, wie schon in 1,1–2 und 7,27. Viele Ausleger sehen einen Rahmenerzähler, der die Worte des Predigers vorstellt und am Ende einordnet. Ob er ihnen zustimmt oder sie zurechtrückt, wird verschieden gelesen."),
        E("Was heißt „das ist der ganze Mensch“?", "Wörtlich nur: „denn das ist jeder Mensch“ oder „das ist des Menschen Ganzes“. Die Übersetzungen ergänzen verschieden: die Pflicht, die Bestimmung, das Ganze des Menschen."),
        E("Wer ist der eine Hirte (V. 11)?", "Manche denken an Gott, der in den Psalmen Hirte heißt (Ps 23; 80,2), andere an Salomo oder einen Lehrer, der die Sprüche gesammelt hat."),
    ],
    cards=["laubhuettenfest"],
    fact="In vielen Synagogen wird das Buch Prediger am Laubhüttenfest gelesen – dem fröhlichsten Fest des jüdischen Jahres.",
    try_="Lies 1,2–3 und dann 12,8–14. Was ist am Anfang und am Ende gleich, was ist am Ende dazugekommen?")

P.write()
