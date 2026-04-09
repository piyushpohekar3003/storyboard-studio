import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_script_stream(research_text, channel_config, images=None):
    system = channel_config["script_system_prompt"]

    # Build content blocks: text + images
    content = []

    text_block = f"""Here is the research document. Transform this into a complete video script following the format and style guidelines.

## Research Document

{research_text}"""

    content.append({"type": "text", "text": text_block})

    # Add images if present
    if images:
        content.append({"type": "text", "text": "\n\n## Screenshots & Charts from the Research Document\nThe following images were embedded in the research doc. Reference any relevant data, charts, or visuals in the script:"})
        for img in images:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": img["media_type"],
                    "data": img["data"],
                },
            })

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": content}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def generate_storyboard_stream(script_text, channel_config):
    system = channel_config["storyboard_system_prompt"]
    user_msg = f"""Here is the video script. Transform this into a detailed storyboard with Dialogue and Caption/Graphics columns.

## Video Script

{script_text}"""

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def redo_section_stream(full_text, selected_text, feedback, channel_config, content_type="script"):
    system = channel_config[f"{content_type}_system_prompt"]
    user_msg = f"""Here is the current {content_type}:

{full_text}

---

The user wants to revise THIS SPECIFIC SECTION:
\"\"\"{selected_text}\"\"\"

User's feedback: {feedback}

Rewrite ONLY the selected section based on the feedback. Keep everything else exactly the same. Return the COMPLETE {content_type} with only the selected section modified."""

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def structure_script_stream(script, category_key):
    """Reformat a raw script to match a category's visual framework pattern."""
    system = """You are a video script structurer for Angel One Bytes — short-form financial news reels (30-60 seconds).

You restructure raw scripts to follow precise visual framework patterns. Each category has a defined sequence of visual types.

## Rules
- The screen shows EITHER the presenter OR full-screen b-roll at any given time — never both simultaneously.
- Supers (text overlays) can accompany both presenter and b-roll shots.
- Keep the script concise — this is a reel, not a documentary.
- Every script ends with a CTA: "Stay in the loop with Angel One Bytes for more updates." or "Subscribe to Angel One Bytes for more updates."

## Category Frameworks

### Stock Price Movement
Pattern: Avatar+StockCard (price hook) → B-roll+Text (catalyst 1) → B-roll+Text (catalyst 2) → Avatar+Text (so-what) → Avatar (CTA)
Hook is always the price move. Middle sections explain the "why".

### IPO
Pattern: Avatar+Text (name+dates) → B-roll+Text (company context) → Avatar+Text (price band, issue size) → B-roll+Text (lot size, min investment) → Avatar+Text (listing date) → Avatar+Text+Disclaimer (GMP) → Avatar (CTA)
Data-heavy — dates, price band, lot size, GMP. GMP section always carries a disclaimer.

### Earnings / Results
Pattern: Avatar+Text (beat/miss headline) → [Persistent widget ON] → B-roll+Text (revenue) → B-roll+Text (profit) → B-roll+Text (TCV/deals) → B-roll+Text (dividend) → [Widget OFF] → Avatar+StockCard (price reaction) → Avatar (CTA)
Number after number. A persistent on-screen widget gives visual continuity during the data section.

### Knowledge / Macro
Pattern: Avatar+Text (headline/hook) → B-roll+Text (context/ranking/data) → B-roll+Text (supporting detail) → B-roll+Text (implication) → Avatar+Text (so-what/thesis) → Avatar (CTA)
Narrative-driven, more cinematic. Text overlays support key stats.

### Tech / Strategic Update
Pattern: Avatar+Text (announcement) → Avatar+StockCard (price reaction) → B-roll+Text (benefits checklist) → Avatar (forward-looking question) → Avatar (CTA)
Opens with announcement, grounds with stock card, checklist benefits in middle.

## Output Format
Output the restructured script as plain text, with each line prefixed by the visual type in brackets:
[Avatar + Stock Card] Voiceover line here...
[B-roll + Text] Voiceover line here... | Supers: TEXT1, TEXT2
[Avatar + Text] Voiceover line here... | Supers: TEXT1
[Avatar] CTA line here...

Include super suggestions after a | pipe character where relevant."""

    user_msg = f"""Restructure this raw script to follow the **{category_key}** category framework pattern.

## Raw Script
{script}

Output the restructured script with visual type prefixes and super suggestions."""

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def generate_visuals_stream(script, category_key):
    """Generate a shot-by-shot visual breakdown as JSON for a structured script."""
    system = """You are a visual storyboard generator for Angel One Bytes — short-form financial news reels.

You generate shot-by-shot visual breakdowns as a JSON array.

## Rules
- The screen shows EITHER the presenter OR full-screen b-roll — never both simultaneously.
- Supers (text overlays) can accompany both presenter and b-roll shots.
- Each shot should be 2-6 seconds.
- visual_type must be one of: "presenter", "broll", "presenter_stockcard"
- For b-roll shots, always provide a broll_description (what footage to use).
- Supers should be concise — max 4-5 per shot.
- Include practical production notes where helpful.

## Output Format
Output ONLY a valid JSON array (no markdown, no explanation):
[
  {
    "shot": 1,
    "voiceover": "The voiceover text for this shot...",
    "visual_type": "presenter",
    "supers": ["TEXT1", "TEXT2"],
    "broll_description": null,
    "duration_hint": "3s",
    "notes": "Any production notes"
  }
]"""

    user_msg = f"""Generate a shot-by-shot visual breakdown for this **{category_key}** category script.

## Script
{script}

Output ONLY a valid JSON array. No markdown wrapping, no explanation."""

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def redo_full_stream(full_text, feedback, channel_config, content_type="script"):
    system = channel_config[f"{content_type}_system_prompt"]
    user_msg = f"""Here is the current {content_type}:

{full_text}

---

The user wants to revise the ENTIRE {content_type} with this feedback:
{feedback}

Rewrite the complete {content_type} incorporating this feedback while maintaining the same structure and format."""

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        for text in stream.text_stream:
            yield text
