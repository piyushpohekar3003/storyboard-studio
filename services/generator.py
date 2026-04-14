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
    # Category-specific strict patterns
    CATEGORY_PATTERNS = {
        'stock': """## STRICT PATTERN: Stock Price Movement

You MUST follow this EXACT sequence. REORDER the script content to fit this structure:

LINE 1: [Avatar + Stock Card] — MUST open with the stock name and price movement (e.g. "X is up Y% today"). This is the HOOK. Extract the price data from anywhere in the script and put it FIRST.
LINE 2: [B-roll + Text] — First catalyst/reason for the move. | Supers: key data points
LINE 3: [B-roll + Text] — Second catalyst/reason. | Supers: key data points
LINE 4: [Avatar + Text] — The "so what" / analysis / significance. | Supers: key takeaway
LINE 5: [Avatar] — CTA: "Stay in the loop with Angel One Bytes for more updates."

CRITICAL: The price movement MUST be in LINE 1, even if it appears at the end of the raw script. Reorder accordingly. If there are more than 2 catalysts, combine them or add extra B-roll lines, but the FIRST line must ALWAYS be the price hook.""",

        'ipo': """## STRICT PATTERN: IPO

You MUST follow this EXACT sequence:

LINE 1: [Avatar + Text] — IPO name + open/close dates. | Supers: IPO name, dates
LINE 2: [B-roll + Text] — Company background/sector. | Supers: sector, experience
LINE 3: [Avatar + Text] — Issue size + price band. | Supers: issue size, price band
LINE 4: [B-roll + Text] — Lot size + minimum investment. | Supers: lot size, min investment
LINE 5: [Avatar + Text] — Expected listing date. | Supers: listing date
LINE 6: [Avatar + Text + Disclaimer] — GMP and listing expectation. | Supers: GMP value. MUST include disclaimer note.
LINE 7: [Avatar] — CTA.""",

        'earnings': """## STRICT PATTERN: Earnings / Results

You MUST follow this EXACT sequence:

LINE 1: [Avatar + Text] — Beat/miss headline (did they beat or miss?). | Supers: company, beat/miss
LINE 2: [B-roll + Text] — Revenue figure. | Supers: revenue number, % change. [Widget ON from here]
LINE 3: [B-roll + Text] — Profit figure. | Supers: profit number, beat/miss
LINE 4: [B-roll + Text] — Key deal metric (TCV, order book, deals). | Supers: deal numbers
LINE 5: [B-roll + Text] — Dividend or other metric. | Supers: dividend per share. [Widget OFF]
LINE 6: [Avatar + Stock Card] — Stock price reaction. | Supers: stock price, % change
LINE 7: [Avatar] — CTA.

CRITICAL: Open with beat/miss verdict, NOT the numbers. Numbers come in the middle B-roll section.""",

        'macro': """## STRICT PATTERN: Knowledge / Macro

You MUST follow this EXACT sequence:

LINE 1: [Avatar + Text] — Headline hook (the big claim/ranking/news). | Supers: key headline
LINE 2: [B-roll + Text] — Context, data, ranking details. | Supers: numbers, rankings
LINE 3: [B-roll + Text] — Supporting detail or how it happened. | Supers: key stats
LINE 4: [B-roll + Text] — Implication (what it means for investors/economy). | Supers: implications
LINE 5: [Avatar + Text] — Editorial "so what" / thesis confirmation. | Supers: thesis
LINE 6: [Avatar] — CTA.""",

        'tech': """## STRICT PATTERN: Tech / Strategic Update

You MUST follow this EXACT sequence:

LINE 1: [Avatar + Text] — The announcement (what happened). | Supers: company, announcement
LINE 2: [Avatar + Stock Card] — Stock price reaction (even if flat). | Supers: price, % change
LINE 3: [B-roll + Text] — What it enables (checklist of benefits). | Supers: ✅ benefit 1, ✅ benefit 2, ✅ benefit 3
LINE 4: [Avatar] — Forward-looking question.
LINE 5: [Avatar] — CTA.""",
    }

    pattern_block = CATEGORY_PATTERNS.get(category_key, CATEGORY_PATTERNS['stock'])

    system = f"""You are a video script structurer for Angel One Bytes — short-form financial news reels (30-60 seconds).

Your job is to REORDER and RESTRUCTURE raw scripts to follow a STRICT visual framework pattern. You must rearrange the content — do NOT just add prefixes to existing lines in their original order.

## Rules
- The screen shows EITHER the presenter OR full-screen b-roll — never both simultaneously.
- Supers (text overlays) can accompany both presenter and b-roll shots.
- Keep it concise — this is a reel, 30-60 seconds.
- REORDER content from the raw script to fit the pattern. The raw script's line order does NOT matter.
- Every script ends with a CTA.

{pattern_block}

## Output Format
Each line must start with a visual type prefix in brackets, followed by the voiceover text, followed by | Supers: if applicable.

Example:
[Avatar + Stock Card] Stock X is up 15% today — and here's why. | Supers: STOCK X, ↑ 15%
[B-roll + Text] The company just announced a major deal worth $2 billion. | Supers: $2B deal, Major expansion
[Avatar + Text] This could be a turning point for the sector. | Supers: Sector turning point
[Avatar] Stay in the loop with Angel One Bytes for more updates.

DO NOT just prefix the raw script lines in order. RESTRUCTURE the content to match the pattern."""

    user_msg = f"""Restructure this raw script to STRICTLY follow the **{category_key}** category framework.

IMPORTANT: REORDER the content. The pattern dictates which information comes first, second, etc. Extract and rearrange accordingly.

## Raw Script
{script}

Output the restructured script following the EXACT pattern above."""

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
