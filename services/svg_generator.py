"""
SVG template engine for Shorts storyboard frames.

Converts a JSON frame definition into a valid SVG string (1080x1920, 9:16 vertical).
Also generates the storyboard.html overview page from the complete storyboard JSON.
"""

import html
import os
import math


# ── Color palette ──────────────────────────────────────────────────────────────

COLORS = {
    "cyan": "#00e5ff",
    "gold": "#ffd700",
    "purple": "#b388ff",
    "mint": "#00e5a0",
    "red": "#ff4466",
    "white": "#ffffff",
    "muted": "#6a6a7a",
    "body": "#b0b0b8",
}

FONT = "'Poppins', sans-serif"


def _esc(text):
    """XML-escape a string for safe embedding in SVG."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def _color(name):
    """Resolve a color name to its hex value, or pass through raw hex."""
    if name is None:
        return COLORS["white"]
    if name.startswith("#"):
        return name
    return COLORS.get(name, COLORS["white"])


# ── SVG Frame Renderer ────────────────────────────────────────────────────────

class ShortsFrameRenderer:
    """Renders a single storyboard frame as an SVG string."""

    def render(self, frame: dict, screenshot_dir: str = "", aparna_path: str = "aparna.png") -> str:
        """Generate complete SVG string for a frame."""
        frame_type = frame.get("frame_type", "presenter")
        dispatcher = {
            "presenter": self._render_presenter,
            "presenter_cards": self._render_presenter_cards,
            "data": self._render_data,
            "section_header": self._render_section_header,
            "cta": self._render_cta,
        }
        render_fn = dispatcher.get(frame_type, self._render_presenter)

        if frame_type == "data":
            content = render_fn(frame, screenshot_dir)
        else:
            content = render_fn(frame)

        # Add presenter image if requested
        show_presenter = frame.get("show_presenter", False)
        if show_presenter:
            content += self._presenter_image(aparna_path)

        # Add source line if present
        source = frame.get("source")
        if source:
            content += self._source(source)

        return self._wrap_svg(
            self._bg()
            + self._logo()
            + content
            + self._disclaimer()
        )

    # ── Boilerplate pieces ─────────────────────────────────────────────────

    def _wrap_svg(self, content: str) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">\n'
            "  <defs>\n"
            '    <radialGradient id="warm-bl" cx="0%" cy="100%" r="60%">'
            '<stop offset="0%" stop-color="#b4641e" stop-opacity="0.2"/>'
            '<stop offset="100%" stop-color="#b4641e" stop-opacity="0"/>'
            "</radialGradient>\n"
            '    <radialGradient id="warm-tr" cx="100%" cy="0%" r="50%">'
            '<stop offset="0%" stop-color="#b4641e" stop-opacity="0.1"/>'
            '<stop offset="100%" stop-color="#b4641e" stop-opacity="0"/>'
            "</radialGradient>\n"
            '    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">'
            '<circle cx="2" cy="2" r="1.5" fill="#b4641e" opacity="0.12"/>'
            "</pattern>\n"
            "  </defs>\n"
            f"{content}"
            "</svg>\n"
        )

    def _bg(self) -> str:
        return (
            '  <g id="BG">\n'
            '    <rect width="1080" height="1920" fill="#0a0a0f"/>\n'
            '    <rect width="1080" height="1920" fill="url(#warm-bl)"/>\n'
            '    <rect width="1080" height="1920" fill="url(#warm-tr)"/>\n'
            '    <rect x="0" y="0" width="300" height="400" fill="url(#dots)" opacity="0.5"/>\n'
            '    <rect x="780" y="1520" width="300" height="400" fill="url(#dots)" opacity="0.5"/>\n'
            "  </g>\n"
        )

    def _logo(self) -> str:
        return (
            '  <g id="LOGO">\n'
            f'    <text x="980" y="80" text-anchor="end" font-family="{FONT}" '
            f'font-weight="800" font-size="28" fill="#ffffff" letter-spacing="1">'
            f'Angel<tspan font-weight="400">One</tspan></text>\n'
            "  </g>\n"
        )

    def _disclaimer(self) -> str:
        return (
            '  <g id="DISCLAIMER">\n'
            f'    <text x="540" y="1880" text-anchor="middle" font-family="{FONT}" '
            f'font-weight="400" font-size="14" fill="#6a6a7a" opacity="0.5">'
            f"This video is for educational/informational purposes only</text>\n"
            "  </g>\n"
        )

    def _presenter_image(self, path: str) -> str:
        # From 34 reference screenshots:
        # Aparna fills 80%+ of frame. Head at y~15-20% (y=290-380).
        # Body extends to y~95% (y=1820). She's centered horizontally.
        # Image must be LARGE — covering most of the frame.
        return (
            '  <g id="PRESENTER-IMAGE">\n'
            f'    <image href="{_esc(path)}" x="90" y="350" width="900" height="1550" '
            f'preserveAspectRatio="xMidYMax meet"/>\n'
            "  </g>\n"
        )

    def _source(self, text: str) -> str:
        return (
            '  <g id="SOURCE">\n'
            f'    <text x="540" y="1500" text-anchor="middle" font-family="{FONT}" '
            f'font-weight="400" font-size="16" fill="#6a6a7a">{_esc(text)}</text>\n'
            "  </g>\n"
        )

    # ── Frame type dispatchers ─────────────────────────────────────────────

    def _render_presenter(self, frame: dict) -> str:
        """Presenter frame: text overlays + optional on-screen elements."""
        parts = []
        elements = frame.get("on_screen_elements") or []

        text_overlays = [e for e in elements if e.get("type") == "text_overlay"]
        other_elements = [e for e in elements if e.get("type") != "text_overlay"]

        if text_overlays:
            parts.append(self._render_text_overlays(text_overlays))
        else:
            # Empty presenter text group
            parts.append('  <g id="PRESENTER-TEXT">\n  </g>\n')

        for elem in other_elements:
            parts.append(self._render_element(elem))

        # Bottom text
        bottom = next((e for e in elements if e.get("type") == "bottom_text"), None)
        if bottom:
            parts.append(self._render_bottom_text(bottom))

        return "".join(parts)

    def _render_presenter_cards(self, frame: dict) -> str:
        """Presenter + cards frame: section badge, callout cards, ranking cards, etc."""
        parts = []
        elements = frame.get("on_screen_elements") or []

        for elem in elements:
            parts.append(self._render_element(elem))

        return "".join(parts)

    def _render_data(self, frame: dict, screenshot_dir: str = "") -> str:
        """Data frame: headline + screenshot + stat badges."""
        parts = []

        # Gold headline
        headline = frame.get("headline")
        headline_sub = frame.get("headline_sub")
        if headline:
            parts.append(self._render_headline(headline, headline_sub))

        # Screenshot
        screenshot_index = frame.get("screenshot_index")
        screenshot_y = 340
        screenshot_h = 760
        if screenshot_index is not None:
            parts.append(self._render_screenshot(screenshot_index, screenshot_dir, screenshot_y, screenshot_h))

        # On-screen elements (stat badges, etc.)
        elements = frame.get("on_screen_elements") or []
        stat_start_y = 1140 if screenshot_index is not None else 400
        for elem in elements:
            if elem.get("type") == "stat_badge":
                parts.append(self._render_stat_badges(elem, stat_start_y))
            else:
                parts.append(self._render_element(elem))

        return "".join(parts)

    def _render_section_header(self, frame: dict) -> str:
        """Section header: section badge centered, presenter below."""
        parts = []
        elements = frame.get("on_screen_elements") or []

        for elem in elements:
            parts.append(self._render_element(elem))

        if not elements:
            parts.append('  <g id="PRESENTER-TEXT">\n  </g>\n')

        return "".join(parts)

    def _render_cta(self, frame: dict) -> str:
        """CTA / end card frame."""
        parts = []
        elements = frame.get("on_screen_elements") or []

        # Top text overlays
        text_overlays = [e for e in elements if e.get("type") == "text_overlay"]
        if text_overlays:
            parts.append(self._render_text_overlays(text_overlays))
        else:
            parts.append('  <g id="TOP-TEXT">\n  </g>\n')

        # CTA cards and other elements
        other = [e for e in elements if e.get("type") != "text_overlay"]
        for elem in other:
            parts.append(self._render_element(elem))

        return "".join(parts)

    # ── Element dispatcher ─────────────────────────────────────────────────

    def _render_element(self, elem: dict) -> str:
        """Dispatch to the correct element renderer."""
        t = elem.get("type", "")
        dispatch = {
            "text_overlay": lambda e: self._render_text_overlays([e]),
            "ranking_card": self._render_ranking_cards,
            "callout_card": self._render_callout_cards,
            "stat_badge": lambda e: self._render_stat_badges(e, 1140),
            "section_badge": self._render_section_badge,
            "cta_card": self._render_cta_cards,
            "bottom_text": self._render_bottom_text,
        }
        fn = dispatch.get(t)
        if fn:
            return fn(elem)
        return ""

    # ── Element renderers ──────────────────────────────────────────────────

    def _render_headline(self, headline: str, subtitle: str = None) -> str:
        """Gold headline at top of data frames."""
        svg = '  <g id="HEADLINE">\n'
        svg += (
            f'    <text x="540" y="240" text-anchor="middle" font-family="{FONT}" '
            f'font-size="52" fill="#ffd700" letter-spacing="3">{_esc(headline)}</text>\n'
        )
        if subtitle:
            svg += (
                f'    <text x="540" y="290" text-anchor="middle" font-family="{FONT}" '
                f'font-weight="600" font-size="22" fill="#b0b0b8">{_esc(subtitle)}</text>\n'
            )
        svg += "  </g>\n"
        return svg

    def _render_text_overlays(self, elements: list) -> str:
        """Stack of text lines in TOP of frame, ABOVE Aparna's head.

        From 34 reference screenshots:
        - Text starts at y=150-200 (top 8-10% of frame)
        - Left-aligned at x=50
        - Font sizes: 72-160px for headlines, very bold (800-900)
        - Aparna's head starts at y~350, so text must end by y~330
        - Each line gets ~100px vertical space (for 72px text)
        """
        svg = '  <g id="PRESENTER-TEXT">\n'
        n = len(elements)
        if n == 0:
            svg += "  </g>\n"
            return svg

        # Start at y=180, each line ~100px apart
        # For single large numbers, center them
        start_y = 200
        line_height = 100

        for i, elem in enumerate(elements):
            text = elem.get("text", "")
            color = _color(elem.get("color", "gold"))
            font_size = elem.get("font_size", 72)
            weight = elem.get("weight", "800")
            y = start_y + i * line_height

            # For very large single numbers (>100px), center horizontally
            x = "540" if (n == 1 and font_size >= 100) else "60"
            anchor = "middle" if (n == 1 and font_size >= 100) else "start"

            weight_attr = f' font-weight="{weight}"' if weight != "400" else ""
            svg += (
                f'    <text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}"'
                f'{weight_attr} font-size="{font_size}" fill="{color}">{_esc(text)}</text>\n'
            )

        svg += "  </g>\n"
        return svg

    def _render_ranking_cards(self, element: dict) -> str:
        """Stacked ranking rows with optional badge pills (above Aparna, y=130-330)."""
        items = element.get("items", [])
        svg = '  <g id="RANKING">\n'

        n = len(items)
        card_w = 960
        card_h = 90
        card_x = 60
        gap = min(110, (300 - 130) // max(n, 1))
        start_y = max(130, 340 - n * gap)

        for i, item in enumerate(items):
            y = start_y + i * gap
            rank = item.get("rank", f"#{i+1}")
            label = item.get("label", "")
            sublabel = item.get("sublabel", "")
            color = _color(item.get("color", "muted"))
            highlight = item.get("highlight", False)
            badge = item.get("badge")

            stroke_w = 3 if highlight else 2
            opacity_attr = "" if highlight else ' opacity="0.5"'
            label_fill = "#ffffff" if highlight else color
            label_weight = "700" if highlight else "600"
            sublabel_fill = "#b0b0b8" if highlight else color

            # Card background
            svg += (
                f'    <rect x="{card_x}" y="{y}" width="{card_w}" height="{card_h}" rx="16" '
                f'fill="#0e0e19" fill-opacity="0.95" stroke="{color}" stroke-width="{stroke_w}"'
                f'{opacity_attr}/>\n'
            )

            # Rank number
            rank_y = y + 52
            svg += (
                f'    <text x="{card_x + 50}" y="{rank_y}" font-family="{FONT}" '
                f'font-size="48" fill="{color}">{_esc(rank)}</text>\n'
            )

            # Label
            svg += (
                f'    <text x="{card_x + 140}" y="{rank_y}" font-family="{FONT}" '
                f'font-weight="{label_weight}" font-size="32" fill="{label_fill}">'
                f'{_esc(label)}</text>\n'
            )

            # Sublabel
            sublabel_y = y + 98
            svg += (
                f'    <text x="{card_x + 140}" y="{sublabel_y}" font-family="{FONT}" '
                f'font-weight="400" font-size="20" fill="{sublabel_fill}">'
                f'{_esc(sublabel)}</text>\n'
            )

            # Badge pill
            if badge:
                badge_x = 780
                badge_y = y + 62
                pill_y = badge_y - 25
                svg += (
                    f'    <rect x="{badge_x}" y="{pill_y}" width="160" height="50" rx="25" '
                    f'fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-width="1.5"/>\n'
                )
                svg += (
                    f'    <text x="{badge_x + 80}" y="{badge_y + 8}" text-anchor="middle" '
                    f'font-family="{FONT}" font-weight="700" font-size="22" fill="{color}">'
                    f'{_esc(badge)}</text>\n'
                )

        svg += "  </g>\n"
        return svg

    def _render_callout_cards(self, element: dict) -> str:
        """Numbered callout cards stacked vertically (above Aparna, y=150-330)."""
        items = element.get("items", [])
        svg = '  <g id="CALLOUT-CARDS">\n'

        # Cards must be above Aparna's head at y~350
        n = len(items)
        card_h = 90
        gap = min(110, (300 - 130) // max(n, 1))
        start_y = max(130, 340 - n * gap)
        card_x = 60
        card_w = 960

        for i, item in enumerate(items):
            y = start_y + i * gap
            number = item.get("number", i + 1)
            text = item.get("text", "")
            color = _color(item.get("color", "red"))

            # Card rect
            svg += (
                f'    <rect x="{card_x}" y="{y}" width="{card_w}" height="{card_h}" rx="16" '
                f'fill="#0e0e19" fill-opacity="0.95" stroke="{color}" stroke-width="2"/>\n'
            )

            # Numbered circle
            circle_cx = card_x + 70
            circle_cy = y + card_h // 2
            svg += (
                f'    <circle cx="{circle_cx}" cy="{circle_cy}" r="24" '
                f'fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-width="1.5"/>\n'
            )
            svg += (
                f'    <text x="{circle_cx}" y="{circle_cy + 8}" text-anchor="middle" '
                f'font-family="{FONT}" font-weight="700" font-size="20" fill="{color}">'
                f'{number}</text>\n'
            )

            # Text
            text_x = circle_cx + 60
            text_y = circle_cy + 8
            svg += (
                f'    <text x="{text_x}" y="{text_y}" font-family="{FONT}" '
                f'font-weight="600" font-size="30" fill="#ffffff">{_esc(text)}</text>\n'
            )

        svg += "  </g>\n"
        return svg

    def _render_stat_badges(self, element: dict, start_y: int = 1140) -> str:
        """2-column grid of stat badges."""
        items = element.get("items", [])
        svg = '  <g id="HIGHLIGHT-STATS">\n'

        col_left_x = 60
        col_right_x = 560
        badge_w = 460
        badge_h = 120
        row_gap = 160

        for i, item in enumerate(items):
            row = i // 2
            col = i % 2
            x = col_left_x if col == 0 else col_right_x
            y = start_y + row * row_gap

            label = item.get("label", "")
            value = item.get("value", "")
            color = _color(item.get("color", "cyan"))
            center_x = x + badge_w // 2

            # Badge rect
            svg += (
                f'    <rect x="{x}" y="{y}" width="{badge_w}" height="{badge_h}" rx="14" '
                f'fill="#0e0e19" fill-opacity="0.95" stroke="{color}" stroke-width="2"/>\n'
            )

            # Label
            svg += (
                f'    <text x="{center_x}" y="{y + 50}" text-anchor="middle" font-family="{FONT}" '
                f'font-weight="600" font-size="18" fill="#b0b0b8" letter-spacing="2">'
                f'{_esc(label)}</text>\n'
            )

            # Value — scale font size if text is long
            value_size = 38 if len(value) < 20 else 30
            svg += (
                f'    <text x="{center_x}" y="{y + 95}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="{value_size}" fill="{color}">{_esc(value)}</text>\n'
            )

        svg += "  </g>\n"
        return svg

    def _render_section_badge(self, element: dict) -> str:
        """Centered pill badge for section headers."""
        text = element.get("text", "")
        color = _color(element.get("color", "gold"))

        # Approximate width from text length (roughly 18px per char at size 30-32)
        char_width = 18
        text_width = len(text) * char_width
        pill_w = text_width + 80
        pill_h = 60
        pill_x = 540 - pill_w // 2
        pill_y = 200
        rx = 30

        # Use larger y for section_header frame types (badge is lower)
        # The caller can override if needed
        text_y = pill_y + 40

        svg = '  <g id="SECTION-BADGE">\n'
        svg += (
            f'    <rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="{pill_h}" rx="{rx}" '
            f'fill="none" stroke="{color}" stroke-width="2"/>\n'
        )
        svg += (
            f'    <text x="540" y="{text_y}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="32" fill="{color}" letter-spacing="3">{_esc(text)}</text>\n'
        )
        svg += "  </g>\n"
        return svg

    def _render_cta_cards(self, element: dict) -> str:
        """Stacked CTA action cards."""
        items = element.get("items", [])
        svg = '  <g id="CTA-CARDS">\n'

        start_y = 720
        gap = 150
        card_x = 180
        card_w = 720
        card_h = 110
        rx = 20

        for i, item in enumerate(items):
            y = start_y + i * gap
            text = item.get("text", "")
            color = _color(item.get("color", "gold"))

            svg += (
                f'    <rect x="{card_x}" y="{y}" width="{card_w}" height="{card_h}" rx="{rx}" '
                f'fill="#0e0e19" fill-opacity="0.95" stroke="{color}" stroke-width="2"/>\n'
            )
            svg += (
                f'    <text x="540" y="{y + 68}" text-anchor="middle" font-family="{FONT}" '
                f'font-weight="600" font-size="30" fill="{color}">{_esc(text)}</text>\n'
            )

        svg += "  </g>\n"
        return svg

    def _render_bottom_text(self, element: dict) -> str:
        """Single line of emphasized text near the bottom of the content area."""
        text = element.get("text", "")
        color = _color(element.get("color", "gold"))

        return (
            '  <g id="BOTTOM-TEXT">\n'
            f'    <text x="540" y="1120" text-anchor="middle" font-family="{FONT}" '
            f'font-weight="700" font-size="30" fill="{color}">{_esc(text)}</text>\n'
            "  </g>\n"
        )

    def _render_screenshot(self, index: int, screenshot_dir: str, y: int = 340, height: int = 760) -> str:
        """Screenshot image in a bordered container."""
        # Build path to screenshot file
        # Screenshots are named page{page}_img{img}.png in the screenshots/ subfolder
        # index is 0-based sequential; we map to file naming convention
        # Try common naming patterns
        if screenshot_dir:
            # Look for screenshot files matching index
            png_path = self._find_screenshot_path(index, screenshot_dir)
        else:
            png_path = f"screenshots/screenshot_{index + 1}.png"

        svg = '  <g id="SCREENSHOT">\n'
        svg += (
            f'    <rect x="40" y="{y}" width="1000" height="{height}" rx="12" '
            f'fill="#0e0e19" fill-opacity="0.95" stroke="#00e5ff" stroke-width="2.5"/>\n'
        )
        svg += (
            f'    <image href="{_esc(png_path)}" x="55" y="{y + 15}" '
            f'width="970" height="{height - 30}" preserveAspectRatio="xMidYMid meet"/>\n'
        )
        svg += "  </g>\n"
        return svg

    def _find_screenshot_path(self, index: int, screenshot_dir: str) -> str:
        """Find the screenshot file for a given index.

        Searches the screenshot_dir for files matching common patterns
        and returns a path relative to the SVG file's location.
        """
        # The screenshots subfolder relative path for SVG hrefs
        rel_prefix = "screenshots/"

        # Try to list actual files
        full_dir = screenshot_dir
        if os.path.isdir(full_dir):
            files = sorted([
                f for f in os.listdir(full_dir)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ])
            if index < len(files):
                return rel_prefix + files[index]

        # Fallback to generic naming
        return f"{rel_prefix}screenshot_{index + 1}.png"


# ── Storyboard HTML Generator ─────────────────────────────────────────────────

def generate_storyboard_html(storyboard_json: dict, project_dir: str) -> str:
    """Generate the complete storyboard.html from storyboard JSON.

    Args:
        storyboard_json: Full storyboard dict with keys: title, format, language,
                         style, sections (list of {name, frames}).
        project_dir: Absolute path to the project directory where frame SVGs live.

    Returns:
        Complete HTML string for the storyboard overview page.
    """
    title = _esc(storyboard_json.get("title", "Storyboard"))
    fmt = _esc(storyboard_json.get("format", "Short (9:16)"))
    language = _esc(storyboard_json.get("language", "Hinglish"))
    style = _esc(storyboard_json.get("style", "Presenter + Data Overlays"))
    sections = storyboard_json.get("sections", [])

    # Count total frames
    total_frames = sum(len(s.get("frames", [])) for s in sections)

    html_parts = []
    html_parts.append(_storyboard_html_head(title))
    html_parts.append(_storyboard_html_header(title, fmt, language, style, total_frames))
    html_parts.append('<div class="gallery">\n')

    for section in sections:
        section_name = _esc(section.get("name", ""))
        html_parts.append(f'\n<div class="section-divider"><span>{section_name}</span></div>\n')

        for frame in section.get("frames", []):
            html_parts.append(_storyboard_frame_row(frame))

    html_parts.append("\n</div>\n</body>\n</html>\n")
    return "".join(html_parts)


def _storyboard_html_head(title: str) -> str:
    """HTML head with embedded CSS."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#060609;color:#f0f0f5;font-family:'Poppins',sans-serif;padding:40px 0}}

.page-header{{text-align:center;padding:40px;border-bottom:1px solid rgba(255,255,255,.05);margin-bottom:40px}}
.page-header h1{{font-family:'Poppins',sans-serif;font-size:42px;letter-spacing:4px;color:#ffd700;text-shadow:0 0 20px rgba(255,215,0,.4)}}
.page-header p{{font-size:13px;color:#6a6a7a;margin-top:6px}}
.page-header .meta{{display:flex;gap:24px;justify-content:center;margin-top:16px;flex-wrap:wrap}}
.page-header .tag{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);padding:4px 14px;border-radius:20px;font-size:11px;color:#b0b0b8;letter-spacing:1px}}

.gallery{{max-width:1400px;margin:0 auto;padding:0 32px;display:flex;flex-direction:column;gap:48px}}

.frame-row{{display:flex;gap:36px;align-items:flex-start}}
.frame-info{{flex:1;padding-top:16px}}
.frame-num{{font-family:'Poppins',sans-serif;font-size:20px;color:#6a6a7a;letter-spacing:2px;margin-bottom:4px}}
.frame-type{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:2px;padding:3px 10px;border-radius:4px;display:inline-block;margin-bottom:16px}}
.frame-type.presenter{{background:rgba(0,229,255,.1);color:#00e5ff;border:1px solid rgba(0,229,255,.2)}}
.frame-type.presenter_cards{{background:rgba(0,229,255,.1);color:#00e5ff;border:1px solid rgba(0,229,255,.2)}}
.frame-type.data{{background:rgba(255,215,0,.1);color:#ffd700;border:1px solid rgba(255,215,0,.2)}}
.frame-type.chart{{background:rgba(0,229,160,.1);color:#00e5a0;border:1px solid rgba(0,229,160,.2)}}
.frame-type.section_header{{background:rgba(179,136,255,.1);color:#b388ff;border:1px solid rgba(179,136,255,.2)}}
.frame-type.cta{{background:rgba(179,136,255,.1);color:#b388ff;border:1px solid rgba(179,136,255,.2)}}

.info-section{{margin-bottom:16px}}
.info-label{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;display:flex;align-items:center;gap:6px}}
.info-label.dialogue{{color:#00e5ff}}
.info-label.dialogue::before{{content:'\\1F399';font-size:12px}}
.info-label.visual{{color:#ffd700}}
.info-label.visual::before{{content:'\\1F3AC';font-size:12px}}
.info-label.screenshot{{color:#00e5a0}}
.info-label.screenshot::before{{content:'\\1F4F7';font-size:12px}}
.info-content{{font-size:14px;color:#b0b0b8;line-height:1.7;padding-left:22px;border-left:2px solid rgba(255,255,255,.06)}}
.info-content em{{color:#6a6a7a;font-style:italic}}

.svg-frame{{width:360px;height:640px;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.06);background:#0a0a0f;flex-shrink:0}}
.svg-frame object{{width:100%;height:100%;border:0}}

.section-divider{{text-align:center;padding:20px 0;margin:8px 0}}
.section-divider span{{font-family:'Poppins',sans-serif;font-size:14px;letter-spacing:4px;color:#ffd700;background:#060609;padding:0 20px;position:relative}}
.section-divider::before{{content:'';display:block;height:1px;background:linear-gradient(90deg,transparent,rgba(255,215,0,.2),transparent);position:relative;top:10px}}
</style>
</head>
<body>
"""


def _storyboard_html_header(title: str, fmt: str, language: str, style: str, total_frames: int) -> str:
    return f"""
<div class="page-header">
    <h1>{title}</h1>
    <p>AV Storyboard — Short-form Vertical Video</p>
    <div class="meta">
        <span class="tag">Format: {fmt}</span>
        <span class="tag">Language: {language}</span>
        <span class="tag">Style: {style}</span>
        <span class="tag">Frames: {total_frames}</span>
    </div>
</div>
"""


def _storyboard_frame_row(frame: dict) -> str:
    """Generate a single frame row for the storyboard HTML."""
    frame_num = frame.get("frame_number", 0)
    frame_type = frame.get("frame_type", "presenter")
    dialogue = frame.get("dialogue", "")
    visual_cue = frame.get("visual_cue", "")
    screenshot_index = frame.get("screenshot_index")

    num_str = f"{frame_num:02d}"
    svg_file = f"frame-{num_str}.svg"

    # Frame type display and CSS class
    type_display = _esc(frame_type.replace("_", " ").title())
    type_class = _esc(frame_type)

    parts = []
    parts.append(f'\n<!-- Frame {frame_num} -->\n')
    parts.append('<div class="frame-row">\n')
    parts.append(f'    <div class="svg-frame"><object data="{svg_file}" type="image/svg+xml"></object></div>\n')
    parts.append('    <div class="frame-info">\n')
    parts.append(f'        <div class="frame-num">FRAME {num_str}</div>\n')
    parts.append(f'        <span class="frame-type {type_class}">{type_display}</span>\n')

    # Dialogue section
    if dialogue:
        dialogue_html = _esc(dialogue).replace("\n", "<br>")
        parts.append('        <div class="info-section">\n')
        parts.append('            <div class="info-label dialogue">Dialogue</div>\n')
        parts.append(f'            <div class="info-content">{dialogue_html}</div>\n')
        parts.append('        </div>\n')

    # Visual cue section
    if visual_cue:
        visual_html = _esc(visual_cue).replace("\n", "<br>")
        parts.append('        <div class="info-section">\n')
        parts.append('            <div class="info-label visual">Visual Cue</div>\n')
        parts.append(f'            <div class="info-content">{visual_html}</div>\n')
        parts.append('        </div>\n')

    # Screenshot reference
    if screenshot_index is not None:
        parts.append('        <div class="info-section">\n')
        parts.append('            <div class="info-label screenshot">Screenshot</div>\n')
        parts.append(f'            <div class="info-content">Screenshot #{screenshot_index + 1}</div>\n')
        parts.append('        </div>\n')

    parts.append('    </div>\n')
    parts.append('</div>\n')

    return "".join(parts)
