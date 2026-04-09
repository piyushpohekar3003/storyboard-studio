# Angel One for Investors — Visual Style Guide

> **Channel:** Angel One for Investors (16.7K subs)
> **Content:** Educational deep-dives on Indian stock market, mutual funds, stock picks
> **Language:** English
> **Anchor:** Aparna (white shirt or black top, lapel mic, warm-lit studio)

---

## 1. Canvas

| Property | Value |
|---|---|
| Frame size | 1920 × 1080 px |
| Background | `#0A0A0F` (near-black) |
| Background texture | Hexagonal grid pattern, stroke `rgba(180,100,30,0.05)` |
| Corner warmth | Radial gradients of `#B4641E` at bottom-left, bottom-right, top-right corners (opacity 8–18%) |
| Overall feel | Dark, premium, cinematic — like a Bloomberg terminal meets neon signage |

---

## 2. Color Palette

### Primary Neon Colors (used for data, borders, highlights)

| Name | Hex | Usage |
|---|---|---|
| Cyan | `#00E5FF` | Primary accent — stock names, card borders, positive metrics, category 1 |
| Gold | `#FFD700` | Secondary accent — titles, promoter data, numbers, category 2 |
| Purple | `#B388FF` | Tertiary — big headings ("Promoter Buying"), category 3 |
| Mint | `#00E5A0` | Positive signals — returns, growth, "buy" indicators |
| Red | `#FF4466` | Negative/warning — risks, negative returns, caution cards |

### Neutral Colors

| Name | Hex | Usage |
|---|---|---|
| White | `#F0F0F5` | Body text, labels, card labels |
| Muted | `#6A6A7A` | Subtitles, source attributions, secondary info |
| Body text | `#B0B0B8` | Callout descriptions, supporting text |
| Card fill | `#0E0E19` at 95% opacity | Background of all cards and callouts |

### Color Assignment Rules

- **Stock #1, #4, #7, #10** → Gold title
- **Stock #2, #5, #8** → Cyan title
- **Stock #3, #6, #9** → Purple title
- **Positive metrics** (revenue growth, returns) → Mint or Cyan
- **Negative metrics** (losses, risks) → Red
- **Promoter stake changes** → Gold (always)
- Cycle through `cyan → gold → purple → mint → red` for multi-item lists

---

## 3. Typography

| Element | Font | Size | Weight | Tracking | Color |
|---|---|---|---|---|---|
| Big title (intro splash) | Bebas Neue | 96–130px | Regular | 4–6px | Purple or Gold with glow |
| Section header ("STOCK #1") | Bebas Neue | 80–88px | Regular | 4px | Neon color with glow |
| Card value (big number) | Bebas Neue | 52–92px | Regular | 0 | Neon color with glow |
| Card label ("REVENUE") | Inter | 16–20px | 700 (Bold) | 2–3px | White at 85% opacity |
| Card sub-label | Inter | 14–16px | 600 | 1.5px | White at 55% opacity |
| Callout title | Inter | 17–22px | 800 (ExtraBold) | 1.5–2px | Neon color (matches border) |
| Callout body | Inter | 15–18px | 400 | 0 | `#B0B0B8` |
| Source citation | Inter | 11px | 400 | 1px | Muted at 50% opacity |
| Quote text | Inter | 26–34px | 700 | 0 | Gold, italic |

### Text Rules

- All labels and headers are **UPPERCASE**
- Big numbers always use **Bebas Neue** (never Inter for data values)
- Body/description text uses **sentence case**
- Indian number formatting: ₹1,566 / 1.34 Lakh Cr. / ₹4,235 Cr
- Percentage always with `%` immediately after number, no space

---

## 4. Card Components

### Stat Card (floating metric)

```
┌─────────────────────┐
│     LABEL (caps)    │  ← Inter 16-20px, White 85%
│                     │
│     BIG VALUE       │  ← Bebas Neue 52-92px, neon color
│                     │
│    Sub-label        │  ← Inter 14-16px, White 55%
└─────────────────────┘
        ◆               ← accent dot (8-12px, neon color)
```

- Background: `#0E0E19` at 95% opacity
- Border: 2–2.5px, neon color at 35–50% opacity
- Border radius: 14–20px
- Padding: 32–40px horizontal, 28–36px vertical
- Min width: 220–340px depending on content

### Callout Card (info label)

```
                    ◆    ← accent dot (top-right, 8-12px)
┌─────────────────────┐
│  TITLE (caps)       │  ← Inter 17-22px, neon color
│  Description text   │  ← Inter 15-18px, body color
└─────────────────────┘
```

- Same card fill and border as stat card
- Border radius: 11–16px
- Max width: 280–440px

### Comparison Card (VS layout)

```
┌────────┐         ┌────────┐
│ PERIOD │   VS    │ PERIOD │
│ VALUE  │ ──── ── │ VALUE  │
│ LABEL  │         │ LABEL  │
└────────┘         └────────┘
```

- Two stat cards side by side
- VS divider: two vertical lines with "VS" text in Bebas Neue, muted color
- Optional result badge below

---

## 5. Layout Patterns

### Pattern A: Anchor + Floating Cards

```
┌──────────────────────────────────────┐
│         STOCK #1 (top center)        │
│                                      │
│  ┌─────────┐           ┌──────────┐ │
│  │ Callout │           │ Stat     │ │
│  │ (left)  │  ANCHOR   │ Card     │ │
│  └─────────┘  (center) │ (right)  │ │
│                         └──────────┘ │
│  ┌─────────┐           ┌──────────┐ │
│  │ Stat    │           │ Callout  │ │
│  │ Card    │           │ (right)  │ │
│  └─────────┘           └──────────┘ │
└──────────────────────────────────────┘
```

- Anchor image: centered, bottom-aligned, 85–88% frame height
- Cards positioned at: `top:200-320, left:80` and `top:280-520, right:80`
- Title at `top:50-80`, centered
- Safe margin: 80px from all edges

### Pattern B: Full-Screen Data (no anchor)

```
┌──────────────────────────────────────┐
│           TITLE (centered)           │
│                                      │
│    ┌──────┐  ┌──────┐  ┌──────┐    │
│    │ Card │  │ Card │  │ Card │    │
│    └──────┘  └──────┘  └──────┘    │
│                                      │
│         or TABLE / CHART             │
│                                      │
│          Source: xxxxxxxx            │
└──────────────────────────────────────┘
```

- Used for: intro splashes, data tables, summary screens, comparison layouts
- Padding: 64–80px from edges
- Content centered both axes

### Pattern C: Anchor + Quote

```
┌──────────────────────────────────────┐
│            "                         │
│     Quote text goes here             │
│     in gold italic                   │
│                                      │
│              ANCHOR                  │
│             (center)                 │
│                                      │
│  ┌─────────┐           ┌──────────┐ │
│  │ Takeaway│           │ Takeaway │ │
│  └─────────┘           └──────────┘ │
└──────────────────────────────────────┘
```

---

## 6. Glow & Effects (editor applies in Figma/Illustrator)

> **Note:** SVG deliverables are clean vectors without effects.
> The editor applies these in post:

| Element | Effect | Settings |
|---|---|---|
| Card border | Drop Shadow (0 offset) | Color = border color, blur 20–30px, opacity 40–50% |
| Big value text | Drop Shadow (0 offset) | Color = text color, blur 25–35px, opacity 50–60% |
| Accent dot | Drop Shadow (0 offset) | Color = dot color, blur 12–16px, opacity 60–70% |
| Callout title | Drop Shadow (0 offset) | Color = title color, blur 10–15px, opacity 30–40% |
| Quote text | Drop Shadow (0 offset) | Color = gold, blur 20–30px, opacity 25–35% |

### Glow Rule

- Every neon-colored element gets a same-color glow
- White text does NOT glow
- Muted text does NOT glow
- The glow should feel like the element is emitting light, not just blurred

---

## 7. Decorative Elements

| Element | Description |
|---|---|
| Accent dot (◆) | 8–12px square, rounded corners (2–3px radius), placed at card bottom-center or top-right |
| Connecting lines | Dashed or solid, 2px, `rgba(255,255,255,0.15)`, used in flow charts |
| Corner brackets | Cyan squares (8px) at corners of the frame, connected by thin lines — used in full-screen data frames |
| Hexagonal grid | Background pattern, never foreground — very subtle |

---

## 8. Do's and Don'ts

### Do
- Use at most **4 cards per frame** with anchor, **6 without**
- Keep big numbers BIG — they should be the first thing the eye sees
- Use neon colors sparingly — max 3 distinct colors per frame
- Always include source citation on data-heavy frames
- Use ₹ symbol for Indian currency, never "Rs." or "INR"

### Don't
- Don't put cards over the anchor's face or hands
- Don't use gradients on text (only solid fills with glow effects)
- Don't mix more than 2 fonts (Bebas Neue + Inter only)
- Don't use thin strokes (minimum 2px for borders)
- Don't place text below y:1000 (bottom 80px is dead zone)
- Don't use colored backgrounds on cards (always `#0E0E19`)

---

## 9. SVG Layer Naming Convention

When generating SVGs, use these layer/group IDs:

```
BG                    → Background (solid + gradients + hex grid)
TITLE                 → Frame title text
CARD-{NAME}           → Card shape (fill + border)
CARD-{NAME}-TEXT      → Text inside the card (label, value, sub)
CARD-{NAME}-DOT       → Accent dot
CALLOUT-{NAME}        → Callout shape
CALLOUT-{NAME}-TEXT   → Callout text
VS-DIVIDER            → VS layout divider
INSIGHT               → Bottom insight/takeaway text
SOURCE                → Source attribution
ANCHOR                → Presenter image (if applicable)
```

Each text element should have a unique `id` matching its content purpose:
`title-text`, `card-gold-label`, `card-gold-value`, `card-gold-sub`, etc.

---

## 10. File Delivery

| Asset | Format | Notes |
|---|---|---|
| Frame SVG | `.svg` | Clean vectors, named layers, editable text, no effects |
| Anchor cutout | `.png` | Transparent background, placed via `<image>` tag |
| Style guide | This document | Referenced by SVG generator and editors |
| Glow reference | HTML preview | Shows intended final look with CSS glow effects |
