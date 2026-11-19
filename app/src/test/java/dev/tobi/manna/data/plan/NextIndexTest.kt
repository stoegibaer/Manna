package dev.tobi.manna.data.plan

import org.junit.Assert.assertEquals
import org.junit.Test

class NextIndexTest {
    private val plan = Plan(id = "p", title = "P", sections = listOf("a", "b", "c").map { Section(id = it, refs = emptyList(), title = it, summary = "") })

    @Test
    fun firstRunSkipsDoneSections() {
        assertEquals(0, plan.nextIndex(emptySet(), null))
        assertEquals(1, plan.nextIndex(setOf("a", "c"), null))
        assertEquals(-1, plan.nextIndex(setOf("a", "b", "c"), null))
    }

    @Test
    fun rereadFollowsItsPositionEvenIfEverythingIsDone() {
        val all = setOf("a", "b", "c")
        assertEquals(0, plan.nextIndex(all, 0))
        assertEquals(2, plan.nextIndex(all, 2))
        assertEquals(-1, plan.nextIndex(all, 3))
    }
}
