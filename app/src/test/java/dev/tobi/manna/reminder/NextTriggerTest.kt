package dev.tobi.manna.reminder

import dev.tobi.manna.data.settings.Settings
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test
import java.time.LocalDateTime

class NextTriggerTest {
    private val day = LocalDateTime.of(2026, 11, 16, 0, 0)
    private fun at(h: Int, m: Int = 0) = day.withHour(h).withMinute(m)
    private val tomorrowAnchor = day.plusDays(1).withHour(7).withMinute(30)
    private val s = Settings(remindersOn = true, anchorMinute = 7 * 60 + 30, quietMinute = 22 * 60)

    @Test fun off_returnsNull() = assertNull(Reminders.nextTrigger(s.copy(remindersOn = false), at(9), false))

    @Test fun beforeAnchor_firesAtAnchor() = assertEquals(at(7, 30), Reminders.nextTrigger(s, at(6), false))

    @Test fun exactlyAtAnchor_nextIsOneHourLater() = assertEquals(at(8, 30), Reminders.nextTrigger(s, at(7, 30), false))

    @Test fun afterAnchor_hourlySlots() = assertEquals(at(10, 30), Reminders.nextTrigger(s, at(9, 45), false))

    @Test fun lastSlotBeforeQuiet() = assertEquals(at(21, 30), Reminders.nextTrigger(s, at(20, 31), false))

    @Test fun afterLastSlot_planBTime() = assertEquals(at(22), Reminders.nextTrigger(s, at(21, 31), false))

    @Test fun noHourlySlotRightBeforePlanB() =
        assertEquals(at(21, 45), Reminders.nextTrigger(s.copy(quietMinute = 21 * 60 + 45), at(20, 31), false))

    @Test fun afterPlanB_tomorrow() = assertEquals(tomorrowAnchor, Reminders.nextTrigger(s, at(22, 1), false))

    @Test fun alreadyRead_tomorrow() = assertEquals(tomorrowAnchor, Reminders.nextTrigger(s, at(9), true))

    @Test fun pausedToday_tomorrow() = assertEquals(tomorrowAnchor, Reminders.nextTrigger(s.copy(pausedDate = "2026-11-16"), at(9), false))

    @Test fun pausedYesterday_isIgnored() = assertEquals(at(9, 30), Reminders.nextTrigger(s.copy(pausedDate = "2026-11-15"), at(9), false))

    @Test fun quietBeforeAnchor_meansUntilMidnight() {
        val late = s.copy(anchorMinute = 21 * 60, quietMinute = 6 * 60)
        assertEquals(at(23), Reminders.nextTrigger(late, at(22, 10), false))
    }
}
