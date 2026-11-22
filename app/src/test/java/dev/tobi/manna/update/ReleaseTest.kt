package dev.tobi.manna.update

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class ReleaseTest {
    @Test
    fun comparesVersionsNumerically() {
        assertTrue(Versions.isNewer("v0.2.3", "0.2.2"))
        assertTrue(Versions.isNewer("0.2.10", "0.2.9"))
        assertTrue(Versions.isNewer("1.0", "0.9.9"))
        assertFalse(Versions.isNewer("v0.2.2", "0.2.2"))
        assertFalse(Versions.isNewer("0.2.1", "0.2.2"))
        assertFalse(Versions.isNewer("0.2.2", "0.2.2-debug"))
        assertFalse(Versions.isNewer("0.2", "0.2.0"))
    }

    @Test
    fun readsGithubRelease() {
        val r = parseRelease(
            """{"tag_name":"v0.2.3","name":"Manna 0.2.3","draft":false,"prerelease":false,"html_url":"x",
               "body":"## Neu\n\n- **Updates** direkt in der App\n\nInstallation: APK herunterladen und öffnen.",
               "assets":[{"name":"notes.txt","browser_download_url":"https://e/n","size":3},
                         {"name":"manna-0.2.3.apk","browser_download_url":"https://e/a.apk","size":1234,"content_type":"x"}]}"""
        )!!
        assertEquals("0.2.3", r.version)
        assertEquals("https://e/a.apk", r.apkUrl)
        assertEquals(1234L, r.size)
        assertEquals("Neu\n\n• Updates direkt in der App", r.notes)
    }

    @Test
    fun ignoresReleasesWithoutApkOrPrerelease() {
        assertNull(parseRelease("""{"tag_name":"v1","assets":[]}"""))
        assertNull(parseRelease("""{"tag_name":"v1","prerelease":true,"assets":[{"name":"a.apk","browser_download_url":"u"}]}"""))
    }
}
