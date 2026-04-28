# Slack mrkdwn Complete Reference Guide

This document provides comprehensive details on Slack's markdown variant ("mrkdwn"), including syntax comparisons, edge cases, and best practices.

## Official Documentation Sources

- **Slack API Reference**: https://api.slack.com/reference/surfaces/formatting
- **Slack Developer Documentation**: https://docs.slack.dev/messaging/formatting-message-text
- **Block Kit Builder**: https://api.slack.com/block-kit/building
- **DX Documentation Guide**: https://docs.getdx.com/slack-markdown/
- **SupraSend mrkdwn Guide**: https://dev.to/suprsend/the-only-guide-to-slack-mrkdwn-not-markdown-formatting-w-codes-4329
- **Wrangle Comprehensive Guide**: https://www.wrangle.io/post/slack-markdown-a-comprehensive-guide-to-formatting-messages

## Complete Syntax Comparison Table

| Feature | Standard Markdown | Slack mrkdwn | Notes |
|---------|------------------|--------------|-------|
| **Bold** | `**text**` or `__text__` | `*text*` | Single asterisks only |
| **Italic** | `*text*` or `_text_` | `_text_` | Underscores only |
| **Strikethrough** | `~~text~~` | `~text~` | Single tildes |
| **Inline code** | `` `code` `` | `` `code` `` | Same syntax |
| **Code block** | ` ```lang\ncode\n``` ` | ` ```\ncode\n``` ` | No language syntax highlighting |
| **Blockquote** | `> quote` | `> quote` | Same for single line |
| **Multi-line quote** | `> line1\n> line2` | `>>> multi\nline\nquote` | Slack has special multi-line syntax |
| **Link** | `[text](url)` | `<url\|text>` | Completely different syntax |
| **Auto-link** | `<url>` | `<url>` | Same syntax |
| **Unordered list** | `- item` or `* item` | `- item` or `* item` | Both work, rendering may differ |
| **Ordered list** | `1. item` | Limited support | Better to use bullets |
| **Headings** | `# H1`, `## H2`, etc. | Not supported | Use bold text instead |
| **Tables** | Markdown tables | Not supported | Use Block Kit or pre-formatted text |
| **Images** | `![alt](url)` | Not supported | Use Block Kit image blocks |
| **Horizontal rule** | `---` or `***` | Not supported | Use Block Kit dividers |
| **HTML** | Sometimes supported | Not supported | Use Block Kit instead |
| **Task lists** | `- [ ]` and `- [x]` | Not supported | Use emoji checkmarks |

## Text Formatting Details

### Bold Text

**Syntax:** `*bold text*`

**Requirements:**
- Must have spaces or punctuation before/after asterisks
- Does NOT work mid-word: `wo*rd*` will not bold "rd"
- DOES work: `This is *bold* text`

**Examples:**
```
*Bold at start* of sentence
Word in *bold* here
*Bold* and *more bold*
```

**Common mistakes:**
```
No*space*works - ❌ Won't render as bold
*Nospaceatstart-❌
```

### Italic Text

**Syntax:** `_italic text_`

**Requirements:**
- Must have spaces or punctuation before/after underscores
- Does NOT work mid-word
- Cannot be nested with bold

**Examples:**
```
This is _italic text_
_Italic_ at the start
```

### Strikethrough

**Syntax:** `~strikethrough~`

**Requirements:**
- Single tildes (not double like standard markdown)
- Must have spaces or punctuation boundaries

**Examples:**
```
This is ~wrong~ correct
~Entire phrase can be struck~
```

### Code Formatting

**Inline code:** `` `code` ``
- Same as standard markdown
- Preserves exact spacing
- Disables other formatting

**Code blocks:**
```
```
multi-line
code block
```
```

**Important notes:**
- No language syntax highlighting (no `python`, `javascript`, etc.)
- All code blocks render the same way
- Indentation and spacing preserved exactly

## Links

### Standard Links with Text

**Syntax:** `<url|link text>`

**Examples:**
```
<https://example.com|Visit Example>
<https://slack.com|Slack Homepage>
<mailto:user@example.com|Email Us>
```

**Notes:**
- Pipe character `|` separates URL from display text
- No nested formatting in link text
- URL must be complete (include protocol)

### Auto-Links

**Syntax:** `<url>`

**Examples:**
```
<https://example.com>
<mailto:user@example.com>
```

**Behavior:**
- Automatically creates clickable link
- Shows full URL as text
- No custom text display

### Email Links

```
<mailto:email@example.com|Email Support>
<mailto:email@example.com>  # Shows email address
```

## Slack-Specific Features

### User Mentions

**By User ID (recommended):**
```
<@U12345678>
```

**By Username (limited contexts):**
```
<@username>
```

**Behavior:**
- Highlights the mentioned user
- Sends notification to user
- Displays user's display name (not ID)
- Only works with valid user IDs in the workspace

**Finding User IDs:**
- Use Slack API methods like `users.list`
- Check user profile in Slack (View profile → More → Copy member ID)
- Available in webhook payloads and events

### Channel Mentions

**Basic syntax:**
```
<#C12345678>
```

**With custom display name:**
```
<#C12345678|general>
```

**Behavior:**
- Creates clickable channel link
- Shows channel name (with #)
- Only works with valid channel IDs

### Special Mentions

**Notify active users:**
```
<!here>
```
- Notifies only currently active users in channel
- Use for time-sensitive, non-critical updates

**Notify all channel members:**
```
<!channel>
```
- Notifies ALL members of the channel (even inactive)
- Use sparingly for important announcements

**Notify entire workspace:**
```
<!everyone>
```
- Notifies EVERYONE in the workspace
- Usually restricted to admins
- Use only for critical, workspace-wide announcements

**Other special mentions:**
```
<!date^timestamp^format|fallback>
<!subteam^ID|handle>  # User group mentions
```

### Date Formatting

**Syntax:**
```
<!date^unix_timestamp^format_string|fallback_text>
```

**Common format strings:**
- `{date_short}` - "Feb 18, 2014"
- `{date_long}` - "February 18, 2014"
- `{date_pretty}` - "February 18, 2014"
- `{date_num}` - "02/18/2014"
- `{time}` - "2:34 PM"
- `{time_secs}` - "2:34:56 PM"

**Example:**
```
<!date^1392734382^{date_short} at {time}|Feb 18, 2014 at 2:34 PM>
```

**Behavior:**
- Displays in user's timezone automatically
- Falls back to provided text if formatting fails
- Useful for scheduling and time-based notifications

### Emoji

**Syntax:** `:emoji_name:`

**Examples:**
```
:smile: :rocket: :white_check_mark:
:tada: :fire: :eyes:
```

**Custom emoji:**
```
:custom_emoji_name:
```

**Notes:**
- Must match Slack's emoji names exactly
- Custom emoji must exist in the workspace
- Emoji codes: https://www.webfx.com/tools/emoji-cheat-sheet/

## Lists and Structured Content

### Unordered Lists

**Syntax:**
```
• Item 1
• Item 2
• Item 3
```

OR

```
- Item 1
- Item 2
- Item 3
```

**Notes:**
- Both `•` and `-` work
- Consistent indentation recommended
- Nested lists have limited support

### Ordered Lists

**Limited support:**
```
1. First item
2. Second item
3. Third item
```

**Best practice:**
- Use bullet points instead
- If numbering is needed, include in text:
```
• Step 1: Do this
• Step 2: Do that
• Step 3: Finish
```

### Structured Layouts

For complex layouts with columns, sections, or interactive elements, use Block Kit instead of plain mrkdwn.

## Blockquotes

### Single-Line Quote

**Syntax:** `> quote text`

**Example:**
```
> This is a quoted line
```

### Multi-Line Quote

**Syntax:** `>>>` followed by all quote content

**Example:**
```
>>> This is a multi-line quote.
It continues here.
And here.
All text after >>> is quoted.
```

**Notes:**
- Everything after `>>>` is quoted until end of message or Block Kit section
- No closing syntax needed
- Cannot end mid-message (continues to end)

## Edge Cases and Limitations

### Nested Formatting

**NOT supported:**
```
*bold and _italic_ together*  # ❌ Won't work
_italic with *bold* inside_    # ❌ Won't work
```

**Workaround:**
- Use separate formatting: `*bold* and _italic_`
- Consider Block Kit rich text for complex formatting

### Escaping Characters

**To display special characters literally:**
```
\*not bold\*
\_not italic\_
\~not strikethrough\~
```

**Escaping in links:**
```
<https://example.com?param=value\&other=value|Link>
```

### Whitespace and Line Breaks

**Single line break:**
- Press Enter once
- Creates a line break in the message

**Paragraph break:**
- Press Enter twice
- Creates visible spacing between paragraphs

**Preserving formatting:**
- Use code blocks for exact spacing
- Blockquotes preserve line breaks

### Character Limits

- **Single message:** ~40,000 characters (webhook/API)
- **Text block in Block Kit:** ~3,000 characters
- **Link text:** ~300 characters recommended

### URLs and Auto-Linking

**Auto-linked URLs:**
- Slack automatically links `http://` and `https://` URLs
- Also auto-links emails
- No need to use `<url>` syntax unless customizing text

**Example:**
```
Check out https://example.com  # Auto-linked
Or <https://example.com|click here>  # Custom text
```

## Block Kit Integration

### When to Use Block Kit vs mrkdwn

**Use plain mrkdwn for:**
- Simple text messages
- Quick notifications
- User-to-user chat
- Bot responses without interaction

**Use Block Kit for:**
- Rich layouts with sections and columns
- Interactive elements (buttons, menus, modals)
- Structured data display
- Images and media
- Forms and user input

### mrkdwn in Block Kit

Block Kit text fields can use mrkdwn:

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "This is *bold* and this is _italic_ with <https://example.com|a link>"
  }
}
```

**Block Kit text types:**
- `"type": "mrkdwn"` - Enables mrkdwn formatting
- `"type": "plain_text"` - No formatting, displays literally

### Block Kit Builder

Interactive tool for designing Block Kit messages:
https://api.slack.com/block-kit/building

**Features:**
- Visual message editor
- Real-time preview
- JSON payload generator
- Template library

## Best Practices

### Message Formatting

1. **Keep it readable:**
   - Use formatting sparingly
   - Don't overuse bold/italic
   - Break up long messages into sections

2. **Use appropriate mentions:**
   - `<!here>` for time-sensitive, non-critical
   - `<!channel>` for important channel announcements
   - `<!everyone>` only for critical workspace alerts
   - Avoid mass mentions for routine messages

3. **Link text should be descriptive:**
   ```
   ✅ <https://docs.example.com|View Documentation>
   ❌ <https://docs.example.com|click here>
   ```

4. **Code formatting:**
   - Use inline code for commands, variables, file names
   - Use code blocks for multi-line code or output
   - Don't use code blocks for emphasis

5. **Structure long messages:**
   - Use bullet points for lists
   - Use blockquotes for references or quotes
   - Consider Block Kit for complex layouts

### Accessibility

1. **Don't rely solely on formatting:**
   - Don't use bold as only indication of importance
   - Include context in text, not just formatting

2. **Link text should be meaningful:**
   - Screen readers read link text
   - Avoid "click here" or bare URLs

3. **Use emoji thoughtfully:**
   - Can enhance meaning but don't rely on them
   - Provide text alternatives when critical

### Performance

1. **Message size:**
   - Keep messages under 4,000 characters when possible
   - Break very long content into multiple messages
   - Use Block Kit for large structured data

2. **Avoid excessive mentions:**
   - Mass mentions can cause notification fatigue
   - Consider DMs for urgent individual notifications

3. **Rate limits:**
   - Respect Slack API rate limits
   - Consider batching messages when possible

## Common Mistakes

### 1. Using Standard Markdown Syntax

**Wrong:**
```
**bold**  # Won't work
# Heading  # Won't work
[link](url)  # Won't work
```

**Right:**
```
*bold*
*Heading in bold*
<url|link>
```

### 2. Mid-Word Formatting

**Wrong:**
```
un*bold*ed  # Won't format
in_italic_ed  # Won't format
```

**Right:**
```
un-*bold*-ed  # Use separators
in *italic* text  # Separate words
```

### 3. Nested Formatting

**Wrong:**
```
*bold _and italic_*  # Won't work
```

**Right:**
```
*bold* and _italic_  # Separate
```

### 4. Incorrect Link Syntax

**Wrong:**
```
[Visit site](https://example.com)  # Standard markdown
<https://example.com, visit site>  # Wrong separator
```

**Right:**
```
<https://example.com|Visit site>  # Pipe separator
```

### 5. Invalid Mentions

**Wrong:**
```
@username  # Plain text, no notification
<@username>  # May not work without valid ID
```

**Right:**
```
<@U12345678>  # Valid user ID
```

## Testing and Validation

### Testing Messages

1. **Use Slack App tester:**
   - Block Kit Builder preview
   - Test in private channel first
   - Verify formatting renders correctly

2. **Check mentions:**
   - Verify user/channel IDs are valid
   - Confirm notifications are sent
   - Test special mentions in safe channel

3. **Cross-platform testing:**
   - Desktop app
   - Mobile app
   - Web client

### Debugging

**Common issues:**

1. **Formatting not rendering:**
   - Check for spaces around format markers
   - Verify not mid-word
   - Ensure proper syntax

2. **Links not working:**
   - Verify pipe separator `|` not comma
   - Check URL includes protocol
   - Ensure no nested formatting

3. **Mentions not notifying:**
   - Verify user/channel IDs are correct
   - Check bot has permission to mention
   - Confirm users are in the channel

## Migration from Standard Markdown

When converting standard markdown to Slack mrkdwn:

1. **Replace bold:**
   - Find: `**text**` or `__text__`
   - Replace: `*text*`

2. **Replace italic:**
   - Find: `*text*`
   - Replace: `_text_`

3. **Replace strikethrough:**
   - Find: `~~text~~`
   - Replace: `~text~`

4. **Convert links:**
   - Find: `[text](url)`
   - Replace: `<url|text>`

5. **Remove headings:**
   - Find: `# Heading`
   - Replace: `*Heading*` (use bold instead)

6. **Handle tables:**
   - Convert to bulleted lists or
   - Use Block Kit sections

7. **Handle images:**
   - Remove `![alt](url)` syntax
   - Use Block Kit image blocks or share links

## Quick Reference Card

### Essential Syntax

| Formatting | Syntax | Example |
|------------|--------|---------|
| Bold | `*text*` | This is *bold* |
| Italic | `_text_` | This is _italic_ |
| Strikethrough | `~text~` | This is ~wrong~ |
| Code | `` `code` `` | Run `npm install` |
| Link | `<url\|text>` | <https://slack.com\|Slack> |
| Mention | `<@U123>` | Hey <@U123> |
| Channel | `<#C123>` | See <#C123> |
| Quote | `> text` | > Quoted |
| Multi-quote | `>>> text` | >>> Multiple<br>lines |
| Emoji | `:name:` | :smile: |

### Special Mentions

| Mention | Effect |
|---------|--------|
| `<!here>` | Active users in channel |
| `<!channel>` | All channel members |
| `<!everyone>` | Entire workspace |

## Additional Resources

- **Slack API Documentation**: https://api.slack.com/
- **Block Kit Framework**: https://api.slack.com/block-kit
- **mrkdwn Formatting Guide**: https://api.slack.com/reference/surfaces/formatting
- **Emoji Cheat Sheet**: https://www.webfx.com/tools/emoji-cheat-sheet/
- **Block Kit Builder**: https://api.slack.com/block-kit/building
- **Message Builder**: https://app.slack.com/block-kit-builder
