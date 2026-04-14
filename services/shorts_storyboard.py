"""
Visual Storyboard Generator for Shorts
Generates structured JSON from script + images using Claude API.
The JSON is then rendered into SVG frames by svg_generator.py.
"""

import json
import os
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS

client = Anthropic(api_key=ANTHROPIC_API_KEY)

STYLE_GUIDE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "style-guides",
    "a1_investors_shorts_rules.md",
)


def _load_style_guide():
    """Load the shorts visual rulebook."""
    try:
        with open(STYLE_GUIDE_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "(Style guide not found — use sensible defaults for 1080x1920 dark neon style)"


SYSTEM_PROMPT_TEMPLATE = """You are a Visual Storyboard Designer for Angel One Investors YouTube shorts.

Your job: Take a video script (with dialogue and visual cue descriptions) and convert it into a structured JSON storyboard that can be rendered as SVG frames.

## FORMAT
- Vertical video: 1080×1920px (9:16)
- Presenter: Aparna (her image is composited separately — you just decide show_presenter: true/false)
- Style: Dark background, neon-colored cards, professional financial data visualization

## VISUAL STYLE GUIDE
{style_guide}

## CRITICAL RULES

### Dialogue vs Visual
- **dialogue**: What the presenter SAYS out loud. Goes in the JSON "dialogue" field but NEVER appears as on-screen text in the SVG.
- **on_screen_elements**: Visual overlays that appear ON SCREEN as graphic elements. Only short, impactful text (stats, headlines, transition phrases) — never full sentences of dialogue.

Examples of VISUAL text (on_screen_elements): "18/20", "But today...", "Phase or Shift?", "FII Selling: >$10 Billion", "Not strength. Relative Resilience."
Examples of DIALOGUE (NOT visual): "For years, SBI was known for...", "Look at the last 1 year.", "And this is interesting."

### Frame Types
You must assign one of these 5 types to each frame:
1. **presenter** — Aparna with optional text overlay (big stat, transition phrase, key insight)
2. **presenter_cards** — Aparna with ranking cards, callout cards, or stat cards
3. **data** — No presenter. Gold headline + screenshot + stat badges. Use when showing charts, tables, or detailed data.
4. **section_header** — Aparna with a section badge pill (e.g., "THE SBI TURNAROUND")
5. **cta** — End card with Comment/Like/Subscribe CTA cards

### Screenshot Placement
- You will be shown images extracted from the input document
- Use screenshot_index to reference which image goes in which frame
- Screenshots ONLY go in "data" frames
- Not every frame needs a screenshot — only data-heavy ones

### Section Structure
Group frames into narrative sections (e.g., "HOOK", "THE SBI TURNAROUND", "MACRO CONTEXT", "CLOSING / CTA")
Each section has a label and contains 1+ frames.

## OUTPUT JSON SCHEMA

```json
{{
  "metadata": {{
    "title": "Video title",
    "total_frames": 16
  }},
  "sections": [
    {{
      "section_label": "HOOK",
      "frames": [
        {{
          "frame_number": 1,
          "frame_type": "presenter_cards",
          "dialogue": "SBI has just overtaken ICICI Bank in market cap.",
          "visual_cue": "Market cap ranking visual showing HDFC #1, SBI #2 (up), ICICI #3 (down)",
          "headline": null,
          "headline_sub": null,
          "on_screen_elements": [
            {{
              "type": "ranking_card",
              "items": [
                {{"rank": "#1", "label": "HDFC Bank", "sublabel": "Largest by Market Cap", "color": "muted", "highlight": false}},
                {{"rank": "#2", "label": "SBI", "sublabel": "State Bank of India", "color": "mint", "badge": "▲ UP", "highlight": true}},
                {{"rank": "#3", "label": "ICICI Bank", "sublabel": "Now 3rd Largest", "color": "red", "badge": "▼ DOWN", "highlight": false}}
              ]
            }},
            {{
              "type": "bottom_text",
              "text": "India's 2nd Largest Bank by Market Value",
              "color": "gold"
            }}
          ],
          "screenshot_index": null,
          "show_presenter": true,
          "source": null
        }}
      ]
    }}
  ]
}}
```

### Element Types for on_screen_elements:

**text_overlay** — Big text displayed on screen
Fields: type, text, color, font_size (48-140), weight ("400"|"500"|"600"|"700"|"800")

**ranking_card** — Stacked ranking rows
Fields: type, items (array of {{rank, label, sublabel, color, badge, highlight}})

**callout_card** — Numbered callout cards
Fields: type, items (array of {{number, text, color}})

**stat_badge** — Data stat badges (used below screenshots in data frames)
Fields: type, items (array of {{label, value, color}})

**section_badge** — Section header pill
Fields: type, text, color

**cta_card** — CTA action cards
Fields: type, items (array of {{text, color}})

**bottom_text** — Annotation text at bottom of card area
Fields: type, text, color

## GUIDELINES
- Aim for 12-20 frames total for a short
- Don't overload frames — max 3-4 visual elements per presenter frame
- Use section_header frames to transition between narrative sections
- Every short should end with a cta frame
- Use "presenter" (bare) frames for emotional beats, curiosity builders, transitions
- Use "data" frames only when there's actual chart/table data to show
- Color cycle for multi-item lists: cyan → gold → purple → mint → red

Output ONLY the JSON. No markdown, no explanation, no code fences. Just the raw JSON object.
"""


def _build_system_prompt():
    """Build the full system prompt with style guide injected."""
    style_guide = _load_style_guide()
    return SYSTEM_PROMPT_TEMPLATE.format(style_guide=style_guide)


def _build_user_content(script_text, images=None, feedback=None, previous_json=None):
    """Build the user message content blocks (text + optional images)."""
    content = []

    # Main instruction
    text_parts = [f"## Script\n\n{script_text}\n"]

    if images:
        text_parts.append(f"\n## Available Images ({len(images)} extracted from document)")
        for i, img in enumerate(images):
            desc = img.get("description", f"Image {i}")
            text_parts.append(f"- Image {i}: {desc}")
        text_parts.append(
            "\nUse screenshot_index to reference these images in data frames. "
            "Look at each image carefully to understand what data it contains."
        )

    if previous_json and feedback:
        text_parts.append(f"\n## Previous Storyboard (to revise)\n{previous_json}\n")
        text_parts.append(f"\n## Feedback\n{feedback}\n")
        text_parts.append(
            "Revise the storyboard based on this feedback. "
            "Output the complete revised JSON (all frames, not just changed ones)."
        )
    else:
        text_parts.append(
            "\nGenerate the complete visual storyboard JSON for this short-form video."
        )

    content.append({"type": "text", "text": "\n".join(text_parts)})

    # Add images as multimodal content blocks
    if images:
        for i, img in enumerate(images):
            content.append({
                "type": "text",
                "text": f"\n--- Image {i} ---",
            })
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": img.get("media_type", "image/png"),
                    "data": img["data"],
                },
            })

    return content


def generate_visual_storyboard_stream(script_text, images=None, feedback=None, previous_json=None):
    """
    Stream the visual storyboard JSON from Claude.

    Args:
        script_text: The video script (dialogue + visual cues)
        images: List of dicts with {media_type, data, description, width, height}
        feedback: Optional feedback for redo
        previous_json: Optional previous storyboard JSON string for redo

    Yields:
        Text chunks of the JSON response
    """
    system = _build_system_prompt()
    content = _build_user_content(script_text, images, feedback, previous_json)

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": content}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def add_image_to_storyboard_stream(storyboard_json, new_image, script_text):
    """
    Stream a revised storyboard JSON that incorporates a new image.

    The LLM decides which frame the image belongs to, or creates a new data frame.

    Args:
        storyboard_json: Current storyboard JSON string
        new_image: Dict with {media_type, data, description}
        script_text: Original script text for context

    Yields:
        Text chunks of the revised JSON
    """
    system = _build_system_prompt()

    content = [
        {
            "type": "text",
            "text": (
                f"## Current Storyboard\n{storyboard_json}\n\n"
                f"## Original Script\n{script_text}\n\n"
                "## New Image to Place\n"
                "A new image has been added. Look at it carefully and decide:\n"
                "1. Which existing data frame should it go into? (update screenshot_index)\n"
                "2. Or should a new data frame be created for it?\n"
                "3. What headline and stat badges should accompany it?\n\n"
                "Output the complete revised storyboard JSON with the image placed."
            ),
        },
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": new_image.get("media_type", "image/png"),
                "data": new_image["data"],
            },
        },
    ]

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": content}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def parse_storyboard_json(raw_text):
    """
    Parse the LLM output into a storyboard dict.
    Handles common issues: markdown code fences, trailing commas.
    """
    text = raw_text.strip()

    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines if they're fences
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try fixing trailing commas (common LLM issue)
    import re
    text = re.sub(r",\s*([}\]])", r"\1", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse storyboard JSON: {e}\nRaw text starts with: {text[:200]}")
