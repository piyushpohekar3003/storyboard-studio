/* ===== Shorts Visual Storyboard ===== */

// ── Cost tracker ──
// Sonnet: $3/M input, $15/M output
const COST_PER_INPUT_TOKEN = 3 / 1_000_000;
const COST_PER_OUTPUT_TOKEN = 15 / 1_000_000;
let sessionCost = { inputTokens: 0, outputTokens: 0, calls: 0 };

function estimateTokens(text) {
  return Math.ceil((text || '').length / 3.5);
}

function addCost(inputText, outputText) {
  sessionCost.inputTokens += estimateTokens(inputText);
  sessionCost.outputTokens += estimateTokens(outputText);
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
}

// Show counter on page load
document.addEventListener('DOMContentLoaded', () => { updateCostDisplay(); });

// ── State management ──
let currentState = 'input'; // 'input' | 'loading' | 'preview'
let currentScript = '';
let currentImages = []; // [{media_type, data, description}]
let currentStoryboardJson = null;
let projectDir = '';
let versionHistory = []; // last 3 versions for undo

// ── DOM refs ──
const $ = id => document.getElementById(id);

// ── Input method switching ──
function switchInputMethod(method) {
  document.querySelectorAll('.input-method-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.input-method-panel').forEach(p => p.classList.remove('active'));
  document.querySelector(`.input-method-tab[data-method="${method}"]`).classList.add('active');
  $(`method-${method}`).classList.add('active');
}

// ── File upload handling ──
async function handleFileUpload(file) {
  if (!file) return;
  const formData = new FormData();
  formData.append('file', file);

  $('file-name').textContent = `Uploading: ${file.name}...`;
  $('file-name').style.display = 'block';

  try {
    const resp = await fetch('/api/shorts/upload', { method: 'POST', body: formData });
    if (!resp.ok) throw new Error(`Upload failed: ${resp.status}`);
    const data = await resp.json();

    // Populate script textarea
    currentScript = data.text || '';
    $('script-textarea').value = currentScript;
    switchInputMethod('paste');

    // Populate images
    if (data.images && data.images.length > 0) {
      currentImages = data.images;
      renderImageThumbnails(currentImages);
    }

    $('file-name').textContent = `Loaded: ${file.name}`;
  } catch (err) {
    console.error('Upload error:', err);
    $('file-name').textContent = `Error: ${err.message}`;
    $('file-name').style.color = 'var(--red)';
  }
}

async function handleGDocFetch() {
  const url = $('gdoc-url').value.trim();
  if (!url) return;

  const btn = $('btn-fetch-gdoc');
  btn.classList.add('loading');
  btn.disabled = true;

  try {
    const resp = await fetch('/api/shorts/fetch-gdoc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    if (!resp.ok) throw new Error(`Fetch failed: ${resp.status}`);
    const data = await resp.json();

    currentScript = data.text || '';
    $('script-textarea').value = currentScript;
    switchInputMethod('paste');

    if (data.images && data.images.length > 0) {
      currentImages = data.images;
      renderImageThumbnails(currentImages);
    }
  } catch (err) {
    console.error('GDoc fetch error:', err);
    alert('Failed to fetch Google Doc: ' + err.message);
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

// ── Image thumbnail rendering ──
function renderImageThumbnails(images) {
  const section = $('images-section');
  const grid = $('thumb-grid');
  const countEl = $('image-count');

  if (!images || images.length === 0) {
    section.style.display = 'none';
    return;
  }

  section.style.display = '';
  countEl.textContent = `${images.length} image${images.length !== 1 ? 's' : ''}`;

  grid.innerHTML = images.map((img, i) => `
    <div class="thumb-item" data-index="${i}">
      <img src="data:${img.media_type};base64,${img.data}" alt="Image ${i + 1}">
      <span class="thumb-num">${i + 1}</span>
      <button class="thumb-remove" onclick="removeImage(${i})" title="Remove">&times;</button>
    </div>
  `).join('');
}

function removeImage(index) {
  currentImages.splice(index, 1);
  renderImageThumbnails(currentImages);
}

function addImage(file) {
  const reader = new FileReader();
  reader.onload = () => {
    const base64 = reader.result.split(',')[1];
    const mediaType = file.type || 'image/png';
    currentImages.push({ media_type: mediaType, data: base64, description: file.name });
    renderImageThumbnails(currentImages);
  };
  reader.readAsDataURL(file);
}

// ── Generation ──
async function generateStoryboard() {
  currentScript = $('script-textarea').value.trim();
  if (!currentScript) {
    alert('Please enter a script first.');
    return;
  }

  switchState('loading');

  const formData = new FormData();
  formData.append('script', currentScript);
  formData.append('project_dir', projectDir);
  formData.append('images', JSON.stringify(currentImages));

  try {
    let text = '';
    await streamSSE('/api/shorts/generate', formData,
      (chunk) => {
        text += chunk;
        const preview = $('stream-preview');
        if (preview) {
          preview.textContent = text.slice(-800);
          preview.scrollTop = preview.scrollHeight;
        }
      },
      (fullText) => {
        // fullText is the clean accumulated LLM output (JSON string)
        console.log('LLM output length:', fullText.length);
        try {
          // Strip markdown code fences if present
          let jsonStr = fullText.trim();
          if (jsonStr.startsWith('```')) {
            jsonStr = jsonStr.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '');
          }
          currentStoryboardJson = JSON.parse(jsonStr);
          currentStoryboardJson._project_dir = projectDir;
          addCost(currentScript, fullText);
          renderStoryboard();
        } catch (parseErr) {
          console.error('JSON parse error:', parseErr);
          console.log('Raw text:', fullText.slice(0, 500));
          // Try to find JSON object in the text
          const jsonMatch = fullText.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              currentStoryboardJson = JSON.parse(jsonMatch[0]);
              currentStoryboardJson._project_dir = projectDir;
              addCost(currentScript, fullText);
              renderStoryboard();
            } catch (e2) {
              alert('Failed to parse storyboard JSON. Check console.');
              switchState('input');
            }
          } else {
            alert('No valid JSON found in response. Check console.');
            switchState('input');
          }
        }
      }
    );
  } catch (err) {
    console.error('Generate error:', err);
    alert('Generation failed: ' + err.message);
    switchState('input');
  }
}

// ── SSE streaming helper ──
async function streamSSE(url, formData, onChunk, onDone) {
  const response = await fetch(url, { method: 'POST', body: formData });
  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let accumulatedText = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    // Parse SSE events from buffer
    const lines = buffer.split('\n');
    buffer = lines.pop() || ''; // keep incomplete line in buffer

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.text) {
            accumulatedText += data.text;
            onChunk(data.text);
          }
          if (data.done) {
            // Server signals completion — use full_text if provided
            if (data.full_text) {
              accumulatedText = data.full_text;
            }
          }
        } catch (e) {
          // Not valid JSON, skip
        }
      }
    }
  }

  onDone(accumulatedText);
}

// ── Rendering ──
async function renderStoryboard() {
  if (!currentStoryboardJson) return;

  $('loading-sub').textContent = 'Rendering SVG frames...';

  try {
    const resp = await fetch('/api/shorts/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({}, currentStoryboardJson, { _project_dir: projectDir })),
    });

    if (!resp.ok) throw new Error(`Render failed: ${resp.status}`);
    const data = await resp.json();

    const svgPaths = data.svg_paths || [];
    const htmlPath = data.html_path || '';

    // Update project dir from render response
    if (data.project_dir) projectDir = data.project_dir;

    // Store html path for download
    currentStoryboardJson._html_path = htmlPath;
    currentStoryboardJson._svg_paths = svgPaths;

    const html = buildPreviewHTML(currentStoryboardJson, svgPaths);
    $('storyboard-view').innerHTML = html;
    switchState('preview');
  } catch (err) {
    console.error('Render error:', err);
    // Fall back: show preview without SVGs
    const html = buildPreviewHTML(currentStoryboardJson, []);
    $('storyboard-view').innerHTML = html;
    switchState('preview');
  }
}

// ── Build preview HTML ──
function buildPreviewHTML(json, svgPaths) {
  const meta = json.metadata || {};
  const title = meta.title || json.title || 'Untitled Storyboard';
  const sections = json.sections || [];

  let html = '';

  // Header
  html += `
    <div class="sb-header">
      <h2>${escapeHtml(title)}</h2>
      <p>AV Storyboard — Short-form Vertical Video</p>
      <div class="sb-meta">
        <span class="sb-tag">Format: Short (9:16)</span>
        ${json.language ? `<span class="sb-tag">Language: ${escapeHtml(json.language)}</span>` : ''}
        <span class="sb-tag">Frames: ${getFrameCount(json)}</span>
      </div>
    </div>
  `;

  // If sections-based structure
  if (sections.length > 0 && sections[0].frames) {
    sections.forEach(section => {
      const sectionName = section.section_label || section.name || section.label || '';
      if (sectionName) {
        html += `<div class="sb-section-divider"><span>${escapeHtml(sectionName.toUpperCase())}</span></div>`;
      }
      (section.frames || []).forEach((frame, fi) => {
        html += buildFrameRow(frame, svgPaths);
      });
    });
  }
  // If flat frames array (fallback)
  else if (json.frames && Array.isArray(json.frames)) {
    let lastSection = '';
    json.frames.forEach(frame => {
      if (frame.section && frame.section !== lastSection) {
        html += `<div class="sb-section-divider"><span>${escapeHtml(frame.section.toUpperCase())}</span></div>`;
        lastSection = frame.section;
      }
      html += buildFrameRow(frame, svgPaths);
    });
  }

  return html;
}

function buildFrameRow(frame, svgPaths) {
  const num = frame.frame_number || frame.number || frame.shot || '??';
  const numPadded = String(num).padStart(2, '0');
  const type = frame.type || frame.visual_type || frame.frame_type || 'presenter';
  const typeClass = getTypeClass(type);

  // Find matching SVG path
  let svgTag = `<div class="svg-placeholder">Frame ${numPadded}</div>`;
  if (svgPaths && svgPaths.length > 0) {
    const svgPath = svgPaths.find(p => p.includes(`frame-${numPadded}`));
    if (svgPath) {
      svgTag = `<object data="${svgPath}" type="image/svg+xml" style="width:100%;height:100%;border:0;background:#0a0a0f;"></object>`;
    }
  }
  // Fallback: try by index
  if (svgTag.includes('svg-placeholder') && svgPaths && svgPaths.length >= num) {
    const svgPath = svgPaths[num - 1];
    if (svgPath) {
      svgTag = `<object data="${svgPath}" type="image/svg+xml" style="width:100%;height:100%;border:0;background:#0a0a0f;"></object>`;
    }
  }

  // Info sections
  let infoHtml = '';

  // Dialogue
  const dialogue = frame.dialogue || frame.voiceover || frame.script || '';
  if (dialogue) {
    infoHtml += `
      <div class="sb-info-section">
        <div class="sb-info-label dialogue">&#127908; Dialogue</div>
        <div class="sb-info-content">${escapeHtml(dialogue)}</div>
      </div>
    `;
  }

  // Visual cue
  const visualCue = frame.visual_cue || frame.visual_description || frame.visual || '';
  if (visualCue) {
    infoHtml += `
      <div class="sb-info-section">
        <div class="sb-info-label visual">&#127916; Visual Cue</div>
        <div class="sb-info-content">${escapeHtml(visualCue)}</div>
      </div>
    `;
  }

  // Supers / text overlays
  const supers = frame.supers || frame.text_overlays || [];
  if (Array.isArray(supers) && supers.length > 0) {
    infoHtml += `
      <div class="sb-info-section">
        <div class="sb-info-label visual">&#128221; Supers</div>
        <div class="sb-info-content">${supers.map(s => escapeHtml(s)).join('<br>')}</div>
      </div>
    `;
  }

  // Screenshot reference
  const screenshot = frame.screenshot || frame.screenshot_ref || '';
  if (screenshot) {
    infoHtml += `
      <div class="sb-info-section">
        <div class="sb-info-label screenshot">&#128247; Screenshot</div>
        <div class="sb-info-content">${escapeHtml(screenshot)}</div>
      </div>
    `;
  }

  // B-roll description
  const broll = frame.broll_description || frame.broll || '';
  if (broll) {
    infoHtml += `
      <div class="sb-info-section">
        <div class="sb-info-label visual">&#127910; B-Roll</div>
        <div class="sb-info-content"><em>${escapeHtml(broll)}</em></div>
      </div>
    `;
  }

  // Notes
  const notes = frame.notes || '';
  if (notes) {
    infoHtml += `
      <div class="sb-info-section">
        <div class="sb-info-label" style="color:#b388ff;">&#128172; Notes</div>
        <div class="sb-info-content" style="color:#6a6a7a;font-style:italic;">${escapeHtml(notes)}</div>
      </div>
    `;
  }

  return `
    <div class="sb-frame-row">
      <div class="sb-svg-frame">${svgTag}</div>
      <div class="sb-frame-info">
        <div class="sb-frame-num">FRAME ${numPadded}</div>
        <span class="sb-frame-type ${typeClass}">${escapeHtml(type)}</span>
        ${infoHtml}
      </div>
    </div>
  `;
}

function getTypeClass(type) {
  const t = (type || '').toLowerCase();
  if (t.includes('presenter')) return 'presenter';
  if (t.includes('data') || t.includes('card') || t.includes('stock')) return 'data';
  if (t.includes('chart') || t.includes('screen')) return 'chart';
  if (t.includes('cta') || t.includes('close')) return 'cta';
  if (t.includes('broll') || t.includes('b-roll') || t.includes('b_roll')) return 'broll';
  return 'presenter';
}

function getFrameCount(json) {
  if (json.frames && Array.isArray(json.frames)) return json.frames.length;
  if (json.sections) {
    return json.sections.reduce((sum, s) => sum + (s.frames ? s.frames.length : 0), 0);
  }
  return 0;
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}

// ── Export ──
async function exportPDF() {
  if (!currentStoryboardJson) return;
  const btn = $('btn-export-pdf');
  btn.classList.add('loading');
  btn.disabled = true;

  try {
    const resp = await fetch('/api/shorts/export-pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({}, currentStoryboardJson, { _project_dir: projectDir })),
    });

    if (!resp.ok) throw new Error(`Export failed: ${resp.status}`);

    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (currentStoryboardJson.title || 'storyboard').replace(/\s+/g, '-') + '.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error('PDF export error:', err);
    alert('PDF export failed: ' + err.message);
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

async function downloadHTML() {
  const htmlPath = currentStoryboardJson?._html_path;
  if (htmlPath) {
    window.open(htmlPath, '_blank');
  } else if (projectDir) {
    window.open(`/static/projects/${projectDir}/storyboard.html`, '_blank');
  } else {
    alert('HTML file not available yet.');
  }
}

// ── Feedback / Redo ──
async function submitFeedback() {
  const feedback = $('feedback-textarea').value.trim();
  if (!feedback) {
    alert('Please enter feedback.');
    return;
  }

  // Save current version to history (keep last 3)
  if (currentStoryboardJson) {
    versionHistory.push(JSON.parse(JSON.stringify(currentStoryboardJson)));
    if (versionHistory.length > 3) versionHistory.shift();
  }

  switchState('loading');
  $('loading-sub').textContent = 'Regenerating with feedback...';

  const formData = new FormData();
  formData.append('script', currentScript);
  formData.append('images', JSON.stringify(currentImages));
  formData.append('feedback', feedback);
  formData.append('previous_json', JSON.stringify(currentStoryboardJson));

  try {
    let text = '';
    await streamSSE('/api/shorts/redo', formData,
      (chunk) => {
        text += chunk;
        const preview = $('stream-preview');
        if (preview) {
          preview.textContent = text.slice(-800);
          preview.scrollTop = preview.scrollHeight;
        }
      },
      () => {
        try {
          let jsonStr = text;
          const dataLines = text.split('\n')
            .filter(l => l.startsWith('data: '))
            .map(l => l.slice(6));
          if (dataLines.length > 0) {
            jsonStr = dataLines.join('');
          }
          currentStoryboardJson = JSON.parse(jsonStr);
          projectDir = currentStoryboardJson.project_dir || projectDir;
          addCost(feedback + currentScript, redoText);
          $('feedback-textarea').value = '';
          renderStoryboard();
        } catch (parseErr) {
          console.error('Redo parse error:', parseErr);
          const jsonMatch = text.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              currentStoryboardJson = JSON.parse(jsonMatch[0]);
              projectDir = currentStoryboardJson.project_dir || projectDir;
              addCost(feedback + currentScript, redoText);
              $('feedback-textarea').value = '';
              renderStoryboard();
            } catch (e2) {
              alert('Failed to parse redo response.');
              switchState('preview');
            }
          } else {
            alert('Failed to parse redo response.');
            switchState('preview');
          }
        }
      }
    );
  } catch (err) {
    console.error('Redo error:', err);
    alert('Redo failed: ' + err.message);
    switchState('preview');
  }
}

// ── State switching ──
function switchState(newState) {
  currentState = newState;
  const inputPanel = $('input-panel');
  const previewPanel = $('preview-panel');
  const loadingOverlay = $('loading-overlay');
  const generateBtn = $('btn-generate');

  switch (newState) {
    case 'input':
      inputPanel.style.display = '';
      previewPanel.classList.remove('active');
      loadingOverlay.classList.remove('active');
      generateBtn.classList.remove('loading');
      generateBtn.disabled = false;
      $('stream-preview').textContent = '';
      break;

    case 'loading':
      inputPanel.style.display = '';
      previewPanel.classList.remove('active');
      loadingOverlay.classList.add('active');
      generateBtn.classList.add('loading');
      generateBtn.disabled = true;
      $('loading-sub').textContent = 'Streaming response from LLM';
      $('stream-preview').textContent = '';
      // Scroll to loading
      loadingOverlay.scrollIntoView({ behavior: 'smooth', block: 'center' });
      break;

    case 'preview':
      inputPanel.style.display = 'none';
      previewPanel.classList.add('active');
      loadingOverlay.classList.remove('active');
      generateBtn.classList.remove('loading');
      generateBtn.disabled = false;
      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
      break;
  }
}

function backToEdit() {
  switchState('input');
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  // File drop zone
  const dropZone = $('file-drop-zone');
  const fileInput = $('file-input');

  dropZone.addEventListener('click', () => fileInput.click());

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });
  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  });
  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFileUpload(fileInput.files[0]);
  });

  // Add more images zone
  const addMoreZone = $('add-more-zone');
  const addImageInput = $('add-image-input');

  addMoreZone.addEventListener('click', () => addImageInput.click());
  addImageInput.addEventListener('change', () => {
    Array.from(addImageInput.files).forEach(f => addImage(f));
    addImageInput.value = '';
  });

  // Also support drag-drop on the add-more zone
  addMoreZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    addMoreZone.style.borderColor = 'var(--blue)';
  });
  addMoreZone.addEventListener('dragleave', () => {
    addMoreZone.style.borderColor = '';
  });
  addMoreZone.addEventListener('drop', (e) => {
    e.preventDefault();
    addMoreZone.style.borderColor = '';
    Array.from(e.dataTransfer.files).forEach(f => {
      if (f.type.startsWith('image/')) addImage(f);
    });
  });

  // Global drag-drop on paste panel (for convenience)
  const inputPanel = $('input-panel');
  inputPanel.addEventListener('dragover', (e) => {
    e.preventDefault();
  });
  inputPanel.addEventListener('drop', (e) => {
    // Only handle if not already handled by specific zones
    if (e.target.closest('.drop-zone') || e.target.closest('.add-more-zone')) return;
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        addImage(file);
      } else {
        handleFileUpload(file);
      }
    }
  });
});
