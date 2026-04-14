# Angel One Investors Shorts — SVG Storyboard Rulebook

> **Channel:** Angel One Investors  
> **Format:** 9:16 vertical short (1080x1920 px)  
> **Presenter:** Aparna  
> **Usage:** Injected into LLM system prompt + referenced by SVG generator

---

## 1. Canvas

- **Dimensions:** 1080x1920 px (9:16 vertical)
- **Background:** `#0A0A0F` solid fill
- **Warm brown radial gradients:**
  - Bottom-left: `#B4641E` at 20% opacity
  - Top-right: `#B4641E` at 10% opacity
- **Dot grid pattern:**
  - Top-left corner: 300x400 area
  - Bottom-right corner: 300x400 area
  - Dots: 1.5px circles, color `#B4641E` at 12% opacity, 20px spacing
- **AngelOne logo:** top-right, `x=980 y=80`, "Angel" bold + "One" regular, white, Poppins 28px
- **Disclaimer:** bottom, `x=540 y=1880`, centered, "This video is for educational/informational purposes only", Poppins 14px, `#6A6A7A` at 50% opacity

---

## 2. Typography

- **Font:** Poppins ONLY (no Bebas Neue, no Inter, no exceptions)
- **Headlines / big numbers:** 48-140px, bold/extrabold
- **Labels:** 18-22px, bold, uppercase, letter-spacing 2-3px
- **Body text:** 26-34px, medium weight
- **Source text:** 16px, `#6A6A7A`

---

## 3. Color Palette

| Token   | Hex        | Usage                                  |
|---------|------------|----------------------------------------|
| Cyan    | `#00E5FF`  | Primary accent, data borders           |
| Gold    | `#FFD700`  | Headlines, emphasis, gold stats        |
| Purple  | `#B388FF`  | Tertiary accent                        |
| Mint    | `#00E5A0`  | Positive indicators, growth            |
| Red     | `#FF4466`  | Negative indicators, warnings, risks   |
| White   | `#FFFFFF`  | Primary text                           |
| Muted   | `#6A6A7A`  | Secondary text, sources                |
| Body    | `#B0B0B8`  | Body text, descriptions                |
| Card BG | `#0E0E19`  | Card fill at 95% opacity              |

---

## 4. Frame Types

There are exactly **5 frame types**. Every frame must be one of these.

### 4.1 `presenter` — Aparna only + optional text overlay

- Presenter image at bottom: `x=115 y=1000 w=850 h=880`
- Text overlays centered in `y=700-900` range
- Use cases: bare presenter, big stat number, transition phrase, key quote

### 4.2 `presenter_cards` — Aparna + cards/rankings

- Cards occupy the `y=300-1000` zone (above presenter)
- **Ranking cards:** 880px wide, 130px tall, stacked with 170px gap, starting `y=520`
- **Callout cards:** 800px wide, 120px tall, with numbered circles, stacked with 160px gap
- **Stat cards:** side-by-side (460px each) or single centered

### 4.3 `data` — No presenter, screenshot + data overlays

- Gold headline at `y=240`, Poppins 48-64px
- Optional subtitle at `y=290`
- Screenshot in cyan-bordered rect (`#00E5FF`, 2.5px stroke, `rx=12`): `x=40 y=340 w=1000`
- Screenshot height varies: 600-960px depending on content
- Stat badges below screenshot: 2-column grid, each 460x120px, starting after screenshot
- Source text at bottom of data area

### 4.4 `section_header` — Presenter + section badge pill

- Rounded rect pill (`rx=28-30`): centered, ~460-520px wide, 56-60px tall
- Badge text: Poppins 30-32px, uppercase, letter-spacing 3px
- Badge colors: gold border for narrative sections, cyan border for data sections

### 4.5 `cta` — Presenter + CTA cards

- 3 cards stacked: 720px wide, 110px tall, `rx=20`, gap=150px, starting `y=720`
- Card 1: "Comment your view" — gold border (`#FFD700`)
- Card 2: "Like if this helped" — cyan border (`#00E5FF`)
- Card 3: "Subscribe for more" — mint border (`#00E5A0`)

---

## 5. CRITICAL RULE: Dialogue vs Visual

This is the single most important rule. Getting this wrong breaks the storyboard.

- **Dialogue** = what the presenter SAYS. This goes ONLY in the HTML info panel (right side), NEVER in the SVG frame.
- **Visual overlays** = text that appears ON SCREEN as a graphic element. These go in the SVG.

### Examples of visual overlays (DO put in SVG):
- `"18/20"` (big stat number)
- `"But today..."` (transition phrase)
- `"Phase or Shift?"` (closing hook)
- `"FII Selling: >$10 Billion"` (data headline)
- `"Not strength. Relative Resilience."` (key insight)

### Examples of dialogue (DO NOT put in SVG):
- `"For years, SBI was known for..."`
- `"Look at the last 1 year."`
- `"And this is interesting."`
- `"Let me know what you think."`

---

## 6. Screenshot Placement Rules

- Only in `data` frames (never in presenter frames)
- Always wrapped in a `<rect>` with cyan border (`#00E5FF`, 2.5px stroke, `rx=12`)
- `<image>` inside with 15px padding from border
- `preserveAspectRatio="xMidYMid meet"`
- Multiple screenshots can stack vertically (e.g., two stock cards)

---

## 7. Card Styling

- **All cards:** fill `#0E0E19` at 95% opacity
- **Border:** 2-2.5px stroke in neon color
- **Border radius:** 14-20px
- **Labels inside:** Poppins, uppercase, letter-spacing 2px
- **Values inside:** Poppins bold, neon color

---

## 8. Ranking Card Specifics

- **Rank number** (#1, #2, #3): Poppins 48px
- **Company name:** Poppins 32px, font-weight 600-700
- **Sublabel:** Poppins 20px, body color
- **Badge pills** (up/down arrows): 160x50px, `rx=25`, colored border + 15% fill opacity
- **Highlighted row:** thicker border (3px), brighter colors
- **Dimmed rows:** 50% opacity, gray border

---

## 9. Stat Badge Specifics (data frames, below screenshots)

- **2-column grid:** left badge `x=60`, right badge `x=560`, both 460px wide
- **Height:** 120-140px, `rx=14-16`
- **Label:** Poppins 18-20px, body color, uppercase, letter-spacing 2px
- **Value:** Poppins 38-48px, bold, neon color

---

## 10. SVG Layer Naming Convention

Every SVG must use these group IDs:

| Group ID            | Content                                          | Used in              |
|---------------------|--------------------------------------------------|----------------------|
| `BG`                | Background (solid + gradients + dots)            | All frames           |
| `LOGO`              | AngelOne branding                                | All frames           |
| `SECTION-BADGE`     | Section header pill                              | section_header       |
| `HEADLINE`          | Gold headline text                               | data                 |
| `SCREENSHOTS`       | Screenshot images with borders                   | data                 |
| `RANKING`           | Ranking card rows                                | presenter_cards      |
| `CALLOUT-CARDS`     | Callout cards                                    | presenter_cards      |
| `STAT-CARDS`        | Stat cards                                       | presenter_cards      |
| `HIGHLIGHT-STATS`   | Stat badges below screenshots                    | data                 |
| `COMPARISON-STATS`  | Comparison stat badges                           | data                 |
| `PERF-BADGES`       | Performance badges                               | data                 |
| `CTA-CARDS`         | CTA cards                                        | cta                  |
| `PRESENTER-TEXT`    | Visual text overlays                             | presenter            |
| `BOTTOM-TEXT`       | Bottom annotation text                           | Various              |
| `PRESENTER-IMAGE`   | aparna.png image                                 | presenter, presenter_cards, section_header, cta |
| `SOURCE`            | Source attribution                               | data                 |
| `DISCLAIMER`        | Educational disclaimer                           | All frames           |

---

## 11. Do's

- Use at most 3-4 visual elements per presenter frame
- Keep big numbers BIG (80-140px)
- Use neon colors sparingly — max 3 distinct per frame
- Always include source citation on data frames
- Use `₹` for Indian currency
- Cycle colors for multi-item lists: cyan, gold, purple, mint, red

---

## 12. Don'ts

- Don't put dialogue text in the SVG
- Don't place elements below `y=1000` on presenter frames (Aparna covers that area)
- Don't use SVG filters (no blur, no glow — the editor adds those)
- Don't use gradients on text
- Don't use more than 1 font (Poppins only)
- Don't use `stroke-width` less than 1.5px
- Don't place text above `y=120` (logo area) or below `y=1860` (disclaimer area)
