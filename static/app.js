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

let lessonData = null;

generateBtn.disabled = true;

// =========================
// ЗАГРУЗКА СОХРАНЁННЫХ ДАННЫХ
// =========================
window.onload = () => {
  const savedCreds = localStorage.getItem('softiumCreds');
  if (savedCreds) {
    const creds = JSON.parse(savedCreds);
    usernameInput.value = creds.username;
    passwordInput.value = creds.password;
    usernameInput.disabled = true;
    passwordInput.disabled = true;
    saveBtn.style.display = 'none';
    editBtn.style.display = 'block';
  }
};

// =========================
// СОХРАНЕНИЕ КРЕДОВ
// =========================
saveBtn.addEventListener('click', () => {
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();

  if (!username || !password) {
    message.style.color = 'red';
    message.innerText = 'Введите логин и пароль!';
    return;
  }

  localStorage.setItem('softiumCreds', JSON.stringify({ username, password }));
  usernameInput.disabled = true;
  passwordInput.disabled = true;
  saveBtn.style.display = 'none';
  editBtn.style.display = 'block';

  message.style.color = 'green';
  message.innerText = 'Креды сохранены!';
});

// =========================
// РЕДАКТИРОВАНИЕ КРЕДОВ
// =========================
editBtn.addEventListener('click', () => {
  usernameInput.disabled = false;
  passwordInput.disabled = false;
  saveBtn.style.display = 'block';
  editBtn.style.display = 'none';
  message.innerText = '';
});

// =========================
// ЗАГРУЗКА ДАННЫХ УРОКА
// =========================
fetchBtn.addEventListener('click', async () => {
  const savedCreds = JSON.parse(localStorage.getItem('softiumCreds') || '{}');
  const lessonId = lessonIdInput.value.trim();

  if (!savedCreds.username || !savedCreds.password || !lessonId) {
    message.style.color = 'red';
    message.innerText = 'Заполните креды и ID урока!';
    return;
  }

  message.style.color = 'black';
  message.innerText = 'Загрузка данных...';
  loader.style.display = 'block';
  lessonPreviewContent.innerHTML = '';
  lessonPreviewSection.style.display = 'none';
  reportsSection.style.display = 'none';
  report.innerHTML = '';
  generateBtn.disabled = true;

  try {
    const params = new URLSearchParams({
      username: savedCreds.username,
      password: savedCreds.password,  // ТЕПЕРЬ ОТПРАВЛЯЕМ КАК ЕСТЬ
      lesson_id: lessonId
    });

    const response = await fetch(`/scraper/get_lesson_data?${params.toString()}`);
    if (!response.ok) throw new Error(response.statusText);

    lessonData = await response.json();

    if (!lessonData.children || lessonData.children.length === 0) {
      message.style.color = 'red';
      message.innerText = 'Не удалось получить данные об уроке.';
      lessonData = null;
      return;
    }

    displayLessonData(lessonData);
    lessonPreviewSection.style.display = 'block';

    message.style.color = 'green';
    message.innerText = 'Данные успешно получены!';
    generateBtn.disabled = false;

  } catch (err) {
    message.style.color = 'red';
    message.innerText = `Ошибка: ${err.message}`;
  } finally {
    loader.style.display = 'none';
  }
});

// =========================
// ГЕНЕРАЦИЯ ОТЧЁТА
// =========================
generateBtn.addEventListener('click', async () => {
  if (!lessonData || !lessonData.children?.length) return;

  message.style.color = 'black';
  message.innerText = 'Генерация отчётов...';
  loader.style.display = 'block';
  report.innerHTML = '';
  reportsSection.style.display = 'block';
  generateBtn.disabled = true;

  for (let i = 0; i < lessonData.children.length; i++) {
    const child = lessonData.children[i];

    // Плейсхолдер сразу в DOM
    const blockId = `report-${child.child_id}`;
    report.insertAdjacentHTML(
  'beforeend',
  `<div id="${blockId}" class="report-item">
    <div class="report-name">${child.name}</div>
    <div class="report-loading">Генерация...</div>
  </div>`
);


    try {
      const response = await fetch('/reports/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ child }), // ✅ ТЕПЕРЬ ПО ОДНОМУ
      });

      if (!response.ok) throw new Error(response.statusText);

      const result = await response.json();

      renderSingleGeneratedReport(blockId, result);

    } catch (err) {
      document.getElementById(blockId).innerHTML = `
        <div class="report-name">${child.name}</div>
        <div class="report-error">Ошибка генерации: ${err.message}</div>
      `;
    }
  }

  loader.style.display = 'none';
  generateBtn.disabled = false;
  message.style.color = 'green';
  message.innerText = 'Все отчёты сгенерированы!';
});


// =========================
// ОТОБРАЖЕНИЕ ОТЧЁТА
// =========================
function renderGeneratedReport(result) {
  if (result.status !== "success") {
    report.innerHTML = `<div class="error">Ошибка: ${result.message || 'Неизвестно'}</div>`;
    return;
  }

  const paragraphs = result.report
    .split("\n")
    .filter(p => p.trim())
    .map(p => `<p style="margin-bottom: 12px; line-height: 1.5;">${p}</p>`)
    .join('');

  report.innerHTML = `
    <div style="
      background: #fff;
      border-radius: 8px;
      padding: 15px;
      line-height: 1.6;
      border-left: 4px solid #007BFF;
    ">
      ${paragraphs}
    </div>
  `;
}

// =========================
// ОТОБРАЖЕНИЕ ДАННЫХ УРОКА
// =========================
function displayLessonData(data) {
  const html = data.children.map(child => {
    const tasksHtml = child.tasks.map(task => `
      <div class="task-row">
        <div class="task-title">${task.name}</div>
        <div class="task-meta">
          <span class="task-badge blue">${task.direction}</span>
          <span class="task-badge yellow">Уровень ${task.level}</span>
          <span class="task-badge green">+${task.reward}</span>
        </div>
      </div>
    `).join('');

    return `
      <div class="child-card">
        <div class="child-header">
          <div class="child-name">${child.name}</div>
          <div class="child-count">Выполнено заданий: ${child.done_tasks_count}</div>
        </div>

        <div class="tasks-list">
          ${tasksHtml}
        </div>
      </div>
    `;
  }).join('');

  lessonPreviewContent.innerHTML = html;
}


function renderSingleGeneratedReport(blockId, result) {
  const container = document.getElementById(blockId);

  if (result.status !== "success") {
    container.innerHTML = `
      <div class="report-name">Ошибка</div>
      <div class="report-error">${result.message || 'Не удалось получить отчёт'}</div>
    `;
    return;
  }

  const paragraphs = result.report
    .split("\n")
    .filter(p => p.trim())
    .map(p => `<p>${p.trim()}</p>`)
    .join('');

  container.innerHTML = `
    <div class="report-name">${result.child_name}</div>
    <div class="report-text">${paragraphs}</div>
  `;
  
  // Добавляем плавное появление
  container.style.opacity = '0';
  setTimeout(() => {
    container.style.transition = 'opacity 0.4s ease';
    container.style.opacity = '1';
  }, 10);
}

