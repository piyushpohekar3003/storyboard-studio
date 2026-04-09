/* ===== 1080x1920 SVG Frame Renderer for A1 Bytes ===== */

const FW = 1080;
const FH = 1920;

const FRAME_COLORS = {
  bg_dark: '#1a1d2e',
  bg_presenter: '#f0ebe3',
  blue_pill: '#4a6fa5',
  blue_pill_text: '#ffffff',
  white: '#ffffff',
  caption_bg: 'rgba(0,0,0,0.55)',
  card_bg: '#ffffff',
  angel_one_blue: '#2541B2',
  green_up: '#22c55e',
  red_down: '#ef4444',
};

const FONT_MAIN = "'Inter', 'SF Pro Display', -apple-system, sans-serif";
const FONT_MONO = "'JetBrains Mono', monospace";
const PRESENTER_IMG = '/static/aparna.png';

// Stock footage by keyword
const BROLL_IMAGES = {
  'default': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=1000&fit=crop',
  'electric': 'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=1000&fit=crop',
  'motorcycle': 'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&h=1000&fit=crop',
  'battery': 'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&h=1000&fit=crop',
  'power': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&h=1000&fit=crop',
  'transmission': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&h=1000&fit=crop',
  'cash': 'https://images.unsplash.com/photo-1554672408-730436b60dde?w=600&h=1000&fit=crop',
  'money': 'https://images.unsplash.com/photo-1554672408-730436b60dde?w=600&h=1000&fit=crop',
  'car': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&h=1000&fit=crop',
  'highway': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&h=1000&fit=crop',
  'dashboard': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&h=1000&fit=crop',
  'solar': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=600&h=1000&fit=crop',
  'renewable': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=600&h=1000&fit=crop',
  'wind': 'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=600&h=1000&fit=crop',
  'graph': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=1000&fit=crop',
  'office': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&h=1000&fit=crop',
  'server': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=1000&fit=crop',
  'data': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=1000&fit=crop',
  'handshake': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=600&h=1000&fit=crop',
  'deal': 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=600&h=1000&fit=crop',
  'grocery': 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&h=1000&fit=crop',
  'food': 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&h=1000&fit=crop',
  'coal': 'https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=600&h=1000&fit=crop',
  'lpg': 'https://images.unsplash.com/photo-1585003791032-aed0171db943?w=600&h=1000&fit=crop',
  'product': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=1000&fit=crop',
  'retail': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&h=1000&fit=crop',
  'store': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&h=1000&fit=crop',
  'stock': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=1000&fit=crop',
  'trading': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=1000&fit=crop',
  'grid': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&h=1000&fit=crop',
  'smart': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=1000&fit=crop',
  'dividend': 'https://images.unsplash.com/photo-1554672408-730436b60dde?w=600&h=1000&fit=crop',
  // Company-specific footage for stock card frames
  'ola': 'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=1000&fit=crop',
  'bosch': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&h=1000&fit=crop',
  'honasa': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=1000&fit=crop',
  'mamaearth': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=1000&fit=crop',
  'tcs': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&h=1000&fit=crop',
  'tata': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&h=1000&fit=crop',
};

function getBrollImage(description) {
  if (!description) return BROLL_IMAGES['default'];
  const desc = description.toLowerCase();
  for (const [key, url] of Object.entries(BROLL_IMAGES)) {
    if (desc.includes(key)) return url;
  }
  return BROLL_IMAGES['default'];
}

// Find stock image from the stock name in supers
function getStockImage(supers) {
  if (!supers || !supers.length) return BROLL_IMAGES['default'];
  const name = supers[0].toLowerCase();
  for (const [key, url] of Object.entries(BROLL_IMAGES)) {
    if (name.includes(key)) return url;
  }
  return BROLL_IMAGES['stock'];
}

// ── SVG helpers ──

function svgEscape(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Blue pill super — LARGER font (42px default, was 34)
function svgPillSuper(text, cx, cy, fontSize = 42, pillColor = FRAME_COLORS.blue_pill) {
  const textLen = text.length * fontSize * 0.5;
  const pw = Math.max(textLen + 56, 220);
  const ph = fontSize + 34;
  const rx = ph / 2;
  return `
    <g>
      <rect x="${cx - pw/2}" y="${cy - ph/2}" width="${pw}" height="${ph}" rx="${rx}" fill="${pillColor}" opacity="0.92"/>
      <text x="${cx}" y="${cy + fontSize * 0.35}" text-anchor="middle" fill="${FRAME_COLORS.blue_pill_text}" font-family="${FONT_MAIN}" font-size="${fontSize}" font-weight="700" letter-spacing="0.5">${svgEscape(text)}</text>
    </g>`;
}

// Subtitle — ONLY shown when there are no supers
function svgSubtitle(text, cx, cy) {
  const maxChars = 42;
  const words = text.split(' ');
  const lines = [];
  let current = '';
  for (const w of words) {
    if ((current + ' ' + w).trim().length > maxChars) {
      lines.push(current.trim());
      current = w;
    } else {
      current = (current + ' ' + w).trim();
    }
  }
  if (current) lines.push(current);
  const displayLines = lines.slice(0, 2);

  const lineH = 46;
  const totalH = displayLines.length * lineH + 20;
  const totalW = Math.max(...displayLines.map(l => l.length)) * 20 + 48;
  const startY = cy - totalH / 2;

  return `<g>
    <rect x="${cx - totalW/2}" y="${startY}" width="${totalW}" height="${totalH}" rx="12" fill="${FRAME_COLORS.caption_bg}"/>
    ${displayLines.map((line, i) => `
      <text x="${cx}" y="${startY + 36 + i * lineH}" text-anchor="middle" fill="#fff" font-family="${FONT_MAIN}" font-size="32" font-weight="600" opacity="0.95">${svgEscape(line)}</text>
    `).join('')}
  </g>`;
}

function svgAngelOneLogo(x = FW - 220, y = 50) {
  return `
    <g transform="translate(${x}, ${y})">
      <polygon points="0,28 16,0 32,28" fill="${FRAME_COLORS.angel_one_blue}"/>
      <polygon points="14,28 22,14 30,28" fill="#ffffff" opacity="0.4"/>
      <text x="40" y="24" fill="${FRAME_COLORS.white}" font-family="${FONT_MAIN}" font-size="28" font-weight="700" letter-spacing="1">AngelOne</text>
    </g>`;
}

function svgShotLabel(shotNum, duration, type) {
  const typeLabels = { presenter: 'PRESENTER', broll: 'B-ROLL', presenter_stockcard: 'STOCK CARD' };
  const label = typeLabels[type] || 'SHOT';
  return `
    <g>
      <rect x="30" y="${FH - 80}" width="180" height="44" rx="22" fill="rgba(0,0,0,0.6)"/>
      <text x="120" y="${FH - 52}" text-anchor="middle" fill="#fff" font-family="${FONT_MONO}" font-size="20" font-weight="500">SHOT ${shotNum} · ${duration || '3s'}</text>
      <rect x="220" y="${FH - 80}" width="${label.length * 16 + 30}" height="44" rx="22" fill="rgba(255,255,255,0.15)"/>
      <text x="${220 + (label.length * 16 + 30) / 2}" y="${FH - 52}" text-anchor="middle" fill="#fff" font-family="${FONT_MAIN}" font-size="18" font-weight="600">${label}</text>
    </g>`;
}

// ── PRESENTER FRAME ──
// Full-screen Aparna, never windowed. Head always visible (anchored from top).
// Supers in lower-center area. Subtitle ONLY if no supers.
function renderPresenterFrame(shot) {
  const supers = shot.supers || [];
  const hasSupers = supers.length > 0;
  const uid = 'p-' + shot.shot + '-' + Math.random().toString(36).slice(2, 6);

  // Supers positioned in lower third
  let supersHtml = '';
  const superStartY = FH * 0.58;
  supers.forEach((s, i) => {
    supersHtml += svgPillSuper(s, FW / 2, superStartY + i * 76);
  });

  // Subtitle only when NO supers — positioned at lower third
  const subtitleHtml = (!hasSupers && shot.voiceover)
    ? svgSubtitle(shot.voiceover.slice(0, 85), FW / 2, FH * 0.65)
    : '';

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${FW} ${FH}" width="100%" height="100%">
    <defs>
      <linearGradient id="pres-bg-${uid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#e8e0d4"/>
        <stop offset="100%" stop-color="#d4cbbf"/>
      </linearGradient>
      <!-- Bottom vignette for text readability over presenter -->
      <linearGradient id="pres-vig-${uid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="rgba(0,0,0,0)"/>
        <stop offset="50%" stop-color="rgba(0,0,0,0)"/>
        <stop offset="85%" stop-color="rgba(0,0,0,0.25)"/>
        <stop offset="100%" stop-color="rgba(0,0,0,0.45)"/>
      </linearGradient>
    </defs>

    <!-- Background fill -->
    <rect width="${FW}" height="${FH}" fill="url(#pres-bg-${uid})"/>

    <!-- Presenter — FULL SCREEN, head anchored at top (xMidYMin) so face is always visible -->
    <image href="${PRESENTER_IMG}" x="0" y="0" width="${FW}" height="${FH}" preserveAspectRatio="xMidYMin slice"/>

    <!-- Bottom vignette for text readability -->
    <rect width="${FW}" height="${FH}" fill="url(#pres-vig-${uid})"/>

    <!-- Supers OR subtitle (never both) -->
    ${supersHtml}
    ${subtitleHtml}

    <!-- Shot label -->
    ${svgShotLabel(shot.shot, shot.duration_hint, 'presenter')}
  </svg>`;
}

// ── B-ROLL FRAME ──
// Full-screen stock footage. Supers in lower-center. Subtitle ONLY if no supers.
function renderBrollFrame(shot) {
  const supers = shot.supers || [];
  const hasSupers = supers.length > 0;
  const brollDesc = shot.broll_description || 'Stock footage';
  const brollImg = getBrollImage(brollDesc);
  const uid = 'b-' + shot.shot + '-' + Math.random().toString(36).slice(2, 6);

  let supersHtml = '';
  const superStartY = FH * 0.55;
  supers.forEach((s, i) => {
    supersHtml += svgPillSuper(s, FW / 2, superStartY + i * 76);
  });

  const subtitleHtml = (!hasSupers && shot.voiceover)
    ? svgSubtitle(shot.voiceover.slice(0, 85), FW / 2, FH * 0.65)
    : '';

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${FW} ${FH}" width="100%" height="100%">
    <defs>
      <linearGradient id="broll-vig-${uid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="rgba(0,0,0,0.2)"/>
        <stop offset="30%" stop-color="rgba(0,0,0,0)"/>
        <stop offset="60%" stop-color="rgba(0,0,0,0)"/>
        <stop offset="100%" stop-color="rgba(0,0,0,0.5)"/>
      </linearGradient>
    </defs>

    <!-- Full-bleed stock footage -->
    <image href="${brollImg}" x="0" y="0" width="${FW}" height="${FH}" preserveAspectRatio="xMidYMid slice"/>

    <!-- Vignette overlay -->
    <rect width="${FW}" height="${FH}" fill="url(#broll-vig-${uid})"/>

    <!-- B-roll description label (top-left) -->
    <rect x="40" y="40" width="${brollDesc.length * 15 + 36}" height="40" rx="8" fill="rgba(0,0,0,0.5)"/>
    <text x="58" y="67" fill="#fff" font-family="${FONT_MAIN}" font-size="22" font-weight="400" opacity="0.85">${svgEscape(brollDesc)}</text>

    <!-- Supers OR subtitle (never both) -->
    ${supersHtml}
    ${subtitleHtml}

    <!-- Shot label -->
    ${svgShotLabel(shot.shot, shot.duration_hint, 'broll')}
  </svg>`;
}

// ── STOCK CARD FRAME ──
// NO windowed presenter. Full-screen stock footage of the company.
// Price data shown as supers. Subtitle ONLY if no supers.
function renderStockCardFrame(shot) {
  const supers = shot.supers || [];
  const hasSupers = supers.length > 0;
  const stockImg = getStockImage(supers);
  const uid = 'sc-' + shot.shot + '-' + Math.random().toString(36).slice(2, 6);

  // Extract price data for overlay card
  const stockName = supers[0] || 'STOCK';
  const priceChange = supers[1] || '';
  const priceValue = supers[2] || '';
  const isUp = priceChange.includes('↑') || priceChange.includes('+');
  const changeColor = isUp ? FRAME_COLORS.green_up : FRAME_COLORS.red_down;

  // Price data card (floating, top area)
  const priceCardH = 180;
  const priceCard = `
    <g>
      <rect x="60" y="100" width="${FW - 120}" height="${priceCardH}" rx="24" fill="rgba(255,255,255,0.93)"/>
      <text x="110" y="160" fill="#222" font-family="${FONT_MAIN}" font-size="36" font-weight="700">${svgEscape(stockName)}</text>
      <text x="110" y="215" fill="#111" font-family="${FONT_MAIN}" font-size="48" font-weight="700">${svgEscape(priceValue || '')}</text>
      ${priceChange ? `
        <rect x="450" y="185" width="${priceChange.length * 22 + 36}" height="44" rx="10" fill="${changeColor}" opacity="0.18"/>
        <text x="468" y="217" fill="${changeColor}" font-family="${FONT_MONO}" font-size="30" font-weight="700">${svgEscape(priceChange)}</text>
        <text x="${468 + priceChange.length * 22 + 46}" y="217" fill="#888" font-family="${FONT_MAIN}" font-size="24">Today</text>
      ` : ''}
    </g>`;

  const subtitleHtml = (!hasSupers && shot.voiceover)
    ? svgSubtitle(shot.voiceover.slice(0, 85), FW / 2, FH * 0.75)
    : '';

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${FW} ${FH}" width="100%" height="100%">
    <defs>
      <linearGradient id="sc-vig-${uid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="rgba(0,0,0,0.35)"/>
        <stop offset="25%" stop-color="rgba(0,0,0,0.05)"/>
        <stop offset="65%" stop-color="rgba(0,0,0,0)"/>
        <stop offset="100%" stop-color="rgba(0,0,0,0.45)"/>
      </linearGradient>
    </defs>

    <!-- Full-screen stock footage of the company -->
    <image href="${stockImg}" x="0" y="0" width="${FW}" height="${FH}" preserveAspectRatio="xMidYMid slice"/>

    <!-- Vignette -->
    <rect width="${FW}" height="${FH}" fill="url(#sc-vig-${uid})"/>

    <!-- Angel One Logo -->
    ${svgAngelOneLogo()}

    <!-- Floating price data card -->
    ${priceCard}

    <!-- Subtitle (only if no supers — but stock card always has price supers, so this is rare) -->
    ${subtitleHtml}

    <!-- Shot label -->
    ${svgShotLabel(shot.shot, shot.duration_hint, 'presenter_stockcard')}
  </svg>`;
}

// ── Main dispatch ──

function renderFrameSVG(shot) {
  switch (shot.visual_type) {
    case 'presenter_stockcard': return renderStockCardFrame(shot);
    case 'broll': return renderBrollFrame(shot);
    case 'presenter':
    default: return renderPresenterFrame(shot);
  }
}

// ── Render strip ──

function renderFrameStrip(visuals) {
  const legend = `<div class="frame-legend">
    <div class="legend-item"><div class="legend-dot presenter"></div>Presenter</div>
    <div class="legend-item"><div class="legend-dot broll"></div>B-Roll</div>
    <div class="legend-item"><div class="legend-dot stockcard"></div>Stock Card</div>
  </div>`;

  const frames = visuals.map(shot => `
    <div class="frame-card type-${shot.visual_type}">
      <div class="frame-svg-wrap">
        ${renderFrameSVG(shot)}
      </div>
      <div class="frame-info">
        <div class="frame-info-header">
          <span class="frame-shot-num">Shot ${shot.shot}</span>
          <span class="frame-duration">${shot.duration_hint || ''}</span>
        </div>
        <div class="frame-vo">${svgEscape(shot.voiceover || '')}</div>
        ${shot.supers && shot.supers.length ? `<div class="frame-supers">${shot.supers.map(s => `<span class="frame-super-tag">${svgEscape(s)}</span>`).join('')}</div>` : ''}
        ${shot.broll_description ? `<div class="frame-broll-desc">B-roll: ${svgEscape(shot.broll_description)}</div>` : ''}
        ${shot.notes ? `<div class="frame-notes">${svgEscape(shot.notes)}</div>` : ''}
      </div>
    </div>
  `).join('');

  return legend + `<div class="frame-strip">${frames}</div>`;
}
