/* ===== A1 Bytes — News Shorts Visual Tool ===== */

// ── Category definitions ──
const CATEGORIES = {
  stock: {
    name: 'Stock Price Movement',
    cssClass: 'cat-stock',
    coreFormat: 'Presenter (Avatar) + Stock Card + B-roll + Text overlays',
    description: 'Hook is always the price move. Opens with avatar + stock card. Middle alternates b-roll+text (catalysts) and avatar (analysis). Closes on avatar.',
    pattern: [
      { type: 'stockcard', label: 'Avatar + Stock Card', sub: 'Price hook' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Catalyst 1' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Catalyst 2' },
      { type: 'presenter', label: 'Avatar + Text', sub: 'So-what' },
      { type: 'presenter', label: 'Avatar', sub: 'CTA' },
    ],
  },
  ipo: {
    name: 'IPO',
    cssClass: 'cat-ipo',
    coreFormat: 'Presenter (Avatar) + Data Cards + B-roll + Text overlays',
    description: 'Data-heavy — dates, price band, lot size, GMP. Leans on clean data cards/text overlays. Avatar anchors open and close. GMP section always carries a disclaimer.',
    pattern: [
      { type: 'presenter', label: 'Avatar + Text', sub: 'Name + dates' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Company context' },
      { type: 'presenter', label: 'Avatar + Text', sub: 'Price band / Issue size' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Lot size / Min invest' },
      { type: 'presenter', label: 'Avatar + Text', sub: 'Listing date' },
      { type: 'disclaimer', label: 'Avatar + Disclaimer', sub: 'GMP' },
      { type: 'presenter', label: 'Avatar', sub: 'CTA' },
    ],
  },
  earnings: {
    name: 'Earnings / Results',
    cssClass: 'cat-earnings',
    coreFormat: 'Presenter (Avatar) + Persistent Data Widget + B-roll + Text overlays',
    description: 'Number after number — a persistent on-screen widget stays visible throughout data section for visual continuity. Each metric gets its own b-roll+text card. Avatar bookends.',
    pattern: [
      { type: 'presenter', label: 'Avatar + Text', sub: 'Beat/miss headline' },
      { type: 'widget', label: '[Widget ON]', sub: '' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Revenue' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Profit' },
      { type: 'broll', label: 'B-roll + Text', sub: 'TCV / Deals' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Dividend' },
      { type: 'widget', label: '[Widget OFF]', sub: '' },
      { type: 'stockcard', label: 'Avatar + Stock Card', sub: 'Price reaction' },
      { type: 'presenter', label: 'Avatar', sub: 'CTA' },
    ],
  },
  macro: {
    name: 'Knowledge / Macro',
    cssClass: 'cat-macro',
    coreFormat: 'Presenter (Avatar) + Stock Footage + Text overlays',
    description: 'Narrative-driven, not data-card-driven. More cinematic b-roll. Text overlays support key stats but tone is explanatory. Avatar carries editorial angle.',
    pattern: [
      { type: 'presenter', label: 'Avatar + Text', sub: 'Headline / hook' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Context / ranking' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Supporting detail' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Implication' },
      { type: 'presenter', label: 'Avatar + Text', sub: 'So-what / thesis' },
      { type: 'presenter', label: 'Avatar', sub: 'CTA' },
    ],
  },
  tech: {
    name: 'Tech / Strategic Update',
    cssClass: 'cat-tech',
    coreFormat: 'Presenter (Avatar) + Stock Card + B-roll + Checklist Text overlays',
    description: 'Opens with announcement, immediately grounds with stock card (even if flat). Middle uses b-roll + checklist-style text overlays. Avatar poses forward-looking question.',
    pattern: [
      { type: 'presenter', label: 'Avatar + Text', sub: 'Announcement' },
      { type: 'stockcard', label: 'Avatar + Stock Card', sub: 'Price reaction' },
      { type: 'broll', label: 'B-roll + Text', sub: 'Benefits checklist' },
      { type: 'presenter', label: 'Avatar', sub: 'Forward question' },
      { type: 'presenter', label: 'Avatar', sub: 'CTA' },
    ],
  },
};

// ── 8 Sample scripts + pre-generated visuals ──
const NEWS_DATA = [
  {
    id: 1, title: 'Ola Electric share price surge', category: 'stock', source: 'Business Standard',
    script: `Ola Electric is up over 16% today and there are multiple reasons. Apart from PLI registration approval, Roadster X+ price cut, and higher March registrations, there's a new battery announcement that could also be the reason. The company just announced its in-house LFP cell — a bigger, more cost-efficient battery format than its current technology. Lower costs, higher capacity — a possible structural shift for Ola's margins. Stay in the loop with Angel One Bytes for more updates.`,
    visuals: [
      { shot: 1, voiceover: 'Ola Electric is up over 16% today and there are multiple reasons.', visual_type: 'presenter_stockcard', supers: ['OLA ELECTRIC', '↑ 16%'], broll_description: null, duration_hint: '3s', notes: 'Google Finance stock card' },
      { shot: 2, voiceover: 'Apart from PLI registration approval, Roadster X+ price cut, and higher March registrations—', visual_type: 'broll', supers: ['✅ PLI certification', '✅ Roadster X+ price cut', '✅ March registrations ↑ 150% MoM'], broll_description: 'Electric motorcycle (Roadster X+)', duration_hint: '5s', notes: '' },
      { shot: 3, voiceover: "there's a new battery announcement that could also be the reason.", visual_type: 'presenter', supers: ['New battery announcement'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 4, voiceover: 'The company just announced its in-house LFP cell — a bigger, more cost-efficient battery format than its current technology.', visual_type: 'broll', supers: ['In-house LFP cell', 'Bigger format', 'More cost-efficient'], broll_description: 'EV battery close-up', duration_hint: '5s', notes: '' },
      { shot: 5, voiceover: "Lower costs, higher capacity — a possible structural shift for Ola's margins.", visual_type: 'presenter', supers: ['Lower costs', 'Higher capacity', 'Possible margin shift'], broll_description: null, duration_hint: '4s', notes: '' },
      { shot: 6, voiceover: 'Stay in the loop with Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 2, title: 'Om Power Transmission IPO', category: 'ipo', source: 'Chittorgarh',
    script: `Om Power Transmission IPO opens today and closes April 13. The company is an EPC player with 14 years of experience in high-voltage power transmission infrastructure. Issue size: ₹150 crore. Price band: ₹166 to ₹175 per share. Minimum investment: ₹14,875 for 85 shares. Listing is expected on April 17. GMP currently stands at ₹1.5 implying a very flat listing as of now. Subscribe to Angel One Bytes for more updates.`,
    visuals: [
      { shot: 1, voiceover: 'Om Power Transmission IPO opens today and closes April 13.', visual_type: 'presenter', supers: ['OM POWER TRANSMISSION IPO', 'Open: Today', 'Close: 13 April'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 2, voiceover: 'The company is an EPC player with 14 years of experience in high-voltage power transmission infrastructure.', visual_type: 'broll', supers: ['EPC company', '14 years experience', 'High-voltage power transmission'], broll_description: 'High-voltage power transmission towers', duration_hint: '4s', notes: '' },
      { shot: 3, voiceover: 'Issue size: ₹150 crore. Price band: ₹166 to ₹175 per share.', visual_type: 'presenter', supers: ['Issue size: ₹150 crore', 'Price band: ₹166 – ₹175'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 4, voiceover: 'Minimum investment: ₹14,875 for 85 shares.', visual_type: 'broll', supers: ['Min investment: ₹14,875', 'Lot size: 85 shares'], broll_description: 'Cash / money visual', duration_hint: '3s', notes: '' },
      { shot: 5, voiceover: 'Listing is expected on April 17.', visual_type: 'presenter', supers: ['Listing date: 17 April (tentative)'], broll_description: null, duration_hint: '2s', notes: '' },
      { shot: 6, voiceover: 'GMP currently stands at ₹1.5 — implying a very flat listing as of now.', visual_type: 'presenter', supers: ['GMP: ₹1.5', '⚠️ Flat listing expected'], broll_description: null, duration_hint: '4s', notes: 'Include GMP disclaimer' },
      { shot: 7, voiceover: 'Subscribe to Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 3, title: 'Bosch share price up', category: 'stock', source: 'Angel One',
    script: `Bosch is over 2% up today — and here's why. The company has announced plans to acquire 100% of Bosch Chassis Systems India — a leading player in automotive safety systems. India is tightening vehicle safety regulations. Mandatory ABS, ESC and airbag requirements are expanding. Bosch acquiring a safety systems company right now could be a significant move. Stay in the loop with Angel One Bytes for more updates.`,
    visuals: [
      { shot: 1, voiceover: "Bosch is over 2% up today — and here's why.", visual_type: 'presenter_stockcard', supers: ['BOSCH', '↑ 2%'], broll_description: null, duration_hint: '3s', notes: 'Google Finance stock card' },
      { shot: 2, voiceover: 'The company has announced plans to acquire 100% of Bosch Chassis Systems India — a leading player in automotive safety systems.', visual_type: 'broll', supers: ['Acquiring: Bosch Chassis Systems India', 'Automotive safety systems'], broll_description: 'Cars driving on highway', duration_hint: '5s', notes: '' },
      { shot: 3, voiceover: 'India is tightening vehicle safety regulations.', visual_type: 'presenter', supers: ['⚠️ India tightening vehicle safety regulations'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 4, voiceover: 'Mandatory ABS, ESC and airbag requirements are expanding.', visual_type: 'broll', supers: ['✅ ABS', '✅ ESC', '✅ Airbag systems'], broll_description: 'Car dashboard close-up / steering wheel shot', duration_hint: '4s', notes: '' },
      { shot: 5, voiceover: 'Bosch acquiring a safety systems company right now could be a significant move.', visual_type: 'presenter', supers: ['Timely move for Bosch 🎯'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 6, voiceover: 'Stay in the loop with Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 4, title: 'India Ranks Third Globally in Renewable Energy', category: 'macro', source: 'Angel One',
    script: `India is now the world's third largest country in renewable energy capacity — surpassing Brazil. China is the leader and the US stands at the second place. India stands at third place with 250 GW. This has become possible after the addition of 55.3 GW of non-fossil capacity in FY26. India has hit its 50% non-fossil target five years ahead of schedule. India's renewable sector is attracting billions in investment from Adani Green to Tata Power to global funds. The ranking confirms the thesis. Subscribe to Angel One Bytes for more updates.`,
    visuals: [
      { shot: 1, voiceover: "India is now the world's third largest country in renewable energy capacity — surpassing Brazil.", visual_type: 'presenter', supers: ['🎯 India — #3 in Renewable Energy', 'Surpassed Brazil'], broll_description: null, duration_hint: '4s', notes: '' },
      { shot: 2, voiceover: 'China is the leader and the US stands at second place. India stands at third place with 250 GW.', visual_type: 'broll', supers: ['🏆 1st: China 2,258 GW', '🥈 2nd: USA 467 GW', '🥉 3rd: India 250 GW'], broll_description: 'Solar panels + wind turbines', duration_hint: '5s', notes: 'IRENA 2026 rankings' },
      { shot: 3, voiceover: 'This has become possible after the addition of 55.3 GW of non-fossil capacity in FY26.', visual_type: 'presenter', supers: ['Added in FY26:', '55.3 GW non-fossil capacity'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 4, voiceover: 'India has hit its 50% non-fossil target five years ahead of schedule.', visual_type: 'presenter', supers: ['50% non-fossil target ✅', '5 years ahead of 2030 goal'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 5, voiceover: "India's renewable sector is attracting billions in investment from Adani Green to Tata Power to global funds.", visual_type: 'broll', supers: ['💰 Adani Green', '💰 Tata Power', '💰 Global funds'], broll_description: 'Money / upward graph', duration_hint: '4s', notes: '' },
      { shot: 6, voiceover: 'The ranking confirms the thesis.', visual_type: 'presenter', supers: ['The ranking confirms the thesis ✅📊'], broll_description: null, duration_hint: '2s', notes: '' },
      { shot: 7, voiceover: 'Subscribe to Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 5, title: 'Honasa / Mamaearth pre-result rally', category: 'stock', source: 'Mint',
    script: `This stock hit a 52-week high and is up 12%. Honasa — the parent of Mamaearth — just dropped a business update ahead of its results. But what's driving investor excitement? The company is expected to post growth in the high twenties percent range in Q4. Offline distribution expanded over 25%. Direct outlet coverage crossed 1 lakh outlets. And Q4 marks the first full quarter of its BTM Ventures acquisition. The market seems to be pricing in a strong quarter — before the numbers are even out. Stay in the loop with Angel One Bytes for more updates.`,
    visuals: [
      { shot: 1, voiceover: 'This stock hit a 52-week high and is up 12%.', visual_type: 'presenter_stockcard', supers: ['HONASA', '↑ 12%', '52-week high'], broll_description: null, duration_hint: '3s', notes: 'Google Finance stock card' },
      { shot: 2, voiceover: 'Honasa — the parent of Mamaearth — just dropped a business update ahead of its results.', visual_type: 'broll', supers: ['Honasa Consumers - Parent of:', '✅ Mamaearth', '✅ The Derma Co.', '✅ Aqualogica', '✅ BBlunt'], broll_description: 'Mamaearth product shots', duration_hint: '5s', notes: '' },
      { shot: 3, voiceover: "But what's driving investor excitement?", visual_type: 'presenter', supers: ["What's driving excitement? 👇"], broll_description: null, duration_hint: '2s', notes: '' },
      { shot: 4, voiceover: 'The company is expected to post growth in the high twenties percent range in Q4.', visual_type: 'broll', supers: ['Q4 expected growth: ~26-29% YoY'], broll_description: 'Growth charts', duration_hint: '3s', notes: '' },
      { shot: 5, voiceover: 'Offline distribution expanded over 25%. Direct outlet coverage crossed 1 lakh outlets.', visual_type: 'broll', supers: ['Offline distribution: ↑ 25%+ YoY', 'Total outlets: 2.7 lakh', 'Direct coverage: 1 lakh'], broll_description: 'Retail store shelves', duration_hint: '4s', notes: '' },
      { shot: 6, voiceover: 'And Q4 marks the first full quarter of its BTM Ventures acquisition.', visual_type: 'presenter', supers: ["BTM Ventures: Honasa's newest acquisition", 'Q4 = First full quarter ✅'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 7, voiceover: 'The market seems to be pricing in a strong quarter — before the numbers are even out.', visual_type: 'broll', supers: [], broll_description: 'Stock market trading screens', duration_hint: '3s', notes: '' },
      { shot: 8, voiceover: 'Stay in the loop with Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 6, title: 'Govt LPG / Energy Policy changes', category: 'macro', source: 'Angel One',
    script: `The government raised bulk LPG allocation to 70% for pharma, food, agriculture and other key sectors — capped at 200 tonnes per day. Fertiliser plants got a 5% boost in natural gas supply. And Coal India cut coal e-auction reserve prices by 20%. This could help stabilize food prices, keep essential goods affordable, and reduce pressure on household expenses. The West Asia conflict is squeezing energy supply whereas the government is trying to cushion the impact.`,
    visuals: [
      { shot: 1, voiceover: 'The government raised bulk LPG allocation to 70% for pharma, food, agriculture and other key sectors — capped at 200 tonnes per day.', visual_type: 'broll', supers: ['Bulk LPG allocation: ↑ 70%', 'Cap: 200 tonnes/day', 'Pharma, food, agriculture'], broll_description: 'LPG cylinders / industrial plant', duration_hint: '5s', notes: '' },
      { shot: 2, voiceover: 'Fertiliser plants got a 5% boost in natural gas supply.', visual_type: 'presenter', supers: ['Natural gas supply ↑ 5%', 'For fertiliser plants'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 3, voiceover: 'And Coal India cut coal e-auction reserve prices by 20%.', visual_type: 'broll', supers: ['Coal India', 'E-auction reserve price ↓ 20%'], broll_description: 'Coal mining / Coal India operations', duration_hint: '3s', notes: '' },
      { shot: 4, voiceover: 'This could help stabilize food prices, keep essential goods affordable, and reduce pressure on household expenses.', visual_type: 'broll', supers: ['✅ Stable food prices', '✅ Affordable essentials', '✅ Lower household pressure'], broll_description: 'Grocery shopping / household items', duration_hint: '5s', notes: '' },
      { shot: 5, voiceover: 'The West Asia conflict is squeezing energy supply whereas the government is trying to cushion the impact.', visual_type: 'presenter', supers: ['West Asia conflict → energy squeeze', 'Govt cushioning impact'], broll_description: null, duration_hint: '4s', notes: '' },
      { shot: 6, voiceover: 'Subscribe to Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 7, title: 'TCS Q4 Results', category: 'earnings', source: 'Angel One',
    script: `TCS just reported its Q4 numbers — and they beat expectations. Revenue came in at ₹70,698 crore — up ~5% quarter-on-quarter. Net profit hit ₹13,718 crore — beating estimates. Total Contract Value came in at $8.5 billion — the second highest ever — including three large deal wins. TCS declared a final dividend of ₹31 per share. The stock was already up modestly ahead of the results, ended at +1.20% at ₹2590. Stay in the loop with Angel One Bytes for more updates.`,
    visuals: [
      { shot: 1, voiceover: 'TCS just reported its Q4 numbers — and they beat expectations.', visual_type: 'presenter', supers: ['TCS Q4 FY26 Results:', '✅ Beat expectations'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 2, voiceover: 'Revenue came in at ₹70,698 crore — up ~5% quarter-on-quarter.', visual_type: 'broll', supers: ['Revenue: ₹70,698 crore', '↑ ~5% QoQ'], broll_description: 'TCS office / IT campus footage', duration_hint: '4s', notes: 'Persistent widget ON' },
      { shot: 3, voiceover: 'Net profit hit ₹13,718 crore — beating estimates.', visual_type: 'broll', supers: ['Net profit: ₹13,718 crore', '✅ Beat estimates'], broll_description: 'Data center / server room', duration_hint: '3s', notes: 'Widget continues' },
      { shot: 4, voiceover: 'Total Contract Value came in at $8.5 billion — the second highest ever — including three large deal wins.', visual_type: 'broll', supers: ['TCV: $8.5 billion', '2nd highest ever', '🤝 3 large deal wins'], broll_description: 'Business handshake / deal signing', duration_hint: '5s', notes: 'Widget continues' },
      { shot: 5, voiceover: 'TCS declared a final dividend of ₹31 per share.', visual_type: 'broll', supers: ['Final dividend: ₹31/share', 'FY26 total: ₹110/share'], broll_description: 'Dividend / money visual', duration_hint: '3s', notes: 'Widget OFF' },
      { shot: 6, voiceover: 'The stock was already up modestly ahead of the results, ended at +1.20% at ₹2,590.', visual_type: 'presenter_stockcard', supers: ['TCS', '+1.20%', '₹2,590'], broll_description: null, duration_hint: '3s', notes: 'Google Finance stock card' },
      { shot: 7, voiceover: 'Stay in the loop with Angel One Bytes for more updates.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
  {
    id: 8, title: 'Tata Power x Databricks AI', category: 'tech', source: 'Business Standard',
    script: `Tata Power announced the enterprise-wide adoption of Databricks AI. However, the stock ended flat at ₹394.85, down -0.02% from its open price. The AI platform will enable smarter grid management, improved renewable forecasting, and more efficient billing across Tata Power's 16 GW portfolio. Is Tata Power setting a new tech benchmark? Stay in the loop with Angel One Bytes to find out.`,
    visuals: [
      { shot: 1, voiceover: 'Tata Power announced the enterprise-wide adoption of Databricks AI.', visual_type: 'presenter', supers: ['TATA POWER 🤖', 'Adopts Databricks AI', 'Enterprise-wide'], broll_description: null, duration_hint: '3s', notes: '' },
      { shot: 2, voiceover: 'However, the stock ended flat at ₹394.85, down -0.02% from its open price.', visual_type: 'presenter_stockcard', supers: ['TATA POWER', '₹394.85', '-0.02%'], broll_description: null, duration_hint: '3s', notes: 'Google Finance stock card' },
      { shot: 3, voiceover: "The AI platform will enable smarter grid management, improved renewable forecasting, and more efficient billing across Tata Power's 16 GW portfolio.", visual_type: 'broll', supers: ['✅ Smarter grid management', '✅ Better renewable forecasting', '✅ Efficient billing', '✅ Portfolio: 16 GW'], broll_description: 'Power grid / solar farm / smart meters', duration_hint: '6s', notes: '' },
      { shot: 4, voiceover: 'Is Tata Power setting a new tech benchmark?', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'Forward-looking question' },
      { shot: 5, voiceover: 'Stay in the loop with Angel One Bytes to find out.', visual_type: 'presenter', supers: [], broll_description: null, duration_hint: '2s', notes: 'CTA' },
    ],
  },
];

// ── Visual type metadata ──
const VISUAL_TYPES = {
  presenter: { icon: '🎙️', label: 'Presenter' },
  broll: { icon: '🎬', label: 'B-Roll' },
  presenter_stockcard: { icon: '📊', label: 'Stock Card' },
};

// ── Cost tracker ──
// Sonnet: $3/M input, $15/M output
const COST_PER_INPUT_TOKEN = 3 / 1_000_000;
const COST_PER_OUTPUT_TOKEN = 15 / 1_000_000;
let sessionCost = { inputTokens: 0, outputTokens: 0, calls: 0 };

function estimateTokens(text) {
  return Math.ceil(text.length / 3.5);
}

function addCost(inputText, outputText) {
  const inTok = estimateTokens(inputText);
  const outTok = estimateTokens(outputText);
  sessionCost.inputTokens += inTok;
  sessionCost.outputTokens += outTok;
  sessionCost.calls += 1;
  updateCostDisplay();
}

function updateCostDisplay() {
  const el = document.getElementById('cost-counter');
  if (!el) return;
  const totalCost = (sessionCost.inputTokens * COST_PER_INPUT_TOKEN) + (sessionCost.outputTokens * COST_PER_OUTPUT_TOKEN);
  el.innerHTML = `
    <span class="cost-label">Session</span>
    <span class="cost-value">$${totalCost.toFixed(4)}</span>
    <span class="cost-detail">${sessionCost.calls} call${sessionCost.calls !== 1 ? 's' : ''} · ~${(sessionCost.inputTokens + sessionCost.outputTokens).toLocaleString()} tok</span>
  `;
  el.style.display = 'flex';
}

// ── Tab switching ──
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab).classList.add('active');
    });
  });
}

// ── Render pattern flow diagram ──
function renderPatternFlow(pattern) {
  return pattern.map(p => {
    return `<div class="pattern-block ${p.type}">
      <span>${p.label}</span>
      ${p.sub ? `<span class="block-label">${p.sub}</span>` : ''}
    </div>`;
  }).join('');
}

// ── Render visual strip — delegates to frames.js renderFrameStrip ──
function renderVisualStrip(visuals) {
  return renderFrameStrip(visuals);
}

// ── Tab 1: Render structures ──
function renderTab1() {
  const container = document.getElementById('tab1-content');
  let html = '';
  for (const [key, cat] of Object.entries(CATEGORIES)) {
    const sampleNews = NEWS_DATA.find(n => n.category === key);
    html += `<div class="structure-card">
      <h3><span class="cat-badge ${cat.cssClass}">${cat.name}</span></h3>
      <div class="core-format">${cat.coreFormat}</div>
      <p style="font-size:0.84rem;color:var(--t2);margin-bottom:14px;">${cat.description}</p>
      <div style="font-size:0.75rem;font-weight:500;color:var(--t3);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Visual Pattern</div>
      <div class="pattern-flow">${renderPatternFlow(cat.pattern)}</div>
      ${sampleNews ? `
        <button class="sample-toggle" onclick="this.nextElementSibling.classList.toggle('open'); this.textContent = this.nextElementSibling.classList.contains('open') ? '▾ Hide sample' : '▸ Show sample: ${sampleNews.title}'">▸ Show sample: ${sampleNews.title}</button>
        <div class="sample-content">
          <div style="margin-bottom:12px;font-size:0.82rem;line-height:1.6;">${sampleNews.script}</div>
          <div style="font-size:0.75rem;font-weight:500;color:var(--t3);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Shot-by-Shot Breakdown</div>
          ${renderVisualStrip(sampleNews.visuals)}
        </div>` : ''}
    </div>`;
  }
  container.innerHTML = html;
}

// ── Tab 4: Render all 8 news visuals ──
function renderTab4() {
  const container = document.getElementById('tab4-content');
  let html = '';
  NEWS_DATA.forEach(news => {
    const cat = CATEGORIES[news.category];
    html += `<div class="news-item" id="news-${news.id}">
      <div class="news-item-header" onclick="this.parentElement.classList.toggle('open')">
        <span class="cat-badge ${cat.cssClass}">${cat.name}</span>
        <h4>${news.title}</h4>
        <span style="font-size:0.75rem;color:var(--t3);">${news.source}</span>
        <span class="chevron">▸</span>
      </div>
      <div class="news-item-body">
        <div class="news-script">${news.script}</div>
        ${renderVisualStrip(news.visuals)}
      </div>
    </div>`;
  });
  container.innerHTML = html;
}

// ── Tab 2: Structure script via LLM ──
function structureScript() {
  const script = document.getElementById('input-script').value.trim();
  const category = document.getElementById('input-category').value;
  if (!script) return alert('Please paste a script first.');
  if (!category) return alert('Please select a category.');

  const btn = document.getElementById('btn-structure');
  const output = document.getElementById('output-structured');
  btn.classList.add('loading');
  btn.disabled = true;
  output.textContent = '';

  const formData = new FormData();
  formData.append('script', script);
  formData.append('category', category);

  const inputForCost = script;

  fetch('/api/bytes/structure', { method: 'POST', body: formData })
    .then(response => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            btn.classList.remove('loading');
            btn.disabled = false;
            addCost(inputForCost, output.textContent);
            return;
          }
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop();
          lines.forEach(line => {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.text) output.textContent += data.text;
                if (data.done) {
                  btn.classList.remove('loading');
                  btn.disabled = false;
                  addCost(inputForCost, data.full_text || output.textContent);
                }
              } catch (e) {}
            }
          });
          read();
        });
      }
      read();
    })
    .catch(err => {
      output.textContent = 'Error: ' + err.message;
      btn.classList.remove('loading');
      btn.disabled = false;
    });
}

// ── Tab 3: Generate visuals via LLM ──
function generateVisuals() {
  const script = document.getElementById('visual-script').value.trim();
  const category = document.getElementById('visual-category').value;
  if (!script) return alert('Please paste a script first.');
  if (!category) return alert('Please select a category.');

  const btn = document.getElementById('btn-visuals');
  const output = document.getElementById('output-visuals');
  const rawOutput = document.getElementById('output-visuals-raw');
  btn.classList.add('loading');
  btn.disabled = true;
  output.innerHTML = '<p style="color:var(--t3);font-style:italic;">Generating visual breakdown...</p>';
  rawOutput.textContent = '';

  const formData = new FormData();
  formData.append('script', script);
  formData.append('category', category);

  let fullText = '';
  const inputForCost = script;

  fetch('/api/bytes/visuals', { method: 'POST', body: formData })
    .then(response => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            btn.classList.remove('loading');
            btn.disabled = false;
            tryRenderVisuals(fullText, output);
            addCost(inputForCost, fullText);
            return;
          }
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop();
          lines.forEach(line => {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.text) {
                  fullText += data.text;
                  rawOutput.textContent = fullText;
                }
                if (data.done) {
                  fullText = data.full_text || fullText;
                  btn.classList.remove('loading');
                  btn.disabled = false;
                  tryRenderVisuals(fullText, output);
                  addCost(inputForCost, fullText);
                }
              } catch (e) {}
            }
          });
          read();
        });
      }
      read();
    })
    .catch(err => {
      output.innerHTML = '<p style="color:var(--red);">Error: ' + err.message + '</p>';
      btn.classList.remove('loading');
      btn.disabled = false;
    });
}

function tryRenderVisuals(text, container) {
  try {
    // Extract JSON array from the response (may have markdown wrapping)
    let jsonStr = text;
    const match = text.match(/\[[\s\S]*\]/);
    if (match) jsonStr = match[0];
    const visuals = JSON.parse(jsonStr);
    if (Array.isArray(visuals) && visuals.length > 0) {
      container.innerHTML = renderVisualStrip(visuals);
      lastVisualsJson = visuals;
      const exportBtn = document.getElementById('btn-export-visuals');
      if (exportBtn) exportBtn.style.display = 'inline-block';
    } else {
      container.innerHTML = '<p style="color:var(--t3);">Could not parse visual data. Check raw output below.</p>';
    }
  } catch (e) {
    container.innerHTML = '<p style="color:var(--t3);">Could not parse JSON. Check raw output below.</p>';
  }
}

// ── Export visuals as DOCX ──
let lastVisualsJson = null; // stored after successful generation

function exportVisuals() {
  if (!lastVisualsJson) return alert('Generate visuals first.');

  const script = document.getElementById('visual-script').value.trim();
  const formData = new FormData();
  formData.append('visuals', JSON.stringify(lastVisualsJson));
  formData.append('script', script);
  formData.append('title', 'A1 Bytes — Visual Storyboard');

  fetch('/api/bytes/export', { method: 'POST', body: formData })
    .then(resp => {
      if (!resp.ok) throw new Error('Export failed');
      return resp.blob();
    })
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'A1 Bytes — Visual Storyboard.pdf';
      a.click();
      URL.revokeObjectURL(url);
    })
    .catch(err => alert('Export error: ' + err.message));
}

// ── Utility: Copy text ──
function copyOutput(elementId) {
  const el = document.getElementById(elementId);
  navigator.clipboard.writeText(el.textContent).then(() => {
    const btn = el.parentElement.querySelector('.btn-copy');
    if (btn) { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1500); }
  });
}

// ── Utility: Use structured output in Tab 3 ──
function useInTab3() {
  const text = document.getElementById('output-structured').textContent;
  if (!text) return;
  document.getElementById('visual-script').value = text;
  const cat = document.getElementById('input-category').value;
  if (cat) document.getElementById('visual-category').value = cat;
  // Switch to Tab 3
  document.querySelector('[data-tab="tab3"]').click();
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  renderTab1();
  renderTab4();
});
