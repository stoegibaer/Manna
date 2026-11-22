package dev.tobi.manna.update

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

/** A published version of the app on GitHub with its APK. */
data class Release(val version: String, val notes: String, val apkUrl: String, val size: Long)

@Serializable
private data class GhAsset(val name: String, @SerialName("browser_download_url") val url: String, val size: Long = 0)

@Serializable
private data class GhRelease(
    @SerialName("tag_name") val tag: String,
    val body: String? = null,
    val draft: Boolean = false,
    val prerelease: Boolean = false,
    val assets: List<GhAsset> = emptyList(),
)

private val json = Json { ignoreUnknownKeys = true }

/** Answer of `GET /repos/{owner}/{repo}/releases/latest` → release with an APK, or null if there is none. */
fun parseRelease(body: String): Release? {
    val r = json.decodeFromString<GhRelease>(body)
    if (r.draft || r.prerelease) return null
    val apk = r.assets.firstOrNull { it.name.endsWith(".apk", ignoreCase = true) } ?: return null
    return Release(Versions.clean(r.tag), plainNotes(r.body.orEmpty()), apk.url, apk.size)
}

object Versions {
    /** "v0.2.10-debug" → "0.2.10" */
    fun clean(v: String): String = v.trim().removePrefix("v").removePrefix("V").substringBefore('-')

    private fun parts(v: String): List<Int> = clean(v).split('.').map { it.toIntOrNull() ?: 0 }

    /** True if [remote] is a higher version than [local] (0.2.10 > 0.2.9). */
    fun isNewer(remote: String, local: String): Boolean {
        val a = parts(remote)
        val b = parts(local)
        for (i in 0 until maxOf(a.size, b.size)) {
            val x = a.getOrElse(i) { 0 }
            val y = b.getOrElse(i) { 0 }
            if (x != y) return x > y
        }
        return false
    }
}

/** Release notes are Markdown; for the app they become plain text with bullets. The install hint is dropped. */
fun plainNotes(md: String): String = md.lines()
    .map { it.trim() }
    .filterNot { it.startsWith("Installation:", ignoreCase = true) }
    .map { line ->
        line.replace(Regex("""\*\*(.+?)\*\*"""), "$1")
            .replace(Regex("""(?<!\w)_(.+?)_(?!\w)"""), "$1")
            .replace(Regex("""\[(.+?)]\(.+?\)"""), "$1")
            .replace("`", "")
            .let {
                when {
                    it.startsWith("#") -> it.trimStart('#').trim()
                    it.startsWith("- ") || it.startsWith("* ") -> "• " + it.drop(2)
                    else -> it
                }
            }
    }
    .joinToString("\n")
    .replace(Regex("\n{3,}"), "\n\n")
    .trim()
