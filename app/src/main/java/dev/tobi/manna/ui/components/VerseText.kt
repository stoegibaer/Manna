package dev.tobi.manna.ui.components

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.foundation.text.appendInlineContent
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Bookmark
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.Placeholder
import androidx.compose.ui.text.PlaceholderVerticalAlign
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.BaselineShift
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import dev.tobi.manna.data.bible.Verse

/** Key of a verse for favorite sets. */
fun Verse.key() = Triple(book, chapter, verse)

/**
 * One verse with a small verse number. Long-press saves it as a favorite (bookmark mark at the end);
 * [highlighted] marks the verse that is being read aloud.
 */
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun VerseText(
    verse: Verse,
    style: TextStyle,
    modifier: Modifier = Modifier,
    alpha: Float = 1f,
    highlighted: Boolean = false,
    favorite: Boolean = false,
    onTap: () -> Unit = {},
    onLongPress: () -> Unit = {},
) {
    val primary = MaterialTheme.colorScheme.primary
    val text = buildAnnotatedString {
        withStyle(SpanStyle(fontSize = 0.62.em, color = primary, baselineShift = BaselineShift(0.35f), fontWeight = FontWeight.Bold)) {
            append("${verse.verse} ")
        }
        append(verse.text)
        if (favorite) { append(" "); appendInlineContent("fav", "[Lieblingsvers]") }
    }
    val inline = mapOf(
        "fav" to InlineTextContent(Placeholder(0.9.em, 0.9.em, PlaceholderVerticalAlign.TextCenter)) {
            Icon(Icons.Rounded.Bookmark, contentDescription = "Lieblingsvers", tint = MaterialTheme.colorScheme.secondary, modifier = Modifier.fillMaxSize())
        }
    )
    Text(
        text,
        style = style,
        inlineContent = inline,
        color = MaterialTheme.colorScheme.onBackground,
        modifier = modifier
            .fillMaxWidth()
            .alpha(alpha)
            .background(if (highlighted) MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.55f) else Color.Transparent, RoundedCornerShape(8.dp))
            .combinedClickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onTap,
                onLongClick = onLongPress,
            )
            .padding(horizontal = 4.dp, vertical = 2.dp),
    )
}
