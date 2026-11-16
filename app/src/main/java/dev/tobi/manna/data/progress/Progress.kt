package dev.tobi.manna.data.progress

import android.content.Context
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Room
import androidx.room.RoomDatabase
import kotlinx.coroutines.flow.Flow
import java.time.LocalDate

@Entity(primaryKeys = ["planId", "sectionId"])
data class SectionDone(val planId: String, val sectionId: String, val completedAt: Long)

/** One answered quiz question; basis for spaced repetition later. */
@Entity(primaryKeys = ["planId", "sectionId", "quizIndex"])
data class QuizResult(
    val planId: String,
    val sectionId: String,
    val quizIndex: Int,
    val firstTry: Boolean,
    val answeredAt: Long,
)

@Entity(primaryKeys = ["planId", "cardId"])
data class CardUnlock(val planId: String, val cardId: String, val unlockedAt: Long)

/** Per-day reading log (date = ISO yyyy-MM-dd). Basis for daily minimum and weekly goal. */
@Entity(primaryKeys = ["date"])
data class ReadingDay(val date: String, val verses: Int, val sections: Int)

@Dao
interface ProgressDao {
    @Query("SELECT * FROM SectionDone WHERE planId = :planId")
    fun sectionsDone(planId: String): Flow<List<SectionDone>>

    @Query("SELECT * FROM SectionDone")
    fun allSectionsDone(): Flow<List<SectionDone>>

    @Query("SELECT COUNT(*) FROM SectionDone")
    fun totalSections(): Flow<Int>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertSection(s: SectionDone): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertQuiz(r: QuizResult)

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertCard(c: CardUnlock): Long

    /** Card ids that were renamed in a plan update: keep the user's unlocks. */
    @Query("UPDATE OR IGNORE CardUnlock SET cardId = :to WHERE planId = :planId AND cardId = :from")
    suspend fun renameCard(planId: String, from: String, to: String)

    @Query("SELECT * FROM CardUnlock ORDER BY unlockedAt")
    fun cards(): Flow<List<CardUnlock>>

    @Query("SELECT * FROM ReadingDay WHERE date = :date")
    suspend fun day(date: String): ReadingDay?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertDay(d: ReadingDay)

    @Query("SELECT * FROM ReadingDay WHERE date >= :from ORDER BY date")
    fun daysSince(from: String): Flow<List<ReadingDay>>
}

@Database(entities = [SectionDone::class, QuizResult::class, CardUnlock::class, ReadingDay::class], version = 1)
abstract class MannaDb : RoomDatabase() {
    abstract fun progress(): ProgressDao

    companion object {
        fun create(context: Context) = Room.databaseBuilder(context, MannaDb::class.java, "manna.db").build()
    }
}

class ProgressRepository(private val dao: ProgressDao) {
    fun sectionsDone(planId: String) = dao.sectionsDone(planId)
    val totalSections: Flow<Int> = dao.totalSections()
    val allSectionsDone: Flow<List<SectionDone>> = dao.allSectionsDone()
    val cards = dao.cards()

    /** @return true if the section was newly completed (not a re-read). */
    suspend fun completeSection(planId: String, sectionId: String): Boolean =
        dao.insertSection(SectionDone(planId, sectionId, System.currentTimeMillis())) != -1L

    suspend fun recordQuiz(planId: String, sectionId: String, index: Int, firstTry: Boolean) =
        dao.upsertQuiz(QuizResult(planId, sectionId, index, firstTry, System.currentTimeMillis()))

    /** @return ids of cards that were newly unlocked. */
    suspend fun unlockCards(planId: String, cardIds: List<String>): List<String> {
        val now = System.currentTimeMillis()
        return cardIds.filter { dao.insertCard(CardUnlock(planId, it, now)) != -1L }
    }

    /** Small data migrations after content updates. Idempotent. */
    suspend fun migrate() {
        dao.renameCard("habakuk", "jehova", "gottesname")
    }

    suspend fun logReading(verses: Int, sections: Int) {
        val today = LocalDate.now().toString()
        val d = dao.day(today) ?: ReadingDay(today, 0, 0)
        dao.upsertDay(d.copy(verses = d.verses + verses, sections = d.sections + sections))
    }
}
