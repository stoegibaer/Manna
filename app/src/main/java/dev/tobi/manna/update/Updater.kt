package dev.tobi.manna.update

import android.app.Application
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageInstaller
import android.net.Uri
import android.os.Build
import android.os.SystemClock
import androidx.core.content.IntentCompat
import dev.tobi.manna.MannaApp
import dev.tobi.manna.data.settings.SettingsRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

sealed interface UpdateState {
    data object Idle : UpdateState
    data object Checking : UpdateState
    data object UpToDate : UpdateState
    /** [ready]: the APK is already downloaded, a tap installs it right away. */
    data class Available(val release: Release, val ready: Boolean = false) : UpdateState
    /** Installing from unknown sources must be allowed once in the system settings. */
    data class NeedsPermission(val release: Release) : UpdateState
    data class Downloading(val release: Release, val progress: Float) : UpdateState
    data class Installing(val release: Release) : UpdateState
    data class Failed(val message: String, val release: Release?) : UpdateState
}

/**
 * Looks on GitHub for a newer release and installs its APK – always after the user tapped „Aktualisieren“.
 * Only the release check goes out (no data from the app); Android checks that the APK is signed with the same key.
 */
class Updater(private val app: Application, private val settings: SettingsRepository, private val scope: CoroutineScope) {
    private val _state = MutableStateFlow<UpdateState>(UpdateState.Idle)
    val state: StateFlow<UpdateState> = _state.asStateFlow()

    val currentVersion: String = runCatching { app.packageManager.getPackageInfo(app.packageName, 0).versionName }.getOrNull().orEmpty()

    /** The test app („Manna (Test)“) is a separate app – a release APK would not update it. */
    val available: Boolean = (app.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) == 0

    private var lastCheck = 0L
    private var job: Job? = null
    /** Installer session waiting for the user; abandoned when they start over. */
    private var sessionId = -1
    private val dir get() = File(app.cacheDir, "update")

    init {
        // after an update the APK is not needed any more – no leftovers in the cache
        scope.launch(Dispatchers.IO) { cleanUp() }
    }

    /** Deletes downloaded APKs that are not newer than the installed version (or unfinished downloads). */
    private fun cleanUp() {
        dir.listFiles()?.forEach { f ->
            val version = f.name.removePrefix("manna-").removeSuffix(".apk")
            if (!f.name.endsWith(".apk") || !Versions.isNewer(version, currentVersion)) f.delete()
        }
    }

    private fun apkFile(release: Release) = File(dir, "manna-${release.version}.apk")

    /** Complete download of this release already on the device? */
    private fun downloaded(release: Release) = apkFile(release).let { it.exists() && (release.size <= 0 || it.length() == release.size) }

    /** On app start: at most every few hours, quietly, if the user did not switch it off. */
    fun checkOccasionally() {
        if (!available) return
        if (lastCheck != 0L && SystemClock.elapsedRealtime() - lastCheck < CHECK_INTERVAL_MS) return
        scope.launch { if (settings.current().updateCheck) check(quiet = true) }
    }

    /** [quiet]: failures (no internet) are not shown, the user did not ask. */
    fun check(quiet: Boolean = false) {
        if (!available || job?.isActive == true) return
        val busy = _state.value
        if (busy is UpdateState.Downloading || busy is UpdateState.Installing) return
        job = scope.launch {
            if (!quiet) _state.value = UpdateState.Checking
            _state.value = try {
                val release = withContext(Dispatchers.IO) { fetchLatest() }
                lastCheck = SystemClock.elapsedRealtime()
                if (release != null && Versions.isNewer(release.version, currentVersion)) UpdateState.Available(release, downloaded(release)) else UpdateState.UpToDate
            } catch (e: Exception) {
                if (quiet) UpdateState.Idle else UpdateState.Failed("Keine Verbindung zu GitHub. Bist du online?", null)
            }
        }
    }

    /**
     * Downloads the APK (unless it is already there) and hands it to Android's installer, which asks the user to confirm.
     * Can be called again at any time, e.g. after the installation was cancelled or got stuck – it starts over with the same file.
     */
    fun install(release: Release) {
        if (job?.isActive == true) return
        if (!app.packageManager.canRequestPackageInstalls()) {
            _state.value = UpdateState.NeedsPermission(release)
            return
        }
        job = scope.launch {
            try {
                val apk = if (downloaded(release)) apkFile(release) else {
                    _state.value = UpdateState.Downloading(release, 0f)
                    withContext(Dispatchers.IO) { download(release) { p -> _state.value = UpdateState.Downloading(release, p) } }
                }
                _state.value = UpdateState.Installing(release)
                try {
                    withContext(Dispatchers.IO) { commit(apk) }
                } catch (e: Exception) {
                    _state.value = UpdateState.Failed("Die Installation ließ sich nicht starten. Versuch es gleich noch mal.", release)
                }
            } catch (e: Exception) {
                _state.value = UpdateState.Failed("Der Download hat nicht geklappt. Versuch es gleich noch mal.", release)
            }
        }
    }

    /** Intent for the system page „Unbekannte Apps installieren“ of this app. */
    fun permissionIntent() = Intent(android.provider.Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:${app.packageName}"))

    /** Back from the system settings: if installing is allowed now, go on right away. */
    fun onResume() {
        val s = _state.value
        if (s is UpdateState.NeedsPermission && app.packageManager.canRequestPackageInstalls()) install(s.release)
    }

    private fun fetchLatest(): Release? {
        val con = (URL(LATEST_URL).openConnection() as HttpURLConnection).apply {
            connectTimeout = 10_000
            readTimeout = 15_000
            setRequestProperty("Accept", "application/vnd.github+json")
            setRequestProperty("User-Agent", "Manna-App")
        }
        try {
            if (con.responseCode == 404) return null // no release yet
            if (con.responseCode != 200) throw IOException("HTTP ${con.responseCode}")
            return parseRelease(con.inputStream.bufferedReader().use { it.readText() })
        } finally {
            con.disconnect()
        }
    }

    private fun download(release: Release, onProgress: (Float) -> Unit): File {
        dir.mkdirs()
        dir.listFiles()?.forEach { it.delete() }
        val file = apkFile(release)
        val part = File(dir, "${file.name}.part")
        val con = (URL(release.apkUrl).openConnection() as HttpURLConnection).apply {
            connectTimeout = 15_000
            readTimeout = 30_000
            instanceFollowRedirects = true
            setRequestProperty("User-Agent", "Manna-App")
        }
        try {
            if (con.responseCode != 200) throw IOException("HTTP ${con.responseCode}")
            val total = con.contentLengthLong.takeIf { it > 0 } ?: release.size
            con.inputStream.use { input ->
                part.outputStream().use { out ->
                    val buf = ByteArray(64 * 1024)
                    var read = 0L
                    var shown = -1
                    while (true) {
                        val n = input.read(buf)
                        if (n < 0) break
                        out.write(buf, 0, n)
                        read += n
                        if (total > 0) {
                            val pct = (read * 100 / total).toInt()
                            if (pct != shown) { shown = pct; onProgress(pct / 100f) }
                        }
                    }
                }
            }
            if (release.size > 0 && part.length() != release.size) throw IOException("incomplete download")
            if (!part.renameTo(file)) throw IOException("rename failed")
            return file
        } finally {
            con.disconnect()
        }
    }

    private fun commit(apk: File) {
        val installer = app.packageManager.packageInstaller
        // an earlier attempt may still be waiting (e.g. Play Protect did not answer) – start over cleanly
        if (sessionId >= 0) runCatching { installer.abandonSession(sessionId) }
        installer.mySessions.filter { it.appPackageName == app.packageName }.forEach { runCatching { installer.abandonSession(it.sessionId) } }
        val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL).apply {
            setAppPackageName(app.packageName)
            // Android may skip the confirmation once Manna installed itself; otherwise it asks
            if (Build.VERSION.SDK_INT >= 31) setRequireUserAction(PackageInstaller.SessionParams.USER_ACTION_NOT_REQUIRED)
        }
        val id = installer.createSession(params)
        sessionId = id
        installer.openSession(id).use { session ->
            try {
                session.openWrite("manna.apk", 0, apk.length()).use { out ->
                    apk.inputStream().use { it.copyTo(out) }
                    session.fsync(out)
                }
                val intent = Intent(app, InstallReceiver::class.java).setAction(ACTION_STATUS)
                val flags = PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= 31) PendingIntent.FLAG_MUTABLE else 0)
                session.commit(PendingIntent.getBroadcast(app, id, intent, flags).intentSender)
            } catch (e: Exception) {
                session.abandon()
                throw e
            }
        }
    }

    /** Result from Android's installer. On success the app is replaced and restarted anyway. */
    internal fun onStatus(context: Context, intent: Intent) {
        // late answer of an abandoned attempt (after „Neu starten“) – ignore
        val id = intent.getIntExtra(PackageInstaller.EXTRA_SESSION_ID, -1)
        if (sessionId >= 0 && id >= 0 && id != sessionId) return
        val release = when (val s = _state.value) {
            is UpdateState.Installing -> s.release
            is UpdateState.Available -> s.release
            else -> null
        }
        when (val status = intent.getIntExtra(PackageInstaller.EXTRA_STATUS, PackageInstaller.STATUS_FAILURE)) {
            PackageInstaller.STATUS_PENDING_USER_ACTION -> {
                val confirm = IntentCompat.getParcelableExtra(intent, Intent.EXTRA_INTENT, Intent::class.java)
                if (confirm != null) context.startActivity(confirm.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
            }
            PackageInstaller.STATUS_SUCCESS -> {
                sessionId = -1
                _state.value = UpdateState.UpToDate
                scope.launch(Dispatchers.IO) { dir.deleteRecursively() }
            }
            // cancelled (or Play Protect said „Nicht installieren“): the APK stays, one tap starts again
            PackageInstaller.STATUS_FAILURE_ABORTED -> _state.value = release?.let { UpdateState.Available(it, downloaded(it)) } ?: UpdateState.Idle
            else -> _state.value = UpdateState.Failed(
                when (status) {
                    PackageInstaller.STATUS_FAILURE_STORAGE -> "Auf dem Handy ist nicht genug Platz für das Update."
                    PackageInstaller.STATUS_FAILURE_CONFLICT, PackageInstaller.STATUS_FAILURE_INCOMPATIBLE ->
                        "Das Update passt nicht zu dieser Installation. Lade die neue Version einmal von Hand von GitHub herunter."
                    else -> "Die Installation hat nicht geklappt. Versuch es gleich noch mal."
                },
                release,
            )
        }
    }

    companion object {
        const val RELEASES_PAGE = "https://github.com/stoegibaer/Manna/releases/latest"
        private const val LATEST_URL = "https://api.github.com/repos/stoegibaer/Manna/releases/latest"
        private const val ACTION_STATUS = "dev.tobi.manna.UPDATE_STATUS"
        private const val CHECK_INTERVAL_MS = 6 * 60 * 60 * 1000L
    }
}

class InstallReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        (context.applicationContext as MannaApp).container.updater.onStatus(context, intent)
    }
}
