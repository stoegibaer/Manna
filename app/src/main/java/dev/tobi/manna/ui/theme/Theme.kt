package dev.tobi.manna.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import dev.tobi.manna.data.settings.ThemeMode

private val Light = lightColorScheme(
    primary = Color(0xFF2F6B4F),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFD3EADB),
    onPrimaryContainer = Color(0xFF0E2C1E),
    secondary = Color(0xFFB8860B),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFF6E7B8),
    onSecondaryContainer = Color(0xFF3A2B00),
    tertiary = Color(0xFF7A5C3E),
    background = Color(0xFFFAF7F0),
    onBackground = Color(0xFF1F1D1A),
    surface = Color(0xFFFFFDF8),
    onSurface = Color(0xFF1F1D1A),
    surfaceVariant = Color(0xFFEFEADF),
    onSurfaceVariant = Color(0xFF55514A),
    surfaceContainer = Color(0xFFF3EFE6),
    surfaceContainerHigh = Color(0xFFECE7DC),
    outline = Color(0xFFB9B2A5),
    error = Color(0xFFB4532A),
    errorContainer = Color(0xFFFBE3D6),
    onErrorContainer = Color(0xFF4A1A05),
)

private val Dark = darkColorScheme(
    primary = Color(0xFF8FCDAA),
    onPrimary = Color(0xFF0B2A1C),
    primaryContainer = Color(0xFF1E4A35),
    onPrimaryContainer = Color(0xFFD3EADB),
    secondary = Color(0xFFE7C15C),
    onSecondary = Color(0xFF3A2B00),
    secondaryContainer = Color(0xFF4D3C0C),
    onSecondaryContainer = Color(0xFFF6E7B8),
    tertiary = Color(0xFFD7B898),
    background = Color(0xFF15171A),
    onBackground = Color(0xFFE8E4DC),
    surface = Color(0xFF1B1E21),
    onSurface = Color(0xFFE8E4DC),
    surfaceVariant = Color(0xFF2A2D30),
    onSurfaceVariant = Color(0xFFBDB7AD),
    surfaceContainer = Color(0xFF212427),
    surfaceContainerHigh = Color(0xFF282B2F),
    outline = Color(0xFF5C5953),
    error = Color(0xFFF0A27E),
    errorContainer = Color(0xFF5A2A14),
    onErrorContainer = Color(0xFFFBE3D6),
)

/** Extra colors not covered by Material. */
@Immutable
data class MannaColors(
    val leaf: Color, val leafDark: Color, val trunk: Color, val blossom: Color, val ground: Color, val success: Color,
    val sea: Color = Color.Blue, val land: Color = Color.LightGray, val river: Color = Color.Blue, val marker: Color = Color.Red,
    val dark: Boolean = false,
)

val LocalMannaColors = staticCompositionLocalOf {
    MannaColors(Color.Green, Color.Green, Color.Gray, Color.Yellow, Color.Gray, Color.Green)
}

private val LightExtra = MannaColors(
    leaf = Color(0xFF5E9E62), leafDark = Color(0xFF3F7A4A), trunk = Color(0xFF7A5C3E),
    blossom = Color(0xFFE8B931), ground = Color(0xFFD9CFBD), success = Color(0xFF2F7D4F),
    sea = Color(0xFFCFE0E8), land = Color(0xFFF1E8D4), river = Color(0xFF7FA7C2), marker = Color(0xFFB4532A),
)
private val DarkExtra = MannaColors(
    leaf = Color(0xFF7FBF84), leafDark = Color(0xFF5A9B66), trunk = Color(0xFFB08A63),
    blossom = Color(0xFFF2C94C), ground = Color(0xFF3A3631), success = Color(0xFF8FCDAA),
    sea = Color(0xFF15212B), land = Color(0xFF3B372F), river = Color(0xFF5B8BA8), marker = Color(0xFFF0A27E),
    dark = true,
)

val BibleFont = FontFamily.Serif

fun bibleTextStyle(scale: Float) = TextStyle(fontFamily = BibleFont, fontSize = (19 * scale).sp, lineHeight = (30 * scale).sp)

private val Type = Typography().let { t ->
    t.copy(
        headlineLarge = t.headlineLarge.copy(fontFamily = BibleFont, fontWeight = FontWeight.SemiBold),
        headlineMedium = t.headlineMedium.copy(fontFamily = BibleFont, fontWeight = FontWeight.SemiBold),
        headlineSmall = t.headlineSmall.copy(fontFamily = BibleFont, fontWeight = FontWeight.SemiBold),
        titleLarge = t.titleLarge.copy(fontFamily = BibleFont, fontWeight = FontWeight.SemiBold),
    )
}

@Composable
fun MannaTheme(mode: ThemeMode, content: @Composable () -> Unit) {
    val dark = when (mode) {
        ThemeMode.SYSTEM -> isSystemInDarkTheme()
        ThemeMode.LIGHT -> false
        ThemeMode.DARK -> true
    }
    androidx.compose.runtime.CompositionLocalProvider(LocalMannaColors provides if (dark) DarkExtra else LightExtra) {
        MaterialTheme(colorScheme = if (dark) Dark else Light, typography = Type, content = content)
    }
}
