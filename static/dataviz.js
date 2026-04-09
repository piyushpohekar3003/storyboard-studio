/* ========================================
   DATA VISUALIZATION RENDERER
   ======================================== */

const COLORS = {
    cyan: '#00e5ff',
    gold: '#ffd700',
    purple: '#b388ff',
    mint: '#00e5a0',
    red: '#ff4466',
    blue: '#4488ff',
    orange: '#ff8844',
};

const COLOR_CYCLE = ['cyan', 'gold', 'purple', 'mint', 'red', 'blue', 'orange'];

// --- Preset Templates ---
const PRESETS = {
    stats: {
        type: "stats",
        cards: [
            { label: "Revenue Growth", value: "10%", sub: "Compounded", color: "cyan" },
            { label: "Profit Growth", value: "8%", sub: "Compounded", color: "gold" },
            { label: "ROCE", value: "22%", sub: "5-Year Avg", color: "purple" }
        ]
    },
    comparison: {
        type: "comparison",
        left: { period: "FY25", value: "1.55L", label: "Scooters Sold", color: "cyan" },
        right: { period: "9M FY26", value: "1.79L", label: "Scooters Sold", color: "purple" },
        result: { value: "50%", label: "Jump", color: "mint" }
    },
    bars: {
        type: "bars",
        title: "Revenue Breakdown",
        bars: [
            { label: "Q1", value: "2,400 Cr", height: 55, color: "cyan" },
            { label: "Q2", value: "3,100 Cr", height: 70, color: "cyan" },
            { label: "Q3", value: "2,800 Cr", height: 63, color: "gold" },
            { label: "Q4", value: "3,900 Cr", height: 88, color: "mint" }
        ]
    },
    callouts: {
        type: "callouts",
        items: [
            { title: "Production Cost", text: "~4,000 per tonne", color: "purple" },
            { title: "Renewable Power", text: "Helps lower long-term energy costs", color: "cyan" },
            { title: "Premium Cement", text: "35% of Trade Sales - Better Margins", color: "gold" },
            { title: "No Net Debt", text: "Strong balance sheet position", color: "mint" }
        ]
    },
    title: {
        type: "title",
        super: "PPFAS",
        main: "STOCK #1",
        sub: "TCS",
        color: "purple"
    },
    flowchart: {
        type: "flowchart",
        center: { label: "Managed by", value: "Rajeev Thakkar", color: "gold" },
        left: { label: "India's Largest", value: "1.34 Lakh Cr.", color: "cyan" },
        right: [
            { text: "Generate Strong Cash", color: "cyan" },
            { text: "Use Money Wisely", color: "gold" },
            { text: "Reasonably Priced", color: "purple" },
            { text: "Hold for Long Term", color: "mint" }
        ]
    },
    table: {
        type: "table",
        title: "Fund Performance",
        columns: ["Fund Name", "1Y Return", "3Y Return", "AUM"],
        rows: [
            ["PPFAS Flexi Cap", { text: "18.5%", color: "mint" }, { text: "22.1%", color: "mint" }, "62,400 Cr"],
            ["HDFC Mid Cap", { text: "24.3%", color: "cyan" }, { text: "28.7%", color: "cyan" }, "48,200 Cr"],
            ["Nippon Small Cap", { text: "31.2%", color: "gold" }, { text: "35.4%", color: "gold" }, "35,600 Cr"]
        ]
    },
    donut: {
        type: "donut",
        title: "Portfolio Allocation",
        centerLabel: "Total",
        centerValue: "100%",
        segments: [
            { label: "Large Cap", value: 45, color: "cyan" },
            { label: "Mid Cap", value: 25, color: "gold" },
            { label: "Small Cap", value: 15, color: "purple" },
            { label: "Debt", value: 10, color: "mint" },
            { label: "Cash", value: 5, color: "red" }
        ]
    },
    hbar: {
        type: "hbar",
        title: "Market Share",
        bars: [
            { label: "Ather", value: "18.8%", percent: 18.8, color: "cyan" },
            { label: "Ola", value: "25.1%", percent: 25.1, color: "purple" },
            { label: "TVS", value: "22.4%", percent: 22.4, color: "gold" },
            { label: "Bajaj", value: "15.2%", percent: 15.2, color: "mint" },
            { label: "Others", value: "18.5%", percent: 18.5, color: "red" }
        ]
    }
};


// --- Render Functions ---

function renderStats(data) {
    let html = '<div class="viz-stat-cards">';
    for (const card of data.cards) {
        const c = card.color || 'cyan';
        html += `
        <div class="stat-card color-${c}">
            <div class="stat-label">${esc(card.label)}</div>
            <div class="stat-value">${esc(card.value)}</div>
            ${card.sub ? `<div class="stat-sub">${esc(card.sub)}</div>` : ''}
        </div>`;
    }
    html += '</div>';
    return html;
}

function renderBars(data) {
    const maxH = 350;
    let html = `<div class="viz-bar-chart">`;
    if (data.title) html += `<div class="bar-chart-title">${esc(data.title)}</div>`;
    html += `<div class="bar-chart-body">`;
    for (const bar of data.bars) {
        const c = bar.color || 'cyan';
        const h = Math.max(20, (bar.height / 100) * maxH);
        html += `
        <div class="bar-group">
            <div class="bar-value" style="color: ${COLORS[c] || COLORS.cyan}">${esc(bar.value)}</div>
            <div class="bar-rect color-${c}" style="height: ${h}px"></div>
            <div class="bar-label">${esc(bar.label)}</div>
        </div>`;
    }
    html += '</div></div>';
    return html;
}

function renderComparison(data) {
    const lc = data.left.color || 'cyan';
    const rc = data.right.color || 'purple';
    let html = `<div class="viz-comparison">`;
    html += `
    <div class="comparison-card color-${lc}" style="border-color: ${COLORS[lc]}40;">
        <div class="comp-period">${esc(data.left.period)}</div>
        <div class="comp-value" style="color: ${COLORS[lc]}; text-shadow: 0 0 20px ${COLORS[lc]}80;">${esc(data.left.value)}</div>
        <div class="comp-label">${esc(data.left.label)}</div>
    </div>`;
    html += `
    <div class="comparison-vs">
        <div class="vs-line"></div>
        <div class="vs-badge">VS</div>
        <div class="vs-line"></div>
    </div>`;
    html += `
    <div class="comparison-card color-${rc}" style="border-color: ${COLORS[rc]}40;">
        <div class="comp-period">${esc(data.right.period)}</div>
        <div class="comp-value" style="color: ${COLORS[rc]}; text-shadow: 0 0 20px ${COLORS[rc]}80;">${esc(data.right.value)}</div>
        <div class="comp-label">${esc(data.right.label)}</div>
    </div>`;
    if (data.result) {
        const resc = data.result.color || 'mint';
        html += `
        <div class="comparison-result color-${resc}" style="border-color: ${COLORS[resc]}40;">
            <div class="result-value" style="color: ${COLORS[resc]}; text-shadow: 0 0 20px ${COLORS[resc]}80;">${esc(data.result.value)}</div>
            <div class="result-label">${esc(data.result.label)}</div>
        </div>`;
    }
    html += '</div>';
    return html;
}

function renderCallouts(data) {
    let html = '<div class="viz-callouts">';
    for (const item of data.items) {
        const c = item.color || 'cyan';
        html += `
        <div class="callout-card color-${c}">
            <div class="callout-title">${esc(item.title)}</div>
            <div class="callout-text">${esc(item.text)}</div>
        </div>`;
    }
    html += '</div>';
    return html;
}

function renderTitle(data) {
    const c = data.color || 'purple';
    let html = `<div class="viz-title color-${c}">`;
    if (data.super) html += `<div class="title-super">${esc(data.super)}</div>`;
    html += `<div class="title-main">${esc(data.main)}</div>`;
    if (data.sub) html += `<div class="title-sub" style="color: ${COLORS[c]}">${esc(data.sub)}</div>`;
    html += '</div>';
    return html;
}

function renderFlowchart(data) {
    const cc = data.center.color || 'gold';
    let html = `<div class="viz-flowchart">`;

    // Left node
    if (data.left) {
        const lc = data.left.color || 'cyan';
        html += `
        <div class="flow-center" style="border-color: ${COLORS[lc]}60; margin-right: 0;">
            <div class="flow-center-label">${esc(data.left.label)}</div>
            <div class="flow-center-value" style="color: ${COLORS[lc]}; text-shadow: 0 0 15px ${COLORS[lc]}60;">${esc(data.left.value)}</div>
        </div>
        <div class="flow-line" style="width: 40px;"></div>`;
    }

    // Center
    html += `
    <div class="flow-center" style="border-color: ${COLORS[cc]}60;">
        <div class="flow-center-label">${esc(data.center.label)}</div>
        <div class="flow-center-value" style="color: ${COLORS[cc]}; text-shadow: 0 0 15px ${COLORS[cc]}60;">${esc(data.center.value)}</div>
    </div>`;

    // Right branches
    if (data.right && data.right.length) {
        html += `<div style="display: flex; align-items: center;"><div class="flow-line" style="width: 30px;"></div><div class="flow-branches">`;
        for (const node of data.right) {
            const nc = node.color || 'cyan';
            html += `
            <div class="flow-connector">
                <div class="flow-line"></div>
                <div class="flow-node color-${nc}">${esc(node.text)}</div>
            </div>`;
        }
        html += '</div></div>';
    }

    html += '</div>';
    return html;
}

function renderTable(data) {
    let html = `<div class="viz-table">`;
    if (data.title) html += `<div class="table-title">${esc(data.title)}</div>`;
    html += `<table class="neon-table"><thead><tr>`;
    for (const col of data.columns) {
        html += `<th>${esc(col)}</th>`;
    }
    html += `</tr></thead><tbody>`;
    for (const row of data.rows) {
        html += '<tr>';
        for (const cell of row) {
            if (typeof cell === 'object' && cell.text) {
                const c = cell.color || 'cyan';
                html += `<td class="highlight ${c}">${esc(cell.text)}</td>`;
            } else {
                html += `<td>${esc(String(cell))}</td>`;
            }
        }
        html += '</tr>';
    }
    html += '</tbody></table></div>';
    return html;
}

function renderDonut(data) {
    const total = data.segments.reduce((s, seg) => s + seg.value, 0);
    const radius = 100;
    const circumference = 2 * Math.PI * radius;
    let offset = 0;

    let svgPaths = '';
    for (const seg of data.segments) {
        const pct = seg.value / total;
        const dashLen = pct * circumference;
        const c = COLORS[seg.color] || COLORS.cyan;
        svgPaths += `<circle cx="130" cy="130" r="${radius}" fill="none" stroke="${c}" stroke-width="24"
            stroke-dasharray="${dashLen} ${circumference - dashLen}"
            stroke-dashoffset="${-offset}"
            style="filter: drop-shadow(0 0 6px ${c}80);"/>`;
        offset += dashLen;
    }

    let html = `<div class="viz-donut">`;
    html += `<div class="donut-chart">
        <svg viewBox="0 0 260 260">${svgPaths}</svg>
        <div class="donut-center-text">
            <div class="donut-center-value">${esc(data.centerValue || '')}</div>
            <div class="donut-center-label">${esc(data.centerLabel || '')}</div>
        </div>
    </div>`;

    html += `<div class="donut-legend">`;
    for (const seg of data.segments) {
        const c = seg.color || 'cyan';
        html += `
        <div class="donut-legend-item">
            <div class="donut-legend-dot" style="background: ${COLORS[c]}; box-shadow: 0 0 8px ${COLORS[c]}60;"></div>
            <span class="donut-legend-label">${esc(seg.label)}</span>
            <span class="donut-legend-value" style="color: ${COLORS[c]}">${seg.value}%</span>
        </div>`;
    }
    html += '</div></div>';
    return html;
}

function renderHbar(data) {
    const maxPct = Math.max(...data.bars.map(b => b.percent));
    let html = `<div class="viz-hbar">`;
    if (data.title) html += `<div class="hbar-title">${esc(data.title)}</div>`;
    for (const bar of data.bars) {
        const c = bar.color || 'cyan';
        const w = (bar.percent / maxPct) * 100;
        html += `
        <div class="hbar-row">
            <div class="hbar-label">${esc(bar.label)}</div>
            <div class="hbar-track">
                <div class="hbar-fill color-${c}" style="width: ${w}%">
                    <span class="hbar-val">${esc(bar.value)}</span>
                </div>
            </div>
        </div>`;
    }
    html += '</div>';
    return html;
}


// --- Main Render Dispatcher ---

function renderVisualization(data) {
    const container = document.getElementById('frame-content');
    try {
        let html = '';
        switch (data.type) {
            case 'stats': html = renderStats(data); break;
            case 'bars': html = renderBars(data); break;
            case 'comparison': html = renderComparison(data); break;
            case 'callouts': html = renderCallouts(data); break;
            case 'title': html = renderTitle(data); break;
            case 'flowchart': html = renderFlowchart(data); break;
            case 'table': html = renderTable(data); break;
            case 'donut': html = renderDonut(data); break;
            case 'hbar': html = renderHbar(data); break;
            default:
                html = `<div class="viz-error"><div class="error-icon">?</div><div class="error-msg">Unknown type "${esc(data.type)}". Use: stats, bars, comparison, callouts, title, flowchart, table, donut, hbar</div></div>`;
        }
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div class="viz-error"><div class="error-icon">!</div><div class="error-msg">${esc(e.message)}</div></div>`;
    }
}

function esc(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('data-input');
    const renderBtn = document.getElementById('render-btn');
    const clearBtn = document.getElementById('clear-btn');
    const presetBtns = document.querySelectorAll('.preset-btn');

    // Load preset
    presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.dataset.preset;
            if (PRESETS[key]) {
                presetBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                input.value = JSON.stringify(PRESETS[key], null, 2);
                doRender();
            }
        });
    });

    // Render
    renderBtn.addEventListener('click', doRender);

    // Clear
    clearBtn.addEventListener('click', () => {
        input.value = '';
        presetBtns.forEach(b => b.classList.remove('active'));
        document.getElementById('frame-content').innerHTML = `
            <div class="frame-placeholder">
                <div class="icon">&#9672;</div>
                <p>Enter JSON data and click Render</p>
            </div>`;
    });

    // Ctrl+Enter to render
    input.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            doRender();
        }
    });

    // Export as PNG
    document.getElementById('export-png')?.addEventListener('click', exportPNG);

    function doRender() {
        try {
            const data = JSON.parse(input.value);
            renderVisualization(data);
        } catch (e) {
            document.getElementById('frame-content').innerHTML = `
                <div class="viz-error">
                    <div class="error-icon">!</div>
                    <div class="error-msg">Invalid JSON: ${esc(e.message)}</div>
                </div>`;
        }
    }

    // Start with stats preset
    input.value = JSON.stringify(PRESETS.stats, null, 2);
    doRender();
});


// --- Export to PNG ---
async function exportPNG() {
    const frame = document.getElementById('viz-frame');
    try {
        // Use html2canvas
        if (typeof html2canvas === 'undefined') {
            alert('Loading export library...');
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
            script.onload = () => doExport(frame);
            document.head.appendChild(script);
        } else {
            doExport(frame);
        }
    } catch(e) {
        alert('Export failed: ' + e.message);
    }
}

async function doExport(frame) {
    const canvas = await html2canvas(frame, {
        backgroundColor: '#0a0a0f',
        scale: 2,
        useCORS: true,
    });
    const link = document.createElement('a');
    link.download = 'dataviz-export.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}
