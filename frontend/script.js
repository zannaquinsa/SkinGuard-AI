/* ═══════════════════════════════════════════════
   SKINGUARD AI — script.js
   Complete Frontend Logic + FastAPI Integration
   ═══════════════════════════════════════════════ */

'use strict';

const API_BASE = 'http://localhost:8000';

// ── STATE ─────────────────────────────────────
const state = {
  currentFile: null,
  currentImageBase64: null,
  lastPrediction: null,
  cameraStream: null,
  predictionHistory: [],
};

// ── INIT ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  loadCities();
  renderHistoryTable();
});

// ── NAVBAR ────────────────────────────────────
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  });

  hamburger.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('open');
    hamburger.classList.toggle('open', isOpen);
  });
}

function closeMobileMenu() {
  document.getElementById('mobileMenu').classList.remove('open');
  document.getElementById('hamburger').classList.remove('open');
}

// ── SCROLL HELPER ─────────────────────────────
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── TABS ──────────────────────────────────────
function switchTab(tab) {
  const tabUpload  = document.getElementById('tabUpload');
  const tabCamera  = document.getElementById('tabCamera');
  const panelUp    = document.getElementById('panelUpload');
  const panelCam   = document.getElementById('panelCamera');

  if (tab === 'upload') {
    tabUpload.classList.add('active');
    tabCamera.classList.remove('active');
    panelUp.classList.remove('hidden');
    panelCam.classList.add('hidden');
    stopCamera();
  } else {
    tabCamera.classList.add('active');
    tabUpload.classList.remove('active');
    panelCam.classList.remove('hidden');
    panelUp.classList.add('hidden');
  }
}

// ── DRAG & DROP ───────────────────────────────
function handleDragOver(e) {
  e.preventDefault();
  document.getElementById('dropZone').classList.add('drag-over');
}
function handleDragLeave() {
  document.getElementById('dropZone').classList.remove('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropZone').classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) processFile(file);
}
function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) processFile(file);
}

function processFile(file) {
  if (!file.type.startsWith('image/')) {
    showToast('Format file tidak didukung. Gunakan JPG, PNG, atau WEBP.', 'error');
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showToast('Ukuran file terlalu besar. Maksimal 10 MB.', 'error');
    return;
  }

  state.currentFile = file;

  const reader = new FileReader();
  reader.onload = (ev) => {
    state.currentImageBase64 = ev.target.result;
    showPreview(ev.target.result);
    enableAnalyzeButton();
  };
  reader.readAsDataURL(file);
}

function showPreview(src) {
  const container = document.getElementById('previewContainer');
  const img = document.getElementById('previewImage');
  img.src = src;
  container.classList.remove('hidden');
}

function clearImage() {
  state.currentFile = null;
  state.currentImageBase64 = null;
  document.getElementById('previewContainer').classList.add('hidden');
  document.getElementById('previewImage').src = '';
  document.getElementById('fileInput').value = '';
  disableAnalyzeButton();
  showToast('Gambar dihapus.', 'info');
}

function enableAnalyzeButton() {
  const btn = document.getElementById('btnAnalyze');
  btn.disabled = false;
}
function disableAnalyzeButton() {
  const btn = document.getElementById('btnAnalyze');
  btn.disabled = true;
}

// ── CAMERA ────────────────────────────────────
async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
    state.cameraStream = stream;
    const video = document.getElementById('cameraVideo');
    video.srcObject = stream;

    document.getElementById('btnStartCam').classList.add('hidden');
    document.getElementById('btnCapture').classList.remove('hidden');
    document.getElementById('btnStopCam').classList.remove('hidden');

    showToast('Kamera aktif.', 'success');
  } catch (err) {
    console.error('Camera error:', err);
    showToast('Tidak dapat mengakses kamera. Periksa izin browser.', 'error');
  }
}

function capturePhoto() {
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  canvas.width  = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);

  canvas.toBlob((blob) => {
    const file = new File([blob], `capture_${Date.now()}.jpg`, { type: 'image/jpeg' });
    processFile(file);
    stopCamera();
    showToast('Foto berhasil diambil.', 'success');
  }, 'image/jpeg', 0.92);
}

function stopCamera() {
  if (state.cameraStream) {
    state.cameraStream.getTracks().forEach(track => track.stop());
    state.cameraStream = null;
  }
  const video = document.getElementById('cameraVideo');
  if (video) video.srcObject = null;

  document.getElementById('btnStartCam').classList.remove('hidden');
  document.getElementById('btnCapture').classList.add('hidden');
  document.getElementById('btnStopCam').classList.add('hidden');
}

// ── ANALYZE ───────────────────────────────────
async function analyzeImage() {
  if (!state.currentFile && !state.currentImageBase64) {
    showToast('Pilih gambar terlebih dahulu.', 'error');
    return;
  }

  showLoadingOverlay();

  try {
    const formData = new FormData();
    if (state.currentFile) {
      formData.append('file', state.currentFile);
    } else {
      const res = await fetch(state.currentImageBase64);
      const blob = await res.blob();
      formData.append('file', new File([blob], 'image.jpg', { type: 'image/jpeg' }));
    }

    advanceLoadingStep(1);

    const response = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      body: formData,
    });

    advanceLoadingStep(2);

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `HTTP ${response.status}`);
    }

    const data = await response.json();
    advanceLoadingStep(3);

    state.lastPrediction = data;

    renderResult(data);
    updateChatContext(data);
    saveToHistory(data);

    advanceLoadingStep(4);

    await sleep(400);
    hideLoadingOverlay();

    document.getElementById('sectionResult').classList.remove('hidden');
    scrollToSection('sectionResult');
    showToast('Analisis selesai.', 'success');

    // Fetch GradCAM after result is shown (non-blocking)
    fetchGradCAM();

  } catch (err) {
    hideLoadingOverlay();
    console.error('Predict error:', err);
    showToast(`Gagal melakukan analisis: ${err.message}`, 'error');
  }
}

// ── RESULT RENDER ─────────────────────────────
function renderResult(data) {
  const label = data.diagnosis || data.label || data.class_name || '—';
  const className = data.class_id || data.class || '';
  const confRaw = data.confidence ?? data.confidence_score ?? 0;
  const conf = typeof confRaw === 'number' ? confRaw : parseFloat(confRaw);
  const confPct = `${(conf * 100).toFixed(2)}%`;

  const riskRaw = data.risk_level || detectRisk(label, conf);
  const riskText = data.risk_label || normalizeRiskLabel(riskRaw);
  const riskCls  = normalizeRiskClass(riskRaw);

  const badgeEl = document.getElementById('resultRiskBadge');
  badgeEl.innerHTML = `<span class="risk-badge ${riskCls}">${riskText}</span>`;

  document.getElementById('resultLabel').textContent = label;
  document.getElementById('resultClass').textContent = className ? `Kelas: ${className}` : '';
  document.getElementById('confVal').textContent = confPct;

  const bar = document.getElementById('confBar');
  bar.style.width = '0%';
  setTimeout(() => {
    bar.style.width = `${Math.min(conf * 100, 100)}%`;
  }, 100);

  const riskDescMap = {
    critical: 'Kondisi ini menunjukkan risiko sangat tinggi. Segera konsultasikan ke dokter spesialis kulit sesegera mungkin.',
    high:     'Kondisi ini memerlukan perhatian medis segera. Segera konsultasikan ke dokter spesialis kulit.',
    medium:   'Kondisi ini perlu dipantau. Disarankan untuk berkonsultasi dengan dokter.',
    low:      'Kondisi ini umumnya tidak membahayakan, namun tetap disarankan memantau perkembangannya.',
  };

  const recText = data.recommendation || riskDescMap[riskCls] || 'Silakan konsultasikan ke dokter untuk informasi lebih lanjut.';

  document.getElementById('riskInfo').classList.remove('hidden');
  document.getElementById('riskDesc').textContent = recText;

  // Update next step recommendation
  const nextStepEl = document.getElementById('nextStepRec');
  if (nextStepEl) nextStepEl.textContent = recText;

  // Probability list
  const probList = document.getElementById('probList');
  probList.innerHTML = '';

  let entries = [];

  if (Array.isArray(data.all_probabilities)) {
    entries = data.all_probabilities.map((item) => [
      item.label || item.class_name || item.name || 'Unknown',
      typeof item.probability === 'number' ? item.probability : parseFloat(item.probability)
    ]);
  } else {
    const probMap = data.probabilities || data.probability || {};
    entries = Object.entries(probMap).map(([k, v]) => [
      k,
      typeof v === 'number' ? v : parseFloat(v)
    ]);
  }

  entries = entries
    .filter(([, val]) => !Number.isNaN(val))
    .sort((a, b) => b[1] - a[1])
    .slice(0, 7);

  if (!entries.length) {
    probList.innerHTML = `<p style="font-size:.85rem;color:var(--neutral-400)">Data probabilitas tidak tersedia.</p>`;
    return;
  }

  entries.forEach(([name, val]) => {
    const pct = `${(val * 100).toFixed(2)}%`;
    const item = document.createElement('div');
    item.className = 'prob-item';
    item.innerHTML = `
      <div class="prob-header">
        <span class="prob-name">${escapeHtml(name)}</span>
        <span class="prob-val">${pct}</span>
      </div>
      <div class="prob-track">
        <div class="prob-fill" style="width:0%"></div>
      </div>
    `;
    probList.appendChild(item);
    setTimeout(() => {
      item.querySelector('.prob-fill').style.width = `${Math.min(val * 100, 100)}%`;
    }, 150);
  });
}

function normalizeRiskClass(risk) {
  const r = String(risk || '').toLowerCase();

  if (r.includes('critical') || r.includes('kritis')) return 'critical';
  if (r.includes('high') || r.includes('tinggi')) return 'high';
  if (r.includes('medium') || r.includes('sedang')) return 'medium';
  return 'low';
}

function normalizeRiskLabel(risk) {
  const cls = normalizeRiskClass(risk);
  if (cls === 'critical') return 'Risiko Kritis';
  if (cls === 'high')     return 'Risiko Tinggi';
  if (cls === 'medium')   return 'Risiko Sedang';
  return 'Risiko Rendah';
}

function detectRisk(label, conf) {
  const highRisk = ['melanoma', 'basal cell carcinoma', 'actinic keratosis'];
  const l = label.toLowerCase();
  if (highRisk.some(h => l.includes(h))) return 'Risiko Tinggi';
  if (conf > 0.75) return 'Risiko Sedang';
  return 'Risiko Rendah';
}

function clearResults() {
  clearImage();
  document.getElementById('sectionResult').classList.add('hidden');
  state.lastPrediction = null;
  scrollToSection('deteksi');
  showToast('Siap melakukan analisis baru.', 'info');
}

// ── GRADCAM ───────────────────────────────────
async function fetchGradCAM() {
  if (!state.currentFile && !state.currentImageBase64) return;

  const loading     = document.getElementById('gcamLoading');
  const gcamImg     = document.getElementById('gradcamImage');
  const origImg     = document.getElementById('originalImageGcam');
  const placeholder = document.getElementById('gcamPlaceholder');

  if (!loading || !gcamImg || !origImg) return;

  // Set original image immediately
  origImg.src = state.currentImageBase64 || '';

  // Show loading, hide others
  loading.classList.remove('hidden');
  gcamImg.classList.add('hidden');
  gcamImg.src = '';
  if (placeholder) placeholder.classList.add('hidden');

  try {
    const formData = new FormData();
    if (state.currentFile) {
      formData.append('file', state.currentFile);
    } else {
      const res = await fetch(state.currentImageBase64);
      const blob = await res.blob();
      formData.append('file', new File([blob], 'image.jpg', { type: 'image/jpeg' }));
    }

    const response = await fetch(`${API_BASE}/gradcam`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    const imgSrc = data.gradcam_image || data.image || data.gradcam || '';

    if (!imgSrc) throw new Error('No image in response');

    gcamImg.src = imgSrc.startsWith('data:') ? imgSrc : `data:image/png;base64,${imgSrc}`;
    gcamImg.classList.remove('hidden');
    loading.classList.add('hidden');

  } catch (err) {
    loading.classList.add('hidden');
    console.warn('GradCAM not available:', err.message);
    if (placeholder) placeholder.classList.remove('hidden');
  }
}

// ── AI CHAT ───────────────────────────────────
function updateChatContext(data) {
  const ctx = document.getElementById('ctxDiagnosis');
  const label = data.diagnosis || data.label || data.class_name || '—';
  const conf = data.confidence ?? data.confidence_score ?? 0;
  ctx.textContent = `Konteks aktif: ${label} (tingkat keyakinan ${(conf * 100).toFixed(2)}%). Silakan ajukan pertanyaan.`;
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 140) + 'px';
}

function handleChatKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChat();
  }
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();

  if (!msg) return;

  appendUserMessage(msg);
  input.value = '';
  autoResize(input);

  const typingId = appendTypingIndicator();

  const diagnosisName =
    state.lastPrediction?.diagnosis ||
    state.lastPrediction?.label ||
    state.lastPrediction?.class_name ||
    null;

  const confidence =
    state.lastPrediction?.confidence ??
    state.lastPrediction?.confidence_score ??
    null;

  const riskLabel =
    state.lastPrediction?.risk_label ||
    state.lastPrediction?.risk_level ||
    null;

  const description =
    state.lastPrediction?.description ||
    '';

  const recommendation =
    state.lastPrediction?.recommendation ||
    '';

  const probabilitySummary = Array.isArray(state.lastPrediction?.all_probabilities)
    ? state.lastPrediction.all_probabilities
        .slice()
        .sort((a, b) => b.probability - a.probability)
        .slice(0, 3)
        .map(item => `${item.label}: ${(item.probability * 100).toFixed(2)}%`)
        .join(', ')
    : 'tidak tersedia';

  const systemContext = diagnosisName
    ? `
Diagnosis AI: ${diagnosisName}
Confidence: ${confidence !== null ? (confidence * 100).toFixed(2) + '%' : 'tidak tersedia'}
Risk level: ${riskLabel || 'tidak tersedia'}
Deskripsi diagnosis: ${description || 'tidak tersedia'}
Rekomendasi awal: ${recommendation || 'tidak tersedia'}
Probabilitas tertinggi: ${probabilitySummary}

Instruksi penting:
Jawab pertanyaan user secara langsung.
Jangan hanya mengulang definisi diagnosis.
Jika user bertanya "penyebab", jelaskan penyebab.
Jika user bertanya "harus apa", jelaskan langkah lanjutan.
Jika user bertanya "bahaya atau tidak", jelaskan tingkat risiko.
Gunakan bahasa Indonesia yang mudah dipahami.
Tetap ingatkan bahwa hasil AI bukan diagnosis final.
`
    : `
Belum ada hasil diagnosis AI.
Jawab pertanyaan user secara umum tentang kesehatan kulit.
Gunakan bahasa Indonesia yang mudah dipahami.
Tetap ingatkan bahwa jawaban AI bukan diagnosis final.
`;

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: msg,
        diagnosis_context: systemContext
      }),
    });

    removeTypingIndicator(typingId);

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();

    console.log('CHAT RESPONSE:', data);

    const reply =
      data.response ||
      data.message ||
      data.reply ||
      'Maaf, terjadi kesalahan pada server.';

    appendAIMessage(reply);

  } catch (err) {
    removeTypingIndicator(typingId);
    console.error('Chat error:', err);
    appendAIMessage(
      'Maaf, tidak dapat terhubung ke server AI saat ini. Pastikan backend berjalan dan coba kembali.'
    );
  }
}
function appendUserMessage(text) {
  const container = document.getElementById('chatMessages');
  const now = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  const el = document.createElement('div');
  el.className = 'chat-msg user-msg';
  el.innerHTML = `
    <div class="msg-ava">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
    </div>
    <div class="msg-content">
      <div class="msg-bubble">${escapeHtml(text)}</div>
      <span class="msg-time">${now}</span>
    </div>`;
  container.appendChild(el);
  scrollChatBottom();
}

function appendAIMessage(text) {
  const container = document.getElementById('chatMessages');
  const now = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  const el = document.createElement('div');
  el.className = 'chat-msg ai-msg';
  el.innerHTML = `
    <div class="msg-ava">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 012 2v2a2 2 0 01-2 2 2 2 0 01-2-2V4a2 2 0 012-2z"/><path d="M20 10a2 2 0 00-2-2h-1V7a5 5 0 00-10 0v1H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V10z"/></svg>
    </div>
    <div class="msg-content">
      <div class="msg-bubble">${formatChatText(text)}</div>
      <span class="msg-time">${now}</span>
    </div>`;
  container.appendChild(el);
  scrollChatBottom();
}

function appendTypingIndicator() {
  const container = document.getElementById('chatMessages');
  const id = 'typing_' + Date.now();
  const el = document.createElement('div');
  el.id = id;
  el.className = 'chat-msg ai-msg typing-indicator';
  el.innerHTML = `
    <div class="msg-ava">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a2 2 0 012 2v2a2 2 0 01-2 2 2 2 0 01-2-2V4a2 2 0 012-2z"/><path d="M20 10a2 2 0 00-2-2h-1V7a5 5 0 00-10 0v1H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V10z"/></svg>
    </div>
    <div class="msg-content">
      <div class="msg-bubble">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    </div>`;
  container.appendChild(el);
  scrollChatBottom();
  return id;
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function scrollChatBottom() {
  const container = document.getElementById('chatMessages');
  container.scrollTop = container.scrollHeight;
}

function formatChatText(text) {
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── HOSPITALS ─────────────────────────────────
async function loadCities() {
  try {
    const response = await fetch(`${API_BASE}/hospitals`);
    if (!response.ok) throw new Error();
    const data = await response.json();

    const hospitals = Array.isArray(data) ? data : data.hospitals || [];
    const cities = [...new Set(hospitals.map(h => h.city || h.kota || h.kabupaten || '').filter(Boolean))].sort();

    const select = document.getElementById('citySelect');
    cities.forEach(city => {
      const opt = document.createElement('option');
      opt.value = city;
      opt.textContent = city;
      select.appendChild(opt);
    });

    // Store all hospitals globally
    window._allHospitals = hospitals;

  } catch (err) {
    console.warn('Could not load cities:', err);
    // Show empty state
    document.getElementById('hospitalEmpty').classList.remove('hidden');
  }
}

async function fetchHospitals() {
  const city = document.getElementById('citySelect').value;
  const grid    = document.getElementById('hospitalGrid');
  const loading = document.getElementById('hospitalLoading');
  const empty   = document.getElementById('hospitalEmpty');

  grid.innerHTML = '';
  empty.classList.add('hidden');

  if (!city) {
    empty.classList.remove('hidden');
    return;
  }

  loading.classList.remove('hidden');

  try {
    let hospitals = [];

    if (window._allHospitals) {
      // Filter from cached data
      hospitals = window._allHospitals.filter(h => {
        const c = h.city || h.kota || h.kabupaten || '';
        return c.toLowerCase() === city.toLowerCase();
      });
    } else {
      // Fetch from API with city param
      const response = await fetch(`${API_BASE}/hospitals?city=${encodeURIComponent(city)}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      hospitals = Array.isArray(data) ? data : data.hospitals || [];
    }

    loading.classList.add('hidden');

    if (!hospitals.length) {
      empty.classList.remove('hidden');
      empty.querySelector('p').textContent = `Tidak ada data rumah sakit untuk kota ${city}.`;
      return;
    }

    hospitals.forEach(h => {
      const card = buildHospitalCard(h);
      grid.appendChild(card);
    });

  } catch (err) {
    loading.classList.add('hidden');
    console.error('Hospital fetch error:', err);
    empty.classList.remove('hidden');
    empty.querySelector('p').textContent = 'Gagal memuat data rumah sakit. Pastikan backend berjalan.';
  }
}

function buildHospitalCard(h) {
  const name    = h.name   || h.nama   || 'Rumah Sakit';
  const type    = h.type   || h.tipe   || h.jenis || 'Rumah Sakit';
  const address = h.address || h.alamat || '—';
  const maps    = h.maps_url || h.google_maps || h.maps || '';
  const city    = h.city   || h.kota   || '';
  const mapsUrl = maps || `https://maps.google.com/?q=${encodeURIComponent(name + ' ' + address)}`;

  const div = document.createElement('div');
  div.className = 'hospital-card';
  div.innerHTML = `
    <span class="hcard-type">${escapeHtml(type)}</span>
    <h3 class="hcard-name">${escapeHtml(name)}</h3>
    <div class="hcard-address">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
      <span>${escapeHtml(address)}${city ? `, ${escapeHtml(city)}` : ''}</span>
    </div>
    <a href="${mapsUrl}" target="_blank" rel="noopener noreferrer" class="hcard-maps">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
      Buka Google Maps
    </a>`;
  return div;
}

// ── PREDICTION HISTORY ────────────────────────
function saveToHistory(data) {
  const label   = data.diagnosis || data.label || data.class_name || '—';
  const conf    = data.confidence ?? data.confidence_score ?? 0;
  const risk    = data.risk_level || detectRisk(label, conf);
  const imgSrc  = state.currentImageBase64 || '';
  const now     = new Date().toLocaleString('id-ID', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });

  state.predictionHistory.unshift({
    date: now,
    image: imgSrc,
    patient: 'Pasien',
    result: label,
    category: risk,
    confidence: `${(conf * 100).toFixed(2)}%`,
  });

  renderHistoryTable();
  updateHistoryCount();
}

function renderHistoryTable() {
  const tbody   = document.getElementById('historyBody');
  const emptyRow = document.getElementById('historyEmptyRow');

  // Remove all rows except empty row
  Array.from(tbody.querySelectorAll('tr:not(#historyEmptyRow)')).forEach(r => r.remove());

  if (!state.predictionHistory.length) {
    emptyRow.classList.remove('hidden');
    updateHistoryCount();
    return;
  }

  emptyRow.classList.add('hidden');

  state.predictionHistory.forEach(item => {
    const riskCls = item.category.toLowerCase().includes('tinggi') ? 'high'
                  : item.category.toLowerCase().includes('sedang') ? 'medium'
                  : 'low';
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(item.date)}</td>
      <td><img class="history-thumb" src="${item.image || ''}" alt="gambar" onerror="this.style.display='none'"/></td>
      <td>${escapeHtml(item.patient)}</td>
      <td style="font-weight:600;color:var(--neutral-900)">${escapeHtml(item.result)}</td>
      <td><span class="cond-risk ${riskCls}">${escapeHtml(item.category)}</span></td>
      <td style="font-weight:700;color:var(--pink-600)">${escapeHtml(item.confidence)}</td>`;
    tbody.appendChild(tr);
  });

  updateHistoryCount();
}

function updateHistoryCount() {
  const count = state.predictionHistory.length;
  document.getElementById('historyCount').textContent = `${count} data`;
}

function clearHistory() {
  if (!state.predictionHistory.length) return;
  state.predictionHistory = [];
  renderHistoryTable();
  showToast('Riwayat prediksi dihapus.', 'info');
}

// ── LOADING OVERLAY ───────────────────────────
const LOADING_STEPS_TEXT = [
  'Preprocessing gambar...',
  'Menjalankan inferensi model CNN...',
  'Menghitung tingkat keyakinan...',
  'Memuat analisis probabilitas...',
];

let currentLoadingStep = 0;
let loadingInterval = null;

function showLoadingOverlay() {
  currentLoadingStep = 0;
  resetLoadingSteps();
  document.getElementById('loadingOverlay').classList.remove('hidden');
  advanceLoadingStep(0);
}

function hideLoadingOverlay() {
  document.getElementById('loadingOverlay').classList.add('hidden');
  if (loadingInterval) clearInterval(loadingInterval);
}

function resetLoadingSteps() {
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`lstep${i}`);
    el.classList.remove('active', 'done');
  }
  document.getElementById('loadingStep').textContent = LOADING_STEPS_TEXT[0];
}

function advanceLoadingStep(stepIndex) {
  for (let i = 1; i <= stepIndex; i++) {
    const el = document.getElementById(`lstep${i}`);
    el.classList.remove('active');
    el.classList.add('done');
  }
  const current = document.getElementById(`lstep${stepIndex + 1}`);
  if (current) {
    current.classList.add('active');
    const txt = LOADING_STEPS_TEXT[stepIndex];
    if (txt) document.getElementById('loadingStep').textContent = txt;
  }
}

// ── TOAST ─────────────────────────────────────
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    ${type === 'success' ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>' :
      type === 'error' ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' :
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'}
    <span>${escapeHtml(message)}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    toast.style.transition = 'opacity .3s, transform .3s';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// ── UTILS ─────────────────────────────────────
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
