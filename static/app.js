// =========================
// КОНСТАНТЫ
// =========================
const STORAGE_KEY = 'softiumCreds';
const API_ENDPOINTS = {
  GET_LESSON_DATA: '/scraper/get_lesson_data',
  GENERATE_REPORT: '/report_generation/generate',
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
const message = document.getElementById('message');
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
// УТИЛИТЫ
// =========================
function showMessage(text, color = 'black') {
  message.style.color = color;
  message.innerText = text;
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

// =========================
// ЗАГРУЗКА СОХРАНЁННЫХ ДАННЫХ
// =========================
window.onload = () => {
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
  message.innerText = '';
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
      const errorText = await response.text().catch(() => response.statusText);
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
        const errorText = await response.text().catch(() => response.statusText);
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
          <div class="report-name">${child.name}</div>
          <div class="report-error">Ошибка генерации: ${err.message}</div>
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


function formatReportText(text) {
  if (!text) return '';
  return text
    .split("\n")
    .filter(p => p.trim())
    .map(p => `<p>${escapeHtml(p.trim())}</p>`)
    .join('');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

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

  if (result.status !== "success") {
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
      <div class="report-error">${escapeHtml(result.message || 'Не удалось получить отчёт')}</div>
    `;
    return;
  }

  const reportText = result.report || '';
  const reportId = `report-text-${childId || 'default'}`;

  container.innerHTML = `
    <div class="report-header">
      <div class="report-name">${escapeHtml(result.child_name || 'Без имени')}</div>
      <div class="report-actions">
        <button class="btn-icon btn-copy tooltip-trigger" onclick="copyReportText('${reportId}')" data-tooltip="Копировать отчёт">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
          <span class="tooltip">Копировать отчёт</span>
        </button>
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
    <div class="report-text" id="${reportId}">${formatReportText(reportText)}</div>
  `;
  
  // Плавное появление
  container.style.opacity = '0';
  setTimeout(() => {
    container.style.transition = 'opacity 0.4s ease';
    container.style.opacity = '1';
  }, 10);
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

  const child = lessonData?.children?.find(c => c.child_id === currentRegeneratingChildId);
  if (!child) {
    showMessage('Ребёнок не найден в данных урока', 'red');
    hideModal();
    return;
  }

  // Обновляем комментарий в данных и в UI
  const newComment = regenerateComment.value.trim() || null;
  child.comments = newComment;
  
  // Обновляем комментарий в карточке ребёнка, если она отображается
  const commentInput = document.getElementById(`comment-${currentRegeneratingChildId}`);
  if (commentInput) {
    commentInput.value = newComment || '';
  }

  const blockId = `report-${currentRegeneratingChildId}`;
  const container = document.getElementById(blockId);
  
  if (!container) {
    showMessage('Элемент отчёта не найден', 'red');
    hideModal();
    return;
  }

  // Показываем состояние загрузки на кнопке
  modalRegenerate.disabled = true;
  modalRegenerate.innerHTML = '<span class="spinner"></span> Перегенерация...';

  // Показываем состояние загрузки в контейнере
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
      body: JSON.stringify({ child }),
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => response.statusText);
      throw new Error(errorText || `HTTP ${response.status}`);
    }

    const result = await response.json();
    renderSingleGeneratedReport(blockId, result, currentRegeneratingChildId);
    showMessage('Отчёт успешно перегенерирован!', 'green');

  } catch (err) {
    console.error(`Ошибка перегенерации отчёта для ${child.name}:`, err);
    container.innerHTML = `
      <div class="report-header">
        <div class="report-name">${escapeHtml(child.name || 'Без имени')}</div>
        <div class="report-actions">
          <button class="btn-icon btn-regenerate tooltip-trigger" onclick="handleRegenerate(${currentRegeneratingChildId})" data-tooltip="Попробовать снова">
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

  // Получаем чистый текст без HTML тегов
  const text = reportElement.innerText || reportElement.textContent || '';
  
  if (!text.trim()) {
    showMessage('Нет текста для копирования', 'red');
    return;
  }

  try {
    await navigator.clipboard.writeText(text);
    
    // Находим кнопку копирования и показываем визуальную обратную связь
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
    // Fallback для старых браузеров
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.select();
    try {
      document.execCommand('copy');
      showMessage('Содержимое скопировано', 'green');
    } catch (fallbackErr) {
      showMessage('Не удалось скопировать отчёт', 'red');
    }
    document.body.removeChild(textArea);
  }
}

// Делаем функции доступными глобально для onclick
window.handleRegenerate = handleRegenerate;
window.copyReportText = copyReportText;

