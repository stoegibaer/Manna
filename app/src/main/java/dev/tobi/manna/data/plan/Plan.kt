package dev.tobi.manna.data.plan

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

// Format documented in .claude/skills/leseplan-schreiben/format.md

@Serializable
data class PlanIndex(
    val start: String,
    val directions: List<Direction> = emptyList(),
    val plans: List<PlanEntry> = emptyList(),
)

/** The plan to read now: the chosen one if available, else the start plan, else the first available. */
fun PlanIndex.resolve(chosen: String): String {
    val avail = plans.filter { it.available }.map { it.id }
    return when {
        chosen in avail -> chosen
        start in avail -> start
        else -> avail.first()
    }
}

@Serializable
data class Direction(val id: String, val title: String, val subtitle: String = "")

@Serializable
data class PlanEntry(
    val id: String,
    val title: String,
    val subtitle: String = "",
    val direction: String,
    val available: Boolean = false,
)

@Serializable
data class Plan(
    val id: String,
    val title: String,
    val subtitle: String = "",
    val description: String = "",
    val direction: String = "",
    /** Translation whose wording quote/memory texts use. */
    val basis: String = "elbbk",
    val stages: List<Stage> = emptyList(),
    val cards: List<Card> = emptyList(),
    val sections: List<Section>,
) {
    fun card(id: String) = cards.firstOrNull { it.id == id }
    fun stage(id: String?) = stages.firstOrNull { it.id == id }

    /**
     * Index of the next section to read, or -1 if the plan is finished.
     * [rereadPos] is set while a finished plan is read again from the start (Settings.rereads).
     */
    fun nextIndex(done: Set<String>, rereadPos: Int?): Int =
        if (rereadPos != null) rereadPos.takeIf { it in sections.indices } ?: -1
        else sections.indexOfFirst { it.id !in done }
}

@Serializable
data class Stage(val id: String, val title: String)

@Serializable
data class Card(
    val id: String,
    val type: String,
    val name: String,
    val text: String,
    val refs: String = "",
)

@Serializable
data class Ref(val book: Int, val chapter: Int, val from: Int, val to: Int)

@Serializable
data class Section(
    val id: String,
    val stage: String? = null,
    val refs: List<Ref>,
    val title: String,
    val summary: String,
    val bridge: String? = null,
    val place: String? = null,
    val focus: String? = null,
    val quiz: List<Quiz> = emptyList(),
    val explain: List<Explain> = emptyList(),
    val cards: List<String> = emptyList(),
    val fact: String? = null,
    val teaser: String? = null,
    @SerialName("memory_verse") val memoryVerse: MemoryVerse? = null,
    @SerialName("try") val tryIt: String? = null,
    val prayer: Prayer? = null,
)

@Serializable
data class Quiz(
    val type: String,
    val q: String? = null,
    val options: List<String> = emptyList(),
    val answer: kotlinx.serialization.json.JsonElement? = null,
    val quote: String? = null,
    @SerialName("quote_ref") val quoteRef: Ref? = null,
    val items: List<String> = emptyList(),
    val text: String? = null,
    val fix: String? = null,
    val min: Int = 0,
    val max: Int = 10,
    val tolerance: Int = 0,
    val unit: String = "",
    val hint: String? = null,
    val verse: Int? = null,
    val explain: String = "",
) {
    /** Index answer for choice/whosaid. */
    val answerIndex: Int get() = answer?.toString()?.toIntOrNull() ?: 0
    /** Boolean answer for truefalse. */
    val answerBool: Boolean get() = answer?.toString() == "true"
    /** Integer answer for estimate. */
    val answerInt: Int get() = answer?.toString()?.toIntOrNull() ?: 0
}

@Serializable
data class Explain(val q: String, val a: String, val translation: String? = null)

@Serializable
data class MemoryVerse(val ref: Ref, val text: String)

@Serializable
data class Prayer(val source: String, val text: String = "", val ref: Ref? = null)

@Serializable
data class Place(val id: String, val name: String, val lat: Double, val lon: Double, val text: String = "")

@Serializable
private data class Places(val places: List<Place>)

class PlanRepository(private val context: Context) {
    private val json = Json { ignoreUnknownKeys = true }
    private val mutex = Mutex()
    private val plans = HashMap<String, Plan>()
    private var index: PlanIndex? = null
    private var places: Map<String, Place>? = null

    suspend fun index(): PlanIndex = mutex.withLock {
        index ?: io { json.decodeFromString<PlanIndex>(read("plans/index.json")) }.also { index = it }
    }

    suspend fun plan(id: String): Plan = mutex.withLock {
        plans[id] ?: io { json.decodeFromString<Plan>(read("plans/$id.json")) }.also { plans[id] = it }
    }

    suspend fun place(id: String?): Place? = id?.let { places()[it] }

    /** All places by id (assets/places.json). */
    suspend fun places(): Map<String, Place> = mutex.withLock {
        places ?: io { json.decodeFromString<Places>(read("places.json")).places.associateBy { it.id } }
            .also { places = it }
    }

    private suspend fun <T> io(block: () -> T) = withContext(Dispatchers.IO) { block() }
    private fun read(path: String) = context.assets.open(path).bufferedReader(Charsets.UTF_8).use { it.readText() }
}
