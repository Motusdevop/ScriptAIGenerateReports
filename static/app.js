// =========================
// КОНСТАНТЫ
// =========================
const STORAGE_KEY = 'softiumCreds';
const API_ENDPOINTS = {
  GET_LESSON_DATA: '/scraper/get_lesson_data',
  GENERATE_REPORT: '/report_generation/generate',
  FEEDBACK: '/api/v1/feedback',
};

// =========================
// ЭЛЕМЕНТЫ DOM
// =========================
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const lessonIdInput = document.getElementById('lessonId');
const saveBtn = document.getElementById('saveBtn');
const editBtn = document.getElementById('editBtn');
const fetchBtn = document.getElementById('fetchBtn');
const generateBtn = document.getElementById('generateBtn');
const message = document.getElementById('message'); // оставляем для совместимости/фоллбэка
const loader = document.getElementById('loader');
const report = document.getElementById('report');
const lessonPreviewSection = document.getElementById('lessonPreview');
const lessonPreviewContent = document.getElementById('lessonPreviewContent');
const reportsSection = document.getElementById('reportsSection');
const regenerateModal = document.getElementById('regenerateModal');
const modalClose = document.getElementById('modalClose');
const modalCancel = document.getElementById('modalCancel');
const modalRegenerate = document.getElementById('modalRegenerate');
const regenerateComment = document.getElementById('regenerateComment');

// =========================
// СОСТОЯНИЕ ПРИЛОЖЕНИЯ
// =========================
let lessonData = null;
let currentRegeneratingChildId = null;

generateBtn.disabled = true;

// =========================
// TOAST (без правки style.css)
// =========================
const TOAST_CONTAINER_ID = 'toast-container';
const TOAST_STYLE_ID = 'toast-styles';

let _lastToast = { text: null, ts: 0 };

function ensureToastStyles() {
  if (document.getElementById(TOAST_STYLE_ID)) return;

  const style = document.createElement('style');
  style.id = TOAST_STYLE_ID;
  style.textContent = `
    .toast-container{
      position: fixed;
      top: 16px;
      right: 16px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .toast{
      pointer-events: auto;
      display: grid;
      grid-template-columns: 20px 1fr auto;
      align-items: start;
      gap: 10px;
      min-width: 280px;
      max-width: 420px;
      padding: 12px 12px;
      border-radius: 14px;
      background: rgba(255,255,255,0.92);
      border: 1px solid rgba(15,23,42,0.10);
      box-shadow: 0 12px 30px rgba(2,6,23,0.18);
      backdrop-filter: blur(8px);
      transform: translateY(-8px);
      opacity: 0;
      transition: transform .18s ease, opacity .18s ease;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, "Apple Color Emoji", "Segoe UI Emoji";
      color: #0f172a;
    }
    .toast.toast--visible{
      transform: translateY(0);
      opacity: 1;
    }
    .toast__icon{
      width: 20px;
      height: 20px;
      display:flex;
      align-items:center;
      justify-content:center;
      margin-top: 1px;
    }
    .toast__text{
      font-size: 14px;
      line-height: 1.25rem;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .toast__close{
      appearance: none;
      border: none;
      background: transparent;
      cursor: pointer;
      color: rgba(15,23,42,0.55);
      width: 28px;
      height: 28px;
      border-radius: 10px;
      display:flex;
      align-items:center;
      justify-content:center;
      transition: background .12s ease, color .12s ease;
    }
    .toast__close:hover{
      background: rgba(15,23,42,0.06);
      color: rgba(15,23,42,0.80);
    }
    .toast--success { border-color: rgba(34,197,94,0.25); }
    .toast--error   { border-color: rgba(239,68,68,0.25); }
    .toast--info    { border-color: rgba(59,130,246,0.22); }

    .toast--success .toast__icon{ color:#16a34a; }
    .toast--error   .toast__icon{ color:#ef4444; }
    .toast--info    .toast__icon{ color:#3b82f6; }

    @media (max-width: 520px){
      .toast-container{ left: 12px; right: 12px; top: 12px; }
      .toast{ min-width: unset; max-width: unset; width: 100%; }
    }
  `;
  document.head.appendChild(style);
}

function ensureToastContainer() {
  let container = document.getElementById(TOAST_CONTAINER_ID);
  if (container) return container;

  container = document.createElement('div');
  container.id = TOAST_CONTAINER_ID;
  container.className = 'toast-container';
  document.body.appendChild(container);
  return container;
}

function showToast(text, type = 'info', opts = {}) {
  ensureToastStyles();
  const container = ensureToastContainer();

  // анти-спам: одинаковые тосты подряд в течение 700мс не показываем
  const now = Date.now();
  if (_lastToast.text === text && (now - _lastToast.ts) < 700) return;
  _lastToast = { text, ts: now };

  const duration = opts.duration ?? (type === 'info' ? 2200 : 3800);

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;

  const icon = document.createElement('div');
  icon.className = 'toast__icon';
  icon.textContent = type === 'success' ? '✓' : (type === 'error' ? '!' : 'i');

  const msg = document.createElement('div');
  msg.className = 'toast__text';
  msg.textContent = String(text ?? '');

  const close = document.createElement('button');
  close.className = 'toast__close';
  close.type = 'button';
  close.setAttribute('aria-label', 'Закрыть уведомление');
  close.textContent = '✕';

  toast.appendChild(icon);
  toast.appendChild(msg);
  toast.appendChild(close);

  const removeToast = () => {
    toast.classList.remove('toast--visible');
    // ждём анимацию
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 180);
  };

  close.addEventListener('click', removeToast);

  container.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('toast--visible'));

  if (duration > 0) {
    setTimeout(removeToast, duration);
  }
}

// =========================
// УТИЛИТЫ
// =========================
function showMessage(text, color = 'black') {
  // Все уведомления теперь через toast
  const normalized = String(color || '').toLowerCase();
  const type =
    normalized === 'green' ? 'success' :
    normalized === 'red' ? 'error' :
    'info';

  showToast(text, type);

  // фоллбэк: на случай если на странице где-то завязано на #message
  if (message) {
    message.style.display = 'none';
    message.innerText = '';
  }
}

function setLoading(isLoading) {
  loader.style.display = isLoading ? 'block' : 'none';
}

function toggleCredentialsInputs(disabled) {
  usernameInput.disabled = disabled;
  passwordInput.disabled = disabled;
  saveBtn.style.display = disabled ? 'none' : 'block';
  editBtn.style.display = disabled ? 'block' : 'none';
}

function resetUI() {
  lessonPreviewContent.innerHTML = '';
  lessonPreviewSection.style.display = 'none';
  reportsSection.style.display = 'none';
  report.innerHTML = '';
  generateBtn.disabled = true;
}

function collectComments() {
  if (!lessonData?.children) return;

  lessonData.children.forEach(child => {
    const commentInput = document.getElementById(`comment-${child.child_id}`);
    if (commentInput) {
      child.comments = commentInput.value.trim() || null;
    }
  });
}

function createSkeletonCard() {
  return `
    <div class="skeleton-card">
      <div class="skeleton skeleton-line short"></div>
      <div class="skeleton skeleton-line medium"></div>
      <div class="skeleton skeleton-line long"></div>
      <div class="skeleton skeleton-line long"></div>
    </div>
  `;
}

function showModal(childId, currentComment = '') {
  currentRegeneratingChildId = childId;
  regenerateComment.value = currentComment;
  regenerateModal.style.display = 'flex';
  regenerateComment.focus();
}

function hideModal() {
  regenerateModal.style.display = 'none';
  currentRegeneratingChildId = null;
  regenerateComment.value = '';
}

async function getErrorMessageFromResponse(response) {
  // FastAPI HTTPException чаще возвращает JSON {detail: "..."}
  try {
    const asJson = await response.json();
    if (asJson?.detail) return asJson.detail;
    if (asJson?.message) return asJson.message;
  } catch (_) {
    // ignore
  }

  try {
    const asText = await response.text();
    if (asText?.trim()) return asText;
  } catch (_) {
    // ignore
  }

  return response.statusText || `HTTP ${response.status}`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text ?? '';
  return div.innerHTML;
}

function formatReportText(text) {
  if (!text) return '';
  return text
    .split("\n")
    .filter(p => p.trim())
    .map(p => `<p>${escapeHtml(p.trim())}</p>`)
    .join('');
}

// Генерим локальный "prompt" для сохранения фидбэка (чтобы было что-то полезное в хранилище)
function buildPromptForFeedback(child) {
  const tasks = Array.isArray(child?.tasks) ? child.tasks : [];
  const tasksBlock = tasks.length
    ? tasks.map(t => {
        const taskName = t?.name || 'Без названия';
        const direction = t?.direction || 'Не указано';
        const text = t?.text || 'Нет описания';
        return `- Задание «${taskName}» (направление: ${direction}, ${text})`;
      }).join('\n')
    : 'Нет описаний выполненных заданий.';

  const progress = child?.done_tasks_count ?? tasks.length;
  const comments = (child?.comments || '').trim();
  const commentsBlock = comments
    ? `\n\nКомментарий преподавателя:\n${comments}`
    : `\n\nКомментарий преподавателя: Нет комментариев.`;

  return (
    `Имя ребёнка: ${child?.name || 'Неизвестно'}\n` +
    `Количество выполненных заданий: ${progress}\n` +
    `Выполненные задания:\n${tasksBlock}` +
    commentsBlock
  );
}

// =========================
// ЗАГРУЗКА СОХРАНЁННЫХ ДАННЫХ
// =========================
window.onload = () => {
  ensureToastStyles();
  ensureToastContainer();

  const savedCreds = localStorage.getItem(STORAGE_KEY);
  if (savedCreds) {
    try {
      const creds = JSON.parse(savedCreds);
      usernameInput.value = creds.username || '';
      passwordInput.value = creds.password || '';
      toggleCredentialsInputs(true);
    } catch (err) {
      console.error('Ошибка при загрузке сохранённых данных:', err);
      localStorage.removeItem(STORAGE_KEY);
    }
  }
};

// =========================
// СОХРАНЕНИЕ КРЕДОВ
// =========================
saveBtn.addEventListener('click', () => {
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();

  if (!username || !password) {
    showMessage('Введите логин и пароль!', 'red');
    return;
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ username, password }));
    toggleCredentialsInputs(true);
    showMessage('Креды сохранены!', 'green');
  } catch (err) {
    console.error('Ошибка при сохранении данных:', err);
    showMessage('Ошибка при сохранении данных', 'red');
  }
});

// =========================
// РЕДАКТИРОВАНИЕ КРЕДОВ
// =========================
editBtn.addEventListener('click', () => {
  toggleCredentialsInputs(false);
  if (message) message.innerText = '';
});

// =========================
// ЗАГРУЗКА ДАННЫХ УРОКА
// =========================
fetchBtn.addEventListener('click', async () => {
  let savedCreds = {};
  try {
    const credsStr = localStorage.getItem(STORAGE_KEY);
    if (credsStr) {
      savedCreds = JSON.parse(credsStr);
    }
  } catch (err) {
    console.error('Ошибка при чтении сохранённых данных:', err);
  }

  const lessonId = lessonIdInput.value.trim();

  if (!savedCreds.username || !savedCreds.password || !lessonId) {
    showMessage('Заполните креды и ID урока!', 'red');
    return;
  }

  showMessage('Загрузка данных...', 'black');
  setLoading(true);
  resetUI();

  // Показываем скелетоны во время загрузки
  lessonPreviewSection.style.display = 'block';
  lessonPreviewContent.innerHTML = Array(3).fill(createSkeletonCard()).join('');

  try {
    const response = await fetch(API_ENDPOINTS.GET_LESSON_DATA, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: savedCreds.username,
        password: savedCreds.password,
        lesson_id: Number(lessonId),
      }),
    });

    if (!response.ok) {
      const errorText = await getErrorMessageFromResponse(response);
      throw new Error(errorText || `HTTP ${response.status}`);
    }

    lessonData = await response.json();

    if (!lessonData.children || lessonData.children.length === 0) {
      showMessage('Не удалось получить данные об уроке.', 'red');
      lessonData = null;
      return;
    }

    displayLessonData(lessonData);
    lessonPreviewSection.style.display = 'block';
    generateBtn.disabled = false;
    showMessage('Данные успешно получены!', 'green');

  } catch (err) {
    console.error('Ошибка при загрузке данных урока:', err);
    showMessage(`Ошибка: ${err.message}`, 'red');
    lessonData = null;
  } finally {
    setLoading(false);
  }
});

// =========================
// ГЕНЕРАЦИЯ ОТЧЁТА
// =========================
generateBtn.addEventListener('click', async () => {
  if (!lessonData || !lessonData.children?.length) {
    showMessage('Нет данных для генерации отчёта', 'red');
    return;
  }

  collectComments();

  showMessage('Генерация отчётов...', 'black');
  setLoading(true);
  report.innerHTML = '';
  reportsSection.style.display = 'block';
  generateBtn.disabled = true;

  const generatePromises = lessonData.children.map(async (child) => {
    const blockId = `report-${child.child_id}`;

    // Создаём плейсхолдер с анимацией загрузки
    report.insertAdjacentHTML(
      'beforeend',
      `<div id="${blockId}" class="report-item">
        <div class="report-header">
          <div class="report-name">${escapeHtml(child.name)}</div>
        </div>
        <div class="report-loading">
          <div class="loader" style="width: 32px; height: 32px; margin: 0 auto;"></div>
          <div style="text-align: center; margin-top: 12px; color: #64748b; font-size: 14px;">Генерация...</div>
        </div>
      </div>`
    );

    try {
      const response = await fetch(API_ENDPOINTS.GENERATE_REPORT, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(child),
      });

      if (!response.ok) {
        const errorText = await getErrorMessageFromResponse(response);
        throw new Error(errorText || `HTTP ${response.status}`);
      }

      const result = await response.json();
      renderSingleGeneratedReport(blockId, result, child.child_id);
      return { success: true, childName: child.name };

    } catch (err) {
      console.error(`Ошибка генерации отчёта для ${child.name}:`, err);
      const container = document.getElementById(blockId);
      if (container) {
        container.innerHTML = `
          <div class="report-name">${escapeHtml(child.name)}</div>
          <div class="report-error">Ошибка генерации: ${escapeHtml(err.message)}</div>
        `;
      }
      return { success: false, childName: child.name, error: err.message };
    }
  });

  await Promise.all(generatePromises);

  setLoading(false);
  generateBtn.disabled = false;
  showMessage('Все отчёты сгенерированы!', 'green');
});

// =========================
// ОТОБРАЖЕНИЕ ДАННЫХ УРОКА
// =========================
function displayLessonData(data) {
  if (!data?.children?.length) {
    lessonPreviewContent.innerHTML = '<p>Нет данных для отображения</p>';
    return;
  }

  const html = data.children.map(child => {
    const tasksHtml = child.tasks?.map(task => `
      <div class="task-row">
        <div class="task-title">${escapeHtml(task.name || 'Без названия')}</div>
        <div class="task-meta">
          <span class="task-badge blue">${escapeHtml(task.direction || '')}</span>
          <span class="task-badge yellow">Уровень ${escapeHtml(task.level || '')}</span>
          <span class="task-badge green">+${task.reward || 0}</span>
        </div>
      </div>
    `).join('') || '<p>Нет заданий</p>';

    return `
      <div class="child-card" data-child-id="${child.child_id}">
        <div class="child-header">
          <div class="child-name">${escapeHtml(child.name || 'Без имени')}</div>
          <div class="child-count">Выполнено заданий: ${child.done_tasks_count || 0}</div>
        </div>

        <div class="tasks-list">
          ${tasksHtml}
        </div>

        <div class="comment-section">
          <label for="comment-${child.child_id}" class="comment-label">
            Комментарий преподавателя
          </label>
          <textarea
            id="comment-${child.child_id}"
            class="comment-input"
            placeholder="Введите комментарий для этого ребёнка..."
            rows="3"
          >${escapeHtml(child.comments || '')}</textarea>
        </div>
      </div>
    `;
  }).join('');

  lessonPreviewContent.innerHTML = html;
}

// =========================
// ОТОБРАЖЕНИЕ ОТЧЁТА
// =========================
function renderSingleGeneratedReport(blockId, result, childId = null) {
  const container = document.getElementById(blockId);
  if (!container) {
    console.error(`Контейнер с ID ${blockId} не найден`);
    return;
  }

  // Новый контракт: status="ok", report_id=UUID
  // На всякий случай поддержим старые ответы
  const isOk = (result?.status === 'ok') || (result?.status === 'success') || (!result?.status && !!result?.report);

  if (!isOk) {
    const errMsg = result?.detail || result?.message || 'Не удалось получить отчёт';
    container.innerHTML = `
      <div class="report-header">
        <div class="report-name">Ошибка</div>
        ${childId ? `<div class="report-actions">
          <button class="btn-icon btn-regenerate tooltip-trigger" onclick="handleRegenerate(${childId})" data-tooltip="Перегенерировать отчёт">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
              <path d="M21 3v5h-5"></path>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
              <path d="M3 21v-5h5"></path>
            </svg>
            <span class="tooltip">Перегенерировать отчёт</span>
          </button>
        </div>` : ''}
      </div>
      <div class="report-error">${escapeHtml(errMsg)}</div>
    `;
    return;
  }

  const reportText = result.report || '';
  const reportTextId = `report-text-${childId || 'default'}`;
  const reportUuid = result.report_id || null;

  container.innerHTML = `
    <div class="report-header">
      <div class="report-name">${escapeHtml(result.child_name || 'Без имени')}</div>
      <div class="report-actions">

        <!-- 👍 Like -->
        ${reportUuid && childId ? `
        <button class="btn-icon btn-like tooltip-trigger" onclick="sendFeedback('${reportUuid}', 1, ${childId})" data-tooltip="Лайк">
          <span style="font-size:16px; line-height:1;">👍</span>
          <span class="tooltip">Лайк</span>
        </button>` : ''}

        <!-- 👎 Dislike -->
        ${reportUuid && childId ? `
        <button class="btn-icon btn-dislike tooltip-trigger" onclick="sendFeedback('${reportUuid}', -1, ${childId})" data-tooltip="Дизлайк">
          <span style="font-size:16px; line-height:1;">👎</span>
          <span class="tooltip">Дизлайк</span>
        </button>` : ''}

        <!-- Copy -->
        <button class="btn-icon btn-copy tooltip-trigger" onclick="copyReportText('${reportTextId}')" data-tooltip="Копировать отчёт">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
          <span class="tooltip">Копировать отчёт</span>
        </button>

        <!-- Regenerate -->
        ${childId ? `<button class="btn-icon btn-regenerate tooltip-trigger" onclick="handleRegenerate(${childId})" data-tooltip="Перегенерировать отчёт">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
            <path d="M21 3v5h-5"></path>
            <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
            <path d="M3 21v-5h5"></path>
          </svg>
          <span class="tooltip">Перегенерировать отчёт</span>
        </button>` : ''}

      </div>
    </div>
    <div class="report-text" id="${reportTextId}">${formatReportText(reportText)}</div>
  `;

  // Плавное появление
  container.style.opacity = '0';
  setTimeout(() => {
    container.style.transition = 'opacity 0.4s ease';
    container.style.opacity = '1';
  }, 10);
}

// =========================
// FEEDBACK (LIKE / DISLIKE)
// =========================
async function sendFeedback(reportId, rating, childId) {
  const child = lessonData?.children?.find(c => c.child_id === childId);
  if (!child) {
    showMessage('Не удалось отправить фидбэк: ребёнок не найден', 'red');
    return;
  }

  const reportTextEl = document.getElementById(`report-text-${childId}`);
  const responseText = reportTextEl?.innerText || reportTextEl?.textContent || '';

  // Чтобы не спамили кликами — временно дизейблим обе кнопки
  const reportCard = document.getElementById(`report-${childId}`);
  const likeBtn = reportCard?.querySelector('.btn-like');
  const dislikeBtn = reportCard?.querySelector('.btn-dislike');

  if (likeBtn) likeBtn.disabled = true;
  if (dislikeBtn) dislikeBtn.disabled = true;

  try {
    const payload = {
      report_id: reportId,
      rating: rating,
      comment: null,

      child: child,
      prompt: buildPromptForFeedback(child),
      response: responseText,

      model: 'gemini',
      prompt_version: 'v1',
    };

    const res = await fetch(API_ENDPOINTS.FEEDBACK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errorText = await getErrorMessageFromResponse(res);
      throw new Error(errorText || `HTTP ${res.status}`);
    }

    showMessage(rating === 1 ? '👍 Лайк сохранён!' : '👎 Дизлайк сохранён!', 'green');

  } catch (err) {
    console.error('Ошибка отправки фидбэка:', err);
    showMessage(`Ошибка отправки фидбэка: ${err.message}`, 'red');
  } finally {
    if (likeBtn) likeBtn.disabled = false;
    if (dislikeBtn) dislikeBtn.disabled = false;
  }
}

// =========================
// ПЕРЕГЕНЕРАЦИЯ ОТЧЁТА
// =========================
async function handleRegenerate(childId) {
  const child = lessonData?.children?.find(c => c.child_id === childId);
  if (!child) {
    showMessage('Ребёнок не найден в данных урока', 'red');
    return;
  }

  showModal(childId, child.comments || '');
}

async function regenerateReport() {
  if (!currentRegeneratingChildId) return;

  // ВАЖНО: сохраняем id до hideModal(), чтобы не потерять
  const childId = currentRegeneratingChildId;

  const child = lessonData?.children?.find(c => c.child_id === childId);
  if (!child) {
    showMessage('Ребёнок не найден в данных урока', 'red');
    hideModal();
    return;
  }

  // Обновляем комментарий в данных и в UI
  const newComment = regenerateComment.value.trim() || null;
  child.comments = newComment;

  const commentInput = document.getElementById(`comment-${childId}`);
  if (commentInput) {
    commentInput.value = newComment || '';
  }

  const blockId = `report-${childId}`;
  const container = document.getElementById(blockId);

  if (!container) {
    showMessage('Элемент отчёта не найден', 'red');
    hideModal();
    return;
  }

  modalRegenerate.disabled = true;
  modalRegenerate.innerHTML = '<span class="spinner"></span> Перегенерация...';

  container.innerHTML = `
    <div class="report-header">
      <div class="report-name">${escapeHtml(child.name || 'Без имени')}</div>
    </div>
    <div class="report-loading">
      <div class="loader" style="width: 32px; height: 32px; margin: 0 auto;"></div>
      <div style="text-align: center; margin-top: 12px; color: #64748b; font-size: 14px;">Перегенерация...</div>
    </div>
  `;

  hideModal();

  try {
    const response = await fetch(API_ENDPOINTS.GENERATE_REPORT, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(child),
    });

    if (!response.ok) {
      const errorText = await getErrorMessageFromResponse(response);
      throw new Error(errorText || `HTTP ${response.status}`);
    }

    const result = await response.json();
    renderSingleGeneratedReport(blockId, result, childId);
    showMessage('Отчёт успешно перегенерирован!', 'green');

  } catch (err) {
    console.error(`Ошибка перегенерации отчёта для ${child.name}:`, err);
    container.innerHTML = `
      <div class="report-header">
        <div class="report-name">${escapeHtml(child.name || 'Без имени')}</div>
        <div class="report-actions">
          <button class="btn-icon btn-regenerate tooltip-trigger" onclick="handleRegenerate(${childId})" data-tooltip="Попробовать снова">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
              <path d="M21 3v5h-5"></path>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
              <path d="M3 21v-5h5"></path>
            </svg>
            <span class="tooltip">Попробовать снова</span>
          </button>
        </div>
      </div>
      <div class="report-error">Ошибка перегенерации: ${escapeHtml(err.message)}</div>
    `;
    showMessage(`Ошибка: ${err.message}`, 'red');
  } finally {
    modalRegenerate.disabled = false;
    modalRegenerate.textContent = 'Перегенерировать';
  }
}

// Обработчики модального окна
modalClose.addEventListener('click', hideModal);
modalCancel.addEventListener('click', hideModal);
modalRegenerate.addEventListener('click', regenerateReport);

// Закрытие по клику вне модального окна
regenerateModal.addEventListener('click', (e) => {
  if (e.target === regenerateModal) {
    hideModal();
  }
});

// Закрытие по Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && regenerateModal.style.display !== 'none') {
    hideModal();
  }
});

// =========================
// КОПИРОВАНИЕ ТЕКСТА ОТЧЁТА
// =========================
async function copyReportText(reportId) {
  const reportElement = document.getElementById(reportId);
  if (!reportElement) {
    showMessage('Элемент отчёта не найден', 'red');
    return;
  }

  const text = reportElement.innerText || reportElement.textContent || '';

  if (!text.trim()) {
    showMessage('Нет текста для копирования', 'red');
    return;
  }

  try {
    await navigator.clipboard.writeText(text);

    const copyButton = reportElement.closest('.report-item')?.querySelector('.btn-copy');
    if (copyButton) {
      const originalHTML = copyButton.innerHTML;
      copyButton.classList.add('copied');
      copyButton.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      `;

      setTimeout(() => {
        copyButton.classList.remove('copied');
        copyButton.innerHTML = originalHTML;
      }, 2000);
    }

    showMessage('Содержимое скопировано', 'green');
  } catch (err) {
    console.error('Ошибка при копировании:', err);
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      showMessage('Содержимое скопировано', 'green');
    } catch (_) {
      showMessage('Не удалось скопировать отчёт', 'red');
    }
    document.body.removeChild(textArea);
  }
}

// Делаем функции доступными глобально для onclick
window.handleRegenerate = handleRegenerate;
window.copyReportText = copyReportText;
window.sendFeedback = sendFeedback;
