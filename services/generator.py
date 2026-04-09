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
