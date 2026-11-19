package dev.tobi.manna.ui.garden

import androidx.compose.ui.graphics.Color
import dev.tobi.manna.data.garden.Garden
import dev.tobi.manna.ui.theme.MannaColors

/** Colors of one tree species. */
internal class TreeColors(
    val trunk: Color, val leaf: Color, val leafDark: Color, val leafLight: Color? = null,
    val flower: Color? = null, val flowerCenter: Color? = null,
    val fruit: Color? = null, val fruitDark: Color? = null, val ripe: Color? = null, val trunkDark: Color? = null,
)

internal enum class LeafShape { ELLIPSE, LOBED, ROUND, NONE }
/** CROSS = four petals as the mustard tree has always had them. */
internal enum class FlowerKind { BLOSSOM, BALL, PLUME, CROSS }
internal enum class FruitKind { ROUND, OVAL, PEAR, CROWN }
internal enum class Finale { BIRDS_NEST, DOVE, FIGS, PETALS, PALM_BIRDS, CEDAR_BIRDS, SPARKLE_WHITE, SPARKLE_GOLD, ZACCHAEUS, SPARKLE_PINK, TENT }

/**
 * One tree species with its verse. [article] is „Dein“/„Deine“ for „Dein Senfbaum ist gewachsen“.
 * [finaleText] describes the moment when the tree is fully grown.
 */
internal class TreeSpecies(
    val id: String,
    val name: String,
    val article: String,
    val ref: String,
    val verse: String,
    val finaleText: String,
    val finale: Finale?,
    val build: () -> Model,
    val light: TreeColors,
    val dark: TreeColors,
    val leafShape: LeafShape = LeafShape.ELLIPSE,
    val leafW: Double = 0.38,
    val flat: Double = 0.85,
    val petals: Int = 4,
    val flowerKind: FlowerKind = FlowerKind.BLOSSOM,
    val fruitKind: FruitKind = FruitKind.ROUND,
    val strandW: Double = 0.006,
    /** Shows a little brook at its foot when shown alone (Ps 1,3). */
    val water: Boolean = false,
) {
    val model: Model by lazy { build() }
    fun colors(c: MannaColors): TreeColors = if (c.dark) dark else light
}

private fun hex(v: Long) = Color(0xFF000000 or v)

internal object Trees {
    // the mustard tree uses the app's own plant colors
    private val mustardLight = TreeColors(hex(0x7A5C3E), hex(0x5E9E62), hex(0x3F7A4A), flower = hex(0xE8B931))
    private val mustardDark = TreeColors(hex(0xB08A63), hex(0x7FBF84), hex(0x5A9B66), flower = hex(0xF2C94C))

    val all: List<TreeSpecies> = listOf(
        TreeSpecies(
            "senf", "Senfbaum", "Dein", "Mk 4,32",
            "… und große Zweige treibt, so dass unter seinem Schatten die Vögel des Himmels sich niederlassen können.",
            "Die Vögel kommen und bauen ein Nest.", Finale.BIRDS_NEST,
            { mustard() },
            mustardLight, mustardDark, flowerKind = FlowerKind.CROSS,
        ),
        TreeSpecies(
            "oel", "Ölbaum", "Dein", "Ps 52,10",
            "Ich aber bin wie ein grüner Olivenbaum im Haus Gottes; ich vertraue auf die Güte Gottes immer und ewiglich.",
            "Die Taube kommt mit dem Olivenblatt (1 Mo 8,11).", Finale.DOVE,
            { branchy(Branchy(seed = 33, depth = 5, trunkLen = 0.28, trunkW = 0.05, trunkCurve = 18.0, spread = 16.0 to 34.0, leaf = true, leafCount = 5.0, leafLen = 0.038, fruit = Fruit(0.6, 0.01, 0.72))) },
            TreeColors(hex(0x7C6A55), hex(0x8FA587), hex(0x5F7A5E), fruit = hex(0x7E9A3C)),
            TreeColors(hex(0xA8957C), hex(0x9DB394), hex(0x6F8C6C), fruit = hex(0xA9C266)),
            leafW = 0.16, fruitKind = FruitKind.OVAL,
        ),
        TreeSpecies(
            "feige", "Feigenbaum", "Dein", "Mi 4,4",
            "Und sie werden sitzen, jeder unter seinem Weinstock und unter seinem Feigenbaum, und niemand wird sie aufschrecken.",
            "Die Feigen reifen.", Finale.FIGS,
            { branchy(Branchy(seed = 5, depth = 4, trunkLen = 0.16, trunkW = 0.06, trunkKids = 3, spread = 30.0 to 62.0, lenF = 0.75 to 0.9, sideBoost = 1.2, leaf = true, leafCount = 3.0, leafLen = 0.085, fruit = Fruit(0.9, 0.016, 0.7))) },
            TreeColors(hex(0x8A8073), hex(0x6FA35A), hex(0x4C7F42), fruit = hex(0x9DB35A), ripe = hex(0x6E4A7A)),
            TreeColors(hex(0xB3A898), hex(0x8CC077), hex(0x649A58), fruit = hex(0xB6C977), ripe = hex(0xA07AB0)),
            leafShape = LeafShape.LOBED, fruitKind = FruitKind.PEAR,
        ),
        TreeSpecies(
            "mandel", "Mandelbaum", "Dein", "Jer 1,11–12",
            "Ich sehe einen Mandelstab. Und der HERR sprach zu mir: Du hast recht gesehen; denn ich werde über mein Wort wachen, es auszuführen.",
            "Er blüht als Erster, Blütenblätter fallen leise.", Finale.PETALS,
            { branchy(Branchy(seed = 27, depth = 5, trunkLen = 0.26, trunkW = 0.045, curve = 22.0, spread = 20.0 to 40.0, leaf = true, leafFrom = 2, leafCount = 3.0, leafLen = 0.04, flower = Flower(0.7, 0.018, 0.4, spread = 0.4, along = 3), fruit = Fruit(0.35, 0.012, 0.85))) },
            TreeColors(hex(0x5A463A), hex(0x8DBA6E), hex(0x6E9A55), flower = hex(0xFBEFF2), flowerCenter = hex(0xD07A8C), fruit = hex(0xA4B27A)),
            TreeColors(hex(0x9A8072), hex(0x9FCB82), hex(0x7DAA66), flower = hex(0xF5E6EA), flowerCenter = hex(0xD77A90), fruit = hex(0xB8C690)),
            leafW = 0.22, petals = 5, fruitKind = FruitKind.OVAL,
        ),
        TreeSpecies(
            "palme", "Palme", "Deine", "Ps 92,13",
            "Der Gerechte wird sprossen wie der Palmbaum, wie eine Zeder auf dem Libanon wird er emporwachsen.",
            "Zwei Vögel setzen sich in die Krone.", Finale.PALM_BIRDS,
            { palm(PalmParams(seed = 4, height = 0.8, lean = 0.08, trunkW = 0.032, fronds = 11, frondLen = 0.3, droop = 0.4)) },
            TreeColors(hex(0x9A7B55), hex(0x6E9E4E), hex(0x4E7D3C), trunkDark = hex(0x7A5F40)),
            TreeColors(hex(0xC2A27C), hex(0x8DBF6C), hex(0x6A9A55), trunkDark = hex(0x9C805E)),
        ),
        TreeSpecies(
            "zeder", "Zeder", "Deine", "Ps 104,16–17",
            "Es werden gesättigt die Bäume des HERRN, die Zedern des Libanon, die er gepflanzt hat, worin die Vögel nisten …",
            "Vögel nisten in den Zweigen.", Finale.CEDAR_BIRDS,
            { cedar(CedarParams(seed = 6, height = 0.85, trunkW = 0.04, tiers = 8, span = 0.34, sag = 0.03, pad = 0.05, flat = 0.55)) },
            TreeColors(hex(0x6E5241), hex(0x4F7A62), hex(0x355C4A), leafLight = hex(0x6F977D)),
            TreeColors(hex(0xA68A74), hex(0x6E9C82), hex(0x4F7C66), leafLight = hex(0x8DB59C)),
        ),
        TreeSpecies(
            "wasser", "Baum am Wasser", "Dein", "Ps 1,3",
            "Und er ist wie ein Baum, gepflanzt an Wasserbächen, der seine Frucht bringt zu seiner Zeit und dessen Blatt nicht verwelkt.",
            "Das Wasser glitzert, und er trägt Frucht zu seiner Zeit.", Finale.SPARKLE_WHITE,
            { branchy(Branchy(seed = 19, depth = 4, trunkLen = 0.26, trunkW = 0.055, spread = 24.0 to 48.0, leaf = true, leafCount = 4.0, leafLen = 0.04, clumpAlong = 1, clumpR = 0.06, tipClump = 0.065, fruit = Fruit(0.9, 0.014, 0.72))) },
            TreeColors(hex(0x6F5A47), hex(0x5E9E62), hex(0x3F7A4A), leafLight = hex(0x7DB57E), fruit = hex(0xC2493A)),
            TreeColors(hex(0xA8917A), hex(0x7FBF84), hex(0x5A9B66), leafLight = hex(0x9BD0A0), fruit = hex(0xE0735F)),
            leafShape = LeafShape.ROUND, water = true,
        ),
        TreeSpecies(
            "granat", "Granatapfel", "Dein", "5 Mo 8,8",
            "ein Land von Weizen und Gerste und Weinstöcken und Feigenbäumen und Granatbäumen; ein Land von ölreichen Olivenbäumen und Honig;",
            "Die Früchte werden rot.", Finale.SPARKLE_GOLD,
            { branchy(Branchy(seed = 37, depth = 5, trunkLen = 0.22, trunkW = 0.04, spread = 20.0 to 42.0, leaf = true, leafCount = 4.0, leafLen = 0.03, flower = Flower(0.9, 0.016, 0.5, along = 3), fruit = Fruit(0.5, 0.02, 0.78))) },
            TreeColors(hex(0x6E5A4B), hex(0x5E9A4E), hex(0x3F7A3C), flower = hex(0xE8743A), flowerCenter = hex(0xF2C94C), fruit = hex(0xC0392B), fruitDark = hex(0x8E2A1F)),
            TreeColors(hex(0xA8917F), hex(0x7DB86B), hex(0x5C9A55), flower = hex(0xF08A55), flowerCenter = hex(0xF2C94C), fruit = hex(0xE05A48), fruitDark = hex(0xB04436)),
            leafW = 0.3, petals = 5, fruitKind = FruitKind.CROWN,
        ),
        TreeSpecies(
            "maulbeer", "Maulbeerfeigenbaum", "Dein", "Lk 19,4",
            "Und er lief voraus und stieg auf einen Maulbeerfeigenbaum, damit er ihn sähe; denn er sollte dort durchkommen.",
            "Zachäus sitzt im Baum.", Finale.ZACCHAEUS,
            { branchy(Branchy(seed = 23, depth = 4, trunkLen = 0.16, trunkW = 0.08, trunkKids = 4, spread = 30.0 to 54.0, lenF = 0.74 to 0.86, sideBoost = 1.1, squash = 0.75, leaf = true, leafCount = 3.0, leafLen = 0.035, clumpAlong = 2, clumpR = 0.065, tipClump = 0.07, fruit = Fruit(0.4, 0.01, 0.75))) },
            TreeColors(hex(0x8C7B66), hex(0x6B9A52), hex(0x4D7B40), leafLight = hex(0x88B26C), fruit = hex(0xC98A5A)),
            TreeColors(hex(0xB5A48E), hex(0x88B86E), hex(0x669757), leafLight = hex(0xA3CA88), fruit = hex(0xE0A878)),
            leafShape = LeafShape.ROUND, flat = 0.6,
        ),
        TreeSpecies(
            "tamariske", "Tamariske", "Deine", "1 Mo 21,33",
            "Und Abraham pflanzte eine Tamariske in Beerseba und rief dort den Namen des HERRN, des ewigen Gottes, an.",
            "Rosa Blütenrispen erscheinen.", Finale.SPARKLE_PINK,
            { branchy(Branchy(seed = 16, depth = 5, trunkLen = 0.22, trunkW = 0.045, curve = 30.0, spread = 20.0 to 44.0, strands = 3, strandFrom = 3, strandLen = 0.08, droop = 0.4, flower = Flower(0.7, 0.02, 0.6, along = 4))) },
            TreeColors(hex(0x6B5A50), hex(0x8FA89A), hex(0x6E8A7C), flower = hex(0xD98AAE)),
            TreeColors(hex(0xA39187), hex(0xA3BDB0), hex(0x7F9C8E), flower = hex(0xE7A6C0)),
            leafShape = LeafShape.NONE, flowerKind = FlowerKind.PLUME, strandW = 0.004,
        ),
        TreeSpecies(
            "terebinthe", "Terebinthe", "Deine", "1 Mo 18,1",
            "Und der HERR erschien ihm bei den Terebinthen Mamres; und er saß an dem Eingang des Zeltes bei der Hitze des Tages.",
            "Ein Zelt steht in ihrem Schatten.", Finale.TENT,
            { branchy(Branchy(seed = 31, depth = 4, trunkLen = 0.2, trunkW = 0.09, spread = 28.0 to 50.0, lenF = 0.74 to 0.88, gnarl = 14.0, leaf = true, leafCount = 3.0, leafLen = 0.03, clumpAlong = 2, clumpR = 0.075, tipClump = 0.085, fruit = Fruit(0.3, 0.007, 0.8))) },
            TreeColors(hex(0x6A5644), hex(0x6A8F4E), hex(0x4B6E3A), leafLight = hex(0x87A86A), fruit = hex(0xB0475A)),
            TreeColors(hex(0xA89278), hex(0x86AD69), hex(0x638C52), leafLight = hex(0xA2C485), fruit = hex(0xD06A7C)),
            leafShape = LeafShape.ROUND,
        ),
        TreeSpecies(
            "akazie", "Akazie", "Deine", "Jes 41,19",
            "Ich werde Zedern in die Wüste setzen, Akazien und Myrten und Olivenbäume …",
            "Gelbe Blütenkugeln leuchten.", Finale.SPARKLE_GOLD,
            { branchy(Branchy(seed = 13, depth = 4, trunkLen = 0.24, trunkW = 0.045, trunkKids = 3, spread = 22.0 to 34.0, up = 0.05, lenF = 0.82 to 0.95, squash = 0.6, tipClump = 0.09, clumpAlong = 1, clumpFrom = 3, clumpR = 0.07, flower = Flower(0.9, 0.016, 0.7))) },
            TreeColors(hex(0x6E5A48), hex(0x7E9A4E), hex(0x5C7A3A), leafLight = hex(0x9AB46A), flower = hex(0xE8B931)),
            TreeColors(hex(0xA8927E), hex(0x9AB66A), hex(0x789655), leafLight = hex(0xB3CB86), flower = hex(0xF2C94C)),
            leafShape = LeafShape.NONE, flat = 0.38, flowerKind = FlowerKind.BALL,
        ),
    )

    val life = TreeSpecies(
        Garden.LIFE, "Baum des Lebens", "Dein", "Offb 22,2",
        "… der Baum des Lebens, der zwölf Früchte trägt und jeden Monat seine Frucht gibt; und die Blätter des Baumes sind zur Heilung der Nationen.",
        "Ab jetzt reift alle 4 Abschnitte eine Frucht.", Finale.SPARKLE_GOLD,
        { branchy(Branchy(seed = 77, depth = 5, trunkLen = 0.26, trunkW = 0.07, spread = 24.0 to 46.0, leaf = true, leafCount = 3.0, leafLen = 0.04, clumpAlong = 1, clumpR = 0.06, tipClump = 0.07, fruit = Fruit(1.0, 0.024, 0.6))) },
        TreeColors(hex(0x7A5C3E), hex(0x4F9E6A), hex(0x2F7D4F), leafLight = hex(0x7CC28F), fruit = hex(0xC0392B)),
        TreeColors(hex(0xB08A63), hex(0x6FBF88), hex(0x4F9E6A), leafLight = hex(0x9AD6AA), fruit = hex(0xE05A48)),
    )

    /** Twelve fruits for twelve months (Offb 22,2). */
    val lifeFruits = listOf(0xC0392B, 0xE8B931, 0x8E44AD, 0xE67E22, 0xD35482, 0x7E9A3C, 0x2E86AB, 0xC98A2E, 0xB04436, 0xF2C94C, 0x6E4A7A, 0xE05A48).map { hex(it.toLong()) }

    private val byId = (all + life).associateBy { it.id }
    fun byId(id: String): TreeSpecies = byId[id] ?: all.first()
}
