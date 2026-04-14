# Angel One Investors Shorts -- Visual Specification

> Derived from 34 reference screenshots. All coordinates are in a **1080 x 1920** portrait frame.
> "y" is measured from the top edge; "x" from the left edge.

---

## 0. Global Constants

| Element | Value |
|---|---|
| Frame size | 1080 x 1920 px |
| Background (presenter frames) | Warm amber/brown studio backdrop -- NOT generated; comes from video feed |
| Background (data/info frames) | Dark brown/black (#0D0A06) with radial gold particle vignette in corners |
| Angel One logo | Top-right corner, x ~820, y ~40, white text with mountain icon, approx 200 x 50 px |
| Play / Sound icons | Top-left, two circles ~48 px diameter, x ~40 and x ~100, y ~40 |
| Disclaimer bar | Bottom edge, full width, y ~1870-1920, small white text on semi-transparent dark bar: "This video is for educational/informational purposes only" ~18px |
| Source attribution | Bottom-left, small text ~16px, e.g. "Source: Screener.in" -- only on screener/data frames |

---

## 1. Aparna Proportions

Aparna appears in roughly **60-65% of all frames**. She has two distinct placement modes:

### 1A. Standard Presenter (most common)

- **Head top**: y ~320-420 (roughly 17-22% from top)
- **Head center**: y ~420-500
- **Shoulders start**: y ~550-620
- **Visible body extends to**: y ~1750-1800 (cut off just above disclaimer)
- **Horizontal position**: Centered or very slightly left of center (x ~480-560 head center)
- **Frame fill**: She occupies roughly 70-75% of the frame height
- **Width**: Shoulders span ~500-600 px (roughly 46-56% of frame width)
- **Text zone above head**: y 80 to y 300 (approx 220 px of usable space above her head)

### 1B. Compact Presenter (with large data overlay below)

- Used in Ola Electric screener frame (2.22.06)
- Aparna is inside a **yellow-bordered inset box** in the upper portion
- Inset box: approx x 45, y 90 to y 470 (380 px tall), width ~990 px
- Border: 3px solid gold/yellow (#D4A843)
- Border radius: 16px
- Her head is at y ~200 inside this box
- Data card appears below the inset at y ~520

### 1C. Presenter with Percentage/Number Overlay

- Large number (e.g. "+3.3%", "20%", "1.25L") appears ABOVE her head
- Number y-center: ~240-320
- Her head pushed slightly lower: y ~380-450
- Number is very large (see typography section)

---

## 2. Layout Catalog

### LAYOUT A: Presenter + Left-Aligned Headline Text
**Used in**: 2.21.36, 2.21.53, 2.23.56, 2.24.59, 2.25.12, 2.27.17

- Text block: left-aligned, x ~40-60
- Text top: y ~180-280
- Text bottom: y ~380-450 (must clear above Aparna's head by at least 20px)
- Aparna head: y ~380-480
- Text is 2-4 lines of large bold white or gold text
- No background card behind text -- text floats directly over the dark/blurred edge of frame

**Coordinate template (1080x1920)**:
```
text_x: 50
text_y_start: 200
text_y_end: 400
aparna_head_y: 430
```

### LAYOUT B: Full-Frame Data Screen (no presenter)
**Used in**: 2.21.16, 2.21.44, 2.22.51, 2.23.07, 2.23.26

- Dark background with gold particle vignette
- Title text (gold/yellow): centered, y ~120-180
- Screenshot/chart card: centered horizontally, x ~45-70 margins on each side
- Chart card top: y ~240-300
- Chart card dimensions: ~940-1000 px wide, 400-550 px tall
- Chart card styling: dark (#1A1A1A) fill, 1px border (#333), border-radius 12px
- Second chart (if present): starts ~30-40 px below first chart

**Coordinate template**:
```
title_y: 140
chart_x: 50
chart_y: 280
chart_width: 980
chart_height: 480
chart_bg: #1A1A1A
chart_border: 1px solid #333333
chart_radius: 12px
gap_between_charts: 40
```

### LAYOUT C: Numbered List (no presenter)
**Used in**: 2.21.44

- Dark background with gold vignette
- Large gold headline: x ~50, y ~160, bold
- Numbered items below: x ~50, y starts ~320
- Each item: "1. Text" format, white, ~36px
- Line spacing: ~80px between items
- Left margin: 50px

**Coordinate template**:
```
headline_x: 50
headline_y: 160
item_start_y: 320
item_line_height: 80
item_x: 50
```

### LAYOUT D: Presenter + Question Badge
**Used in**: 2.24.27

- Gold-bordered badge/card overlaps Aparna's head area
- Badge position: x ~30, y ~220, width ~700, height ~100
- Badge styling: dark fill (#1A1816), 2px solid gold border (#D4A843), border-radius 12px
- Text inside badge: white, bold, ~42px
- Aparna's head: y ~360-400, partially behind/below the badge

**Coordinate template**:
```
badge_x: 30
badge_y: 220
badge_w: 700
badge_h: 100
badge_bg: #1A1816
badge_border: 2px solid #D4A843
badge_radius: 12px
text_size: 42px
```

### LAYOUT E: Presenter + Company Badge (icon + name)
**Used in**: 9.42.02, 2.22.06

- Small card above Aparna's head, horizontally centered or slightly left
- Card: ~300-400 px wide, ~80-100 px tall
- Icon on left side (~50x50), company name text on right
- Border: 2px solid gold (#D4A843), border-radius 12px
- Dark fill inside
- Aparna visible below from y ~420 onward

**Coordinate template**:
```
badge_x_center: 540
badge_y: 180
badge_w: 360
badge_h: 90
icon_size: 50
badge_bg: #1A1816
badge_border: 2px solid #D4A843
badge_radius: 12px
```

### LAYOUT F: Diagram -- Parent-Child Hierarchy (no presenter)
**Used in**: 2.24.38, 2.25.49, 9.41.39, 9.41.50

- Dark background with gold vignette
- Parent node: centered, y ~180-250
  - Gold-bordered card: ~360 px wide, ~90 px tall
  - Icon on left, text on right
  - Border: 2px solid gold, radius 16px, dark fill
- Dashed connector lines: gold/yellow dashed stroke, ~2px
- Child nodes: 2-3 cards arranged horizontally at y ~500-620
  - Each card: ~160-180 px wide, ~160-180 px tall
  - Cyan/teal border: 2px solid #00D4AA, radius 16px
  - Icon centered above label text
  - Icon: ~60px, line-art style, cyan/teal color
  - Label: white, ~22px, centered below icon

**Coordinate template**:
```
parent_card_x_center: 540
parent_card_y: 200
parent_card_w: 360
parent_card_h: 90

connector_style: dashed 2px #D4A843

child_row_y: 540
child_card_size: 170
child_gap: 30
child_border: 2px solid #00D4AA
child_radius: 16px
child_icon_size: 60
child_label_size: 22px
```

### LAYOUT G: Diagram -- Linear Chain (no presenter)
**Used in**: 2.24.49, 9.41.39

- Parent card at top: same styling as Layout F parent
- Single dashed vertical connector line
- Child card centered below
- Descriptive text between nodes: large, letter-spaced, white/gold

**Coordinate template**:
```
parent_y: 180
connector_vertical: dashed 2px #D4A843
middle_text_y: 430
child_y: 560
```

### LAYOUT H: Comparison / Side-by-Side Cards (no presenter)
**Used in**: 2.25.39

- Two cards side by side above Aparna or on data screen
- Card 1 (left): gold border, ~220 px wide, ~180 px tall
- Card 2 (right): grey/white border, same size
- Each card has icon on top, label text below
- Dashed line connecting them horizontally
- Cards positioned at y ~220-400

### LAYOUT I: Data Table Card (no presenter)
**Used in**: 2.26.45, 2.26.53, 2.27.02

- Dark background
- Centered card with table layout
- Card: x ~80, width ~920, border-radius 16px, border 2px solid #444
- Dark fill (#141210)
- Header row: large bold white text, e.g. "PORTFOLIO"
- Table rows: alternating dark shades, each ~70-80 px tall
- Left column: white label text ~28px
- Right column: colored value text ~28-32px (colors vary: gold, red, cyan, mint)
- Row separator: 1px solid #333

**Coordinate template**:
```
card_x: 80
card_y: 140
card_w: 920
card_radius: 16px
card_border: 2px solid #444444
card_bg: #141210
header_size: 48px
row_height: 75
label_size: 28px
value_size: 30px
row_separator: 1px solid #333333
```

### LAYOUT J: Highlight Badge Row (no presenter)
**Used in**: 2.27.02

- Below the main data card
- 1-2 standalone badges stacked vertically
- Each badge: dashed border, ~500 px wide, ~70 px tall, centered
- Border: 2px dashed #FFFFFF, radius 12px
- Text inside: mixed colors (gold + white, or cyan + white)
- Gap between badges: 30px

**Coordinate template**:
```
badge_row_start_y: 1050
badge_w: 500
badge_h: 70
badge_x_center: 540
badge_border: 2px dashed #FFFFFF
badge_radius: 12px
badge_gap: 30
```

### LAYOUT K: Comparison Infographic (no presenter)
**Used in**: 2.27.31

- Full data frame, warm dark background
- Title: letter-spaced white text at top, y ~80
- Subtitle: bold gold text, y ~120
- Two profile cards side by side at y ~200
  - Left card: gold border, icon of person + rupee symbol
  - Right card: cyan border, same icon style
  - Each ~200 px wide, ~200 px tall
- Below: comparison data in two columns with bullet markers
- Color coding: gold for Investor 1, cyan for Investor 2
- Timeline dots/markers connected by vertical line

### LAYOUT L: Product Card Rows (no presenter)
**Used in**: 2.26.03, 2.29.09

- 2-3 cards stacked vertically, each containing:
  - Left side: card with company/fund name (colored border)
  - Right side: percentage or value text
  - Dashed line connecting them
- Card colors alternate: gold border, red border, cyan border
- Each card: ~280 px wide, ~100 px tall
- Text beside card: ~28-32px, bold
- Vertical spacing between rows: ~200 px

### LAYOUT M: Presenter + Large Number Above Head
**Used in**: 2.24.20, 2.27.17, 2.27.52, 2.28.24

- Very large number/percentage displayed above Aparna's head
- Number position: centered, y ~180-300
- Number size: 100-160px, bold
- Sometimes with subtitle below in smaller text (~32px, letter-spaced)
- Aparna's head starts at y ~380-450

**Coordinate template**:
```
number_y_center: 240
number_size: 130px
number_weight: 900
subtitle_y: 340
subtitle_size: 32px
subtitle_letter_spacing: 6px
aparna_head_y: 430
```

### LAYOUT N: Flowchart / Process Diagram (no presenter)
**Used in**: 2.28.35, 2.28.43, 2.29.01

- Full data frame
- Uses circles and cards connected by dashed/solid lines
- Circle nodes: 120-180 px diameter, colored borders (red, gold, cyan)
- Square cards: similar to Layout F children
- Bracket/tree connectors from one node to multiple children
- Text labels: white ~22-26px
- Highlighted keywords: gold or red or cyan
- Warning icons: small triangle with "!" inside

---

## 3. Typography Scale

### Font Family
All text appears to be a **sans-serif** font, likely **Montserrat** or **Poppins** (bold geometric sans). Headings use heavy weight; body uses medium.

### Size Scale (mapped to 1080x1920)

| Size (px) | Weight | Usage | Color |
|---|---|---|---|
| **160** | 900 (Black) | Giant single numbers ("20%") | Gold (#D4A843) or white |
| **130** | 900 | Large currency/percentage above head ("1.25L", "+3.3%") | Cyan (#00D4AA) or gold |
| **100** | 800 | Major stat number | Gold or white |
| **72** | 800 (ExtraBold) | Primary headline text on presenter frames ("8 Years", "A 2 week") | White (#FFFFFF) or gold (#D4A843) |
| **56** | 700 (Bold) | Secondary headline / emphasis words ("Cheaper", "Bigger") | Cyan (#00D4AA) or gold or white |
| **48** | 700 | Card headers ("PORTFOLIO", "CHECK") | White or mint/green (#B8FF90) |
| **42** | 700 | Question text in badges, important phrases | White |
| **36** | 600 (SemiBold) | Numbered list items, supporting text | White |
| **32** | 600 | Subtitle text, letter-spaced labels ("COMBINED LIMIT", "STABLE") | White, letter-spacing 4-8px |
| **28** | 500 (Medium) | Table cell text, card labels | White or colored |
| **24** | 500 | Diagram node labels, small card text | White |
| **22** | 400 (Regular) | Child node labels in diagrams | White |
| **18** | 400 | Disclaimer text, source attribution | White at 70% opacity |
| **16** | 400 | Fine print, source citations | White at 50% opacity |

### Color Assignments for Text

| Color | Hex | Usage |
|---|---|---|
| **Gold/Yellow** | #D4A843 | Headlines, company names, emphasis numbers, positive growth, connector lines |
| **Cyan/Teal** | #00D4AA | Percentage values, positive metrics, secondary emphasis, some badges |
| **Mint/Light Green** | #B8FF90 | Card header text ("CHECK"), highlight emphasis |
| **Red** | #E84040 | Negative values, losses, warning states, "LIMIT REACHED" |
| **Coral/Salmon** | #FF8A80 | Secondary negative values in tables |
| **White** | #FFFFFF | Primary text, body text, headlines, labels |
| **Light Gold** | #FFD700 | Bright emphasis on gold variant |
| **Orange** | #E88A30 | Rare accent, "20%" large number variant |

### Text Rendering Rules
- Headlines on presenter frames: **no text shadow**, rely on dark edges of frame for contrast
- Headlines on data frames: **no shadow needed**, dark background provides contrast
- Letter-spacing on label text (e.g. "COMBINED LIMIT", "S T A B L E"): 4-8px
- Some labels use full letter-spacing with spaces between characters: "P R O M O T E R S"
- Line height: 1.2 for headlines, 1.5 for body/list text

---

## 4. Card/Badge Specifications

### 4A. Company Name Badge (parent node in diagrams)
- Width: 340-400 px
- Height: 80-100 px
- Background: #1A1816 (very dark brown)
- Border: 2px solid #D4A843 (gold)
- Border-radius: 16px
- Padding: 12px 24px
- Icon: 50x50 px on the left, gold/yellow line-art style
- Text: 28-32px, bold, white or gold, vertically centered
- Shadow: subtle dark drop shadow, 0 4px 12px rgba(0,0,0,0.5)

### 4B. Child/Category Card (in diagrams)
- Width: 150-180 px
- Height: 150-180 px (square-ish)
- Background: #0D0A06 (near black) or #141414
- Border: 2px solid #00D4AA (cyan/teal)
- Border-radius: 16px
- Icon: 50-60 px, centered horizontally, cyan line-art
- Label: 20-24px, white, centered, below icon
- Padding: 20px
- Glow effect: subtle cyan glow on border (0 0 8px rgba(0,212,170,0.3))

### 4C. Question/Statement Badge
- Width: auto (fits text + padding)
- Height: 80-100 px
- Background: #1A1816
- Border: 2px solid #D4A843
- Border-radius: 12px
- Padding: 16px 32px
- Text: 38-44px, bold, white
- Position: overlaps or sits just above Aparna's head area

### 4D. Data Table Card
- Width: 880-940 px
- Border: 2px solid #444444
- Border-radius: 16px
- Background: #141210
- Header padding: 24px
- Row height: 70-80 px
- Row padding: 16px 24px
- Row separator: 1px solid #333333
- Alternating row colors: #141210 and #1A1714

### 4E. Highlight/Result Badge (dashed border)
- Width: 460-520 px
- Height: 65-75 px
- Background: transparent or #0D0A06
- Border: 2px dashed #FFFFFF
- Border-radius: 12px
- Padding: 12px 28px
- Text: 32-36px, mixed colors (gold value + white label, or cyan value + white label)

### 4F. Screener Data Card (stock price)
- Full-width with side margins (~50px each side)
- Height: 400-500 px
- Background: #1A1A1A
- Border: 1px solid #333333
- Border-radius: 12px
- Internal layout mirrors Google Finance / Screener.in card
- Company name: white, 24px, bold
- Price: white, 36px, bold
- Change: green (#00C853) for positive, red for negative, 18px
- Chart area: fills bottom 60% of card

### 4G. Presenter Inset Box (Ola Electric style)
- Width: ~990 px (frame width minus 45px margins each side)
- Height: ~380 px
- Border: 3px solid #D4A843 (gold)
- Border-radius: 16px
- Contains video feed of Aparna
- Positioned at top of frame: y ~90 to y ~470

---

## 5. Spacing Rules

### Safe Zones (where text must NOT go)

| Zone | Coordinates | Reason |
|---|---|---|
| Top-left controls | x 0-160, y 0-80 | Play/sound buttons |
| Top-right logo | x 750-1080, y 0-90 | Angel One logo |
| Bottom disclaimer | y 1850-1920 (full width) | Disclaimer bar |
| Bottom-left source | x 0-250, y 1800-1870 | Source attribution (when present) |

### Minimum Distances

| Rule | Value |
|---|---|
| Text above Aparna's head (minimum gap) | 20-30 px between text bottom and head top |
| Text from left edge | 40-60 px |
| Text from right edge | 40-60 px (but often ignored on right since Aparna may extend there) |
| Card from left/right edges | 50-80 px |
| Gap between stacked cards | 30-40 px |
| Gap between parent and child nodes in diagrams | 120-180 px vertical |
| Dashed connector overshoot past card edge | 0 px (connects to card border) |

### Presenter Frame Text Placement

When Aparna is on screen, text MUST stay in one of these zones:
1. **Above head zone**: y 100 to y (head_top - 20). Typically y 100 to y 360.
2. **Beside head zone** (rare): x 0-250 or x 750-1080, y 200-500. Text to the left of her head.
3. **Below frame** (never used for overlay text -- this is her body area)

Text must NEVER overlap with Aparna's face (y ~350-550, x ~300-750).

### Data Frame Spacing

On data-only frames (no presenter):
- Top margin for first element: 100-140 px (below logo/controls)
- Bottom margin: 100-120 px (above disclaimer)
- Horizontal margins: 50-80 px
- Usable content area: x 50-1030, y 120-1800

---

## 6. Screenshot/Data Frame Patterns

### 6A. Single Stock Chart
- Gold headline text centered: y ~140
- Chart card: centered, y ~280, width ~980, height ~450
- Dark card background with subtle border
- Below chart: empty dark space with gold corner vignettes

### 6B. Dual Stock Chart
- Gold headline text: y ~120
- Chart 1: y ~220, height ~380
- Gap: ~40 px
- Chart 2: y ~640, height ~380
- Both charts same width (~980) and styling

### 6C. Diagram Frame
- Background: dark (#0D0A06) with radial gold/brown particle effect in corners
- The gold particle vignette is a signature visual element -- concentrated dots/sparkles
- Vignette is strongest in bottom-right and top-left corners
- Content centered in the middle 80% of the frame

### 6D. Table/Portfolio Frame
- Card centered vertically and horizontally
- Card occupies ~60-70% of frame height
- Generous dark space above and below for breathing room

---

## 7. Color Palette Reference

### Primary Palette

| Name | Hex | RGB | Usage |
|---|---|---|---|
| Frame Black | #0D0A06 | 13, 10, 6 | Data frame background |
| Card Dark | #141210 | 20, 18, 16 | Card fills, table backgrounds |
| Card Border Dark | #333333 | 51, 51, 51 | Subtle card borders |
| Card Border Medium | #444444 | 68, 68, 68 | Table card borders |
| Gold Primary | #D4A843 | 212, 168, 67 | Headlines, connectors, parent card borders |
| Gold Bright | #FFD700 | 255, 215, 0 | Bright emphasis variant |
| Gold Muted | #B8952E | 184, 149, 46 | Darker gold for less emphasis |
| Cyan Primary | #00D4AA | 0, 212, 170 | Positive numbers, child card borders, emphasis |
| Mint/Lime | #B8FF90 | 184, 255, 144 | Highlight text ("CHECK") |
| Red Alert | #E84040 | 232, 64, 64 | Negative values, warnings |
| Coral | #FF8A80 | 255, 138, 128 | Secondary negative |
| Orange Accent | #E88A30 | 232, 138, 48 | Large number variant |
| White | #FFFFFF | 255, 255, 255 | Primary text |
| White 70% | rgba(255,255,255,0.7) | -- | Disclaimer text |

### Vignette/Background Effect
- The gold particle vignette consists of small dots (~2-4px) with a radial gradient
- Concentrated in corners, especially bottom-right
- Color: gold (#D4A843) at ~30-50% opacity
- Creates a warm, premium feel against the near-black background
- On presenter frames: NOT present (studio backdrop is real footage)

---

## 8. Connector Line Specifications

Used extensively in diagram layouts (F, G, K, N).

| Property | Value |
|---|---|
| Stroke color | #D4A843 (gold) |
| Stroke width | 2px |
| Dash pattern | 8px dash, 6px gap |
| Connection style | Curved for multi-child (bezier), straight vertical for single-child |
| Arrow heads | None (lines end at card borders) |
| For branching | Lines curve outward from parent center to each child's top-center |

---

## 9. Icon Specifications (Diagram Nodes)

Icons in cards are **line-art / outline style**, not filled.

| Property | Value |
|---|---|
| Style | Thin line-art, monochrome |
| Stroke width | 2-3px |
| Color in cyan cards | #00D4AA |
| Color in gold cards | #D4A843 |
| Size | 50-60px square |
| Padding from card edge | 20px top, centered horizontally |
| Common icons | Flask (chemicals), building (real estate), cart (consumer), computer (software), scooter (EV), wrench (services), factory (manufacturing), brain/chip (AI) |

---

## 10. Frame Type Decision Matrix

Use this to determine which layout pattern to apply based on storyboard content:

| Content Type | Layout | Presenter Visible? |
|---|---|---|
| Opening hook / opinion statement | A (headline + presenter) | Yes |
| Stock price with chart | B (data screen) | No |
| Numbered list of points | C (numbered list) | No |
| Rhetorical question | D (question badge + presenter) | Yes |
| Company introduction | E (company badge + presenter) or F (hierarchy diagram) | Yes or No |
| Company business segments | F (parent-child hierarchy) | No |
| Business attribute/characteristic | G (linear chain) | No |
| Key statistic/number | M (large number + presenter) | Yes |
| Comparison of two things | H or K (side-by-side) | No |
| Financial data / tax table | I (data table) | No |
| Result / outcome highlight | J (dashed badge row) | No |
| Process / flow explanation | N (flowchart) | No |
| Multiple fund/stock comparison | L (product card rows) | No |
| Emphasis words (adjectives) | A variant (stacked words, left-aligned) | Yes |

---

## 11. Animation Notes (for storyboard direction only)

While the storyboard generates static frames, include these motion cues for the video editor:

- Text on presenter frames typically **pops in** word-by-word or line-by-line
- Diagram nodes appear **sequentially** -- parent first, then connectors animate, then children
- Large numbers often have a **scale-up** entrance (from 80% to 100%)
- Cards in data frames **slide in from bottom** or **fade in**
- Charts appear with the data line **drawing itself** left-to-right

---

## 12. Quick Reference: Most Common Configurations

### "Talking Head + Headline" (60% of presenter frames)
```
Background: studio footage
Text position: x=50, y=200, left-aligned
Text size: 72px bold white (or gold for emphasis word)
Aparna head: y=420, centered
Logo: top-right
Disclaimer: bottom bar
```

### "Stock Data Screen" (most common data frame)
```
Background: #0D0A06 with gold vignette
Title: centered, y=140, 42px bold gold
Chart card: x=50, y=280, w=980, h=460
Card: #1A1A1A fill, 1px #333 border, 12px radius
Logo: top-right
Disclaimer: bottom bar
```

### "Company Hierarchy Diagram"
```
Background: #0D0A06 with gold vignette
Parent card: centered, y=200, 360x90, gold border
Connectors: dashed gold, curved to children
Child cards: row at y=540, each 170x170, cyan border
Icons: 60px line-art inside children
Logo: top-right
Disclaimer: bottom bar
```
