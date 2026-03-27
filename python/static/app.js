// Domino Helper - Client-side logic
// Handles camera capture, image resize, upload, and result display.

const MAX_IMAGE_DIM = 2000; // Max px before upload (saves bandwidth)
const JPEG_QUALITY = 0.85;

// DOM elements
const btnCamera = document.getElementById('btn-camera');
const btnGallery = document.getElementById('btn-gallery');
const inputCamera = document.getElementById('input-camera');
const inputGallery = document.getElementById('input-gallery');
const previewSection = document.getElementById('preview-section');
const previewImg = document.getElementById('preview-img');
const btnAnalyze = document.getElementById('btn-analyze');
const btnRetake = document.getElementById('btn-retake');
const loadingSection = document.getElementById('loading-section');
const resultsSection = document.getElementById('results-section');
const resultImg = document.getElementById('result-img');
const summaryCard = document.getElementById('summary-card');
const sumsContainer = document.getElementById('sums-container');
const dominoTableContainer = document.getElementById('domino-table-container');
const errorSection = document.getElementById('error-section');
const errorMsg = document.getElementById('error-msg');
const btnDismissError = document.getElementById('btn-dismiss-error');
const btnNew = document.getElementById('btn-new');
const captureSection = document.querySelector('.capture-section');

let selectedFile = null;

// --- Event Listeners ---

btnCamera.addEventListener('click', () => inputCamera.click());
btnGallery.addEventListener('click', () => inputGallery.click());

inputCamera.addEventListener('change', handleFileSelect);
inputGallery.addEventListener('change', handleFileSelect);

btnAnalyze.addEventListener('click', analyzeImage);
btnRetake.addEventListener('click', resetToCapture);
btnDismissError.addEventListener('click', resetToCapture);
btnNew.addEventListener('click', resetToCapture);

// --- Functions ---

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        showSection('preview');
    };
    reader.readAsDataURL(file);

    // Reset input so same file can be re-selected
    event.target.value = '';
}

async function resizeImage(file) {
    // Use createImageBitmap for efficient decode + automatic EXIF rotation
    const bitmap = await createImageBitmap(file);
    const { width, height } = bitmap;

    let targetW = width;
    let targetH = height;

    if (Math.max(width, height) > MAX_IMAGE_DIM) {
        const scale = MAX_IMAGE_DIM / Math.max(width, height);
        targetW = Math.round(width * scale);
        targetH = Math.round(height * scale);
    }

    const canvas = document.createElement('canvas');
    canvas.width = targetW;
    canvas.height = targetH;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bitmap, 0, 0, targetW, targetH);
    bitmap.close();

    return new Promise((resolve) => {
        canvas.toBlob(resolve, 'image/jpeg', JPEG_QUALITY);
    });
}

async function analyzeImage() {
    if (!selectedFile) return;

    showSection('loading');

    try {
        const resized = await resizeImage(selectedFile);

        const formData = new FormData();
        formData.append('file', resized, 'domino.jpg');

        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({ detail: 'Server error' }));
            throw new Error(err.detail || `HTTP ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (err) {
        showError(err.message || 'Failed to analyze image. Please try again.');
    }
}

function displayResults(data) {
    // Annotated image
    resultImg.src = data.annotated_image;

    // Summary card
    summaryCard.innerHTML = `
        <div class="stat">
            <span class="stat-label">Dominos Detected</span>
            <span class="stat-value">${data.num_dominos}</span>
        </div>
        <div class="stat">
            <span class="stat-label">Rows Found</span>
            <span class="stat-value">${data.rows.length}</span>
        </div>
        <div class="stat">
            <span class="stat-label">Columns Found</span>
            <span class="stat-value">${data.cols.length}</span>
        </div>
    `;

    // Row and column sums
    let sumsHtml = '';

    if (data.rows.length > 0) {
        sumsHtml += '<div class="sums-card"><h3>Row Sums</h3>';
        data.rows.forEach((r, i) => {
            sumsHtml += `<div class="sum-item">
                <span>Row ${i + 1} (${r.num_dominos} dominos)</span>
                <span class="sum-value">${r.sum}</span>
            </div>`;
        });
        sumsHtml += '</div>';
    }

    if (data.cols.length > 0) {
        sumsHtml += '<div class="sums-card"><h3>Column Sums</h3>';
        data.cols.forEach((c, i) => {
            sumsHtml += `<div class="sum-item">
                <span>Col ${i + 1} (${c.num_dominos} dominos)</span>
                <span class="sum-value">${c.sum}</span>
            </div>`;
        });
        sumsHtml += '</div>';
    }

    sumsContainer.innerHTML = sumsHtml;

    // Domino detail table
    if (data.dominos.length > 0) {
        let tableHtml = '<table class="domino-table"><thead><tr>' +
            '<th>#</th><th>Orient.</th><th>Side A</th><th>Side B</th><th>Total</th>' +
            '</tr></thead><tbody>';

        data.dominos.forEach((d) => {
            tableHtml += `<tr>
                <td>${d.index + 1}</td>
                <td>${d.orientation === 'vertical' ? 'V' : 'H'}</td>
                <td>${d.top_left_dots}</td>
                <td>${d.bottom_right_dots}</td>
                <td><strong>${d.total}</strong></td>
            </tr>`;
        });

        tableHtml += '</tbody></table>';
        dominoTableContainer.innerHTML = tableHtml;
    }

    showSection('results');
}

function showError(message) {
    errorMsg.textContent = message;
    showSection('error');
}

function showSection(name) {
    captureSection.classList.toggle('hidden', name !== 'capture');
    previewSection.classList.toggle('hidden', name !== 'preview');
    loadingSection.classList.toggle('hidden', name !== 'loading');
    resultsSection.classList.toggle('hidden', name !== 'results');
    errorSection.classList.toggle('hidden', name !== 'error');
}

function resetToCapture() {
    selectedFile = null;
    previewImg.src = '';
    resultImg.src = '';
    summaryCard.innerHTML = '';
    sumsContainer.innerHTML = '';
    dominoTableContainer.innerHTML = '';
    showSection('capture');
}
