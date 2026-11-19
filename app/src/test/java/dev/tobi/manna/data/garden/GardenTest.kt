package dev.tobi.manna.data.garden

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class GardenTest {
    @Test
    fun firstTreeNeeds30ThenEach40() {
        assertEquals(0, Garden.progress(29).done)
        assertEquals(1, Garden.progress(30).done)
        assertEquals(0f, Garden.progress(30).inTree)
        assertEquals(1, Garden.progress(69).done)
        assertEquals(2, Garden.progress(70).done)
        assertEquals(12, Garden.progress(470).done)
        assertEquals(13, Garden.progress(510).done)
        assertEquals(510, Garden.AFTER_LIFE)
    }

    @Test
    fun fruitsRipenEveryFourSectionsAfterTheTreeOfLife() {
        assertEquals(0, Garden.progress(509).fruits)
        assertEquals(0, Garden.progress(513).fruits)
        assertEquals(1, Garden.progress(514).fruits)
        assertEquals(36, Garden.progress(510 + 144).fruits)
        assertEquals(1f, Garden.progress(2000).t)
    }

    @Test
    fun growthIsVisibleWithEverySection() {
        var last = -1f
        for (s in 0 until 30) {
            val t = Garden.progress(s).t
            assertTrue("section $s", t > last)
            last = t
        }
    }

    @Test
    fun choiceIsPendingUntilTheNextTreeIsPlanted() {
        val senf = listOf("senf")
        assertFalse(Garden.choicePending(29, senf))
        assertTrue(Garden.choicePending(30, senf))
        assertFalse(Garden.choicePending(30, senf + "oel"))
        // after an update with many sections: one choice after the other
        assertTrue(Garden.choicePending(150, senf + "oel"))
        // the tree of life is „chosen“ too, so one knows what comes next
        val all = Garden.ORDER
        assertTrue(Garden.choicePending(470, all))
        assertFalse(Garden.choicePending(470, all + Garden.LIFE))
        assertFalse(Garden.choicePending(5000, all + Garden.LIFE))
    }

    @Test
    fun offersShrinkTowardsTheEndAndEndWithTheTreeOfLife() {
        assertEquals(listOf("oel", "feige", "mandel"), Garden.offers(listOf("senf")))
        val elevenPlanted = Garden.ORDER.dropLast(1)
        assertEquals(listOf("akazie"), Garden.offers(elevenPlanted))
        assertEquals(2, Garden.offers(Garden.ORDER.dropLast(2)).size)
        assertEquals(listOf(Garden.LIFE), Garden.offers(Garden.ORDER))
        assertEquals(emptyList<String>(), Garden.offers(Garden.ORDER + Garden.LIFE))
    }

    @Test
    fun offersRotateSoATreeNotTakenComesBack() {
        val second = Garden.offers(listOf("senf", "oel"))
        assertEquals(listOf("mandel", "palme", "zeder"), second)
        assertFalse("feige" in second)
    }
}
