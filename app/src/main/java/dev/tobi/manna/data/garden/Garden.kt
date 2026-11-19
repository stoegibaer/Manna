package dev.tobi.manna.data.garden

/**
 * The garden: every completed section lets a tree grow. A tree is fully grown after
 * [FIRST] sections (the first one) or [NEXT] sections (all others). Then it moves into the
 * garden and the reader picks the next tree from up to three offers. After the twelve garden
 * trees the tree of life grows at the water (Offb 22,2). After that, every [PER_FRUIT]
 * sections a fruit ripens, and the golden city at the horizon comes down a bit (Offb 21,2).
 *
 * Everything is derived from the number of completed sections – nothing can shrink.
 * The only stored state is which tree was planted at which position.
 */
object Garden {
    const val FIRST = 30
    const val NEXT = 40
    const val TREES = 12
    const val PER_FRUIT = 4
    const val CITY_STEPS = 36
    const val LIFE = "leben"

    /** The twelve garden trees; the first one is always the mustard tree. */
    val ORDER = listOf("senf", "oel", "feige", "mandel", "palme", "zeder", "wasser", "granat", "maulbeer", "tamariske", "terebinthe", "akazie")

    /** Sections needed for tree [i] (0-based; 12 = tree of life). */
    fun need(i: Int) = if (i == 0) FIRST else NEXT

    /** Sections until the tree of life is fully grown. */
    val AFTER_LIFE = FIRST + TREES * NEXT

    /** Sections needed to finish the first [trees] trees. */
    fun sectionsFor(trees: Int): Int = (0 until trees).sumOf { need(it) }

    /**
     * @property done fully grown trees (0..13, 13 = tree of life grown too)
     * @property inTree sections (may be fractional while animating) into the growing tree
     * @property need sections the growing tree needs
     * @property fruits ripe fruits on the tree of life
     */
    data class Progress(val done: Int, val inTree: Float, val need: Int, val fruits: Int) {
        /** Growth 0..1 of the tree that is growing now. */
        val t: Float get() = if (done > TREES) 1f else (inTree / need).coerceIn(0f, 1f)
    }

    fun progress(total: Float): Progress {
        var i = 0
        var left = total.coerceAtLeast(0f)
        while (i <= TREES && left >= need(i)) { left -= need(i); i++ }
        val fruits = if (total < AFTER_LIFE) 0 else ((total - AFTER_LIFE) / PER_FRUIT).toInt()
        return Progress(i, if (i > TREES) 0f else left, need(minOf(i, TREES)), fruits)
    }

    fun progress(total: Int) = progress(total.toFloat())

    /**
     * True when a tree is grown but the next one has not been chosen yet.
     * [planted] = species by position, starting with the mustard tree.
     */
    fun choicePending(total: Int, planted: List<String>): Boolean {
        val done = progress(total).done
        return planted.size <= done && planted.size <= TREES
    }

    /**
     * Up to three trees to choose from. When fewer are left, fewer are offered; after the twelve
     * garden trees only the tree of life. Rotates with every choice, so a tree not taken comes back later.
     */
    fun offers(planted: List<String>): List<String> {
        val rest = ORDER.filter { it !in planted }
        if (rest.isEmpty()) return if (LIFE in planted) emptyList() else listOf(LIFE)
        val offset = planted.size - 1
        return List(minOf(3, rest.size)) { rest[(offset + it) % rest.size] }
    }
}
